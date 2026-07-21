import pandas as pd


class HandoverEngine:
    """Mobility Robustness Optimization (MRO) style ping-pong detector:
    finds A -> B -> A handover triplets where the phone spent only a
    short time on the middle cell B before bouncing back to A."""

    def __init__(
        self,
        session_gap_s=120,
        ping_pong_dwell_s=5
    ):

        self.session_gap_s = session_gap_s
        self.ping_pong_dwell_s = ping_pong_dwell_s

    def _build_segments(self, phone_df):

        df = phone_df.dropna(
            subset=["time", "cell_id", "enb_id"]
        ).copy()

        df["time"] = pd.to_datetime(df["time"])

        df = df.sort_values("time").reset_index(drop=True)

        gap_s = df["time"].diff().dt.total_seconds()

        df["session_id"] = (
            gap_s.isna() | (gap_s > self.session_gap_s)
        ).cumsum()

        changed = (
            (df["cell_id"] != df["cell_id"].shift())
            | (df["session_id"] != df["session_id"].shift())
        )

        df["segment_id"] = changed.cumsum()

        segments = (
            df.groupby(["session_id", "segment_id"])
            .agg(
                cell_id=("cell_id", "first"),
                enb_id=("enb_id", "first"),
                start_time=("time", "min"),
                end_time=("time", "max")
            )
            .reset_index()
            .sort_values(["session_id", "segment_id"])
        )

        segments["dwell_s"] = (
            segments["end_time"] - segments["start_time"]
        ).dt.total_seconds()

        return segments

    def analyze(self, phone_df):

        segments = self._build_segments(phone_df)

        segments["next_cell"] = (
            segments.groupby("session_id")["cell_id"].shift(-1)
        )

        segments["next_enb"] = (
            segments.groupby("session_id")["enb_id"].shift(-1)
        )

        segments["next_dwell"] = (
            segments.groupby("session_id")["dwell_s"].shift(-1)
        )

        segments["next2_cell"] = (
            segments.groupby("session_id")["cell_id"].shift(-2)
        )

        pingpong_events = segments[
            (segments["cell_id"] == segments["next2_cell"])
            & (segments["next_dwell"] <= self.ping_pong_dwell_s)
        ].copy()

        if len(pingpong_events) == 0:
            return pd.DataFrame(
                columns=[
                    "cell_a", "enb_a", "cell_b", "enb_b",
                    "same_site", "ping_pong_count", "median_dwell_s"
                ]
            )

        pingpong_events["same_site"] = (
            pingpong_events["enb_id"] == pingpong_events["next_enb"]
        )

        summary = (
            pingpong_events
            .groupby(
                ["cell_id", "enb_id", "next_cell", "next_enb", "same_site"]
            )
            .agg(
                ping_pong_count=("next_dwell", "count"),
                median_dwell_s=("next_dwell", "median")
            )
            .reset_index()
            .rename(
                columns={
                    "cell_id": "cell_a",
                    "enb_id": "enb_a",
                    "next_cell": "cell_b",
                    "next_enb": "enb_b"
                }
            )
            .sort_values("ping_pong_count", ascending=False)
        )

        return summary
