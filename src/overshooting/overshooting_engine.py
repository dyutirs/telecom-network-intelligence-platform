import pandas as pd


class OvershootingEngine:

    def analyze(
        self,
        cell_table
    ):

        results = []

        for _, row in cell_table.iterrows():

            issue = None

            if (
                pd.notna(row["median_ta"])
                and
                row["median_ta"] > 25
                and
                row["median_rsrp"] > -105  
                and
                row["median_sinr"] > 0
            ):

                issue = "Overshooting"

            elif (
                pd.notna(row["median_ta"])
                and
                row["median_ta"] > 20
                and
                row["median_rsrp"] > -100
                and
                row["median_sinr"] > 3
            ):

                issue = "Possible Overshooting"

            if issue:

                results.append(
                    {
                        "cell_id":
                            row["cell_id"],

                        "enb_id":
                            row["enb_id"],

                        "median_ta":
                            row["median_ta"],

                        "median_rsrp":
                            row["median_rsrp"],

                        "health_score":
                            row["health_score"],

                        "issue":
                            issue
                    }
                )

        return pd.DataFrame(
            results
        )