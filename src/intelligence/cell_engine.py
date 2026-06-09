import pandas as pd

from src.scoring.health_score import HealthScorer


class CellEngine:

    def __init__(self):

        self.scorer = HealthScorer()

    def build_cell_table(
        self,
        phone_df
    ):
        

        cell_df = (
            phone_df
            .groupby("cell_id")
            .agg(
                operator=("operator", "first"),

                enb_id=("enb_id", "first"),

                sector_id=("sector_id", "first"),

                pci=("pci", "first"),

                latitude=("latitude", "median"),

                longitude=("longitude", "median"),

                median_rsrp=("rsrp_dbm", "median"),

                median_rsrq=("rsrq_db", "median"),

                median_sinr=("sinr_db", "median"),

                median_dl=("dl_throughput_mbps", "median"),

                median_ul=("ul_throughput_mbps", "median"),

                median_pathloss=("pathloss_db", "median"),

                median_ta=("timing_advance", "median"),

                measurements=("cell_id", "count")
            )
            .reset_index()
        )
        cell_df = cell_df[
    cell_df["measurements"] >= 30
]

        cell_df["health_score"] = (
            cell_df.apply(
                lambda row:
                self.scorer.overall_score(
                    row["median_rsrp"],
                    row["median_sinr"],
                    row["median_dl"]
                ),
                axis=1
            )
        )
        

        return cell_df