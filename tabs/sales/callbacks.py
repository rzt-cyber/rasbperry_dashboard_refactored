from dash import Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
from components.kpi_cards import create_kpi_card
from datetime import datetime


def register_sales_callbacks(app, data_manager, calculations, charts):
    @app.callback(
        Output("sales-filter-modal", "is_open"),
        [
            Input("filter-button", "n_clicks"),
            Input("sales-apply-filters", "n_clicks"),
            Input("sales-reset-filters", "n_clicks"),
        ],
        [State("sales-filter-modal", "is_open")],
    )
    def toggle_filter_modal(n1, n2, n3, is_open):
        if not ctx.triggered:
            return is_open

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "filter-button":
            return not is_open
        elif trigger_id in ["sales-apply-filters", "sales-reset-filters"]:
            return False

        return is_open

    @app.callback(
        [
            Output("sales-date-range", "start_date"),
            Output("sales-date-range", "end_date"),
            Output("sales-region-filter", "value"),
            Output("sales-category-filter", "value"),
            Output("sales-segment-filter", "value"),
            Output("sales-payment-method-filter", "value"),
            Output("sales-supplier-filter", "value"),
        ],
        [Input("sales-reset-filters", "n_clicks")],
    )
    def reset_filters(n_clicks):
        if n_clicks and n_clicks > 0:
            if not data_manager.df_sales.empty:
                min_date = data_manager.df_sales["transaction_date"].min()
                max_date = data_manager.df_sales["transaction_date"].max()
            else:
                min_date = datetime(2025, 1, 1)
                max_date = datetime(2025, 12, 31)
            return min_date, max_date, [], [], [], [], []
        return no_update

    @app.callback(
        Output("sales-filters-store", "data"),
        [Input("sales-apply-filters", "n_clicks")],
        [
            State("sales-date-range", "start_date"),
            State("sales-date-range", "end_date"),
            State("sales-region-filter", "value"),
            State("sales-category-filter", "value"),
            State("sales-segment-filter", "value"),
            State("sales-payment-method-filter", "value"),
            State("sales-supplier-filter", "value"),
        ],
    )
    def apply_filters(
        n_clicks,
        start_date,
        end_date,
        regions,
        categories,
        segments,
        payment_methods,
        suppliers,
    ):
        if n_clicks is None or n_clicks == 0:
            return {
                "start_date": None,
                "end_date": None,
                "regions": [],
                "categories": [],
                "segments": [],
                "payment_methods": [],
                "suppliers": [],
            }

        return {
            "start_date": start_date,
            "end_date": end_date,
            "regions": regions,
            "categories": categories,
            "segments": segments,
            "payment_methods": payment_methods,
            "suppliers": suppliers,
        }

    @app.callback(
        Output("sales-kpi-cards", "children"), [Input("sales-filters-store", "data")]
    )
    def update_kpi_cards(filters_data):
        if not filters_data:
            return [
                dbc.Col(create_kpi_card("💰 Общая выручка", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("📦 Количество заказов", "0"), width=2),
                dbc.Col(create_kpi_card("🛒 Средний чек", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("📊 Продано товаров", "0"), width=2),
                dbc.Col(create_kpi_card("🔄 Процент возвратов", "0%"), width=2),
                dbc.Col(create_kpi_card("👥 Уникальных покупателей", "0"), width=2),
            ]

        start_date = filters_data.get("start_date")
        end_date = filters_data.get("end_date")
        regions = filters_data.get("regions")
        categories = filters_data.get("categories")
        segments = filters_data.get("segments")
        payment_methods = filters_data.get("payment_methods")
        suppliers = filters_data.get("suppliers")

        try:
            total_revenue = calculations.calculate_total_revenue(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            orders_count = calculations.calculate_orders_count(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            avg_order_value = calculations.calculate_avg_order_value(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            total_quantity = calculations.calculate_total_quantity(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            return_rate = calculations.calculate_return_rate(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            unique_customers = calculations.calculate_unique_customers(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )

            kpi_cards = [
                dbc.Col(
                    create_kpi_card("💰 Общая выручка", f"{total_revenue:,.0f} ₽"),
                    width=2,
                ),
                dbc.Col(
                    create_kpi_card("📦 Количество заказов", f"{orders_count:,}"),
                    width=2,
                ),
                dbc.Col(
                    create_kpi_card("🛒 Средний чек", f"{avg_order_value:,.0f} ₽"),
                    width=2,
                ),
                dbc.Col(
                    create_kpi_card("📊 Продано товаров", f"{total_quantity:,}"), width=2
                ),
                dbc.Col(
                    create_kpi_card("🔄 Процент возвратов", f"{return_rate}%"), width=2
                ),
                dbc.Col(
                    create_kpi_card(
                        "👥 Уникальных покупателей", f"{unique_customers:,}"
                    ),
                    width=2,
                ),
            ]

            return kpi_cards

        except Exception as e:
            print(f"Error updating KPI cards: {e}")
            return [
                dbc.Col(create_kpi_card("💰 Общая выручка", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("📦 Количество заказов", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("🛒 Средний чек", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("📊 Продано товаров", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("🔄 Процент возвратов", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("👥 Уникальных покупателей", "Ошибка"), width=2),
            ]

    @app.callback(
        [
            Output("sales-regions-chart", "figure"),
            Output("sales-segments-chart", "figure"),
            Output("sales-payment-methods-chart", "figure"),
            Output("sales-suppliers-chart", "figure"),
            Output("sales-hourly-chart", "figure"),
            Output("sales-returns-reasons-chart", "figure"),
        ],
        [Input("sales-filters-store", "data")],
    )
    def update_charts(filters_data):
        if not filters_data:
            empty_fig = {
                "data": [],
                "layout": {
                    "title": "Нет данных для отображения",
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                },
            }
            return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

        start_date = filters_data.get("start_date")
        end_date = filters_data.get("end_date")
        regions = filters_data.get("regions")
        categories = filters_data.get("categories")
        segments = filters_data.get("segments")
        payment_methods = filters_data.get("payment_methods")
        suppliers = filters_data.get("suppliers")

        try:
            regions_chart = charts.create_regions_chart(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            segments_chart = charts.create_segments_chart(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            payment_methods_chart = charts.create_payment_methods_chart(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            suppliers_chart = charts.create_suppliers_chart(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            hourly_chart = charts.create_hourly_chart(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )
            returns_reasons_chart = charts.create_returns_reasons_chart(
                start_date,
                end_date,
                regions,
                categories,
                segments,
                payment_methods,
                suppliers,
            )

            return (
                regions_chart,
                segments_chart,
                payment_methods_chart,
                suppliers_chart,
                hourly_chart,
                returns_reasons_chart,
            )

        except Exception as e:
            print(f"Error updating charts: {e}")
            error_fig = {
                "data": [],
                "layout": {
                    "title": f"Ошибка при загрузке данных: {str(e)}",
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                },
            }
            return error_fig, error_fig, error_fig, error_fig, error_fig, error_fig
