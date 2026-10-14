import pandas as pd

from schemas.common import CampaignRecord


class DataNormalizer:
    def to_frame(self, records: list[CampaignRecord]) -> pd.DataFrame:
        if not records:
            return pd.DataFrame(
                columns=[
                    "campaign_id",
                    "campaign_name",
                    "date",
                    "currency",
                    "spend",
                    "clicks",
                    "conversions",
                    "impressions",
                    "revenue",
                ]
            )
        frame = pd.DataFrame([record.model_dump() for record in records])
        frame["date"] = pd.to_datetime(frame["date"])
        return frame
