from dash import Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
from components.kpi_cards import create_kpi_card
from datetime import datetime


def register_overview_callbacks(app, data_manager, calculations, charts):
    @app.callback(
        Output("overview-filter-modal", "is_open"),
        [
            Input("filter-button", "n_clicks"),
            Input("overview-apply-filters", "n_clicks"),
            Input("overview-reset-filters", "n_clicks"),
        ],
        [State("overview-filter-modal", "is_open")],
    )
    def toggle_filter_modal(n1, n2, n3, is_open):
        if not ctx.triggered:
            return is_open

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "filter-button":
            return not is_open
        elif trigger_id in ["overview-apply-filters", "overview-reset-filters"]:
            return False

        return is_open

    @app.callback(
        [
            Output("overview-date-range", "start_date"),
            Output("overview-date-range", "end_date"),
            Output("overview-region-filter", "value"),
            Output("overview-category-filter", "value"),
        ],
        [Input("overview-reset-filters", "n_clicks")],
    )
    def reset_filters(n_clicks):
        if n_clicks and n_clicks > 0:
            min_date = datetime(2025, 1, 1)
            max_date = datetime(2025, 12, 31)
            return min_date, max_date, [], []
        return no_update

    @app.callback(
        Output("overview-filters-store", "data"),
        [Input("overview-apply-filters", "n_clicks")],
        [
            State("overview-date-range", "start_date"),
            State("overview-date-range", "end_date"),
            State("overview-region-filter", "value"),
            State("overview-category-filter", "value"),
        ],
    )
    def apply_filters(n_clicks, start_date, end_date, regions, categories):
        if n_clicks is None or n_clicks == 0:
            return {
                "start_date": None,
                "end_date": None,
                "regions": [],
                "categories": [],
            }

        return {
            "start_date": start_date,
            "end_date": end_date,
            "regions": regions,
            "categories": categories,
        }

    @app.callback(
        Output("overview-kpi-cards", "children"),
        [Input("overview-filters-store", "data")],
    )
    def update_kpi_cards(filters_data):
        if not filters_data:
            return [
                dbc.Col(create_kpi_card("Общий доход", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("Количество заказов", "0"), width=2),
                dbc.Col(create_kpi_card("Средний чек", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("Активные пользователи", "0"), width=2),
                dbc.Col(create_kpi_card("Расходы на рекламу", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("ROMI", "0%"), width=2),
            ]

        start_date = filters_data.get("start_date")
        end_date = filters_data.get("end_date")
        regions = filters_data.get("regions")
        categories = filters_data.get("categories")

        try:
            total_revenue = calculations.calculate_total_revenue(
                start_date, end_date, regions, categories
            )
            orders_count = calculations.calculate_orders_count(
                start_date, end_date, regions, categories
            )
            avg_order = calculations.calculate_avg_order_value(
                start_date, end_date, regions, categories
            )
            active_users = calculations.calculate_active_users(
                start_date, end_date, regions, categories
            )
            ad_spend = calculations.calculate_ad_spend(start_date, end_date)
            romi = calculations.calculate_romi(start_date, end_date)

            kpi_cards = [
                dbc.Col(
                    create_kpi_card("Общий доход", f"{total_revenue:,.0f} ₽"), width=2
                ),
                dbc.Col(
                    create_kpi_card("Количество заказов", f"{orders_count:,}"), width=2
                ),
                dbc.Col(create_kpi_card("Средний чек", f"{avg_order:,.0f} ₽"), width=2),
                dbc.Col(
                    create_kpi_card("Активные пользователи", f"{active_users:,}"),
                    width=2,
                ),
                dbc.Col(
                    create_kpi_card("Расходы на рекламу", f"{ad_spend:,.0f} ₽"), width=2
                ),
                dbc.Col(create_kpi_card("ROMI", f"{romi}%"), width=2),
            ]

            return kpi_cards

        except Exception as e:
            print(f"Error updating KPI cards: {e}")
            return [
                dbc.Col(create_kpi_card("Общий доход", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("Количество заказов", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("Средний чек", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("Активные пользователи", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("Расходы на рекламу", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("ROMI", "Ошибка"), width=2),
            ]

    @app.callback(
        [
            Output("overview-sales-trend-chart", "figure"),
            Output("overview-category-chart", "figure"),
            Output("overview-top-products-chart", "figure"),
        ],
        [Input("overview-filters-store", "data")],
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
            return empty_fig, empty_fig, empty_fig

        start_date = filters_data.get("start_date")
        end_date = filters_data.get("end_date")
        regions = filters_data.get("regions")
        categories = filters_data.get("categories")

        try:
            sales_trend = charts.create_sales_trend_chart(
                start_date, end_date, regions, categories
            )
            category_dist = charts.create_category_distribution_chart(
                start_date, end_date, regions, categories
            )
            top_products = charts.create_top_products_chart(
                start_date, end_date, regions, categories
            )

            return sales_trend, category_dist, top_products

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
            return error_fig, error_fig, error_fig
