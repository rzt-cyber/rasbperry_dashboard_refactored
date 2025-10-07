import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .calculations import SalesCalculations


class SalesCharts:
    def __init__(self, data_manager):
        self.dm = data_manager
        self.calculations = SalesCalculations(data_manager)

    def create_regions_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        regions_data = self.calculations.get_regions_distribution(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )

        if len(regions_data) == 0:
            return self._create_empty_chart(
                "Нет данных по регионам за выбранные фильтры"
            )

        title = "🗺️ Выручка по регионам"
        filter_info = self._get_filter_info(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            regions_data,
            x="revenue",
            y="region",
            orientation="h",
            title=title,
            labels={"revenue": "Выручка, ₽", "region": "Регион"},
            color="revenue",
            color_continuous_scale=["#9370db", "#8a2be2", "#4b0082"],
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

    def create_segments_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        segments_data = self.calculations.get_segments_distribution(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )

        if len(segments_data) == 0:
            return self._create_empty_chart(
                "Нет данных по сегментам за выбранные фильтры"
            )

        segment_colors = {
            "new": "#4ECDC4",
            "returning": "#45B7D1",
            "loyal": "#96CEB4",
            "churn_risk": "#FF6B6B",
            "high_spender": "#FFEAA7",
            "discount_hunter": "#DDA0DD",
        }

        title = "👥 Выручка по сегментам клиентов"
        filter_info = self._get_filter_info(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            segments_data,
            x="revenue",
            y="segment",
            orientation="h",
            title=title,
            labels={"revenue": "Выручка, ₽", "segment": "Сегмент"},
            color="segment",
            color_discrete_map=segment_colors,
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

    def create_payment_methods_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        payment_data = self.calculations.get_payment_methods_distribution(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )

        if len(payment_data) == 0:
            return self._create_empty_chart(
                "Нет данных по способам оплаты за выбранные фильтры"
            )

        title = "💳 Распределение выручки по способам оплаты"
        filter_info = self._get_filter_info(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.pie(
            payment_data,
            values="revenue",
            names="payment_method",
            title=title,
            color_discrete_sequence=[
                "#FF6B6B",
                "#4ECDC4",
                "#45B7D1",
                "#96CEB4",
                "#FFEAA7",
            ],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2)),
            hovertemplate="<b>%{label}</b><br>Выручка: <b>%{value:,.0f} ₽</b><br>Доля: <b>%{percent}</b><extra></extra>",
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

        return fig

    def create_suppliers_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        suppliers_data = self.calculations.get_suppliers_distribution(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )

        if len(suppliers_data) == 0:
            return self._create_empty_chart(
                "Нет данных по поставщикам за выбранные фильтры"
            )

        title = "🏭 Топ-10 поставщиков по выручке"
        filter_info = self._get_filter_info(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            suppliers_data,
            x="revenue",
            y="supplier_name",
            orientation="h",
            title=title,
            labels={"revenue": "Выручка, ₽", "supplier_name": "Поставщик"},
            color="revenue",
            color_continuous_scale=["#9370db", "#8a2be2", "#4b0082"],
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

    def create_hourly_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        hourly_data = self.calculations.get_hourly_distribution(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )

        if len(hourly_data) == 0:
            return self._create_empty_chart("Нет данных по часам за выбранные фильтры")

        title = "⏰ Выручка по часам дня"
        filter_info = self._get_filter_info(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.line(
            hourly_data,
            x="hour",
            y="revenue",
            title=title,
            labels={"hour": "Час дня", "revenue": "Выручка, ₽"},
            color_discrete_sequence=["#8a2be2"],
        )

        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1", tickmode="linear", dtick=1),
            yaxis=dict(gridcolor="#ecf0f1", tickformat=",.0f"),
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate="<b>%{x}:00</b><br>Выручка: <b>%{y:,.0f} ₽</b><extra></extra>",
        )

        return fig

    def _create_empty_chart(self, message):
        """Создает пустой график с сообщением"""
        fig = go.Figure()
        fig.update_layout(
            title=message,
            xaxis={"visible": False},
            yaxis={"visible": False},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
        )
        return fig

    def _get_filter_info(
        self,
        start_date,
        end_date,
        regions,
        categories,
        segments,
        payment_methods,
        suppliers,
    ):
        """Создает строку с информацией о примененных фильтрах"""
        filters = []

        if start_date and end_date:
            start_str = pd.to_datetime(start_date).strftime("%d.%m.%Y")
            end_str = pd.to_datetime(end_date).strftime("%d.%m.%Y")
            filters.append(f"Период: {start_str} - {end_str}")

        if regions and len(regions) > 0:
            filters.append(
                f"Регионы: {', '.join(regions[:2])}{'...' if len(regions) > 2 else ''}"
            )

        if categories and len(categories) > 0:
            filters.append(
                f"Категории: {', '.join(categories[:2])}{'...' if len(categories) > 2 else ''}"
            )

        if segments and len(segments) > 0:
            filters.append(
                f"Сегменты: {', '.join(segments[:2])}{'...' if len(segments) > 2 else ''}"
            )

        if payment_methods and len(payment_methods) > 0:
            filters.append(f"Оплата: {', '.join(payment_methods)}")

        if suppliers and len(suppliers) > 0:
            filters.append(
                f"Поставщики: {', '.join(suppliers[:2])}{'...' if len(suppliers) > 2 else ''}"
            )

        return " | ".join(filters) if filters else ""

    def create_returns_reasons_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        categories=None,
        segments=None,
        payment_methods=None,
        suppliers=None,
    ):
        reasons_data = self.calculations.get_returns_reasons_distribution(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )

        if len(reasons_data) == 0:
            return self._create_empty_chart(
                "Нет данных по возвратам за выбранные фильтры"
            )

        title = "📋 Топ причин возвратов"
        filter_info = self._get_filter_info(
            start_date,
            end_date,
            regions,
            categories,
            segments,
            payment_methods,
            suppliers,
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            reasons_data,
            x="returns_count",
            y="reason",
            orientation="h",
            title=title,
            labels={
                "returns_count": "Количество возвратов",
                "reason": "Причина возврата",
            },
            color="returns_count",
            color_continuous_scale=["#FF6B6B", "#FF9999", "#FFCCCC"],
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1"),
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Возвратов: <b>%{x}</b><extra></extra>"
        )

        return fig
