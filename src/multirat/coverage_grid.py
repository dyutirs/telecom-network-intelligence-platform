import pandas as pd

from src.scoring.health_score import HealthScorer


class CoverageGridEngine:

    def __init__(self, grid_size_deg=0.0004):

        self.grid_size_deg = grid_size_deg
        self.scorer = HealthScorer()

    def _grid_table(self, phone_df, technology):

        df = phone_df.dropna(
            subset=[
                "latitude",
                "longitude",
                "rsrp_dbm",
                "sinr_db",
                "dl_throughput_mbps"
            ]
        )

        grid_lat = (
            (df["latitude"] / self.grid_size_deg)
            .round() * self.grid_size_deg
        )

        grid_lon = (
            (df["longitude"] / self.grid_size_deg)
            .round() * self.grid_size_deg
        )

        grid = df.assign(
            grid_lat=grid_lat,
            grid_lon=grid_lon
        )

        table = (
            grid
            .groupby(["grid_lat", "grid_lon"])
            .agg(
                rsrp=("rsrp_dbm", "median"),
                sinr=("sinr_db", "median"),
                dl=("dl_throughput_mbps", "median"),
                samples=("rsrp_dbm", "count")
            )
            .reset_index()
        )

        table["health_score"] = table.apply(
            lambda row: self.scorer.overall_score(
                row["rsrp"],
                row["sinr"],
                row["dl"]
            ),
            axis=1
        )

        table = table.rename(
            columns={
                "rsrp": f"{technology.lower()}_rsrp",
                "sinr": f"{technology.lower()}_sinr",
                "dl": f"{technology.lower()}_dl",
                "samples": f"{technology.lower()}_samples",
                "health_score": f"{technology.lower()}_score"
            }
        )

        return table

    def build(self, lte_phone_df, nr_phone_df):

        lte_grid = self._grid_table(lte_phone_df, "lte")
        nr_grid = self._grid_table(nr_phone_df, "nr")

        grid = lte_grid.merge(
            nr_grid,
            on=["grid_lat", "grid_lon"],
            how="outer"
        )

        def pick_winner(row):

            has_lte = pd.notna(row["lte_score"])
            has_nr = pd.notna(row["nr_score"])

            if has_lte and has_nr:
                return "5G" if row["nr_score"] > row["lte_score"] else "LTE"

            if has_nr:
                return "5G"

            return "LTE"

        grid["winner"] = grid.apply(
            pick_winner,
            axis=1
        )

        grid["best_score"] = grid[
            ["lte_score", "nr_score"]
        ].max(axis=1)

        return grid.sort_values(
            "best_score",
            ascending=False
        )
