class RecommendationEngine:

    def generate(self, issue):

        recommendations = {

            "Coverage": [

                "Investigate coverage enhancement",

                "Review site density",

                "Evaluate cell edge performance",

                "Review propagation environment"

            ],

            "Quality": [

                "Investigate interference",

                "Review PCI reuse",

                "Review overlapping sectors",

                "Analyze SINR degradation"

            ],

            "Performance": [

                "Investigate congestion",

                "Review throughput bottlenecks",

                "Review scheduling efficiency",

                "Analyze traffic distribution"

            ],

            "Healthy": [

                "No immediate action required"

            ]
        }

        return recommendations.get(
            issue,
            []
        )