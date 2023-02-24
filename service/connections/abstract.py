from abc import ABC, abstractmethod


class AbstractConnection(ABC):

    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def init(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def connect_to_file(self, filename, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def upload(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def download(self, *args, **kwargs):
        raise NotImplementedError
