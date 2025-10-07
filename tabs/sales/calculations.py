import pandas as pd


class SalesCalculations:
    def __init__(self, data_manager):
        self.dm = data_manager

    def get_filtered_sales_data(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        """Получает отфильтрованные данные продаж с учетом ВСЕХ фильтров"""

        try:
            df_sales = self.dm.df_sales.copy()

            df_sales = df_sales.merge(
                self.dm.df_products[
                    ["product_id", "product_name", "category", "price", "supplier_id"]
                ],
                on="product_id",
                how="left",
            )

            df_sales = df_sales.merge(
                self.dm.df_suppliers[["supplier_id", "supplier_name"]],
                on="supplier_id",
                how="left",
            )

            df_sales = df_sales.merge(
                self.dm.df_user_segments[["customer_id", "region", "segment"]],
                on="customer_id",
                how="left",
            )

            if start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df_sales = df_sales[
                    (df_sales["transaction_date"] >= start_date)
                    & (df_sales["transaction_date"] <= end_date)
                ]

            if regions and len(regions) > 0:
                df_sales = df_sales[df_sales["region"].isin(regions)]

            if categories and len(categories) > 0:
                df_sales = df_sales[df_sales["category"].isin(categories)]

            if segments and len(segments) > 0:
                df_sales = df_sales[df_sales["segment"].isin(segments)]

            if payment_methods and len(payment_methods) > 0:
                df_sales = df_sales[df_sales["payment_method"].isin(payment_methods)]

            if suppliers and len(suppliers) > 0:
                df_sales = df_sales[df_sales["supplier_name"].isin(suppliers)]

            df_sales["revenue"] = df_sales["quantity"] * df_sales["price"]

            return df_sales

        except Exception as e:
            print(f"Error in get_filtered_sales_data: {e}")
            return pd.DataFrame()

    def calculate_total_revenue(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return 0
            return round(df["revenue"].sum(), 2)
        except Exception as e:
            print(f"Error calculating total revenue: {e}")
            return 0

    def calculate_orders_count(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return 0
            return df["transaction_id"].nunique()
        except Exception as e:
            print(f"Error calculating orders count: {e}")
            return 0

    def calculate_avg_order_value(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            total_revenue = self.calculate_total_revenue(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            orders_count = self.calculate_orders_count(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            return round(total_revenue / orders_count, 2) if orders_count > 0 else 0
        except Exception as e:
            print(f"Error calculating avg order value: {e}")
            return 0

    def calculate_total_quantity(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return 0
            return df["quantity"].sum()
        except Exception as e:
            print(f"Error calculating total quantity: {e}")
            return 0

    def calculate_return_rate(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            orders_count = self.calculate_orders_count(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if orders_count == 0:
                return 0

            df_returns = self.dm.df_returns.copy()

            df_returns = df_returns.merge(
                self.dm.df_sales[
                    ["transaction_id", "transaction_date", "payment_method"]
                ],
                on="transaction_id",
                how="left",
            )

            df_returns = df_returns.merge(
                self.dm.df_products[["product_id", "category", "supplier_id"]],
                on="product_id",
                how="left",
            )

            df_returns = df_returns.merge(
                self.dm.df_suppliers[["supplier_id", "supplier_name"]],
                on="supplier_id",
                how="left",
            )

            df_returns = df_returns.merge(
                self.dm.df_user_segments[["customer_id", "region", "segment"]],
                on="customer_id",
                how="left",
            )

            if start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df_returns = df_returns[
                    (df_returns["transaction_date"] >= start_date)
                    & (df_returns["transaction_date"] <= end_date)
                ]

            if regions and len(regions) > 0:
                df_returns = df_returns[df_returns["region"].isin(regions)]

            if categories and len(categories) > 0:
                df_returns = df_returns[df_returns["category"].isin(categories)]

            if segments and len(segments) > 0:
                df_returns = df_returns[df_returns["segment"].isin(segments)]

            if payment_methods and len(payment_methods) > 0:
                df_returns = df_returns[
                    df_returns["payment_method"].isin(payment_methods)
                ]

            if suppliers and len(suppliers) > 0:
                df_returns = df_returns[df_returns["supplier_name"].isin(suppliers)]

            returns_count = df_returns["return_id"].nunique()

            return (
                round((returns_count / orders_count) * 100, 2)
                if orders_count > 0
                else 0
            )

        except Exception as e:
            print(f"Error calculating return rate: {e}")
            return 0

    def calculate_unique_customers(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return 0
            return df["customer_id"].nunique()
        except Exception as e:
            print(f"Error calculating unique customers: {e}")
            return 0

    def get_regions_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return pd.DataFrame()
            regions_revenue = df.groupby("region")["revenue"].sum().reset_index()
            return regions_revenue.sort_values("revenue", ascending=False)
        except Exception as e:
            print(f"Error getting regions distribution: {e}")
            return pd.DataFrame()

    def get_segments_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return pd.DataFrame()
            segments_revenue = df.groupby("segment")["revenue"].sum().reset_index()
            return segments_revenue.sort_values("revenue", ascending=False)
        except Exception as e:
            print(f"Error getting segments distribution: {e}")
            return pd.DataFrame()

    def get_payment_methods_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return pd.DataFrame()
            payment_methods_revenue = (
                df.groupby("payment_method")["revenue"].sum().reset_index()
            )
            return payment_methods_revenue.sort_values("revenue", ascending=False)
        except Exception as e:
            print(f"Error getting payment methods distribution: {e}")
            return pd.DataFrame()

    def get_suppliers_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return pd.DataFrame()
            suppliers_revenue = (
                df.groupby("supplier_name")["revenue"].sum().reset_index()
            )
            return suppliers_revenue.nlargest(10, "revenue")
        except Exception as e:
            print(f"Error getting suppliers distribution: {e}")
            return pd.DataFrame()

    def get_hourly_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        try:
            df = self.get_filtered_sales_data(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            if df.empty:
                return pd.DataFrame()
            df["hour"] = df["transaction_date"].dt.hour
            hourly_revenue = df.groupby("hour")["revenue"].sum().reset_index()
            return hourly_revenue.sort_values("hour")
        except Exception as e:
            print(f"Error getting hourly distribution: {e}")
            return pd.DataFrame()

    def get_returns_reasons_distribution(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        """Распределение возвратов по причинам"""
        try:
            df_returns = self.dm.df_returns.copy()

            df_returns = df_returns.merge(
                self.dm.df_sales[
                    ["transaction_id", "transaction_date", "payment_method"]
                ],
                on="transaction_id",
                how="left",
            )

            df_returns = df_returns.merge(
                self.dm.df_products[["product_id", "category", "supplier_id"]],
                on="product_id",
                how="left",
            )

            df_returns = df_returns.merge(
                self.dm.df_suppliers[["supplier_id", "supplier_name"]],
                on="supplier_id",
                how="left",
            )

            df_returns = df_returns.merge(
                self.dm.df_user_segments[["customer_id", "region", "segment"]],
                on="customer_id",
                how="left",
            )

            if start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df_returns = df_returns[
                    (df_returns["transaction_date"] >= start_date)
                    & (df_returns["transaction_date"] <= end_date)
                ]

            if regions and len(regions) > 0:
                df_returns = df_returns[df_returns["region"].isin(regions)]

            if categories and len(categories) > 0:
                df_returns = df_returns[df_returns["category"].isin(categories)]

            if segments and len(segments) > 0:
                df_returns = df_returns[df_returns["segment"].isin(segments)]

            if payment_methods and len(payment_methods) > 0:
                df_returns = df_returns[
                    df_returns["payment_method"].isin(payment_methods)
                ]

            if suppliers and len(suppliers) > 0:
                df_returns = df_returns[df_returns["supplier_name"].isin(suppliers)]

            reasons_distribution = (
                df_returns.groupby("reason")["return_id"].nunique().reset_index()
            )
            reasons_distribution.columns = ["reason", "returns_count"]

            return reasons_distribution.sort_values("returns_count", ascending=False)

        except Exception as e:
            print(f"Error getting returns reasons distribution: {e}")
            return pd.DataFrame()
