from dash import Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
from components.kpi_cards import create_kpi_card
from datetime import datetime


def register_marketing_callbacks(app, data_manager, calculations, charts):
    @app.callback(
        Output("marketing-filter-modal", "is_open"),
        [
            Input("filter-button", "n_clicks"),
            Input("marketing-apply-filters", "n_clicks"),
            Input("marketing-reset-filters", "n_clicks"),
        ],
        [State("marketing-filter-modal", "is_open")],
    )
    def toggle_filter_modal(n1, n2, n3, is_open):
        if not ctx.triggered:
            return is_open

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "filter-button":
            return not is_open
        elif trigger_id in ["marketing-apply-filters", "marketing-reset-filters"]:
            return False

        return is_open

    @app.callback(
        [
            Output("marketing-date-range", "start_date"),
            Output("marketing-date-range", "end_date"),
            Output("marketing-channel-filter", "value"),
            Output("marketing-campaign-filter", "value"),
            Output("marketing-category-filter", "value"),
            Output("marketing-device-filter", "value"),
            Output("marketing-segment-filter", "value"),
        ],
        [Input("marketing-reset-filters", "n_clicks")],
    )
    def reset_filters(n_clicks):
        if n_clicks and n_clicks > 0:
            if not data_manager.df_ad_revenue.empty:
                min_date = data_manager.df_ad_revenue["date"].min()
                max_date = data_manager.df_ad_revenue["date"].max()
            else:
                min_date = datetime(2025, 1, 1)
                max_date = datetime(2025, 12, 31)
            return min_date, max_date, [], [], [], [], []
        return no_update

    @app.callback(
        Output("marketing-filters-store", "data"),
        [Input("marketing-apply-filters", "n_clicks")],
        [
            State("marketing-date-range", "start_date"),
            State("marketing-date-range", "end_date"),
            State("marketing-channel-filter", "value"),
            State("marketing-campaign-filter", "value"),
            State("marketing-category-filter", "value"),
            State("marketing-device-filter", "value"),
            State("marketing-segment-filter", "value"),
        ],
    )
    def apply_filters(
        n_clicks,
        start_date,
        end_date,
        channels,
        campaigns,
        categories,
        devices,
        segments,
    ):
        if n_clicks is None or n_clicks == 0:
            return {
                "start_date": None,
                "end_date": None,
                "channels": [],
                "campaigns": [],
                "categories": [],
                "devices": [],
                "segments": [],
            }

        return {
            "start_date": start_date,
            "end_date": end_date,
            "channels": channels,
            "campaigns": campaigns,
            "categories": categories,
            "devices": devices,
            "segments": segments,
        }

    @app.callback(
        Output("marketing-kpi-cards", "children"),
        [Input("marketing-filters-store", "data")],
    )
    def update_kpi_cards(filters_data):
        if not filters_data:
            return [
                dbc.Col(create_kpi_card("📊 Общий ROMI", "0%"), width=2),
                dbc.Col(create_kpi_card("💰 Расходы на рекламу", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("💸 Доход от рекламы", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("🎯 CTR", "0%"), width=2),
                dbc.Col(create_kpi_card("👥 Стоимость привлечения", "0 ₽"), width=2),
                dbc.Col(create_kpi_card("📈 Конверсия", "0%"), width=2),
            ]

        start_date = filters_data.get("start_date")
        end_date = filters_data.get("end_date")
        channels = filters_data.get("channels")
        campaigns = filters_data.get("campaigns")
        categories = filters_data.get("categories")
        devices = filters_data.get("devices")
        segments = filters_data.get("segments")

        try:
            total_romi = calculations.calculate_total_romi(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            total_spend = calculations.calculate_total_spend(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            total_revenue = calculations.calculate_total_revenue(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            ctr = calculations.calculate_ctr(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            cac = calculations.calculate_cac(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            conversion_rate = calculations.calculate_conversion_rate(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )

            kpi_cards = [
                dbc.Col(create_kpi_card("📊 Общий ROMI", f"{total_romi}%"), width=2),
                dbc.Col(
                    create_kpi_card("💰 Расходы на рекламу", f"{total_spend:,.0f} ₽"),
                    width=2,
                ),
                dbc.Col(
                    create_kpi_card("💸 Доход от рекламы", f"{total_revenue:,.0f} ₽"),
                    width=2,
                ),
                dbc.Col(create_kpi_card("🎯 CTR", f"{ctr}%"), width=2),
                dbc.Col(
                    create_kpi_card("👥 Стоимость привлечения", f"{cac:,.0f} ₽"), width=2
                ),
                dbc.Col(create_kpi_card("📈 Конверсия", f"{conversion_rate}%"), width=2),
            ]

            return kpi_cards

        except Exception as e:
            print(f"Error updating KPI cards: {e}")
            return [
                dbc.Col(create_kpi_card("📊 Общий ROMI", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("💰 Расходы на рекламу", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("💸 Доход от рекламы", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("🎯 CTR", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("👥 Стоимость привлечения", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("📈 Конверсия", "Ошибка"), width=2),
            ]

    @app.callback(
        [
            Output("marketing-romi-trend-chart", "figure"),
            Output("marketing-budget-distribution-chart", "figure"),
            Output("marketing-campaigns-effectiveness-chart", "figure"),
            Output("marketing-ctr-by-channels-chart", "figure"),
            Output("marketing-cac-by-segments-chart", "figure"),
            Output("marketing-conversion-by-devices-chart", "figure"),
        ],
        [Input("marketing-filters-store", "data")],
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
        channels = filters_data.get("channels")
        campaigns = filters_data.get("campaigns")
        categories = filters_data.get("categories")
        devices = filters_data.get("devices")
        segments = filters_data.get("segments")

        try:
            romi_trend_chart = charts.create_romi_trend_chart(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            budget_distribution_chart = charts.create_budget_distribution_chart(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            campaigns_effectiveness_chart = charts.create_campaigns_effectiveness_chart(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            ctr_by_channels_chart = charts.create_ctr_by_channels_chart(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            cac_by_segments_chart = charts.create_cac_by_segments_chart(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )
            conversion_by_devices_chart = charts.create_conversion_by_devices_chart(
                start_date, end_date, channels, campaigns, categories, devices, segments
            )

            return (
                romi_trend_chart,
                budget_distribution_chart,
                campaigns_effectiveness_chart,
                ctr_by_channels_chart,
                cac_by_segments_chart,
                conversion_by_devices_chart,
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
