"""exp30 - a necessary condition matching the two-axis boundary.

Protocol: docs/PROTOCOL_exp30_necessary_condition.md
Runs in a few seconds, no data required.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats, integrate, optimize

OUT = Path(__file__).resolve().parents[1] / "results"


def L(eta):
    """Le Cam threshold: -log of the affinity a two-point argument can tolerate."""
    return -np.log(2 * np.sqrt(eta * (1 - eta)))


def aff_chi2(nu, D0, D1, n):
    return (2 * np.sqrt(D0 * D1) / (D0 + D1)) ** (n * nu / 2)


def aff_norm(V0, V1, K):
    return (2 * np.sqrt(V0 * V1) / (V0 + V1)) ** (K / 2)


def check_affinity():
    """Closed forms against quadrature."""
    nu, D0, D1 = 7, 1.0, 0.83
    f = lambda x: np.sqrt(stats.gamma.pdf(x, nu / 2, scale=2 * D0 / nu)
                          * stats.gamma.pdf(x, nu / 2, scale=2 * D1 / nu))
    g = lambda x: np.sqrt(stats.norm.pdf(x, 0, 1.0) * stats.norm.pdf(x, 0, np.sqrt(1.4)))
    return (abs(aff_chi2(nu, D0, D1, 1) - integrate.quad(f, 0, 60)[0]),
            abs(aff_norm(1.0, 1.4, 1) - integrate.quad(g, -30, 30)[0]))


def nu_nec(r2, eps, eta):
    """nu-axis: hold A+D, move A.  Exact separation, no linearisation."""
    delta = ((1 + eps) / (1 - eps)) ** 2 - 1
    u = delta * (1 - r2) / r2                      # = 1 - D1/D0
    if u >= 1:
        return np.nan                              # leaves the parameter space
    return 2 * L(eta) / np.log((2 - u) / (2 * np.sqrt(1 - u)))


def K_nec(r2, eps, eta):
    """K-axis: hold D, move A.  delta solved exactly."""
    A0, D = 1 - r2, r2
    tgt = (1 + eps) / (1 - eps)
    f = lambda d: np.sqrt((1 + d) * (A0 + D) / (A0 * (1 + d) + D)) - tgt
    d = optimize.brentq(f, 1e-12, 1e8)
    V0, V1 = A0 + D, A0 * (1 + d) + D
    return 2 * L(eta) / np.log((V0 + V1) / (2 * np.sqrt(V0 * V1)))


def suf(r2, eps, eta):
    """The boxed sufficient condition, one axis alone, at the (eps,eta) level."""
    return stats.norm.ppf(1 - eta / 2) ** 2 * r2 ** 2 / (2 * eps ** 2 * (1 - r2) ** 2)


def duality(r2, eps):
    """The two perturbations are reciprocal scale changes -- exact identity."""
    tau = (1 + eps) / (1 - eps)
    k2 = 1 - r2
    ratio_D = (1 - tau ** 2 * k2) / (1 - k2)                 # nu-axis, D1/D0
    A0, D = 1 - r2, r2
    f = lambda d: np.sqrt((1 + d) * (A0 + D) / (A0 * (1 + d) + D)) - tau
    d = optimize.brentq(f, 1e-12, 1e8)
    ratio_V = (A0 * (1 + d) + D) / (A0 + D)                  # K-axis, V1/V0
    return ratio_D, ratio_V, abs(ratio_D * ratio_V - 1.0)


def main():
    e_chi, e_norm = check_affinity()
    rows = []
    for eps in (0.05, 0.02, 0.01, 0.005):
        for r2 in (0.2, 0.4, 0.6, 0.8):
            a, b, c = nu_nec(r2, eps, 0.05), K_nec(r2, eps, 0.05), suf(r2, eps, 0.05)
            rD, rV, err = duality(r2, eps)
            rows.append(dict(eps=eps, rho2=r2, nu_nec=a, K_nec=b, sufficient=c,
                             ratio_suf_nec=c / a if a == a else np.nan,
                             axes_equal=abs(a - b) if a == a else np.nan,
                             duality_err=err,
                             const=a * eps ** 2 * (1 - r2) ** 2 / r2 ** 2 if a == a else np.nan))
    df = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    df.to_csv(OUT / "exp30_necessary_condition.csv", index=False)

    ok = df.dropna(subset=["nu_nec"])
    manifest = dict(
        affinity_max_error=float(max(e_chi, e_norm)),
        axes_max_abs_difference=float(ok.axes_equal.max()),
        duality_max_error=float(df.duality_err.max()),
        P2_no_violation=bool((ok.sufficient >= ok.nu_nec).all()),
        ratio_suf_nec_range=[float(ok.ratio_suf_nec.min()), float(ok.ratio_suf_nec.max())],
        ratio_at_smallest_eps=float(ok[ok.eps == ok.eps.min()].ratio_suf_nec.mean()),
        limiting_constant=float(ok[ok.eps == ok.eps.min()].const.max()),
        L_eta_005=float(L(0.05)),
    )
    (OUT / "exp30_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(df.to_string(index=False, float_format=lambda v: f"{v:,.4g}"))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
