from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

CELL_FILE = DATA_DIR / "cell_info_final_lte.csv"
PHONE_FILE = DATA_DIR / "phone_data_lte.csv"
SCANNER_FILE = DATA_DIR / "scanner_data_lte.csv"

CELL_5G_FILE = BASE_DIR / "estimated_cell_info" / "cell_info_final_5g.csv"
PHONE_5G_FILE = BASE_DIR / "phone" / "phone_data_5g.parquet"

OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)