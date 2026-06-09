import pandas as pd


class PCIAnalysis:

    def analyze(self, cell_table):

        pci_stats = (
            cell_table
            .groupby("pci")
            .agg(
                cells=("cell_id", "count"),

                sites=("enb_id", "nunique"),

                avg_health=(
                    "health_score",
                    "mean"
                )
            )
            .reset_index()
        )

        pci_stats = pci_stats.sort_values(
            "cells",
            ascending=False
        )

        return pci_stats