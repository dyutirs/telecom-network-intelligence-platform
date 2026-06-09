import pandas as pd


class SectorImbalance:

    def analyze(
        self,
        cell_table
    ):

        results = []

        for enb_id, site_df in cell_table.groupby("enb_id"):

            if len(site_df) < 2:
                continue

            best_sector = (
                site_df
                .sort_values(
                    "health_score",
                    ascending=False
                )
                .iloc[0]
            )

            worst_sector = (
                site_df
                .sort_values(
                    "health_score"
                )
                .iloc[0]
            )

            difference = (
                best_sector["health_score"]
                -
                worst_sector["health_score"]
            )

            if difference < 20:
                continue

            results.append(
                {
                    "enb_id": enb_id,

                    "best_sector":
                    best_sector["sector_id"],

                    "best_health":
                    round(
                        best_sector["health_score"],
                        2
                    ),

                    "worst_sector":
                    worst_sector["sector_id"],

                    "worst_health":
                    round(
                        worst_sector["health_score"],
                        2
                    ),

                    "difference":
                    round(
                        difference,
                        2
                    )
                }
            )

        return (
            pd.DataFrame(results)
            .sort_values(
                "difference",
                ascending=False
            )
        )