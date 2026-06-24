from abc import ABC, abstractmethod


class BaseCollector(ABC):
    @abstractmethod
    def get_current_map(self):
        pass