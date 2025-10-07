from abc import ABC, abstractmethod
import dash_bootstrap_components as dbc


class BaseTab(ABC):
    def __init__(self, data_manager):
        self.data_manager = data_manager

    @abstractmethod
    def get_layout(self):
        pass

    @abstractmethod
    def register_callbacks(self, app):
        pass
