"""Emit paper/numbers.tex from the result tables.

Every number in the manuscript comes from here, so a figure cannot drift away
from the artefact that produced it.  Run after any experiment is re-executed.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"


def fmt(x, n=3):
    return f"{x:.{n}f}"


def main() -> None:
    reg = pd.read_csv(R / "exp03_regional.csv")
    nat = pd.read_csv(R / "exp04_national.csv")
    ver = pd.read_csv(R / "exp03b_verification.csv")
    shp = pd.read_csv(R / "exp01_shape_audit.csv")
    inf = pd.read_csv(R / "exp05_information.csv")
    clm = pd.read_csv(R / "exp06_claims.csv")
    wid = pd.read_csv(R / "exp07_widths.csv")
    dom = pd.read_csv(R / "exp08_domains.csv")
    acov = pd.read_csv(R / "exp07_anchor_coverage.csv")
    ref = pd.read_csv(R / "exp06_claims_mofm.csv")
    aud = pd.read_csv(R / "exp02_design_audit.csv")

    reg = reg.assign(ratio=reg.D / reg.K_floor,
                     pred=(1 / reg.scale_ratio ** 2) / np.sqrt(1 - reg.hetero_share_of_D2))
    full = nat[~nat.structure.str.startswith("scan")]
    scan = nat[nat.structure.str.startswith("scan")]
    orc = shp[shp.method == "oracle_rescaled"]

    def cov(structure, rho, d, K=250):
        r = orc[(orc.structure == structure) & (orc.rho == rho) &
                (orc.d == d) & (orc.K == K)]
        return float(r.latent_coverage.iloc[0])

    TAU = 0.147
    kappa = reg.scale_ratio ** 2
    h = reg.hetero_share_of_D2
    D_pred = reg.K_floor / kappa / np.sqrt(1 - h)
    K_req = 1 + 2 / (TAU ** 2 * (1 - reg.rho_hat ** 2) ** 2 * (1 - h))
    boundary_correct = int(((reg.K >= K_req) == reg.gate_B).sum())

    ok = aud[~(aud.psu_equals_idno | aud.psu_constant)]
    split = ok[ok.psu_split_across_regions > 0]

    v = {
        # exp03 regional
        "RegConfigs": len(reg),
        "RegActivations": int((reg.branch == "deconvolution").sum()),
        "RegGateA": int(reg.gate_A.sum()),
        "RegGateB": int(reg.gate_B.sum()),
        "RegRhoLo": fmt(reg.rho_hat.min(), 2),
        "RegRhoHi": fmt(reg.rho_hat.max(), 2),
        "RegKmax": int(reg.K.max()),
        "RegFloorCleared": int((reg.K_floor <= 0.147).sum()),
        "RegCorrRhoRatio": fmt(np.corrcoef(reg.rho_hat, reg.ratio)[0, 1]),
        "RegCorrPred": fmt(np.corrcoef(reg.ratio, reg.pred)[0, 1]),
        "RegPredErr": fmt((abs(reg.ratio - reg.pred) / reg.ratio).mean() * 100, 1),
        "RegRatioLo": fmt(reg.ratio.min(), 2),
        "RegRatioHi": fmt(reg.ratio.max(), 2),
        "RegHeteroMed": fmt(reg.hetero_share_of_D2.median() * 100, 1),
        "IdCorr": fmt(np.corrcoef(reg.D, D_pred)[0, 1], 4),
        "IdErr": fmt((abs(reg.D - D_pred) / reg.D).mean() * 100, 1),
        "IdErrMax": fmt((abs(reg.D - D_pred) / reg.D).max() * 100, 1),
        "BoundCorrect": boundary_correct,
        "BoundNaive": int((reg.K >= 94).sum()),
        "KreqZero": f"{1 + 2 / (TAU ** 2):.0f}",
        "KreqCut": f"{1 + 2 / (TAU ** 2 * (1 - 0.47 ** 2) ** 2):.0f}",
        "KreqSix": f"{1 + 2 / (TAU ** 2 * (1 - 0.60 ** 2) ** 2):.0f}",
        "KreqMax": f"{1 + 2 / (TAU ** 2 * (1 - 0.66 ** 2) ** 2):.0f}",
        # exp03b verification
        "VerMofmOpen": int(ver[ver.bootstrap == "m-of-m"].gate_B.sum()),
        "VerMofmN": int((ver.bootstrap == "m-of-m").sum()),
        "VerRwyOpen": int(ver[ver.bootstrap == "Rao-Wu-Yue"].gate_B.sum()),
        "VerRwyN": int((ver.bootstrap == "Rao-Wu-Yue").sum()),
        "VerUnitEffect": fmt(
            abs(ver[ver.resample_unit == "(stratum,psu)"].D.mean()
                - ver[ver.resample_unit == "(stratum,psu,region)"].D.mean())
            / ver.D.mean() * 100, 1),
        # exp04 national
        "NatRhoLo": fmt(full.rho_hat.min(), 3),
        "NatRhoHi": fmt(full.rho_hat.max(), 3),
        "NatScanHi": fmt(scan.rho_hat.max(), 3),
        "NatScanCells": len(scan),
        "NatGateA": int(nat.gate_A.sum()),
        "NatConfigs": len(nat),
        "NatHeteroLo": fmt(nat.hetero_share_of_D2.min() * 100, 1),
        "NatHeteroHi": fmt(nat.hetero_share_of_D2.max() * 100, 1),
        # exp01 shape
        "ShapeCells": int(len(orc)),
        "ShapeMatched": fmt(cov("matched", 0.80, 48)),
        "ShapeRealNat": fmt(cov("noise_far_more_correlated", 0.29, 48)),
        "ShapeRealReg": fmt(cov("noise_far_more_correlated", 0.52, 48)),
        "ShapeHighDeight": fmt(cov("noise_far_more_correlated", 0.80, 8)),
        "ShapeHighDfortyeight": fmt(cov("noise_far_more_correlated", 0.80, 48)),
        "ShapeReverse": fmt(cov("latent_more_correlated", 0.80, 48)),
        "ShapeRealNatSurvey": fmt(cov("survey_realistic", 0.29, 48)),
        "ShapeRealRegSurvey": fmt(cov("survey_realistic", 0.52, 48)),
        "ShapeHighSurvey": fmt(cov("survey_realistic", 0.80, 48)),
        "ShapeKthirty": fmt(cov("noise_far_more_correlated", 0.80, 48, 30)),
        "ShapeKtwofifty": fmt(cov("noise_far_more_correlated", 0.80, 48, 250)),
        # exp02 audit
        "AudCountryRounds": len(aud),
        "AudRespondents": f"{aud.n.sum():,}",
        "AudDegenerate": int((aud.psu_equals_idno | aud.psu_constant).sum()),
        "AudInformative": len(ok),
        "AudSplit": len(split),
        "AudSplitShare": fmt((split.share_resp_in_split_psu * split.n).sum()
                             / aud.n.sum() * 100, 2),
        "AudStratumSplit": int((aud.stratum_split_across_regions > 0).sum()),
        # exp05 information bound
        "GamRatioMed": fmt(inf[(inf.K >= 100) & (inf.rho <= 0.7)].gamma_ratio.median()),
        "GamRatioLo": fmt(inf[(inf.K >= 100) & (inf.rho <= 0.7)].gamma_ratio.min()),
        "GamRatioHi": fmt(inf[(inf.K >= 100) & (inf.rho <= 0.7)].gamma_ratio.max()),
        "InfCells": len(inf),
        "InfReps": int(inf.reps.iloc[0]),
        "InfRatioMed": fmt(inf[inf.K >= 100].ratio.median()),
        "InfRatioLo": fmt(inf[inf.K >= 100].ratio.min()),
        "InfRatioHi": fmt(inf[inf.K >= 100].ratio.max()),
        "InfClosedErr": f"{(abs(inf[~inf.dispersed].rse_closed_form - inf[~inf.dispersed].rse_bound) / inf[~inf.dispersed].rse_bound).max():.0e}",
        "ZeroHiRhoLoK": fmt(float(inf[(~inf.dispersed) & (inf.rho == 0.9) & (inf.K == 30)].share_at_zero.iloc[0]) * 100, 1),
        "ZeroHiRhoMidK": fmt(float(inf[(~inf.dispersed) & (inf.rho == 0.9) & (inf.K == 100)].share_at_zero.iloc[0]) * 100, 1),
        "ZeroHiRhoHiK": fmt(float(inf[(~inf.dispersed) & (inf.rho == 0.9) & (inf.K == 500)].share_at_zero.iloc[0]) * 100, 1),
        "DomConfigs": len(dom),
        "DomCorrect": int(((dom.K >= dom.K_required) == dom.gate_B).sum()),
        "DomOpen": int(dom.gate_B.sum()),
        "DomTypes": dom.domain.nunique(),
        "DomRoundEleven": int((dom[dom.gate_B].essround == 11).sum()),
        **{f"Dom{tag}{q}": v for tag, name in
           (("Sex", "country x sex"), ("Age", "country x age"),
            ("Reg", "country x region"), ("AgeSex", "country x age x sex"),
            ("RegSex", "country x region x sex"))
           for q, v in (
               ("K", f"{dom[(dom.min_n == 60) & (dom.domain == name)].K.mean():.0f}"),
               ("Rho", fmt(dom[(dom.min_n == 60) & (dom.domain == name)].rho_hat.mean(), 2)),
               ("Req", f"{dom[(dom.min_n == 60) & (dom.domain == name)].K_required.mean():.0f}"))},
        "WidMed": fmt(wid.corr_over_anchor.median()),
        "WidLo": fmt(wid.corr_over_anchor.min()),
        "WidHi": fmt(wid.corr_over_anchor.max()),
        "WidActLo": fmt(wid[wid.branch == "deconvolution"].corr_over_anchor.min()),
        "WidActHi": fmt(wid[wid.branch == "deconvolution"].corr_over_anchor.max()),
        "WidGainLo": fmt((1 - wid[wid.branch == "deconvolution"].corr_over_anchor.max()) * 100, 0),
        "WidGainHi": fmt((1 - wid[wid.branch == "deconvolution"].corr_over_anchor.min()) * 100, 0),
        "WidConsMed": fmt(wid.cons_over_anchor.median(), 2),
        "WidCeilLo": fmt(wid[wid.branch == "deconvolution"].ceiling.min() * 100, 0),
        "WidCeilHi": fmt(wid[wid.branch == "deconvolution"].ceiling.max() * 100, 0),
        "AcovMed": fmt(acov.marginal_coverage.median(), 4),
        "AcovLo": fmt(acov.marginal_coverage.min(), 4),
        "AcovHi": fmt(acov.marginal_coverage.max(), 4),
        "AcovN": len(acov),
        "AcovSE": fmt((0.9 * 0.1 / acov.n_eval.min()) ** 0.5, 3),
        "AcovWorstLo": fmt(acov.worst_country.min(), 2),
        "AcovWorstHi": fmt(acov.worst_country.max(), 2),
        "ClmN": len(clm),
        "ClmAnyPoint": int(clm.any_point.sum()),
        "ClmAnyPointwise": int(clm.any_pointwise.sum()),
        "ClmAnySim": int(clm.any_simultaneous.sum()),
        "ClmNetPoint": int(clm.net_point.sum()),
        "ClmNetPointwise": int(clm.net_pointwise.sum()),
        "ClmNetSim": int(clm.net_simultaneous.sum()),
        "ClmPerPoint": int(clm.persist_point.sum()),
        "ClmPerPointwise": int(clm.persist_pointwise.sum()),
        "ClmPerSim": int(clm.persist_simultaneous.sum()),
        "ClmNetSet": ", ".join(sorted(clm.loc[clm.net_simultaneous, "cntry"])),
        "ClmGateAny": int(ref.any_simultaneous.sum()),
        "ClmGateNet": int(ref.net_simultaneous.sum()),
        "ClmGatePer": int(ref.persist_simultaneous.sum()),
        "ZeroLoRho": fmt(float(inf[(~inf.dispersed) & (inf.rho <= 0.5)].share_at_zero.max()) * 100, 1),
    }
    out = "\n".join(rf"\newcommand{{\{k}}}{{{val}}}" for k, val in v.items()) + "\n"
    (ROOT / "paper" / "numbers.tex").write_text(out)
    print(f"wrote {len(v)} macros to paper/numbers.tex")
    for k, val in v.items():
        print(f"  {k:24s} {val}")


if __name__ == "__main__":
    main()
