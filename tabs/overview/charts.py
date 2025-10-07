import plotly.express as px
import pandas as pd
from .calculations import OverviewCalculations


class OverviewCharts:
    def __init__(self, data_manager):
        self.dm = data_manager
        self.calculations = OverviewCalculations(data_manager)

    def create_sales_trend_chart(
        self, start_date=None, end_date=None, regions=None, categories=None
    ):
        df = self.dm.df_sales.copy()
        df = self.calculations.apply_filters(
            df, start_date, end_date, regions, categories
        )

        df = df.merge(self.dm.df_products[["product_id", "price"]], on="product_id")
        df["revenue"] = df["quantity"] * df["price"]

        df = df[df["transaction_date"].dt.year == 2025]
        daily_sales = (
            df.groupby(df["transaction_date"].dt.date)["revenue"].sum().reset_index()
        )

        daily_sales = daily_sales.sort_values("transaction_date")

        fig = px.line(
            daily_sales,
            x="transaction_date",
            y="revenue",
            title="📈 Тренд продаж по дням",
            labels={"transaction_date": "Дата", "revenue": "Выручка, ₽"},
            color_discrete_sequence=["#8a2be2"],
        )

        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1", tickformat="%d.%m.%Y"),
            yaxis=dict(gridcolor="#ecf0f1", tickformat=",.0f"),
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate="<b>%{x|%d.%m.%Y}</b><br>Выручка: <b>%{y:,.0f} ₽</b><extra></extra>",
        )

        return fig

    def create_category_distribution_chart(
        self, start_date=None, end_date=None, regions=None, categories=None
    ):
        df = self.dm.df_sales.copy()

        df = self.calculations.apply_filters(
            df, start_date, end_date, regions, categories=None
        )

        df = df[df["transaction_date"].dt.year == 2025]

        df = df.merge(
            self.dm.df_products[["product_id", "category", "price"]], on="product_id"
        )
        df["revenue"] = df["quantity"] * df["price"]

        category_revenue = df.groupby("category")["revenue"].sum().reset_index()

        if categories and len(categories) > 0:
            selected_categories = category_revenue[
                category_revenue["category"].isin(categories)
            ]
            other_categories = category_revenue[
                ~category_revenue["category"].isin(categories)
            ]

            others_total = other_categories["revenue"].sum()

            if others_total > 0:
                others_row = pd.DataFrame(
                    {"category": ["Другие категории"], "revenue": [others_total]}
                )
                category_revenue = pd.concat(
                    [selected_categories, others_row], ignore_index=True
                )
            else:
                category_revenue = selected_categories

        colors = [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#FFEAA7",
            "#DDA0DD",
            "#98D8C8",
            "#F7DC6F",
        ]

        title = "🥧 Распределение выручки по категориям"
        if categories and len(categories) > 0:
            title = f"🥧 Сравнение выбранных категорий с рынком"

        fig = px.pie(
            category_revenue,
            values="revenue",
            names="category",
            title=title,
            hole=0.4,
            color_discrete_sequence=colors,
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            showlegend=True,
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2)),
            hovertemplate="<b>%{label}</b><br>Выручка: <b>%{value:,.0f} ₽</b><br>Доля: <b>%{percent}</b><extra></extra>",
        )

        return fig

    def create_top_products_chart(
        self, start_date=None, end_date=None, regions=None, categories=None, top_n=10
    ):
        df = self.dm.df_sales.copy()
        df = self.calculations.apply_filters(
            df, start_date, end_date, regions, categories
        )

        df = df[df["transaction_date"].dt.year == 2025]

        df = df.merge(
            self.dm.df_products[["product_id", "product_name", "price"]],
            on="product_id",
        )
        df["revenue"] = df["quantity"] * df["price"]

        top_products = (
            df.groupby("product_name")["revenue"].sum().nlargest(top_n).reset_index()
        )

        colors = [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#FFEAA7",
            "#DDA0DD",
            "#98D8C8",
            "#F7DC6F",
            "#BB8FCE",
            "#85C1E9",
        ]

        title = f"🏆 Топ {top_n} товаров по выручке"
        if categories and len(categories) > 0:
            title = f"🏆 Топ {top_n} товаров в выбранных категориях"

        fig = px.bar(
            top_products,
            x="revenue",
            y="product_name",
            orientation="h",
            title=title,
            labels={"revenue": "Выручка, ₽", "product_name": "Товар"},
            color="revenue",
            color_continuous_scale=colors,
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1", tickformat=",.0f"),
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Выручка: <b>%{x:,.0f} ₽</b><extra></extra>"
        )

        return fig
