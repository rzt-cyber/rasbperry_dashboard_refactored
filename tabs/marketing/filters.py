from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime


def create_marketing_filters(data_manager):
    channels = sorted(data_manager.df_traffic["channel"].unique().tolist())
    campaigns = sorted(data_manager.df_ad_revenue["campaign_name"].unique().tolist())
    categories = sorted(data_manager.df_products["category"].unique().tolist())
    devices = sorted(data_manager.df_traffic["device"].unique().tolist())
    segments = sorted(data_manager.df_user_segments["segment"].unique().tolist())

    if not data_manager.df_ad_revenue.empty:
        min_date = data_manager.df_ad_revenue["date"].min()
        max_date = data_manager.df_ad_revenue["date"].max()
    else:
        min_date = datetime(2025, 1, 1)
        max_date = datetime(2025, 12, 31)

    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("🔍 Фильтры - Маркетинговая аналитика"),
                    dbc.ModalBody(
                        [
                            html.Label("Период кампаний:", className="filter-label"),
                            dcc.DatePickerRange(
                                id="marketing-date-range",
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
                            html.Label("Каналы трафика:", className="filter-label"),
                            dcc.Dropdown(
                                id="marketing-channel-filter",
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
                            html.Label("Рекламные кампании:", className="filter-label"),
                            dcc.Dropdown(
                                id="marketing-campaign-filter",
                                options=[
                                    {"label": campaign, "value": campaign}
                                    for campaign in campaigns
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите кампании...",
                            ),
                            html.Label("Категории товаров:", className="filter-label"),
                            dcc.Dropdown(
                                id="marketing-category-filter",
                                options=[
                                    {"label": category, "value": category}
                                    for category in categories
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите категории...",
                            ),
                            html.Label("Устройства:", className="filter-label"),
                            dcc.Dropdown(
                                id="marketing-device-filter",
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
                            html.Label("Сегменты клиентов:", className="filter-label"),
                            dcc.Dropdown(
                                id="marketing-segment-filter",
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
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Применить",
                                id="marketing-apply-filters",
                                color="primary",
                                className="wildberries-btn",
                            ),
                            dbc.Button(
                                "Сбросить",
                                id="marketing-reset-filters",
                                color="secondary",
                                className="wildberries-btn",
                            ),
                        ]
                    ),
                ],
                id="marketing-filter-modal",
                size="lg",
                is_open=False,
            ),
        ]
    )
