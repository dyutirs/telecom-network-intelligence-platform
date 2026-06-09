import pandas as pd

from config import (
    CELL_FILE,
    PHONE_FILE,
    SCANNER_FILE
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