class SiteEngine:

    def build_site_table(
        self,
        cell_table
    ):

        site_table = (
            cell_table
            .groupby("enb_id")
            .agg(
                health_score=("health_score", "mean"),

                total_cells=("cell_id", "count"),

                median_rsrp=("median_rsrp", "mean"),

                median_sinr=("median_sinr", "mean"),

                median_dl=("median_dl", "mean")
            )
            .reset_index()
        )

        return site_table