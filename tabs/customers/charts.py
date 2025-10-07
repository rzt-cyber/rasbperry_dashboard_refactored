import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .calculations import CustomersCalculations


class CustomersCharts:
    def __init__(self, data_manager):
        self.dm = data_manager
        self.calculations = CustomersCalculations(data_manager)

    def create_segments_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        segments_data = self.calculations.get_segments_distribution(
            start_date, end_date, regions, segments, channels, devices
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

        title = "📊 Распределение клиентов по сегментам"
        filter_info = self._get_filter_info(
            start_date, end_date, regions, segments, channels, devices
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.pie(
            segments_data,
            values="customer_id",
            names="segment",
            title=title,
            color="segment",
            color_discrete_map=segment_colors,
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2)),
            hovertemplate="<b>%{label}</b><br>Клиентов: <b>%{value}</b><br>Доля: <b>%{percent}</b><extra></extra>",
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

    def create_registrations_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        registrations_data = self.calculations.get_registrations_trend(
            start_date, end_date, regions, segments, channels, devices
        )

        if len(registrations_data) == 0:
            return self._create_empty_chart(
                "Нет данных о регистрациях за выбранные фильтры"
            )

        title = "📈 Динамика регистраций клиентов"
        filter_info = self._get_filter_info(
            start_date, end_date, regions, segments, channels, devices
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.line(
            registrations_data,
            x="date",
            y="registrations",
            title=title,
            labels={"date": "Дата", "registrations": "Регистрации"},
            color_discrete_sequence=["#8a2be2"],
        )

        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1", tickformat="%d.%m.%Y"),
            yaxis=dict(gridcolor="#ecf0f1"),
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate="<b>%{x|%d.%m.%Y}</b><br>Регистраций: <b>%{y}</b><extra></extra>",
        )

        return fig

    def create_regions_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        regions_data = self.calculations.get_regions_distribution(
            start_date, end_date, regions, segments, channels, devices
        )

        if len(regions_data) == 0:
            return self._create_empty_chart(
                "Нет данных по регионам за выбранные фильтры"
            )

        title = "🗺️ Распределение клиентов по регионам"
        filter_info = self._get_filter_info(
            start_date, end_date, regions, segments, channels, devices
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            regions_data,
            x="customer_id",
            y="region",
            orientation="h",
            title=title,
            labels={"customer_id": "Количество клиентов", "region": "Регион"},
            color="customer_id",
            color_continuous_scale=["#9370db", "#8a2be2", "#4b0082"],
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
            hovertemplate="<b>%{y}</b><br>Клиентов: <b>%{x}</b><extra></extra>"
        )

        return fig

    def create_channels_chart(
        self,
        start_date=None,
        end_date=None,
        regions=None,
        segments=None,
        channels=None,
        devices=None,
    ):
        channels_data = self.calculations.get_channels_distribution(
            start_date, end_date, regions, segments, channels, devices
        )

        if len(channels_data) == 0:
            return self._create_empty_chart(
                "Нет данных по каналам привлечения за выбранные фильтры"
            )

        title = "📡 Каналы привлечения клиентов"
        filter_info = self._get_filter_info(
            start_date, end_date, regions, segments, channels, devices
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            channels_data,
            x="unique_customers",
            y="channel",
            orientation="h",
            title=title,
            labels={"unique_customers": "Количество клиентов", "channel": "Канал"},
            color="unique_customers",
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
            hovertemplate="<b>%{y}</b><br>Клиентов: <b>%{x}</b><extra></extra>"
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
        self, start_date, end_date, regions, segments, channels, devices
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

        if segments and len(segments) > 0:
            filters.append(
                f"Сегменты: {', '.join(segments[:2])}{'...' if len(segments) > 2 else ''}"
            )

        if channels and len(channels) > 0:
            filters.append(
                f"Каналы: {', '.join(channels[:2])}{'...' if len(channels) > 2 else ''}"
            )

        if devices and len(devices) > 0:
            filters.append(f"Устройства: {', '.join(devices)}")

        return " | ".join(filters) if filters else ""
