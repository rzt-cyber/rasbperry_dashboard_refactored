from dash import html, dcc
import dash_bootstrap_components as dbc
from .filters import create_customers_filters
from .calculations import CustomersCalculations
from .charts import CustomersCharts
from components.kpi_cards import create_kpi_card


class CustomersTab:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.calculations = CustomersCalculations(data_manager)
        self.charts = CustomersCharts(data_manager)

    def get_layout(self):
        return html.Div(
            [
                create_customers_filters(self.data_manager),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2("👥 Аналитика клиентов", className="page-title"),
                                html.P(
                                    "Сегментация, поведение и удержание клиентов маркетплейса Малинка",
                                    className="page-subtitle",
                                ),
                            ]
                        )
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(create_kpi_card("👥 Всего клиентов", "0"), width=2),
                        dbc.Col(create_kpi_card("🆕 Новые клиенты", "0"), width=2),
                        dbc.Col(create_kpi_card("💎 Лояльные клиенты", "0"), width=2),
                        dbc.Col(create_kpi_card("⚠️ В группе риска", "0"), width=2),
                        dbc.Col(create_kpi_card("💰 Крупные покупатели", "0"), width=2),
                        dbc.Col(create_kpi_card("🎯 Ищущие скидки", "0"), width=2),
                    ],
                    className="mb-4",
                    id="customers-kpi-cards",
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="customers-segments-chart")], width=6),
                        dbc.Col(
                            [dcc.Graph(id="customers-registrations-chart")], width=6
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="customers-regions-chart")], width=6),
                        dbc.Col([dcc.Graph(id="customers-channels-chart")], width=6),
                    ]
                ),
                dcc.Store(
                    id="customers-filters-store",
                    data={
                        "start_date": None,
                        "end_date": None,
                        "regions": [],
                        "segments": [],
                        "channels": [],
                        "devices": [],
                    },
                ),
            ],
            className="tab-container",
        )

    def register_callbacks(self, app):
        from .callbacks import register_customers_callbacks

        register_customers_callbacks(
            app, self.data_manager, self.calculations, self.charts
        )
