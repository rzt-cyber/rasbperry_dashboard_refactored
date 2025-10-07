import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .calculations import MarketingCalculations


class MarketingCharts:
    def __init__(self, data_manager):
        self.dm = data_manager
        self.calculations = MarketingCalculations(data_manager)

    def create_romi_trend_chart(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        romi_data = self.calculations.get_romi_trend(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )

        if len(romi_data) == 0:
            return self._create_empty_chart("Нет данных по ROMI за выбранные фильтры")

        title = "📈 Динамика ROMI по дням"
        filter_info = self._get_filter_info(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.line(
            romi_data,
            x="date",
            y="romi",
            title=title,
            labels={"date": "Дата", "romi": "ROMI, %"},
            color_discrete_sequence=["#8a2be2"],
        )

        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1", tickformat="%d.%m.%Y"),
            yaxis=dict(gridcolor="#ecf0f1", ticksuffix="%"),
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate="<b>%{x|%d.%m.%Y}</b><br>ROMI: <b>%{y}%</b><extra></extra>",
        )

        return fig

    def create_budget_distribution_chart(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        budget_data = self.calculations.get_budget_distribution(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )

        if len(budget_data) == 0:
            return self._create_empty_chart(
                "Нет данных по распределению бюджета за выбранные фильтры"
            )

        title = "💰 Распределение бюджета по каналам"
        filter_info = self._get_filter_info(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.pie(
            budget_data,
            values="sessions",
            names="channel",
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
            hovertemplate="<b>%{label}</b><br>Сессий: <b>%{value}</b><br>Доля: <b>%{percent}</b><extra></extra>",
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

    def create_campaigns_effectiveness_chart(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        campaigns_data = self.calculations.get_campaigns_effectiveness(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )

        if len(campaigns_data) == 0:
            return self._create_empty_chart(
                "Нет данных по кампаниям за выбранные фильтры"
            )

        title = "🏆 Топ-10 кампаний по ROMI"
        filter_info = self._get_filter_info(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            campaigns_data,
            x="romi",
            y="campaign_name",
            orientation="h",
            title=title,
            labels={"romi": "ROMI, %", "campaign_name": "Кампания"},
            color="romi",
            color_continuous_scale=["#FF6B6B", "#FF9999", "#96CEB4", "#4ECDC4"],
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1", ticksuffix="%"),
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>ROMI: <b>%{x}%</b><extra></extra>"
        )

        return fig

    def create_ctr_by_channels_chart(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        ctr_data = self.calculations.get_ctr_by_channels(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )

        if len(ctr_data) == 0:
            return self._create_empty_chart(
                "Нет данных по каналам за выбранные фильтры"
            )

        title = "🎯 Активность по каналам трафика"
        filter_info = self._get_filter_info(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            ctr_data,
            x="sessions",
            y="channel",
            orientation="h",
            title=title,
            labels={"sessions": "Количество сессий", "channel": "Канал"},
            color="sessions",
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
            hovertemplate="<b>%{y}</b><br>Сессий: <b>%{x}</b><extra></extra>"
        )

        return fig

    def create_cac_by_segments_chart(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        cac_data = self.calculations.get_cac_by_segments(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )

        if len(cac_data) == 0:
            return self._create_empty_chart(
                "Нет данных по сегментам за выбранные фильтры"
            )

        title = "👥 Стоимость привлечения по сегментам"
        filter_info = self._get_filter_info(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.bar(
            cac_data,
            x="cac",
            y="segment",
            orientation="h",
            title=title,
            labels={"cac": "CAC, ₽", "segment": "Сегмент"},
            color="cac",
            color_continuous_scale=["#FF6B6B", "#FF9999", "#FFCCCC"],
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#2c3e50"),
            xaxis=dict(gridcolor="#ecf0f1", tickprefix="₽"),
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=12)
            ),
        )

        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>CAC: <b>%{x} ₽</b><extra></extra>"
        )

        return fig

    def create_conversion_by_devices_chart(
        self,
        start_date=None,
        end_date=None,
        channels=None,
        campaigns=None,
        categories=None,
        devices=None,
        segments=None,
    ):
        conversion_data = self.calculations.get_conversion_by_devices(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )

        if len(conversion_data) == 0:
            return self._create_empty_chart(
                "Нет данных по устройствам за выбранные фильтры"
            )

        title = "📱 Активность по устройствам"
        filter_info = self._get_filter_info(
            start_date, end_date, channels, campaigns, categories, devices, segments
        )
        if filter_info:
            title += f"<br><sub>{filter_info}</sub>"

        fig = px.pie(
            conversion_data,
            values="sessions",
            names="device",
            title=title,
            color_discrete_sequence=["#4ECDC4", "#45B7D1", "#96CEB4"],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2)),
            hovertemplate="<b>%{label}</b><br>Сессий: <b>%{value}</b><br>Доля: <b>%{percent}</b><extra></extra>",
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
        self, start_date, end_date, channels, campaigns, categories, devices, segments
    ):
        """Создает строку с информацией о примененных фильтрах"""
        filters = []

        if start_date and end_date:
            start_str = pd.to_datetime(start_date).strftime("%d.%m.%Y")
            end_str = pd.to_datetime(end_date).strftime("%d.%m.%Y")
            filters.append(f"Период: {start_str} - {end_str}")

        if channels and len(channels) > 0:
            filters.append(
                f"Каналы: {', '.join(channels[:2])}{'...' if len(channels) > 2 else ''}"
            )

        if campaigns and len(campaigns) > 0:
            filters.append(
                f"Кампании: {', '.join(campaigns[:2])}{'...' if len(campaigns) > 2 else ''}"
            )

        if categories and len(categories) > 0:
            filters.append(
                f"Категории: {', '.join(categories[:2])}{'...' if len(categories) > 2 else ''}"
            )

        if devices and len(devices) > 0:
            filters.append(f"Устройства: {', '.join(devices)}")

        if segments and len(segments) > 0:
            filters.append(
                f"Сегменты: {', '.join(segments[:2])}{'...' if len(segments) > 2 else ''}"
            )

        return " | ".join(filters) if filters else ""
