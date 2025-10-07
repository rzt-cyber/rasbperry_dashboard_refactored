from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime


def create_overview_filters(data_manager):
    regions = sorted(data_manager.df_user_segments["region"].unique().tolist())
    categories = sorted(data_manager.df_products["category"].unique().tolist())

    min_date = datetime(2025, 1, 1)
    max_date = datetime(2025, 12, 31)

    def is_outside_range(date):
        return date < min_date or date > max_date

    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("🔍 Фильтры - Общий обзор"),
                    dbc.ModalBody(
                        [
                            html.Label("Период дат:", className="filter-label"),
                            dcc.DatePickerRange(
                                id="overview-date-range",
                                start_date=min_date,
                                end_date=max_date,
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                display_format="YYYY-MM-DD",
                                className="date-picker",
                                start_date_placeholder_text="Начальная дата",
                                end_date_placeholder_text="Конечная дата",
                            ),
                            html.Hr(),
                            html.Label("Регионы:", className="filter-label"),
                            dcc.Dropdown(
                                id="overview-region-filter",
                                options=[
                                    {"label": region, "value": region}
                                    for region in regions
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите регионы...",
                                style={"color": "#6c757d"},
                            ),
                            html.Label("Категории товаров:", className="filter-label"),
                            dcc.Dropdown(
                                id="overview-category-filter",
                                options=[
                                    {"label": category, "value": category}
                                    for category in categories
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите категории...",
                                style={"color": "#6c757d"},
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Применить",
                                id="overview-apply-filters",
                                color="primary",
                                className="wildberries-btn",
                            ),
                            dbc.Button(
                                "Сбросить",
                                id="overview-reset-filters",
                                color="secondary",
                                className="wildberries-btn",
                            ),
                        ]
                    ),
                ],
                id="overview-filter-modal",
                size="lg",
                is_open=False,
            ),
        ]
    )
