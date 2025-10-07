from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime


def create_sales_filters(data_manager):
    regions = sorted(data_manager.df_user_segments["region"].unique().tolist())
    categories = sorted(data_manager.df_products["category"].unique().tolist())
    segments = sorted(data_manager.df_user_segments["segment"].unique().tolist())
    payment_methods = sorted(data_manager.df_sales["payment_method"].unique().tolist())
    suppliers = sorted(data_manager.df_suppliers["supplier_name"].unique().tolist())

    if not data_manager.df_sales.empty:
        min_date = data_manager.df_sales["transaction_date"].min()
        max_date = data_manager.df_sales["transaction_date"].max()
    else:
        min_date = datetime(2025, 1, 1)
        max_date = datetime(2025, 12, 31)

    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("🔍 Фильтры - Аналитика продаж"),
                    dbc.ModalBody(
                        [
                            html.Label("Период транзакций:", className="filter-label"),
                            dcc.DatePickerRange(
                                id="sales-date-range",
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
                            html.Label(
                                "Регионы покупателей:", className="filter-label"
                            ),
                            dcc.Dropdown(
                                id="sales-region-filter",
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
                            html.Label("Категории товаров:", className="filter-label"),
                            dcc.Dropdown(
                                id="sales-category-filter",
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
                            html.Label("Сегменты клиентов:", className="filter-label"),
                            dcc.Dropdown(
                                id="sales-segment-filter",
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
                            html.Label("Способы оплаты:", className="filter-label"),
                            dcc.Dropdown(
                                id="sales-payment-method-filter",
                                options=[
                                    {"label": method, "value": method}
                                    for method in payment_methods
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите способы оплаты...",
                            ),
                            html.Label("Поставщики:", className="filter-label"),
                            dcc.Dropdown(
                                id="sales-supplier-filter",
                                options=[
                                    {"label": supplier, "value": supplier}
                                    for supplier in suppliers
                                ],
                                value=[],
                                multi=True,
                                clearable=True,
                                className="filter-dropdown",
                                placeholder="Выберите поставщиков...",
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Применить",
                                id="sales-apply-filters",
                                color="primary",
                                className="wildberries-btn",
                            ),
                            dbc.Button(
                                "Сбросить",
                                id="sales-reset-filters",
                                color="secondary",
                                className="wildberries-btn",
                            ),
                        ]
                    ),
                ],
                id="sales-filter-modal",
                size="lg",
                is_open=False,
            ),
        ]
    )
