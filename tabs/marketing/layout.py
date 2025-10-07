from dash import html, dcc
import dash_bootstrap_components as dbc
from .filters import create_marketing_filters
from .calculations import MarketingCalculations
from .charts import MarketingCharts
from components.kpi_cards import create_kpi_card


class MarketingTab:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.calculations = MarketingCalculations(data_manager)
        self.charts = MarketingCharts(data_manager)

    def get_layout(self):
        return html.Div(
            [
                create_marketing_filters(self.data_manager),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "📢 Маркетинговая аналитика", className="page-title"
                                ),
                                html.P(
                                    "Эффективность рекламных кампаний, каналов привлечения и ROI",
                                    className="page-subtitle",
                                ),
                            ]
                        )
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(create_kpi_card("📊 Общий ROMI", "0%"), width=2),
                        dbc.Col(
                            create_kpi_card("💰 Расходы на рекламу", "0 ₽"), width=2
                        ),
                        dbc.Col(create_kpi_card("💸 Доход от рекламы", "0 ₽"), width=2),
                        dbc.Col(create_kpi_card("🎯 CTR", "0%"), width=2),
                        dbc.Col(
                            create_kpi_card("👥 Стоимость привлечения", "0 ₽"), width=2
                        ),
                        dbc.Col(create_kpi_card("📈 Конверсия", "0%"), width=2),
                    ],
                    className="mb-4",
                    id="marketing-kpi-cards",
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="marketing-romi-trend-chart")], width=6),
                        dbc.Col(
                            [dcc.Graph(id="marketing-budget-distribution-chart")],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [dcc.Graph(id="marketing-campaigns-effectiveness-chart")],
                            width=6,
                        ),
                        dbc.Col(
                            [dcc.Graph(id="marketing-ctr-by-channels-chart")], width=6
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [dcc.Graph(id="marketing-cac-by-segments-chart")], width=6
                        ),
                        dbc.Col(
                            [dcc.Graph(id="marketing-conversion-by-devices-chart")],
                            width=6,
                        ),
                    ]
                ),
                dcc.Store(
                    id="marketing-filters-store",
                    data={
                        "start_date": None,
                        "end_date": None,
                        "channels": [],
                        "campaigns": [],
                        "categories": [],
                        "devices": [],
                        "segments": [],
                    },
                ),
            ],
            className="tab-container",
        )

    def register_callbacks(self, app):
        from .callbacks import register_marketing_callbacks

        register_marketing_callbacks(
            app, self.data_manager, self.calculations, self.charts
        )
