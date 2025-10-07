class CustomersCalculations:
    def __init__(self, data_manager):
        self.dm = data_manager

    def get_filtered_data(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        """Получает отфильтрованные данные клиентов с учетом ВСЕХ фильтров"""

        df_users = self.dm.df_user_segments.copy()

        if start_date and end_date:
            df_users = df_users[
                (df_users["registration_date"] >= start_date)
                & (df_users["registration_date"] <= end_date)
            ]

        if regions and len(regions) > 0:
            df_users = df_users[df_users["region"].isin(regions)]

        if segments and len(segments) > 0:
            df_users = df_users[df_users["segment"].isin(segments)]

        if (channels and len(channels) > 0) or (devices and len(devices) > 0):
            df_traffic = self.dm.df_traffic.copy()

            if channels and len(channels) > 0:
                df_traffic = df_traffic[df_traffic["channel"].isin(channels)]

            if devices and len(devices) > 0:
                df_traffic = df_traffic[df_traffic["device"].isin(devices)]

            df_users = df_users.merge(
                df_traffic[["customer_id"]].drop_duplicates(),
                on="customer_id",
                how="inner",
            )

        return df_users

    def get_filtered_traffic_data(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        """Получает отфильтрованные данные трафика с учетом ВСЕХ фильтров"""

        df_traffic = self.dm.df_traffic.copy()

        df_traffic = df_traffic.merge(
            self.dm.df_user_segments[
                ["customer_id", "region", "segment", "registration_date"]
            ],
            on="customer_id",
            how="inner",
        )

        if start_date and end_date:
            df_traffic = df_traffic[
                (df_traffic["registration_date"] >= start_date)
                & (df_traffic["registration_date"] <= end_date)
            ]

        if regions and len(regions) > 0:
            df_traffic = df_traffic[df_traffic["region"].isin(regions)]

        if segments and len(segments) > 0:
            df_traffic = df_traffic[df_traffic["segment"].isin(segments)]

        if channels and len(channels) > 0:
            df_traffic = df_traffic[df_traffic["channel"].isin(channels)]

        if devices and len(devices) > 0:
            df_traffic = df_traffic[df_traffic["device"].isin(devices)]

        return df_traffic

    def calculate_total_customers(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df["customer_id"].nunique()

    def calculate_new_customers(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df[df["segment"] == "new"]["customer_id"].nunique()

    def calculate_loyal_customers(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df[df["segment"] == "loyal"]["customer_id"].nunique()

    def calculate_risk_customers(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df[df["segment"] == "churn_risk"]["customer_id"].nunique()

    def calculate_high_spender_customers(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df[df["segment"] == "high_spender"]["customer_id"].nunique()

    def calculate_discount_hunter_customers(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df[df["segment"] == "discount_hunter"]["customer_id"].nunique()

    def get_segments_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df.groupby("segment")["customer_id"].nunique().reset_index()

    def get_registrations_trend(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        daily_registrations = (
            df.groupby(df["registration_date"].dt.date)["customer_id"]
            .nunique()
            .reset_index()
        )
        daily_registrations.columns = ["date", "registrations"]
        return daily_registrations.sort_values("date")

    def get_regions_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_data(
            start_date, end_date, regions, segments, channels, devices
        )
        return df.groupby("region")["customer_id"].nunique().reset_index()

    def get_channels_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        df = self.get_filtered_traffic_data(
            start_date, end_date, regions, segments, channels, devices
        )

        channels_distribution = (
            df.groupby("channel")["customer_id"].nunique().reset_index()
        )
        channels_distribution.columns = ["channel", "unique_customers"]

        return channels_distribution

    def get_segments_by_channels_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        """Распределение сегментов по каналам - для кросс-анализа"""
        df = self.get_filtered_traffic_data(
            start_date, end_date, regions, segments, channels, devices
        )

        segments_by_channels = (
            df.groupby(["channel", "segment"])["customer_id"].nunique().reset_index()
        )
        segments_by_channels.columns = ["channel", "segment", "unique_customers"]

        return segments_by_channels
