class CriticalSiteEngine:

    def build(self, cell_table):

        bad_cells = (
            cell_table[
                cell_table["health_score"] < 40
            ]
        )

        result = (
            bad_cells
            .groupby("enb_id")
            .agg(
                bad_cells=(
                    "cell_id",
                    "count"
                ),

                avg_health=(
                    "health_score",
                    "mean"
                )
            )
            .reset_index()
        )

        result = (
            result.sort_values(
                ["bad_cells",
                 "avg_health"],
                ascending=[
                    False,
                    True
                ]
            )
        )

        return result