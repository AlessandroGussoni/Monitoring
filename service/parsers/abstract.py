from abc import ABC, abstractmethod


class AbstractParser(ABC):

    @abstractmethod
    def cast_filename(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def cast_log_string(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def sting_to_data(self, string, *args, **kwargs):
        raise NotImplementedError
