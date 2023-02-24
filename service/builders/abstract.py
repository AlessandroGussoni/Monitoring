from abc import ABC, abstractmethod


class AbstractBuilder(ABC):

    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def construct(self, *args, **kwargs):
        raise NotImplementedError
