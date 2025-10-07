from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime


def create_customers_filters(data_manager):
    regions = sorted(data_manager.df_user_segments["region"].unique().tolist())
    segments = sorted(data_manager.df_user_segments["segment"].unique().tolist())
    channels = sorted(data_manager.df_traffic["channel"].unique().tolist())
    devices = sorted(data_manager.df_traffic["device"].unique().tolist())

    if not data_manager.df_user_segments.empty:
        min_date = data_manager.df_user_segments["registration_date"].min()
        max_date = data_manager.df_user_segments["registration_date"].max()
    else:
        min_date = datetime(2025, 1, 1)
        max_date = datetime(2025, 12, 31)

    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("🔍 Фильтры - Аналитика клиентов"),
                    dbc.ModalBody(
                        [
                            html.Label("Период регистрации:", className="filter-label"),
                            dcc.DatePickerRange(
                                id="customers-date-range",
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
                                id="customers-region-filter",
                                options=[
                                    {"label": region, "value": region}
                                    for region in regions
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите регионы...",
                            ),
                            html.Label("Сегменты клиентов:", className="filter-label"),
                            dcc.Dropdown(
                                id="customers-segment-filter",
                                options=[
                                    {"label": segment, "value": segment}
                                    for segment in segments
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите сегменты...",
                            ),
                            html.Label("Каналы привлечения:", className="filter-label"),
                            dcc.Dropdown(
                                id="customers-channel-filter",
                                options=[
                                    {"label": channel, "value": channel}
                                    for channel in channels
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите каналы...",
                            ),
                            html.Label("Устройства:", className="filter-label"),
                            dcc.Dropdown(
                                id="customers-device-filter",
                                options=[
                                    {"label": device, "value": device}
                                    for device in devices
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите устройства...",
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Применить",
                                id="customers-apply-filters",
                                color="primary",
                                className="wildberries-btn",
                            ),
                            dbc.Button(
                                "Сбросить",
                                id="customers-reset-filters",
                                color="secondary",
                                className="wildberries-btn",
                            ),
                        ]
                    ),
                ],
                id="customers-filter-modal",
                size="lg",
                is_open=False,
            ),
        ]
    )
