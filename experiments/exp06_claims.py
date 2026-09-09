"""exp06 - the claim family: what simultaneity costs a repeated-survey reading.

Protocol: docs/PROTOCOL_exp06_claims.md (written before execution).
Requires licensed ESS microdata; see docs/DATA.md.

Three readings of the same contrasts are reported, because the predecessor's
headline compared the first with the third and described the first as a
"marginal reading".  It is not a statistical reading at all: it is the sign of
the point estimate.  The fair inferential comparison is the second against the
third, and both are given.

    python experiments/exp06_claims.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from dac.survey import replicate_weights, weighted_cdf  # noqa: E402
from exp03_regional import THRESHOLDS  # noqa: E402

CACHE = ROOT / "data" / "ess_r9_11.pkl"
OUT = ROOT / "results"
B, ALPHA = 2000, 0.10
Z_POINTWISE = norm.ppf(1 - ALPHA)


def round_curves(g, rng, rescaled):
    y = g.trstprl.to_numpy()
    ind = (y[:, None] <= THRESHOLDS[None, :]).astype(np.float64)
    w = g.anweight.to_numpy(dtype=np.float64)
    one = np.zeros(len(g), dtype=np.int64)
    pt = weighted_cdf(ind, w, one, 1)[0]
    W, _ = replicate_weights(g.stratum.to_numpy(), g.psu.to_numpy(), w, B, rng,
                             rescaled=rescaled)
    return pt, weighted_cdf(ind, W, one, 1)[0]


def certify(pt, rep, pairs):
    """One-sided studentised sup-t certification over the supplied contrasts.

    The bootstrap distribution of (D* - D_hat) approximates that of
    (D_hat - D); certify when D_hat - c s_hat >= 0 everywhere, with c the
    (1 - alpha) quantile of the one-sided studentised supremum.  A single c
    covers every contrast supplied, so no further multiplicity is spent.
    """
    dh = np.stack([pt[b] - pt[a] for a, b in pairs])
    db = np.stack([rep[b] - rep[a] for a, b in pairs]).transpose(2, 0, 1)
    sd = np.maximum(db.std(axis=0), 1e-6)
    c = float(np.quantile(np.max((db - dh[None]) / sd[None], axis=(1, 2)), 1 - ALPHA))
    return dict(
        point=bool(np.all(dh >= 0)),                      # sign only, no inference
        pointwise=bool(np.all(dh - Z_POINTWISE * sd >= 0)),  # no simultaneity
        simultaneous=bool(np.all(dh - c * sd >= 0)),      # one band, whole surface
        crit=c)


def run(d, rescaled):
    rng = np.random.default_rng(20260911)
    rows = []
    for cty, g in d.groupby("cntry", observed=True):
        rounds = sorted(g.essround.unique())
        if len(rounds) < 2:
            continue
        pt, rep, ok = {}, {}, True
        for r in rounds:
            sub = g[g.essround == r]
            if len(sub) < 200:
                ok = False
                break
            pt[r], rep[r] = round_curves(sub, rng, rescaled)
        if not ok:
            continue
        adj = [(rounds[i], rounds[i + 1]) for i in range(len(rounds) - 1)]
        span = [(rounds[0], rounds[-1])]
        per_pair = [certify(pt, rep, [p]) for p in adj]
        row = dict(cntry=str(cty), n_rounds=len(rounds))
        for key in ("point", "pointwise", "simultaneous"):
            row[f"any_{key}"] = any(r[key] for r in per_pair)
            row[f"net_{key}"] = certify(pt, rep, span)[key]
            row[f"persist_{key}"] = certify(pt, rep, adj)[key]
        rows.append(row)
    return pd.DataFrame(rows).sort_values("cntry")


def main() -> None:
    d = pd.read_pickle(CACHE)
    d = d[d.trstprl.between(0, 10) & d.anweight.gt(0)].copy()

    out = run(d, rescaled=True)
    ref = run(d, rescaled=False)          # archive's m-of-m, for the gate
    out.to_csv(OUT / "exp06_claims.csv", index=False)
    ref.to_csv(OUT / "exp06_claims_mofm.csv", index=False)
    (OUT / "exp06_manifest.json").write_text(json.dumps({
        "protocol": "docs/PROTOCOL_exp06_claims.md", "alpha": ALPHA, "B": B,
        "outcome": "trstprl", "rounds": "9-11", "bootstrap": "Rao-Wu-Yue rescaled",
        "core_thresholds": THRESHOLDS.tolist(),
        "critical_value": "one-sided studentised supremum over the supplied contrasts",
    }, indent=2) + "\n")

    n = len(out)
    print(f"ESS rounds 9-11, trstprl, {n} countries, alpha = {ALPHA}\n")
    print(f"{'claim':<12}{'point sign':>12}{'pointwise':>12}{'simultaneous':>14}")
    for k, lab in (("any", "any pair"), ("net", "net (span)"), ("persist", "persistent")):
        print(f"{lab:<12}{out[f'{k}_point'].sum():>12}{out[f'{k}_pointwise'].sum():>12}"
              f"{out[f'{k}_simultaneous'].sum():>14}")
    print(f"\nnet certified: {sorted(out.loc[out.net_simultaneous, 'cntry'])}")

    got = (int(ref.any_point.sum()), int(ref.any_simultaneous.sum()),
           int(ref.net_simultaneous.sum()), int(ref.persist_simultaneous.sum()))
    ns = set(ref.loc[ref.net_simultaneous, "cntry"])
    print(f"\nREPRODUCTION GATE (archive m-of-m: 20 / 12 / 6 / 1, "
          f"net = AT BE EE GB GR NL)")
    print(f"  ours {got}, net = {sorted(ns)}"
          f"  -> {'CLEARED' if got == (20, 12, 6, 1) and ns == {'AT','BE','EE','GB','GR','NL'} else 'FAILED'}")


if __name__ == "__main__":
    main()
