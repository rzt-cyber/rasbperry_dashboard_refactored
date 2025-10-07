from dash import html, dcc
import dash_bootstrap_components as dbc
from .filters import create_operations_filters
from .calculations import OperationsCalculations
from .charts import OperationsCharts
from components.kpi_cards import create_kpi_card


class OperationsTab:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.calculations = OperationsCalculations(data_manager)
        self.charts = OperationsCharts(data_manager, self.calculations)

    def get_layout(self):
        return html.Div(
            [
                create_operations_filters(),
                dcc.Interval(
                    id="interval-component", interval=30 * 1000, n_intervals=0
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "⚙️ Операционная деятельность",
                                    className="page-title",
                                ),
                                html.P(
                                    "Актуальные показатели управления запасами и поддержки клиентов",
                                    className="page-subtitle",
                                ),
                                html.Div(
                                    [
                                        html.Span("🔄 ", className="me-2"),
                                        html.Span(
                                            "Данные обновляются каждые 30 секунд",
                                            className="text-muted small",
                                        ),
                                    ],
                                    className="text-center mb-3",
                                ),
                            ]
                        )
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4("📦 Управление запасами", className="section-title"),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(create_kpi_card("Уровень доступности", "0%"), width=3),
                        dbc.Col(create_kpi_card("Товары с дефицитом", "0"), width=3),
                        dbc.Col(create_kpi_card("Стоимость запасов", "0 ₽"), width=3),
                    ],
                    className="mb-4",
                    id="operations-inventory-kpi",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H4("📞 Поддержка клиентов", className="section-title"),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(create_kpi_card("Время решения", "0 ч"), width=3),
                        dbc.Col(create_kpi_card("Решено тикетов", "0%"), width=3),
                        dbc.Col(create_kpi_card("Просрочено >24ч", "0"), width=3),
                        dbc.Col(create_kpi_card("Задержки доставки", "0"), width=3),
                    ],
                    className="mb-4",
                    id="operations-support-kpi",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [dcc.Graph(id="operations-stock-heatmap-chart")], width=6
                        ),
                        dbc.Col(
                            [dcc.Graph(id="operations-issue-resolution-chart")], width=6
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [dcc.Graph(id="operations-ticket-status-chart")], width=6
                        ),
                        dbc.Col([dcc.Graph(id="operations-low-stock-chart")], width=6),
                    ]
                ),
            ],
            className="tab-container",
        )

    def register_callbacks(self, app):
        from .callbacks import register_operations_callbacks

        register_operations_callbacks(
            app, self.data_manager, self.calculations, self.charts
        )
