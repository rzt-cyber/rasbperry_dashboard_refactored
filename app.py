import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from core.data_manager import DataManager
from tabs.overview.layout import OverviewTab
from tabs.customers.layout import CustomersTab
from tabs.sales.layout import SalesTab
from tabs.marketing.layout import MarketingTab
from tabs.operations.layout import OperationsTab
from components.navbar import create_navbar

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
app.title = "Малинка - Analytics Dashboard"

data_manager = DataManager()
data_loaded = data_manager.load_data()

if not data_loaded:
    print("Внимание: Данные не загружены. Проверьте наличие CSV файлов.")

overview_tab = OverviewTab(data_manager)
customers_tab = CustomersTab(data_manager)
sales_tab = SalesTab(data_manager)
marketing_tab = MarketingTab(data_manager)
operations_tab = OperationsTab(data_manager)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        create_navbar(),
        html.Div(id="page-content", className="content-container"),
        dcc.Store(id="filter-store", data={}),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/customers":
        return customers_tab.get_layout()
    elif pathname == "/sales":
        return sales_tab.get_layout()
    elif pathname == "/marketing":
        return marketing_tab.get_layout()
    elif pathname == "/operations":
        return operations_tab.get_layout()
    else:
        return overview_tab.get_layout()


overview_tab.register_callbacks(app)
customers_tab.register_callbacks(app)
sales_tab.register_callbacks(app)
marketing_tab.register_callbacks(app)
operations_tab.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
