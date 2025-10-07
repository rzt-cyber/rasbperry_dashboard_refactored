from dash import html, dcc
import dash_bootstrap_components as dbc
from .filters import create_sales_filters
from .calculations import SalesCalculations
from .charts import SalesCharts
from components.kpi_cards import create_kpi_card


class SalesTab:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.calculations = SalesCalculations(data_manager)
        self.charts = SalesCharts(data_manager)

    def get_layout(self):
        return html.Div(
            [
                create_sales_filters(self.data_manager),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2("💰 Аналитика продаж", className="page-title"),
                                html.P(
                                    "Детальная аналитика транзакций, выручки и эффективности продаж",
                                    className="page-subtitle",
                                ),
                            ]
                        )
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(create_kpi_card("💰 Общая выручка", "0 ₽"), width=2),
                        dbc.Col(create_kpi_card("📦 Количество заказов", "0"), width=2),
                        dbc.Col(create_kpi_card("🛒 Средний чек", "0 ₽"), width=2),
                        dbc.Col(create_kpi_card("📊 Продано товаров", "0"), width=2),
                        dbc.Col(create_kpi_card("🔄 Процент возвратов", "0%"), width=2),
                        dbc.Col(
                            create_kpi_card("👥 Уникальных покупателей", "0"), width=2
                        ),
                    ],
                    className="mb-4",
                    id="sales-kpi-cards",
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="sales-regions-chart")], width=6),
                        dbc.Col([dcc.Graph(id="sales-segments-chart")], width=6),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="sales-payment-methods-chart")], width=6),
                        dbc.Col([dcc.Graph(id="sales-suppliers-chart")], width=6),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="sales-hourly-chart")], width=6),
                        dbc.Col([dcc.Graph(id="sales-returns-reasons-chart")], width=6),
                    ]
                ),
                dcc.Store(
                    id="sales-filters-store",
                    data={
                        "start_date": None,
                        "end_date": None,
                        "regions": [],
                        "categories": [],
                        "segments": [],
                        "payment_methods": [],
                        "suppliers": [],
                    },
                ),
            ],
            className="tab-container",
        )

    def register_callbacks(self, app):
        from .callbacks import register_sales_callbacks

        register_sales_callbacks(app, self.data_manager, self.calculations, self.charts)
