import pandas as pd


class OperationsCalculations:
    def __init__(self, data_manager):
        self.dm = data_manager

    def get_latest_inventory_data(self):
        """Получаем актуальные данные по остаткам (последние обновления по каждому товару)"""
        try:
            latest_updates = (
                self.dm.df_inventory.groupby("product_id")["last_updated"]
                .max()
                .reset_index()
            )

            latest_inventory = latest_updates.merge(
                self.dm.df_inventory, on=["product_id", "last_updated"], how="left"
            )

            return latest_inventory
        except Exception as e:
            print(f"Error getting latest inventory data: {e}")
            return self.dm.df_inventory

    def get_latest_support_data(self):
        """Получаем актуальные данные поддержки (можно добавить фильтр по дате если нужно)"""
        return self.dm.df_customer_support.copy()

    def calculate_stock_availability(self):
        """Уровень доступности товаров (% товаров с остатком > 0)"""
        try:
            df = self.get_latest_inventory_data()

            total_products = df["product_id"].nunique()
            available_products = df[df["stock_quantity"] > 0]["product_id"].nunique()

            return (
                round((available_products / total_products) * 100, 2)
                if total_products > 0
                else 0
            )
        except Exception as e:
            print(f"Error calculating stock availability: {e}")
            return 0

    def calculate_low_stock_items(self, threshold=5):
        """Товары с дефицитом (остаток < threshold)"""
        try:
            df = self.get_latest_inventory_data()
            return df[df["stock_quantity"] < threshold]["product_id"].nunique()
        except Exception as e:
            print(f"Error calculating low stock items: {e}")
            return 0

    def calculate_inventory_value(self):
        """Стоимость запасов на складах"""
        try:
            df = self.get_latest_inventory_data()

            df = df.merge(self.dm.df_products[["product_id", "price"]], on="product_id")
            df["item_value"] = df["stock_quantity"] * df["price"]

            return round(df["item_value"].sum(), 2)
        except Exception as e:
            print(f"Error calculating inventory value: {e}")
            return 0

    def calculate_avg_resolution_time(self):
        """Среднее время решения тикетов (в часах)"""
        try:
            df = self.get_latest_support_data()
            resolved_tickets = df[df["resolved"] == True]
            return (
                round(resolved_tickets["resolution_time_minutes"].mean() / 60, 1)
                if len(resolved_tickets) > 0
                else 0
            )
        except Exception as e:
            print(f"Error calculating avg resolution time: {e}")
            return 0

    def calculate_resolved_tickets_rate(self):
        """Процент решенных тикетов"""
        try:
            df = self.get_latest_support_data()
            total_tickets = len(df)
            resolved_tickets = len(df[df["resolved"] == True])

            return (
                round((resolved_tickets / total_tickets) * 100, 2)
                if total_tickets > 0
                else 0
            )
        except Exception as e:
            print(f"Error calculating resolved tickets rate: {e}")
            return 0

    def calculate_overdue_tickets(self, threshold_hours=24):
        """Тикеты с временем решения > threshold_hours"""
        try:
            df = self.get_latest_support_data()
            return len(df[df["resolution_time_minutes"] > (threshold_hours * 60)])
        except Exception as e:
            print(f"Error calculating overdue tickets: {e}")
            return 0

    def calculate_delivery_delays(self):
        """Количество тикетов с задержкой доставки"""
        try:
            df = self.get_latest_support_data()
            delivery_delays = df[df["issue_type"] == "delivery_delay"]
            return len(delivery_delays)
        except Exception as e:
            print(f"Error calculating delivery delays: {e}")
            return 0

    def get_low_stock_products(self, threshold=5):
        """Список товаров с низким запасом"""
        try:
            df = self.get_latest_inventory_data()
            df = df[df["stock_quantity"] < threshold]

            df = df.merge(
                self.dm.df_products[["product_id", "product_name", "category"]],
                on="product_id",
            )

            return df[
                ["product_name", "category", "stock_quantity", "last_updated"]
            ].sort_values("stock_quantity")
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return pd.DataFrame()

    def get_warehouse_stats(self):
        """Статистика по складам на основе актуальных данных"""
        try:
            df = self.get_latest_inventory_data()

            df = df.merge(self.dm.df_products[["product_id", "price"]], on="product_id")
            df["value"] = df["stock_quantity"] * df["price"]

            warehouse_stats = (
                df.groupby("warehouse_id")
                .agg(
                    {
                        "product_id": "nunique",
                        "stock_quantity": "sum",
                        "value": "sum",
                        "last_updated": "max",
                    }
                )
                .reset_index()
            )

            warehouse_stats.columns = [
                "warehouse_id",
                "unique_products",
                "total_quantity",
                "total_value",
                "last_updated",
            ]

            return warehouse_stats
        except Exception as e:
            print(f"Error getting warehouse stats: {e}")
            return pd.DataFrame()

    def get_support_metrics_by_type(self):
        """Метрики поддержки по типам проблем"""
        try:
            df = self.get_latest_support_data()

            metrics_by_type = (
                df.groupby("issue_type")
                .agg(
                    {
                        "ticket_id": "count",
                        "resolution_time_minutes": "mean",
                        "resolved": "mean",
                    }
                )
                .reset_index()
            )

            metrics_by_type["avg_resolution_hours"] = (
                metrics_by_type["resolution_time_minutes"] / 60
            )
            metrics_by_type["resolution_rate"] = metrics_by_type["resolved"] * 100

            metrics_by_type = metrics_by_type.round(2)
            metrics_by_type.columns = [
                "issue_type",
                "ticket_count",
                "avg_minutes",
                "resolution_ratio",
                "avg_hours",
                "resolution_rate",
            ]

            return metrics_by_type[
                ["issue_type", "ticket_count", "avg_hours", "resolution_rate"]
            ]
        except Exception as e:
            print(f"Error getting support metrics by type: {e}")
            return pd.DataFrame()

    def get_data_freshness(self):
        """Возвращает информацию о свежести данных"""
        try:
            inventory_freshness = self.get_latest_inventory_data()["last_updated"].max()
            support_freshness = self.get_latest_support_data()["support_date"].max()

            return {
                "inventory_last_updated": inventory_freshness,
                "support_last_updated": support_freshness,
            }
        except Exception as e:
            print(f"Error getting data freshness: {e}")
            return {}
