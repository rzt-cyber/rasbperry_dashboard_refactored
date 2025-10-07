class OverviewCalculations:
    def __init__(self, data_manager):
        self.dm = data_manager

    def apply_filters(
        self, df, start_date=None, end_date=None, regions=None, categories=None
    ):
        """Применение фильтров к DataFrame"""
        df = df[df["transaction_date"].dt.year == 2025]

        if start_date and end_date:
            df = df[
                (df["transaction_date"] >= start_date)
                & (df["transaction_date"] <= end_date)
            ]

        if regions and len(regions) > 0:
            if "region" not in df.columns:
                df = df.merge(
                    self.dm.df_user_segments[["customer_id", "region"]],
                    on="customer_id",
                )
            df = df[df["region"].isin(regions)]

        if categories is not None and len(categories) > 0:
            if "category" not in df.columns:
                df = df.merge(
                    self.dm.df_products[["product_id", "category"]], on="product_id"
                )
            df = df[df["category"].isin(categories)]

        return df

    def calculate_total_revenue(
        self, start_date=None, end_date=None, regions=None, categories=None
    ):
        df = self.dm.df_sales.copy()
        df = self.apply_filters(df, start_date, end_date, regions, categories)

        df = df.merge(self.dm.df_products[["product_id", "price"]], on="product_id")
        df["revenue"] = df["quantity"] * df["price"]

        return round(df["revenue"].sum(), 2)

    def calculate_orders_count(
        self, start_date=None, end_date=None, regions=None, categories=None
    ):
        df = self.dm.df_sales.copy()
        df = self.apply_filters(df, start_date, end_date, regions, categories)
        return df["transaction_id"].nunique()

    def calculate_avg_order_value(
        self, start_date=None, end_date=None, regions=None, categories=None
    ):
        total_revenue = self.calculate_total_revenue(
            start_date, end_date, regions, categories
        )
        orders_count = self.calculate_orders_count(
            start_date, end_date, regions, categories
        )

        return round(total_revenue / orders_count, 2) if orders_count > 0 else 0

    def calculate_active_users(
        self, start_date=None, end_date=None, regions=None, categories=None
    ):
        df = self.dm.df_sales.copy()
        df = self.apply_filters(df, start_date, end_date, regions, categories)
        return df["customer_id"].nunique()

    def calculate_ad_spend(self, start_date=None, end_date=None):
        df = self.dm.df_ad_revenue.copy()

        if start_date and end_date:
            df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

        return round(df["spend"].sum(), 2)

    def calculate_romi(self, start_date=None, end_date=None):
        ad_spend = self.calculate_ad_spend(start_date, end_date)
        ad_revenue_df = self.dm.df_ad_revenue.copy()

        if start_date and end_date:
            ad_revenue_df = ad_revenue_df[
                (ad_revenue_df["date"] >= start_date)
                & (ad_revenue_df["date"] <= end_date)
            ]

        ad_revenue = ad_revenue_df["revenue"].sum()

        return round((ad_revenue - ad_spend) / ad_spend * 100, 2) if ad_spend > 0 else 0
