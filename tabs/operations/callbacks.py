from dash import callback, Input, Output, State, html, no_update, ctx
import dash_bootstrap_components as dbc
from components.kpi_cards import create_kpi_card


def register_operations_callbacks(app, data_manager, calculations, charts):
    @app.callback(
        Output("operations-filter-modal", "is_open"),
        [
            Input("filter-button", "n_clicks"),
            Input("operations-close-modal", "n_clicks"),
        ],
        [State("operations-filter-modal", "is_open")],
    )
    def toggle_info_modal(n1, n2, is_open):
        if not ctx.triggered:
            return is_open

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "filter-button":
            return True
        elif trigger_id == "operations-close-modal":
            return False

        return is_open

    @app.callback(
        [
            Output("operations-inventory-kpi", "children"),
            Output("operations-support-kpi", "children"),
        ],
        [Input("url", "pathname")],
    )
    def update_kpi_cards(pathname):
        if pathname != "/operations":
            return no_update, no_update

        try:
            stock_availability = calculations.calculate_stock_availability()
            low_stock_items = calculations.calculate_low_stock_items()
            inventory_value = calculations.calculate_inventory_value()
            
            avg_resolution_time = calculations.calculate_avg_resolution_time()
            resolved_rate = calculations.calculate_resolved_tickets_rate()
            overdue_tickets = calculations.calculate_overdue_tickets()
            delivery_delays = calculations.calculate_delivery_delays()

            inventory_kpi = [
                dbc.Col(
                    create_kpi_card("Уровень доступности", f"{stock_availability}%"),
                    width=3,
                ),
                dbc.Col(
                    create_kpi_card("Товары с дефицитом", f"{low_stock_items}"), width=3
                ),
                dbc.Col(
                    create_kpi_card("Стоимость запасов", f"{inventory_value:,.0f} ₽"),
                    width=3,
                ),
            ]

            support_kpi = [
                dbc.Col(
                    create_kpi_card("Время решения", f"{avg_resolution_time} ч"),
                    width=3,
                ),
                dbc.Col(
                    create_kpi_card("Решено тикетов", f"{resolved_rate}%"), width=3
                ),
                dbc.Col(
                    create_kpi_card("Просрочено >24ч", f"{overdue_tickets}"), width=3
                ),
                dbc.Col(
                    create_kpi_card("Задержки доставки", f"{delivery_delays}"), width=3
                ),
            ]

            return inventory_kpi, support_kpi

        except Exception as e:
            print(f"Error updating operations KPI cards: {e}")
            error_kpi = [
                dbc.Col(create_kpi_card("Ошибка", "Ошибка"), width=3),
                dbc.Col(create_kpi_card("Ошибка", "Ошибка"), width=3),
                dbc.Col(create_kpi_card("Ошибка", "Ошибка"), width=3),
                dbc.Col(create_kpi_card("Ошибка", "Ошибка"), width=3),
            ]
            return error_kpi, error_kpi

    @app.callback(
        [
            Output("operations-stock-heatmap-chart", "figure"),
            Output("operations-issue-resolution-chart", "figure"),
            Output("operations-ticket-status-chart", "figure"),
            Output("operations-low-stock-chart", "figure"),
        ],
        [Input("url", "pathname")],
    )
    def update_charts(pathname):
        if pathname != "/operations":
            return no_update, no_update, no_update, no_update

        try:
            stock_heatmap = charts.create_stock_heatmap_chart()
            issue_resolution = charts.create_issue_resolution_chart()
            ticket_status = charts.create_ticket_status_chart()
            low_stock_fig = charts.create_low_stock_chart()

            return stock_heatmap, issue_resolution, ticket_status, low_stock_fig

        except Exception as e:
            print(f"Error updating operations charts: {e}")
            error_fig = {
                "data": [],
                "layout": {
                    "title": f"Ошибка при загрузке данных: {str(e)}",
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                },
            }
            return error_fig, error_fig, error_fig, error_fig

    @app.callback(
        [
            Output("operations-inventory-kpi", "children", allow_duplicate=True),
            Output("operations-support-kpi", "children", allow_duplicate=True),
            Output("operations-stock-heatmap-chart", "figure", allow_duplicate=True),
            Output("operations-issue-resolution-chart", "figure", allow_duplicate=True),
            Output("operations-ticket-status-chart", "figure", allow_duplicate=True),
            Output("operations-low-stock-chart", "figure", allow_duplicate=True),
        ],
        [Input("interval-component", "n_intervals")],
        prevent_initial_call=True,
    )
    def update_data_live(n_intervals):
        try:
            stock_availability = calculations.calculate_stock_availability()
            low_stock_items = calculations.calculate_low_stock_items()
            inventory_value = calculations.calculate_inventory_value()

            avg_resolution_time = calculations.calculate_avg_resolution_time()
            resolved_rate = calculations.calculate_resolved_tickets_rate()
            overdue_tickets = calculations.calculate_overdue_tickets()
            delivery_delays = calculations.calculate_delivery_delays()

            inventory_kpi = [
                dbc.Col(
                    create_kpi_card("Уровень доступности", f"{stock_availability}%"),
                    width=3,
                ),
                dbc.Col(
                    create_kpi_card("Товары с дефицитом", f"{low_stock_items}"), width=3
                ),
                dbc.Col(
                    create_kpi_card("Стоимость запасов", f"{inventory_value:,.0f} ₽"),
                    width=3,
                )
                
            ]

            support_kpi = [
                dbc.Col(
                    create_kpi_card("Время решения", f"{avg_resolution_time} ч"),
                    width=3,
                ),
                dbc.Col(
                    create_kpi_card("Решено тикетов", f"{resolved_rate}%"), width=3
                ),
                dbc.Col(
                    create_kpi_card("Просрочено >24ч", f"{overdue_tickets}"), width=3
                ),
                dbc.Col(
                    create_kpi_card("Задержки доставки", f"{delivery_delays}"), width=3
                ),
            ]

            stock_heatmap = charts.create_stock_heatmap_chart()
            issue_resolution = charts.create_issue_resolution_chart()
            ticket_status = charts.create_ticket_status_chart()
            low_stock_fig = charts.create_low_stock_chart()

            return (
                inventory_kpi,
                support_kpi,
                stock_heatmap,
                issue_resolution,
                ticket_status,
                low_stock_fig,
            )

        except Exception as e:
            print(f"Error in live update: {e}")
            return no_update, no_update, no_update, no_update, no_update, no_update
