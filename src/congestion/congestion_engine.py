import pandas as pd


class CongestionEngine:
    """Flags cells with good signal but poor throughput as likely
    congested (too many users, not a radio problem).

    Caveat: this is inferred from the signal-vs-throughput mismatch,
    not confirmed against a real traffic/PRB utilization counter - this
    dataset doesn't have one. Treat "Congestion" as a strong candidate
    to verify against real traffic KPIs, not a confirmed diagnosis.
    """

    def analyze(
        self,
        cell_table
    ):

        results = []

        for _, row in cell_table.iterrows():

            issue = None

            if (
                row["median_dl"] < 0.3
                and
                row["median_sinr"] > 15
                and
                row["health_score"] > 60
                ):
                issue = "Congestion"
            elif (
                    row["median_dl"] < 1
                    and
                    row["median_sinr"] > 12
                    and
                    row["health_score"] > 50
):

                issue = "Possible Congestion"

            if issue:

                results.append(
                    {
                        "cell_id":
                            row["cell_id"],

                        "enb_id":
                            row["enb_id"],

                        "median_dl":
                            row["median_dl"],

                        "median_sinr":
                            row["median_sinr"],

                        "health_score":
                            row["health_score"],

                        "issue":
                            issue
                    }
                )

        return pd.DataFrame(
            results
        )