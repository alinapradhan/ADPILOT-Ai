import math

import pandas as pd


class MetricsEngine:
    @staticmethod
    def safe_divide(numerator: float | None, denominator: float | None) -> float | None:
        if numerator is None or denominator in (None, 0):
            return None
        return numerator / denominator

    def aggregate(self, frame: pd.DataFrame) -> dict[str, float | None]:
        if frame.empty:
            return {
                "spend": None,
                "clicks": None,
                "conversions": None,
                "impressions": None,
                "revenue": None,
                "cpa": None,
                "ctr": None,
                "cpc": None,
                "roas": None,
            }

        spend = frame["spend"].sum(min_count=1)
        clicks = frame["clicks"].sum(min_count=1)
        conversions = frame["conversions"].sum(min_count=1)
        impressions = frame["impressions"].sum(min_count=1)
        revenue = frame["revenue"].sum(min_count=1)

        def cast(value: object) -> float | None:
            if value is None or (isinstance(value, float) and math.isnan(value)):
                return None
            return float(value)

        spend_v = cast(spend)
        clicks_v = cast(clicks)
        conversions_v = cast(conversions)
        impressions_v = cast(impressions)
        revenue_v = cast(revenue)

        return {
            "spend": spend_v,
            "clicks": clicks_v,
            "conversions": conversions_v,
            "impressions": impressions_v,
            "revenue": revenue_v,
            "cpa": self.safe_divide(spend_v, conversions_v),
            "ctr": self.safe_divide(clicks_v, impressions_v),
            "cpc": self.safe_divide(spend_v, clicks_v),
            "roas": self.safe_divide(revenue_v, spend_v),
        }
