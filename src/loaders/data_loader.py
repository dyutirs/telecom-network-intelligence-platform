import pandas as pd

from config import (
    CELL_FILE,
    PHONE_FILE,
    SCANNER_FILE,
    CELL_5G_FILE,
    PHONE_5G_FILE
)

class DataLoader:

    def __init__(self):
        self.cell_df = None
        self.phone_df = None
        self.scanner_df = None

    def load(self):

        self.cell_df = pd.read_csv(CELL_FILE)

        self.phone_df = pd.read_csv(
            PHONE_FILE,
            low_memory=False
        )

        self.scanner_df = pd.read_csv(
            SCANNER_FILE,
            low_memory=False
        )

        return (
            self.cell_df,
            self.phone_df,
            self.scanner_df
        )

    def load_5g(self):

        cell_5g_df = pd.read_csv(CELL_5G_FILE)

        phone_5g_df = pd.read_parquet(PHONE_5G_FILE)

        return (
            cell_5g_df,
            phone_5g_df
        )