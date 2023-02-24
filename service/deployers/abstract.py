from abc import ABC, abstractmethod


class AbstractDeployer(ABC):

    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def setup(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def deploy(self, *args, **kwargs):
        raise NotImplementedError
