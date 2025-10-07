from dash import html
import dash_bootstrap_components as dbc



def create_operations_filters():
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader("ℹ️ Информация"),
                    dbc.ModalBody(
                        [
                            html.Div(
                                [
                                    html.H4(
                                        "Фильтры не доступны",
                                        className="text-center mb-3",
                                    ),
                                    html.P(
                                        "Для операционной деятельности используются актуальные данные на текущий момент.",
                                        className="text-center mb-2",
                                    ),
                                    html.P(
                                        "Все метрики обновляются в реальном времени.",
                                        className="text-center text-muted",
                                    ),
                                ],
                                className="text-center",
                            )
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Понятно", id="operations-close-modal", color="primary"
                            ),
                        ]
                    ),
                ],
                id="operations-filter-modal",
                size="md",
                is_open=False,
            ),
        ]
    )
