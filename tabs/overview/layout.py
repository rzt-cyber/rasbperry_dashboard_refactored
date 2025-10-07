from dash import html, dcc
import dash_bootstrap_components as dbc
from .filters import create_overview_filters
from .calculations import OverviewCalculations
from .charts import OverviewCharts
from components.kpi_cards import create_kpi_card


class OverviewTab:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.calculations = OverviewCalculations(data_manager)
        self.charts = OverviewCharts(data_manager)

    def get_layout(self):
        return html.Div(
            [
                create_overview_filters(self.data_manager),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "📊 Общий обзор бизнеса", className="page-title"
                                ),
                                html.P(
                                    "Ключевые метрики и аналитика маркетплейса Малинка",
                                    className="page-subtitle",
                                ),
                            ]
                        )
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(create_kpi_card("Общий доход", "0 ₽"), width=2),
                        dbc.Col(create_kpi_card("Количество заказов", "0"), width=2),
                        dbc.Col(create_kpi_card("Средний чек", "0 ₽"), width=2),
                        dbc.Col(create_kpi_card("Активные пользователи", "0"), width=2),
                        dbc.Col(create_kpi_card("Расходы на рекламу", "0 ₽"), width=2),
                        dbc.Col(create_kpi_card("ROMI", "0%"), width=2),
                    ],
                    className="mb-4",
                    id="overview-kpi-cards",
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="overview-sales-trend-chart")], width=6),
                        dbc.Col([dcc.Graph(id="overview-category-chart")], width=6),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [dcc.Graph(id="overview-top-products-chart")], width=12
                        ),
                    ]
                ),
                dcc.Store(
                    id="overview-filters-store",
                    data={
                        "start_date": None,
                        "end_date": None,
                        "regions": ["all"],
                        "categories": ["all"],
                    },
                ),
            ],
            className="tab-container",
        )

    def register_callbacks(self, app):
        from .callbacks import register_overview_callbacks

        register_overview_callbacks(
            app, self.data_manager, self.calculations, self.charts
        )
