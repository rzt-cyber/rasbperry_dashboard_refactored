from dash import html
import dash_bootstrap_components as dbc


def create_kpi_card(title, value, delta=None, delta_color="success", icon=None):
    delta_element = (
        html.Small(f"{delta}", className=f"text-{delta_color}") if delta else None
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H6(title, className="card-title kpi-title"),
                        html.H4(value, className="card-value kpi-value"),
                        delta_element,
                    ],
                    className="kpi-content",
                )
            ]
        ),
        className="kpi-card text-center",
    )
