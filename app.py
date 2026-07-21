import pandas as pd


from src.loaders.data_loader import DataLoader

from src.intelligence.cell_engine import CellEngine
from src.intelligence.site_engine import SiteEngine

from src.overshooting import overshooting_engine
from src.rca.rca_engine import RCAEngine

from src.recommendations.recommendation_engine import (
    RecommendationEngine
)

from src.pci.pci_analysis import PCIAnalysis

from src.visualization.map_generator import (
    MapGenerator
)
from src.intelligence.critical_site_engine import (
    CriticalSiteEngine
)
from src.pci.pci_conflict import PCIConflictAnalysis
from src.sector.sector_imbalance import SectorImbalance
from src.actions.action_engine import ActionEngine
from src.risk.site_risk_engine import (
    SiteRiskEngine
)
from src.congestion.congestion_engine import (
    CongestionEngine
)
from src.overshooting.overshooting_engine import (
    OvershootingEngine
)
from src.multirat.coverage_grid import CoverageGridEngine
from src.multirat.interworking_engine import InterworkingEngine
from src.neighbors.neighbor_analysis import NeighborAnalysis
from src.intelligence.sector_engine import SectorEngine
from src.pci.pci_suggestion import PCISuggestion
from src.mobility.handover_engine import HandoverEngine
from src.propagation.obstruction_engine import ObstructionEngine
from src.energy.cell_sleep_engine import CellSleepEngine
from src.visualization.timeline_chart import TimelineChart
def main():

    print("\n==============================")
    print("LOADING DATA")
    print("==============================")

    loader = DataLoader()

    cell_info, phone_df, scanner_df = loader.load()
    print("\nCELL INFO COLUMNS:")
    print(cell_info.columns.tolist())

    print("\nDATASET CHECK")
    

    print("Inventory Cells:", cell_info["cell_id"].nunique())
    print("Phone Cells:", phone_df["cell_id"].nunique())
    print("Scanner Cells:", scanner_df["cell_id"].nunique())

    print("Inventory Sites:", cell_info["enb_id"].nunique())
    print("Phone Sites:", phone_df["enb_id"].nunique())
    print("Scanner Sites:", scanner_df["enb_id"].nunique())
    print("\nTECHNOLOGY DISTRIBUTION:")

    print(
    cell_info["technology"]
    .value_counts()
)
    # ==================================================
    # CELL INTELLIGENCE
    # ==================================================

    print("\n==============================")
    print("CELL INTELLIGENCE")
    print("==============================")

    cell_engine = CellEngine()

    cell_table = cell_engine.build_cell_table(
        phone_df
    )

    print(
        "Total Cells After Filter:",
        len(cell_table)
    )

    print(
        "Min Measurements:",
        cell_table["measurements"].min()
    )

    print(
        "Median Measurements:",
        cell_table["measurements"].median()
    )

    print(
        "Max Measurements:",
        cell_table["measurements"].max()
    )

    # ==================================================
    # SITE INTELLIGENCE
    # ==================================================

    print("\n==============================")
    print("SITE INTELLIGENCE")
    print("==============================")

    site_engine = SiteEngine()

    site_table = site_engine.build_site_table(
        cell_table
    )

    print(
        "Sites Analyzed:",
        len(site_table)
    )
    print("\n==============================")
    print("CRITICAL SITE RANKING")
    print("==============================")

    critical_engine = (
    CriticalSiteEngine()
)

    critical_sites = (
    critical_engine.build(
        cell_table
    )
)

    print(
    critical_sites.head(20)
)
    print("\n==============================")
    print("SECTOR IMBALANCE ANALYSIS")
    print("==============================")

    imbalance_engine = (
    SectorImbalance()
)

    imbalance_table = (
    imbalance_engine.analyze(
        cell_table
    )
)

    print(
    imbalance_table.head(20)
)
    print("\n==============================")
    print("SITE RISK RANKING")
    print("==============================")

    risk_engine = (
    SiteRiskEngine()
)

    risk_table = (
    risk_engine.build(
        critical_sites,
        imbalance_table,
        site_table
    )
)

    print(
    risk_table.head(20)
)
    # ==================================================
    # RCA
    # ==================================================

    print("\n==============================")
    print("ROOT CAUSE ANALYSIS")
    print("==============================")

    rca_engine = RCAEngine()

    recommendation_engine = (
        RecommendationEngine()
    )

    rca_results = []

    for _, row in cell_table.iterrows():

        result = (
            rca_engine.analyze_cell(
                row
            )
        )

        recommendations = (
            recommendation_engine.generate(
                result["issue"]
            )
        )

        result["cell_id"] = row["cell_id"]
        result["enb_id"] = row["enb_id"]
        result["health_score"] = row["health_score"]

        result["recommendations"] = (
            " | ".join(recommendations)
        )

        rca_results.append(result)

    rca_df = pd.DataFrame(
        rca_results
    )




    # ==================================================
    # PCI ANALYSIS
    # ==================================================

    print("\n==============================")
    print("PCI ANALYSIS")
    print("==============================")

    pci_engine = PCIAnalysis()

    pci_table = pci_engine.analyze(
        cell_table
    )

    print("\nTOP PCI REUSE")

    print(
        pci_table.head(20)
    )
    print("\n==============================")
    print("PCI CONFLICT ANALYSIS")
    print("==============================")

    conflict_engine = PCIConflictAnalysis()

    conflict_table = (
    conflict_engine.analyze(
        cell_info
    )
)

    print(
    conflict_table.head(20)
)
    print("\n==============================")
    print("CONGESTION ANALYSIS")
    print("==============================")

    congestion_engine = (
    CongestionEngine()
)

    congestion_table = (
    congestion_engine.analyze(
        cell_table
    )
)

    congestion_table.sort_values(
    "health_score",
    ascending=False
).head(10)

    print(
    "\nTotal Congestion Candidates:",
    len(congestion_table)
)
    print("\nCONGESTION DISTRIBUTION")

    print(
    congestion_table["issue"]
    .value_counts()
)
    print("\n==============================")
    print("OVERSHOOTING ANALYSIS")
    print("==============================")

    overshooting_engine = (
    OvershootingEngine()
)

    overshooting_table = (
    overshooting_engine.analyze(
        cell_table
    )
)

    print(
    overshooting_table.head(20)
)

    print(
    "\nTotal Overshooting Candidates:",
    len(overshooting_table)
)

    print(
    "\nOVERSHOOTING DISTRIBUTION"
)

    print(
    overshooting_table["issue"]
    .value_counts()
)
    print("\n==============================")
    print("TOP ACTION LIST")
    print("==============================")

    action_engine = ActionEngine()

    action_table = (
    action_engine.generate(
        rca_df,
        imbalance_table,
        conflict_table,
        congestion_table,
        overshooting_table
    )
)
    print(
    action_table
    .sort_values(
        ["priority", "category"]
    )
)
    print("\nACTION DISTRIBUTION")

    print(
    action_table["category"]
    .value_counts()
)

    # ==================================================
    # RCA MAP DATA
    # ==================================================

    rca_map_df = cell_table.merge(
        rca_df[
            [
                "cell_id",
                "issue",
                "confidence"
            ]
        ],
        on="cell_id",
        how="left"
    )

    # ==================================================
    # REPORTS
    # ==================================================

    print("\n==============================")
    print("TOP 20 WORST CELLS")
    print("==============================")

    print(
        cell_table
        .sort_values(
            "health_score"
        )
        .head(20)
    )

    print("\n==============================")
    print("TOP 20 WORST SITES")
    print("==============================")

    print(
        site_table
        .sort_values(
            "health_score"
        )
        .head(20)
    )

    print("\n==============================")
    print("TOP RCA CELLS")
    print("==============================")

    print(
        rca_df
        .sort_values(
            "health_score"
        )
        .head(20)
    )

    print("\n==============================")
    print("RCA DISTRIBUTION")
    print("==============================")

    print(
        rca_df["issue"]
        .value_counts()
    )
    print("\n==============================")
    print("HEALTH SCORE BY RCA")
    print("==============================")

    print(
    rca_df.groupby("issue")["health_score"]
    .mean()
    .sort_values()
)
    # ==================================================
    # EXPORT REPORTS
    # ==================================================

    rca_df.to_csv(
        "outputs/rca_results.csv",
        index=False
    )

    pci_table.to_csv(
        "outputs/pci_analysis.csv",
        index=False
    )
    critical_sites.to_csv(
    "outputs/critical_sites.csv",
    index=False
)
    risk_table.to_csv(
    "outputs/site_risk_ranking.csv",
    index=False
)
    congestion_table.to_csv(
    "outputs/congestion_analysis.csv",
    index=False
)
    overshooting_table.to_csv(
    "outputs/overshooting_analysis.csv",
    index=False
)
    # ==================================================
    # MAP
    # ==================================================

    print("\n==============================")
    print("GENERATING MAP")
    print("==============================")

    map_generator = MapGenerator()

    map_generator.generate_bad_cell_map(
        rca_map_df
    )

    # ==================================================
    # MULTI-RAT (5G) COVERAGE COMPARISON
    # ==================================================

    print("\n==============================")
    print("LOADING 5G DATA")
    print("==============================")

    cell_info_5g, phone_5g_df = loader.load_5g()

    print("5G Cells (known positions):", len(cell_info_5g))
    print("5G Measurements:", len(phone_5g_df))

    print("\n==============================")
    print("BUILDING COVERAGE GRID (LTE vs 5G)")
    print("==============================")

    grid_engine = CoverageGridEngine()

    coverage_grid = grid_engine.build(
        phone_df,
        phone_5g_df
    )

    print("Grid Cells:", len(coverage_grid))
    print(coverage_grid["winner"].value_counts())

    coverage_grid.to_csv(
        "outputs/coverage_grid.csv",
        index=False
    )

    print("\n==============================")
    print("GENERATING MULTI-RAT MAP")
    print("==============================")

    map_generator.generate_multirat_map(
        rca_map_df,
        cell_info_5g,
        coverage_grid
    )

    # ==================================================
    # NEIGHBOR ANALYSIS (ANR)
    # ==================================================

    print("\n==============================")
    print("NEIGHBOR ANALYSIS (ANR)")
    print("==============================")

    neighbor_table = NeighborAnalysis().analyze(cell_table)

    print(neighbor_table["issue"].value_counts())

    neighbor_table.to_csv(
        "outputs/neighbor_analysis.csv",
        index=False
    )

    # ==================================================
    # SECTOR INTELLIGENCE
    # ==================================================

    print("\n==============================")
    print("SECTOR INTELLIGENCE")
    print("==============================")

    sector_table = SectorEngine().build_sector_table(cell_table)

    print("Sectors Analyzed:", len(sector_table))

    sector_table.to_csv(
        "outputs/sector_intelligence.csv",
        index=False
    )

    # ==================================================
    # PCI AUTO-SUGGESTION
    # ==================================================

    print("\n==============================")
    print("PCI AUTO-SUGGESTION")
    print("==============================")

    pci_suggestions = PCISuggestion().suggest(
        conflict_table,
        cell_info,
        cell_table
    )

    print("Suggestions Generated:", len(pci_suggestions))

    pci_suggestions.to_csv(
        "outputs/pci_suggestions.csv",
        index=False
    )

    # ==================================================
    # HANDOVER PING-PONG DETECTION (MRO)
    # ==================================================

    print("\n==============================")
    print("HANDOVER PING-PONG DETECTION (MRO)")
    print("==============================")

    handover_table = HandoverEngine().analyze(phone_df)

    print("Ping-Pong Cell Pairs:", len(handover_table))

    handover_table.to_csv(
        "outputs/handover_pingpong.csv",
        index=False
    )

    # ==================================================
    # BUILDING OBSTRUCTION DIAGNOSIS (COVERAGE CELLS)
    # ==================================================

    print("\n==============================")
    print("BUILDING OBSTRUCTION DIAGNOSIS")
    print("==============================")

    obstruction_table = ObstructionEngine(
        "vienna_city_model/bkm_complete_31287.tif"
    ).analyze(
        rca_df,
        cell_table,
        cell_info
    )

    print(obstruction_table["diagnosis"].value_counts())

    obstruction_table.to_csv(
        "outputs/obstruction_analysis.csv",
        index=False
    )

    # ==================================================
    # 5G/LTE INTERWORKING RECOMMENDATIONS
    # ==================================================

    print("\n==============================")
    print("5G/LTE INTERWORKING")
    print("==============================")

    interworking_grid = InterworkingEngine().analyze(
        coverage_grid,
        cell_info_5g
    )

    print(interworking_grid["interworking_status"].value_counts())

    interworking_grid.to_csv(
        "outputs/interworking_analysis.csv",
        index=False
    )

    # ==================================================
    # CELL SLEEP / ENERGY-SAVING CANDIDATES
    # ==================================================

    print("\n==============================")
    print("CELL SLEEP CANDIDATES")
    print("==============================")

    sleep_candidates = CellSleepEngine().analyze(cell_table)

    print("Candidates:", len(sleep_candidates))

    sleep_candidates.to_csv(
        "outputs/cell_sleep_candidates.csv",
        index=False
    )

    # ==================================================
    # KPI TIMELINE CHART
    # ==================================================

    print("\n==============================")
    print("KPI TIMELINE CHART")
    print("==============================")

    TimelineChart().generate(phone_df)

    # ==================================================
    # SUMMARY
    # ==================================================

    print("\n==============================")
    print("UNIQUE COUNTS")
    print("==============================")

    print(
        "Cells:",
        cell_table["cell_id"].nunique()
    )

    print(
        "Sites:",
        cell_table["enb_id"].nunique()
    )
    cell_table.to_excel(
    "outputs/cell_intelligence.xlsx",
    index=False
)

    site_table.to_excel(
    "outputs/site_intelligence.xlsx",
    index=False
)

    rca_df.to_excel(
    "outputs/rca_results.xlsx",
    index=False
)

    pci_table.to_excel(
    "outputs/pci_analysis.xlsx",
    index=False
)
    cell_table.to_csv(
    "outputs/cell_intelligence.csv",
    index=False
)

    site_table.to_csv(
    "outputs/site_intelligence.csv",
    index=False
)

    imbalance_table.to_csv(
    "outputs/sector_imbalance.csv",
    index=False
)

    conflict_table.to_csv(
    "outputs/pci_conflicts.csv",
    index=False
)

    action_table.to_csv(
    "outputs/action_list.csv",
    index=False
)


    print("\n==============================")
    print("PROCESS COMPLETE")
    print("==============================")
    print("\nDL THROUGHPUT DISTRIBUTION")

    print(
    cell_table["median_dl"]
    .describe()
)

if __name__ == "__main__":
    main()