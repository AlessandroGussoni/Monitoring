from service.service.builders.abstract import AbstractBuilder
from service.service.connections.google import GoogleBucket
from service.service.parsers.simple_text import SimpleTextParser
from service.service.deployers.google import GoogleDeployer


class ConnectionBuilder(AbstractBuilder):

    def __init__(self, config):
        self.config = config

    def construct(self, *args, **kwargs):
        if self.config['service'] == 'google':
            return GoogleBucket(bucket_name=self.config['bucket_name'], *args, **kwargs)


class ParserBuilder(AbstractBuilder):

    def __init__(self, config):
        self.config = config

    def construct(self, *args, **kwargs):
        if self.config['parser'] == 'simple_text':
            return SimpleTextParser(self.config, args, **kwargs)


class DeployBuilder(AbstractBuilder):

    def __init__(self, config):
        self.config = config

    def construct(self, *args, **kwargs):
        if self.config['deploy'] == 'google':
            return GoogleDeployer(self.config, *args, **kwargs)
