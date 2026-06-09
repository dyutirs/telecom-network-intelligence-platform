import pandas as pd


class SiteRiskEngine:

    def build(
        self,
        critical_sites,
        imbalance_table,
        site_table
    ):

        risk = critical_sites.merge(
            imbalance_table[
                [
                    "enb_id",
                    "difference"
                ]
            ],
            on="enb_id",
            how="left"
        )

        risk = risk.merge(
            site_table[
                [
                    "enb_id",
                    "health_score"
                ]
            ],
            on="enb_id",
            how="left"
        )

        risk["difference"] = (
            risk["difference"]
            .fillna(0)
        )

        risk["risk_score"] = (
            (100 - risk["health_score"])
            +
            (risk["bad_cells"] * 3)
            +
            (risk["difference"] * 0.7)
        )

        risk = (
            risk.sort_values(
                "risk_score",
                ascending=False
            )
        )
        risk["risk_level"] = "Low"

        risk.loc[
        risk["risk_score"] >= 100,
        "risk_level"
        ] = "Critical"

        risk.loc[
        (risk["risk_score"] >= 85)
        &
        (risk["risk_score"] < 100),
        "risk_level"
        ] = "High"

        risk.loc[
        (risk["risk_score"] >= 70)
        &
        (risk["risk_score"] < 85),
        "risk_level"
        ] = "Medium"
        
        return risk[
            [
                "enb_id",
                "risk_score",
                "risk_level",
                "bad_cells",
                "health_score",
                "difference"
            ]
        ]