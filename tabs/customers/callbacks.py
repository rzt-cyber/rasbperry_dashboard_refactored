from dash import Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
from components.kpi_cards import create_kpi_card
from datetime import datetime


def register_customers_callbacks(app, data_manager, calculations, charts):
    @app.callback(
        Output("customers-filter-modal", "is_open"),
        [
            Input("filter-button", "n_clicks"),
            Input("customers-apply-filters", "n_clicks"),
            Input("customers-reset-filters", "n_clicks"),
        ],
        [State("customers-filter-modal", "is_open")],
    )
    def toggle_filter_modal(n1, n2, n3, is_open):
        if not ctx.triggered:
            return is_open

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "filter-button":
            return not is_open
        elif trigger_id in ["customers-apply-filters", "customers-reset-filters"]:
            return False

        return is_open

    @app.callback(
        [
            Output("customers-date-range", "start_date"),
            Output("customers-date-range", "end_date"),
            Output("customers-region-filter", "value"),
            Output("customers-segment-filter", "value"),
            Output("customers-channel-filter", "value"),
            Output("customers-device-filter", "value"),
        ],
        [Input("customers-reset-filters", "n_clicks")],
    )
    def reset_filters(n_clicks):
        if n_clicks and n_clicks > 0:
            if not data_manager.df_user_segments.empty:
                min_date = data_manager.df_user_segments["registration_date"].min()
                max_date = data_manager.df_user_segments["registration_date"].max()
            else:
                min_date = datetime(2025, 1, 1)
                max_date = datetime(2025, 12, 31)
            return min_date, max_date, [], [], [], []
        return no_update

    @app.callback(
        Output("customers-filters-store", "data"),
        [Input("customers-apply-filters", "n_clicks")],
        [
            State("customers-date-range", "start_date"),
            State("customers-date-range", "end_date"),
            State("customers-region-filter", "value"),
            State("customers-segment-filter", "value"),
            State("customers-channel-filter", "value"),
            State("customers-device-filter", "value"),
        ],
    )
    def apply_filters(
        n_clicks, start_date, end_date, regions, segments, channels, devices
    ):
        if n_clicks is None or n_clicks == 0:
            return {
                "start_date": None,
                "end_date": None,
                "regions": [],
                "segments": [],
                "channels": [],
                "devices": [],
            }

        return {
            "start_date": start_date,
            "end_date": end_date,
            "regions": regions,
            "segments": segments,
            "channels": channels,
            "devices": devices,
        }

    @app.callback(
        Output("customers-kpi-cards", "children"),
        [Input("customers-filters-store", "data")],
    )
    def update_kpi_cards(filters_data):
        if not filters_data:
            return [
                dbc.Col(create_kpi_card("👥 Всего клиентов", "0"), width=2),
                dbc.Col(create_kpi_card("🆕 Новые клиенты", "0"), width=2),
                dbc.Col(create_kpi_card("💎 Лояльные клиенты", "0"), width=2),
                dbc.Col(create_kpi_card("⚠️ В группе риска", "0"), width=2),
                dbc.Col(create_kpi_card("💰 Крупные покупатели", "0"), width=2),
                dbc.Col(create_kpi_card("🎯 Ищущие скидки", "0"), width=2),
            ]

        start_date = filters_data.get("start_date")
        end_date = filters_data.get("end_date")
        regions = filters_data.get("regions")
        segments = filters_data.get("segments")
        channels = filters_data.get("channels")
        devices = filters_data.get("devices")

        try:
            total_customers = calculations.calculate_total_customers(
                start_date, end_date, regions, segments, channels, devices
            )
            new_customers = calculations.calculate_new_customers(
                start_date, end_date, regions, segments, channels, devices
            )
            loyal_customers = calculations.calculate_loyal_customers(
                start_date, end_date, regions, segments, channels, devices
            )
            risk_customers = calculations.calculate_risk_customers(
                start_date, end_date, regions, segments, channels, devices
            )
            high_spender_customers = calculations.calculate_high_spender_customers(
                start_date, end_date, regions, segments, channels, devices
            )
            discount_hunter_customers = (
                calculations.calculate_discount_hunter_customers(
                    start_date, end_date, regions, segments, channels, devices
                )
            )

            kpi_cards = [
                dbc.Col(
                    create_kpi_card("👥 Всего клиентов", f"{total_customers:,}"), width=2
                ),
                dbc.Col(
                    create_kpi_card("🆕 Новые клиенты", f"{new_customers:,}"), width=2
                ),
                dbc.Col(
                    create_kpi_card("💎 Лояльные клиенты", f"{loyal_customers:,}"),
                    width=2,
                ),
                dbc.Col(
                    create_kpi_card("⚠️ В группе риска", f"{risk_customers:,}"), width=2
                ),
                dbc.Col(
                    create_kpi_card(
                        "💰 Крупные покупатели", f"{high_spender_customers:,}"
                    ),
                    width=2,
                ),
                dbc.Col(
                    create_kpi_card(
                        "🎯 Ищущие скидки", f"{discount_hunter_customers:,}"
                    ),
                    width=2,
                ),
            ]

            return kpi_cards

        except Exception as e:
            print(f"Error updating KPI cards: {e}")
            return [
                dbc.Col(create_kpi_card("👥 Всего клиентов", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("🆕 Новые клиенты", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("💎 Лояльные клиенты", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("⚠️ В группе риска", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("💰 Крупные покупатели", "Ошибка"), width=2),
                dbc.Col(create_kpi_card("🎯 Ищущие скидки", "Ошибка"), width=2),
            ]

    @app.callback(
        [
            Output("customers-segments-chart", "figure"),
            Output("customers-registrations-chart", "figure"),
            Output("customers-regions-chart", "figure"),
            Output("customers-channels-chart", "figure"),
        ],
        [Input("customers-filters-store", "data")],
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
            return empty_fig, empty_fig, empty_fig, empty_fig

        start_date = filters_data.get("start_date")
        end_date = filters_data.get("end_date")
        regions = filters_data.get("regions")
        segments = filters_data.get("segments")
        channels = filters_data.get("channels")
        devices = filters_data.get("devices")

        try:
            segments_chart = charts.create_segments_chart(
                start_date, end_date, regions, segments, channels, devices
            )
            registrations_chart = charts.create_registrations_chart(
                start_date, end_date, regions, segments, channels, devices
            )
            regions_chart = charts.create_regions_chart(
                start_date, end_date, regions, segments, channels, devices
            )
            channels_chart = charts.create_channels_chart(
                start_date, end_date, regions, segments, channels, devices
            )

            return segments_chart, registrations_chart, regions_chart, channels_chart

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
            return error_fig, error_fig, error_fig, error_fig