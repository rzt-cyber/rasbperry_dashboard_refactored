import pandas as pd


class MarketingCalculations:
    def __init__(self, data_manager):
        self.dm = data_manager

    def get_filtered_ad_data(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        """Получает отфильтрованные данные рекламы с учетом ВСЕХ фильтров"""

        try:
            df_ads = self.dm.df_ad_revenue.copy()

            df_ads = df_ads.merge(
                self.dm.df_products[["product_id", "category"]],
                on="product_id",
                how="left",
            )

            if start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df_ads = df_ads[
                    (df_ads["date"] >= start_date) & (df_ads["date"] <= end_date)
                ]

            if campaigns and len(campaigns) > 0:
                df_ads = df_ads[df_ads["campaign_name"].isin(campaigns)]

            if categories and len(categories) > 0:
                df_ads = df_ads[df_ads["category"].isin(categories)]

            return df_ads

        except Exception as e:
            print(f"Error in get_filtered_ad_data: {e}")
            return pd.DataFrame()

    def get_filtered_traffic_data(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        """Получает отфильтрованные данные трафика с учетом ВСЕХ фильтров"""

        try:
            df_traffic = self.dm.df_traffic.copy()

            df_traffic = df_traffic.merge(
                self.dm.df_user_segments[["customer_id", "segment"]],
                on="customer_id",
                how="left",
            )

            if start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df_traffic = df_traffic[
                    (df_traffic["session_start"] >= start_date)
                    & (df_traffic["session_start"] <= end_date)
                ]

            if channels and len(channels) > 0:
                df_traffic = df_traffic[df_traffic["channel"].isin(channels)]

            if devices and len(devices) > 0:
                df_traffic = df_traffic[df_traffic["device"].isin(devices)]

            if segments and len(segments) > 0:
                df_traffic = df_traffic[df_traffic["segment"].isin(segments)]

            return df_traffic

        except Exception as e:
            print(f"Error in get_filtered_traffic_data: {e}")
            return pd.DataFrame()

    def calculate_total_romi(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_ads = self.get_filtered_ad_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_ads.empty:
                return 0

            total_spend = df_ads["spend"].sum()
            total_revenue = df_ads["revenue"].sum()

            return (
                round(((total_revenue - total_spend) / total_spend) * 100, 2)
                if total_spend > 0
                else 0
            )
        except Exception as e:
            print(f"Error calculating total ROMI: {e}")
            return 0

    def calculate_total_spend(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_ads = self.get_filtered_ad_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_ads.empty:
                return 0
            return round(df_ads["spend"].sum(), 2)
        except Exception as e:
            print(f"Error calculating total spend: {e}")
            return 0

    def calculate_total_revenue(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_ads = self.get_filtered_ad_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_ads.empty:
                return 0
            return round(df_ads["revenue"].sum(), 2)
        except Exception as e:
            print(f"Error calculating total revenue: {e}")
            return 0

    def calculate_ctr(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_ads = self.get_filtered_ad_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_ads.empty:
                return 0

            total_clicks = df_ads["clicks"].sum()
            total_impressions = df_ads["impressions"].sum()

            return (
                round((total_clicks / total_impressions) * 100, 2)
                if total_impressions > 0
                else 0
            )
        except Exception as e:
            print(f"Error calculating CTR: {e}")
            return 0

    def calculate_cac(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            total_spend = self.calculate_total_spend(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )

            df_traffic = self.get_filtered_traffic_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_traffic.empty:
                return 0

            unique_customers = df_traffic["customer_id"].nunique()

            return (
                round(total_spend / unique_customers, 2) if unique_customers > 0 else 0
            )
        except Exception as e:
            print(f"Error calculating CAC: {e}")
            return 0

    def calculate_conversion_rate(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_ads = self.get_filtered_ad_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_ads.empty:
                return 0

            total_clicks = df_ads["clicks"].sum()

            total_purchases = len(df_ads[df_ads["revenue"] > 0])

            return (
                round((total_purchases / total_clicks) * 100, 2)
                if total_clicks > 0
                else 0
            )
        except Exception as e:
            print(f"Error calculating conversion rate: {e}")
            return 0

    def get_romi_trend(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_ads = self.get_filtered_ad_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_ads.empty:
                return pd.DataFrame()

            daily_data = (
                df_ads.groupby("date")
                .agg({"spend": "sum", "revenue": "sum"})
                .reset_index()
            )

            daily_data["romi"] = (
                (daily_data["revenue"] - daily_data["spend"]) / daily_data["spend"]
            ) * 100
            daily_data["romi"] = daily_data["romi"].round(2)

            return daily_data[["date", "romi"]].sort_values("date")
        except Exception as e:
            print(f"Error getting ROMI trend: {e}")
            return pd.DataFrame()

    def get_budget_distribution(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_traffic = self.get_filtered_traffic_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_traffic.empty:
                return pd.DataFrame()

            channel_distribution = (
                df_traffic.groupby("channel")["traffic_id"].nunique().reset_index()
            )
            channel_distribution.columns = ["channel", "sessions"]

            return channel_distribution.sort_values("sessions", ascending=False)
        except Exception as e:
            print(f"Error getting budget distribution: {e}")
            return pd.DataFrame()

    def get_campaigns_effectiveness(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_ads = self.get_filtered_ad_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_ads.empty:
                return pd.DataFrame()

            campaigns_data = (
                df_ads.groupby("campaign_name")
                .agg(
                    {
                        "spend": "sum",
                        "revenue": "sum",
                        "clicks": "sum",
                        "impressions": "sum",
                    }
                )
                .reset_index()
            )

            campaigns_data["romi"] = (
                (campaigns_data["revenue"] - campaigns_data["spend"])
                / campaigns_data["spend"]
            ) * 100
            campaigns_data["romi"] = campaigns_data["romi"].round(2)
            campaigns_data["ctr"] = (
                campaigns_data["clicks"] / campaigns_data["impressions"] * 100
            ).round(2)

            return campaigns_data.nlargest(10, "romi")  # Топ-10 кампаний по ROMI
        except Exception as e:
            print(f"Error getting campaigns effectiveness: {e}")
            return pd.DataFrame()

    def get_ctr_by_channels(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_traffic = self.get_filtered_traffic_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_traffic.empty:
                return pd.DataFrame()

            channel_sessions = (
                df_traffic.groupby("channel")["traffic_id"].nunique().reset_index()
            )
            channel_sessions.columns = ["channel", "sessions"]

            return channel_sessions.sort_values("sessions", ascending=False)
        except Exception as e:
            print(f"Error getting CTR by channels: {e}")
            return pd.DataFrame()

    def get_cac_by_segments(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            total_spend = self.calculate_total_spend(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )

            df_traffic = self.get_filtered_traffic_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_traffic.empty:
                return pd.DataFrame()

            segment_data = (
                df_traffic.groupby("segment")
                .agg({"customer_id": "nunique"})
                .reset_index()
            )

            segment_data["cac"] = (total_spend / len(segment_data)) / segment_data[
                "customer_id"
            ]
            segment_data["cac"] = segment_data["cac"].round(2)

            return segment_data[["segment", "cac"]].sort_values("cac")
        except Exception as e:
            print(f"Error getting CAC by segments: {e}")
            return pd.DataFrame()

    def get_conversion_by_devices(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        try:
            df_traffic = self.get_filtered_traffic_data(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            if df_traffic.empty:
                return pd.DataFrame()

            device_sessions = (
                df_traffic.groupby("device")["traffic_id"].nunique().reset_index()
            )
            device_sessions.columns = ["device", "sessions"]

            return device_sessions.sort_values("sessions", ascending=False)
        except Exception as e:
            print(f"Error getting conversion by devices: {e}")
            return pd.DataFrame()
