from abc import ABCMeta, abstractmethod


class Worker():
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, frame):
        """Метод обработки кадра"""
