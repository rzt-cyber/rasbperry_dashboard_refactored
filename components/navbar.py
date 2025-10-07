from dash import html, dcc
import dash_bootstrap_components as dbc


def create_navbar():
    return dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                html.Img(
                                    src="/assets/logo.png",
                                    height="50px",
                                    className="navbar-logo",
                                ),
                                className="logo-container",
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                className="logo-link",
                style={"textDecoration": "none", "marginRight": "30px"},
            ),
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink(
                            "📊 Обзор",
                            href="/",
                            active="exact",
                            className="nav-link-custom",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "👥 Клиенты",
                            href="/customers",
                            active="exact",
                            className="nav-link-custom",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "💰 Продажи",
                            href="/sales",
                            active="exact",
                            className="nav-link-custom",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "📢 Маркетинг",
                            href="/marketing",
                            active="exact",
                            className="nav-link-custom",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "⚙️ Операции",
                            href="/operations",
                            active="exact",
                            className="nav-link-custom",
                        )
                    ),
                ],
                className="me-auto",
                navbar=True,
            ),
            dbc.Button(
                "🔍 Фильтры",
                id="filter-button",
                color="primary",
                className="me-2 wildberries-btn",
            ),
        ],
        color="primary",
        dark=True,
        sticky="top",
        className="navbar-wildberries",
    )
