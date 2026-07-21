import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


class TimelineChart:
    """Two-panel KPI timeline: day-to-day median trend across all drive
    sessions, plus a fine-grained intraday view of the busiest session
    (the raw data is several disconnected drive-test days, not one
    continuous recording, so a single hourly timeline across the full
    span would be mostly blank)."""

    def generate(self, phone_df, output_file="outputs/kpi_timeline.png"):

        df = phone_df.dropna(subset=["time"]).copy()
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time")
        df["date"] = df["time"].dt.date

        daily = (
            df.groupby("date")
            .agg(
                rsrp=("rsrp_dbm", "median"),
                sinr=("sinr_db", "median"),
                dl=("dl_throughput_mbps", "median"),
                samples=("rsrp_dbm", "count")
            )
            .reset_index()
        )

        busiest_date = daily.loc[daily["samples"].idxmax(), "date"]

        intraday = (
            df[df["date"] == busiest_date]
            .set_index("time")
            .resample("10min")
            .agg(
                rsrp=("rsrp_dbm", "median"),
                sinr=("sinr_db", "median"),
                dl=("dl_throughput_mbps", "median")
            )
        )

        fig, axes = plt.subplots(2, 3, figsize=(15, 7))

        metrics = [
            ("rsrp", "Median RSRP (dBm)", "tab:red"),
            ("sinr", "Median SINR (dB)", "tab:blue"),
            ("dl", "Median DL (Mbps)", "tab:green")
        ]

        for col, (metric, label, color) in enumerate(metrics):

            axes[0, col].plot(
                daily["date"], daily[metric],
                marker="o", color=color
            )
            axes[0, col].set_title(f"{label} - By Drive-Test Day")
            axes[0, col].tick_params(axis="x", rotation=45)
            axes[0, col].grid(alpha=0.3)

            axes[1, col].plot(
                intraday.index, intraday[metric],
                marker=".", markersize=3, color=color
            )
            axes[1, col].set_title(
                f"{label} - Intraday ({busiest_date})"
            )
            axes[1, col].tick_params(axis="x", rotation=45)
            axes[1, col].grid(alpha=0.3)

        fig.suptitle("Network KPI Timeline")
        fig.tight_layout()
        fig.savefig(output_file, dpi=120)
        plt.close(fig)

        print(f"\nKPI timeline chart saved to: {output_file}")
