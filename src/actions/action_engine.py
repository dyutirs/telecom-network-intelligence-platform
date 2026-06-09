import pandas as pd


class ActionEngine:

    def generate(
        self,
        rca_df,
        imbalance_table,
        conflict_table,
        congestion_table,
        overshooting_table
    ):

        actions = []

        # ==========================================
        # RCA ACTIONS
        # ==========================================

        for _, row in (
            rca_df
            .sort_values("health_score")
            .head(10)
            .iterrows()
        ):

            actions.append(
                {
                    "priority": "P1",
                    "category": "Cell RCA",
                    "target": row["enb_id"],
                    "issue": row["issue"],
                    "score": row["health_score"],
                    "action": row["recommendations"]
                }
            )

        # ==========================================
        # SECTOR IMBALANCE
        # ==========================================

        for _, row in (
            imbalance_table
            .head(10)
            .iterrows()
        ):

            actions.append(
                {
                    "priority": "P1",
                    "category": "Sector Imbalance",
                    "target": row["enb_id"],
                    "issue":
                        f"Sector {row['worst_sector']} weak",
                    "score":
                        row["difference"],
                    "action":
                        "Check antenna, feeder and tilt"
                }
            )

        # ==========================================
        # PCI CONFLICTS
        # ==========================================

        if len(conflict_table):

            for _, row in (
                conflict_table
                .head(10)
                .iterrows()
            ):

                actions.append(
                    {
                        "priority": "P1",
                        "category": "PCI Conflict",
                        "target":
                            f"{row['site_1']} vs {row['site_2']}",
                        "issue":
                            f"PCI {row['pci']}",
                        "score":
                            round(
                                (1 - row["distance_km"]) * 100,
                                1
                            ),
                        "action":
                            "Review PCI planning"
                    }
                )

        # ==========================================
        # CONGESTION
        # ==========================================

        if len(congestion_table):

            for _, row in (
                congestion_table
                .head(20)
                .iterrows()
            ):

                actions.append(
                    {
                        "priority":
                            "P1"
                            if row["issue"] == "Congestion"
                            else "P2",

                        "category":
                            "Congestion",

                        "target":
                            row["enb_id"],

                        "issue":
                            row["issue"],

                        "score":
                            row["health_score"],

                        "action":
                            "Investigate sector loading and capacity expansion"
                    }
                )
        # Overshooting
        
        for _, row in (
            overshooting_table
            .head(10)
            .iterrows()
):
            actions.append(
        {
            "priority": "P2",

            "category": "Overshooting",

            "target": row["enb_id"],

            "issue": row["issue"],

            "score": row["median_ta"],

            "action":
                "Review antenna tilt and coverage footprint"
        }
    )

        # ==========================================
        # FINAL TABLE
        # ==========================================

        action_df = pd.DataFrame(
            actions
        )
        action_df = action_df.sort_values(
        ["priority", "score"],
        ascending=[True, False]
)
        return action_df