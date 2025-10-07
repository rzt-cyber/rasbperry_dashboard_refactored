import pandas as pd


class DataManager:
    def __init__(self):
        self.df_suppliers = None
        self.df_products = None
        self.df_user_segments = None
        self.df_sales = None
        self.df_events = None
        self.df_ad_revenue = None
        self.df_returns = None
        self.df_traffic = None
        self.df_inventory = None
        self.df_customer_support = None

    def load_data(self):
        try:
            data_dir = "data"

            self.df_suppliers = pd.read_csv(f"{data_dir}/suppliers.csv")
            self.df_products = pd.read_csv(f"{data_dir}/products.csv")
            self.df_user_segments = pd.read_csv(
                f"{data_dir}/user_segments.csv", parse_dates=["registration_date"]
            )
            self.df_sales = pd.read_csv(
                f"{data_dir}/sales.csv", parse_dates=["transaction_date"]
            )
            self.df_events = pd.read_csv(
                f"{data_dir}/events.csv", parse_dates=["event_timestamp"]
            )
            self.df_ad_revenue = pd.read_csv(
                f"{data_dir}/ad_revenue.csv", parse_dates=["date"]
            )
            self.df_returns = pd.read_csv(f"{data_dir}/returns.csv")
            self.df_traffic = pd.read_csv(
                f"{data_dir}/traffic.csv", parse_dates=["session_start"]
            )
            self.df_inventory = pd.read_csv(
                f"{data_dir}/inventory.csv", parse_dates=["last_updated"]
            )
            self.df_customer_support = pd.read_csv(
                f"{data_dir}/customer_support.csv", parse_dates=["support_date"]
            )

            print("Все данные успешно загружены!")
            return True

        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self._create_sample_data()
            return False

    def _create_sample_data(self):
        """Создание тестовых данных если CSV не найдены"""
        print("Создание тестовых данных...")
        self.df_products = pd.DataFrame(
            {
                "product_id": [1, 2, 3],
                "product_name": ["Телефон", "Ноутбук", "Наушники"],
                "category": ["Электроника", "Электроника", "Электроника"],
                "price": [500, 1000, 100],
                "supplier_id": [1, 1, 2],
            }
        )

        self.df_sales = pd.DataFrame(
            {
                "transaction_id": [1, 2, 3],
                "customer_id": [1, 2, 1],
                "product_id": [1, 2, 3],
                "quantity": [1, 1, 2],
                "payment_method": ["card", "card", "cash"],
                "transaction_date": pd.date_range("2025-01-01", periods=3),
            }
        )

        self.df_user_segments = pd.DataFrame(
            {
                "customer_id": [1, 2, 3],
                "segment": ["new", "returning", "loyal"],
                "region": ["Москва", "СПб", "Москва"],
                "registration_date": pd.date_range("2024-12-01", periods=3),
            }
        )

        self.df_ad_revenue = pd.DataFrame(
            {
                "ad_id": [1, 2],
                "campaign_name": ["Кампания 1", "Кампания 2"],
                "product_id": [1, 2],
                "spend": [100, 200],
                "revenue": [500, 800],
                "impressions": [1000, 2000],
                "clicks": [100, 150],
                "date": pd.to_datetime(["2025-01-01", "2025-01-02"]),
            }
        )
