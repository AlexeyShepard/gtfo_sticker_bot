from abc import ABC, abstractmethod
from telegram.ext import BaseHandler

class base_handler(ABC):
    @abstractmethod
    def make(self) -> BaseHandler:
        raise NotImplementedError('Метод make не реализован')

    