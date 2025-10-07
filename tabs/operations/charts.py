import plotly.express as px


class OperationsCharts:
    def __init__(self, data_manager, calculations):
        self.dm = data_manager
        self.calc = calculations

    def create_stock_heatmap_chart(self):
        """Heatmap остатков по складам и категориям на основе актуальных данных"""
        try:
            df = self.calc.get_latest_inventory_data()

            df = df.merge(
                self.dm.df_products[["product_id", "category"]], on="product_id"
            )

            heatmap_data = (
                df.groupby(["warehouse_id", "category"])["stock_quantity"]
                .sum()
                .reset_index()
            )

            fig = px.density_heatmap(
                heatmap_data,
                x="warehouse_id",
                y="category",
                z="stock_quantity",
                title="📊 Распределение остатков по складам и категориям",
                color_continuous_scale="Blues",
            )

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )

            return fig
        except Exception as e:
            print(f"Error creating stock heatmap: {e}")
            return self._create_empty_chart("Ошибка при создании графика")

    def create_issue_resolution_chart(self):
        """Время решения по типам проблем на основе актуальных данных"""
        try:
            df = self.calc.get_latest_support_data()

            resolution_by_issue = (
                df.groupby("issue_type")["resolution_time_minutes"].mean().reset_index()
            )
            resolution_by_issue["hours"] = (
                resolution_by_issue["resolution_time_minutes"] / 60
            )

            fig = px.bar(
                resolution_by_issue,
                x="issue_type",
                y="hours",
                title="⏱️ Среднее время решения по типам проблем",
                labels={"issue_type": "Тип проблемы", "hours": "Часы"},
                color="hours",
                color_continuous_scale="Viridis",
            )

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )

            return fig
        except Exception as e:
            print(f"Error creating issue resolution chart: {e}")
            return self._create_empty_chart("Ошибка при создании графика")

    def create_ticket_status_chart(self):
        """Распределение тикетов по статусам на основе актуальных данных"""
        try:
            df = self.calc.get_latest_support_data()

            status_counts = df["resolved"].value_counts().reset_index()
            status_counts["status"] = status_counts["resolved"].apply(
                lambda x: "Решено" if x else "Не решено"
            )

            fig = px.pie(
                status_counts,
                values="count",
                names="status",
                title="✅ Статус тикетов поддержки",
                hole=0.4,
                color_discrete_sequence=["#00cc96", "#ef553b"],
            )

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )

            return fig
        except Exception as e:
            print(f"Error creating ticket status chart: {e}")
            return self._create_empty_chart("Ошибка при создании графика")

    def create_low_stock_chart(self, threshold=5):
        """Топ товаров с низким запасом на основе актуальных данных"""
        try:
            df = self.calc.get_latest_inventory_data()

            df = df.merge(
                self.dm.df_products[["product_id", "product_name", "category"]],
                on="product_id",
            )

            low_stock = df[df["stock_quantity"] < threshold]

            low_stock_agg = (
                low_stock.groupby(["product_name", "category"])["stock_quantity"]
                .sum()
                .reset_index()
            )
            low_stock_agg = low_stock_agg.nlargest(10, "stock_quantity")

            fig = px.bar(
                low_stock_agg,
                x="stock_quantity",
                y="product_name",
                orientation="h",
                title=f"⚠️ Топ товаров с запасом < {threshold} ед.",
                labels={"stock_quantity": "Количество", "product_name": "Товар"},
                color="category",
            )

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                yaxis={"categoryorder": "total ascending"},
            )

            return fig
        except Exception as e:
            print(f"Error creating low stock chart: {e}")
            return self._create_empty_chart("Ошибка при создании графика")

    def _create_empty_chart(self, message):
        """Создает пустой график с сообщением об ошибке"""
        return {
            "data": [],
            "layout": {
                "title": message,
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [
                    {
                        "text": message,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {"size": 16},
                    }
                ],
            },
        }
