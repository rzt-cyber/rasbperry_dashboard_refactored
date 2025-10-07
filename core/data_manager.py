import pandas as pd
import os


class DataManager:
    def __init__(self):
        self.df_suppliers = None
        self.df_products = None
        self.df_user_segments = None
        self.df_sales = None
        self.df_events = None  # Объединенная таблица events
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
            
            # Загружаем и объединяем части events
            self.df_events = self._load_combined_events(data_dir)
            
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

    def _load_combined_events(self, data_dir):
        """
        Загружает и объединяет части events из нескольких файлов
        """
        events_parts = []
        
        # Проверяем существование частей events
        part1_path = f"{data_dir}/events_part1.csv"
        part2_path = f"{data_dir}/events_part2.csv"
        original_path = f"{data_dir}/events.csv"
        
        # Если есть оригинальный файл, используем его
        if os.path.exists(original_path):
            print("Загружаем оригинальный events.csv")
            return pd.read_csv(original_path, parse_dates=["event_timestamp"])
        
        # Загружаем части если они существуют
        if os.path.exists(part1_path):
            print("Загружаем events_part1.csv")
            events_parts.append(pd.read_csv(part1_path, parse_dates=["event_timestamp"]))
        
        if os.path.exists(part2_path):
            print("Загружаем events_part2.csv")
            events_parts.append(pd.read_csv(part2_path, parse_dates=["event_timestamp"]))
        
        if events_parts:
            # Объединяем все части
            combined_events = pd.concat(events_parts, ignore_index=True)
            print(f"Объединено {len(events_parts)} частей events, всего строк: {len(combined_events)}")
            return combined_events
        else:
            # Если нет ни одного файла events
            print("Файлы events не найдены, создаем пустой DataFrame")
            return pd.DataFrame(columns=["event_id", "customer_id", "event_type", 
                                       "event_timestamp", "page_url", "product_id"])

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
        
        # Создаем тестовые данные для events
        self.df_events = pd.DataFrame(
            {
                "event_id": [1, 2, 3, 4],
                "customer_id": [1, 2, 1, 3],
                "event_type": ["page_view", "add_to_cart", "purchase", "page_view"],
                "event_timestamp": pd.date_range("2025-01-01", periods=4, freq="H"),
                "page_url": ["/home", "/product/1", "/checkout", "/product/2"],
                "product_id": [None, 1, 1, 2],
            }
        )