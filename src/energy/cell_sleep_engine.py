import pandas as pd


class CellSleepEngine:
    """Flags healthy, lightly-used cells as candidates for off-peak sleep
    (Ericsson Cell Sleep Mode / Micro Sleep Tx style energy saving).

    Caveat: 'measurements' is the drive-test sample count for that cell,
    which is only a weak proxy for actual traffic/PRB utilization -
    this dataset has no real traffic counter. Treat this as a shortlist
    to verify against real traffic KPIs, not a standalone decision.
    """

    def __init__(self, health_threshold=70, low_usage_percentile=0.25):

        self.health_threshold = health_threshold
        self.low_usage_percentile = low_usage_percentile

    def analyze(self, cell_table):

        healthy = cell_table[
            cell_table["health_score"] >= self.health_threshold
        ]

        if len(healthy) == 0:
            return pd.DataFrame()

        usage_cutoff = healthy["measurements"].quantile(
            self.low_usage_percentile
        )

        candidates = healthy[
            healthy["measurements"] <= usage_cutoff
        ][
            ["cell_id", "enb_id", "health_score", "measurements"]
        ].copy()

        candidates["recommendation"] = (
            "Off-Peak Sleep Candidate "
            "(verify against real traffic KPIs before acting)"
        )

        return candidates.sort_values("measurements")
