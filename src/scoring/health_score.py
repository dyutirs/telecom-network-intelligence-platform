import numpy as np


class HealthScorer:

    @staticmethod
    def coverage_score(rsrp):

        if rsrp >= -80:
            return 100

        if rsrp <= -120:
            return 0

        return (rsrp + 120) * 2.5

    @staticmethod
    def quality_score(sinr):

        if sinr >= 25:
            return 100

        if sinr <= -10:
            return 0

        return (sinr + 10) * (100 / 35)

    @staticmethod
    def throughput_score(dl):

        if dl >= 100:
            return 100

        if dl <= 0:
            return 0

        return dl

    def overall_score(
        self,
        rsrp,
        sinr,
        dl
    ):

        coverage = self.coverage_score(rsrp)

        quality = self.quality_score(sinr)

        throughput = self.throughput_score(dl)

        score = (
            0.4 * coverage
            + 0.4 * quality
            + 0.2 * throughput
        )

        return round(score, 2)