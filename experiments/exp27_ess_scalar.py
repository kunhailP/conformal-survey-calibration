"""exp27 - the fixed procedure on ESS, scalar target.

Protocol: docs/PROTOCOL_exp27_ess_scalar.md, written before any estimate was
computed from the microdata.  Nothing below was changed after seeing results.

NO latent-target coverage is claimed or computed: ESS has no latent truth and a
held-out region's direct estimate is not the latent value.  What is reported is
what each arm needs as input, how far the intervals differ on the same data, and
which assumptions the data support.

Requires the ESS cache built by experiments/fetch_ess.py (licensed microdata,
not redistributed, kept outside this repository).

    ESS_CACHE=<dir> python experiments/exp27_ess_scalar.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm, f as fdist, skew, kurtosis

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

ITEMS = ("trstprl", "stflife", "happy")     # fixed in the protocol
T0 = 4                                      # fixed by rule: one below the midpoint
MIN_N = (40, 60, 80, 100, 150)
ROUNDS = (9, 10, 11)
ALPHA0, ETA_G, ETA_T = 0.05, 0.025, 0.025
NULL_DRAWS, SLACK = 200000, 1e-9


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def region_stats(g: pd.DataFrame, item: str, Fc: float) -> dict | None:
    """Weighted CDF ordinate and its stratified ultimate-cluster variance."""
    w = g.anweight.to_numpy(float)
    z = (g[item].to_numpy(float) <= T0).astype(float)
    W = w.sum()
    if W <= 0:
        return None
    F = float((w * z).sum() / W)
    u = w * (z - F)
    df = pd.DataFrame({"h": g.stratum.to_numpy(), "p": g.psu.to_numpy(), "u": u})
    psu_tot = df.groupby(["h", "p"], sort=False).u.sum()
    var = 0.0
    n_psu = 0
    strata = psu_tot.index.get_level_values(0).unique()
    for h in strata:
        v = psu_tot.loc[h].to_numpy(float)
        m = len(v)
        n_psu += m
        if m > 1:
            var += m / (m - 1.0) * ((v - v.mean()) ** 2).sum()
    D = var / W ** 2
    nu = n_psu - len(strata)
    return dict(F=F, D=float(D), nu=int(nu), n_psu=int(n_psu),
                n_strata=int(len(strata)), n=int(len(g)), Y=float(F - Fc))


def build(d: pd.DataFrame, item: str) -> pd.DataFrame:
    rows = []
    ok = d[item].between(0, 10) & d.anweight.gt(0) & d.region.notna()
    dd = d[ok]
    for (r, c), gc in dd.groupby(["essround", "cntry"], observed=True):
        wc = gc.anweight.to_numpy(float)
        zc = (gc[item].to_numpy(float) <= T0).astype(float)
        Fc = float((wc * zc).sum() / wc.sum())
        for reg, g in gc.groupby("region", observed=True):
            s = region_stats(g, item, Fc)
            if s is None:
                continue
            s.update(essround=int(r), cntry=str(c), region=str(reg), Fc=Fc)
            rows.append(s)
    return pd.DataFrame(rows)


def certified_band(Y, Dh, x, nu_c, K, m, absY, rng):
    """The method fixed in exp23: C_gamma, certified t, band at (t_lo, a_lo)."""
    lx = np.log(x); lxc = lx - lx.mean(); Sxx = float((lxc ** 2).sum())
    W0 = np.log(rng.chisquare(nu_c, size=(NULL_DRAWS, K)) / nu_c) @ lxc
    wq = float(np.quantile(np.abs(W0), 1 - ETA_G))
    ghat = float(-(np.log(Dh) @ lxc) / Sxx)
    half = wq / Sxx
    gL, gU = ghat - half, ghat + half

    a_of = lambda g: (x ** (-g)) / (x ** (-g)).mean()
    a_lo = np.minimum(a_of(gL), a_of(gU)) * (1 - SLACK)
    nu = float(nu_c.sum())

    def fdf(g):                                   # dhat(g), convex in g
        xg = x ** g; xmg = x ** (-g)
        P, dP = (nu_c * Dh * xg).sum(), (nu_c * Dh * xg * lx).sum()
        Q, dQ = xmg.mean(), -(xmg * lx).mean()
        return P * Q / nu, (dP * Q + P * dQ) / nu
    fL, dL = fdf(gL); fU, dU = fdf(gU)
    if dL >= 0:
        d_lo = fL
    elif dU <= 0:
        d_lo = fU
    else:
        a, b = gL, gU
        for _ in range(80):
            mid = 0.5 * (a + b)
            if fdf(mid)[1] < 0: a = mid
            else: b = mid
        fa, da = fdf(a)
        d_lo = max(0.0, fa + da * (b - a))
    d_lo *= (1 - SLACK)

    q = float(fdist.ppf(1 - ETA_T, nu, K))
    tgt = K * d_lo / q
    Y2 = Y ** 2
    if tgt <= 0 or tgt > (Y2 / a_lo).sum():
        t_lo = 0.0
    else:
        lo, hi = 1e-14, 1e14
        for _ in range(200):
            mid = np.sqrt(lo * hi)
            if (mid * Y2 / (1 + mid * a_lo)).sum() >= tgt: hi = mid
            else: lo = mid
        t_lo = lo
    band = float(np.sort(absY / np.sqrt(1 + t_lo * a_lo))[m - 1])
    Sbar = float((Y2 / (1 + t_lo * a_lo)).sum())
    return dict(band=band, ghat=ghat, gL=gL, gU=gU, t_lo=t_lo, Sbar=Sbar,
                d_lo=d_lo, fallback=int(t_lo == 0.0))


def run_config(sub: pd.DataFrame, item: str, rnd: int, min_n: int) -> dict | None:
    s = sub[(sub.n >= min_n) & (sub.nu >= 2)].copy()
    K = len(s)
    if K < 20:
        return None
    m = conformal_rank(K, ALPHA0)
    if m > K:
        return None
    Y = s.Y.to_numpy(float); absY = np.abs(Y); Y2 = Y ** 2
    Dh = s.D.to_numpy(float); x = s.n_psu.to_numpy(float)
    nu_c = s.nu.to_numpy(float)
    zero = int((Dh <= 0).sum())
    Dh = np.maximum(Dh, 1e-16)

    rng = seed_for(f"exp27|{item}|{rnd}|{min_n}")
    cert = certified_band(Y, Dh, x, nu_c, K, m, absY, rng)

    # gaussian competitor: same C_gamma and t_lo, split FIXED at (0.025, 0.025)
    AU = cert["Sbar"] / chi2.ppf(ALPHA0 / 2, K)
    band_gauss = float(norm.ppf(1 - (ALPHA0 / 2) / 2) * np.sqrt(max(AU, 0.0)))

    # structure-free incumbent
    vL = nu_c * Dh / chi2.ppf(1 - (ETA_G + ETA_T) / 2 / K, nu_c)
    qb = float(chi2.ppf((ETA_G + ETA_T) / 2, K))
    lo, hi = 0.0, 10.0
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if (Y2 / (mid + vL)).sum() < qb: hi = mid
        else: lo = mid
    AU_b = 0.5 * (lo + hi)
    band_sep = float(np.sort(absY / np.sqrt(1 + vL / max(AU_b, 1e-16)))[m - 1])
    band_unc = float(np.sort(absY)[m - 1])

    lD = np.log(Dh); lx = np.log(x); lxc = lx - lx.mean()
    Sxx = float((lxc ** 2).sum())
    slope = float((lD @ lxc) / Sxx)
    resid = lD - (lD.mean() + slope * lxc)
    r2 = float(1 - resid.var() / max(lD.var(), 1e-300))
    std = Y / np.sqrt(np.maximum(Y.var(ddof=1), 1e-300))
    ratio = nu_c * Dh / np.maximum(Dh.mean(), 1e-300)

    return dict(item=item, essround=rnd, min_n=min_n, K=K, m=m,
                nominal_rank=m / (K + 1), n_countries=s.cntry.nunique(),
                zero_Dhat=zero, nu_med=float(np.median(nu_c)),
                nu_q10=float(np.quantile(nu_c, .1)),
                nu_q90=float(np.quantile(nu_c, .9)),
                Fc_med=float(s.Fc.median()),
                gamma_hat=cert["ghat"], gamma_lo=cert["gL"], gamma_hi=cert["gU"],
                t_lo=cert["t_lo"], fallback=cert["fallback"],
                struct_R2_on_Dhat=r2, struct_slope=slope,
                skew_dev=float(skew(std)), kurt_dev=float(kurtosis(std)),
                rho2_hat=float(min(Dh.mean() / max(Y.var(ddof=1), 1e-300), 1.0)),
                w_certified=cert["band"], w_gaussian=band_gauss,
                w_sep_bonf=band_sep, w_uncorrected=band_unc,
                cert_over_unc=cert["band"] / band_unc,
                cert_over_sep=cert["band"] / band_sep,
                cert_over_gauss=cert["band"] / band_gauss)


def main() -> None:
    cache = Path(os.environ.get("ESS_CACHE", str(Path.home() / "ess_cache"))) \
        / "ess_extract.pkl"
    if not cache.exists():
        sys.exit(f"cache not found: {cache}  (run experiments/fetch_ess.py)")
    d = pd.read_pickle(cache)
    rows, diag = [], []
    for item in ITEMS:
        tab = build(d, item)
        diag.append(dict(item=item, region_cells=len(tab),
                         cells_nu_lt2=int((tab.nu < 2).sum()),
                         cells_D_zero=int((tab.D <= 0).sum()),
                         med_nu=float(tab.nu.median())))
        for rnd in ROUNDS:
            sub = tab[tab.essround == rnd]
            for mn in MIN_N:
                r = run_config(sub, item, rnd, mn)
                if r:
                    rows.append(r)
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp27_ess_scalar.csv"
    df.to_csv(out, index=False)
    dg = pd.DataFrame(diag)
    dg.to_csv(ROOT / "results" / "exp27_ess_exclusions.csv", index=False)
    (ROOT / "results" / "exp27_manifest.json").write_text(json.dumps(dict(
        experiment="exp27_ess_scalar", t0=T0, items=list(ITEMS),
        rounds=list(ROUNDS), min_n=list(MIN_N),
        alpha0=ALPHA0, eta_gamma=ETA_G, eta_t=ETA_T,
        structure_variable="x = number of sampled PSUs in the region",
        configs=len(df), latent_coverage_claimed=False,
        centre="estimated (country-round weighted share); theory assumes it known",
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 60)
    print("=== exclusions, per item (reported, not silently dropped)")
    print(dg.to_string(index=False))
    print("\n=== 1. what the data look like where the method would be applied")
    print(df.set_index(["item", "essround", "min_n"])[
        ["K", "n_countries", "nu_med", "nu_q10", "nu_q90", "zero_Dhat",
         "rho2_hat", "skew_dev", "kurt_dev"]].round(3).to_string())
    print("\n=== 2. the structure model on ESS")
    print(df.set_index(["item", "essround", "min_n"])[
        ["gamma_hat", "gamma_lo", "gamma_hi", "struct_R2_on_Dhat",
         "t_lo", "fallback"]].round(4).to_string())
    print("\n=== 3. realised radii, and how far the arms differ")
    print(df.set_index(["item", "essround", "min_n"])[
        ["w_uncorrected", "w_sep_bonf", "w_gaussian", "w_certified",
         "cert_over_unc", "cert_over_sep", "cert_over_gauss"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
