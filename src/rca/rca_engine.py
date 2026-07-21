import pandas as pd

# A cell needs at least this many total penalty points before its
# diagnosis confidence is allowed to reach 100% - a cell with only 1-2
# points is real but marginal, and shouldn't read as "fully certain".
SEVERITY_REFERENCE = 6


class RCAEngine:

    def analyze_cell(self, row):

        coverage = 0
        quality = 0
        performance = 0

        # ------------------
        # COVERAGE
        # ------------------

        if row["median_rsrp"] < -105:
            coverage += 3

        elif row["median_rsrp"] < -100:
            coverage += 2

        elif row["median_rsrp"] < -95:
            coverage += 1

        if row["median_pathloss"] > 130:
            coverage += 2

        elif row["median_pathloss"] > 120:
            coverage += 1

        if pd.notna(row["median_ta"]):

            if row["median_ta"] > 30:
                coverage += 2

            elif row["median_ta"] > 15:
                coverage += 1

        # ------------------
        # QUALITY
        # ------------------
        # Uses SINR rather than RSRQ: RSRQ is partly derived from RSRP,
        # so it re-punishes cells that are already caught by Coverage.
        # SINR isolates interference/noise independent of distance,
        # which is what "Quality" is meant to capture.

        if row["median_sinr"] < 0:
            quality += 2

        elif row["median_sinr"] < 5:
            quality += 1

        # ------------------
        # PERFORMANCE
        # ------------------

        if row["median_dl"] < 0.5:
            performance += 3

        elif row["median_dl"] < 1:
            performance += 2

        elif row["median_dl"] < 2:
            performance += 1

        total = (
            coverage +
            quality +
            performance
        )

        # Healthy threshold
        if total == 0:

            return {
                "issue": "Healthy",
                "confidence": 100,
                "coverage_score": 0,
                "quality_score": 0,
                "performance_score": 0
            }

        coverage_pct = coverage / total
        quality_pct = quality / total
        performance_pct = performance / total

        scores = {
            "Coverage": coverage_pct,
            "Quality": quality_pct,
            "Performance": performance_pct
        }

        if coverage >= 3:
            issue = "Coverage" 
        elif quality >= 3:
            issue = "Quality"

        elif performance >= 3:
            issue = "Performance"
        else:
        
            issue = max(
        scores,
        key=scores.get
    )

        # Confidence blends two things: how much the winning category
        # dominates the others (scores[issue]), and how severe the
        # total picture actually is (severity_cap). Without the cap, a
        # cell that trips just one lenient threshold shows the same
        # 100% confidence as a cell that is severely broken.
        severity_cap = min(total / SEVERITY_REFERENCE, 1.0)

        confidence = round(
            scores[issue] * severity_cap * 100,
            1
        )

        return {
            "issue": issue,
            "confidence": confidence,
            "coverage_score": round(
                coverage_pct * 100,
                1
            ),
            "quality_score": round(
                quality_pct * 100,
                1
            ),
            "performance_score": round(
                performance_pct * 100,
                1
            )
        }