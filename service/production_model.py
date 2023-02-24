from service.service.builders.builders import ConnectionBuilder, ParserBuilder, DeployBuilder
import time


class ProductionModel:

    @staticmethod
    def postprocess(y):
        return int(y)

    def __init__(self,
                 model,
                 config) -> None:
        self.connection = ConnectionBuilder(config).construct()
        self.connection.init()
        self.parser = ParserBuilder(config).construct()
        self.deployer = DeployBuilder(config).construct()
        self.deployer.setup('app.py')
        self.deployer.deploy()
        self.model = model

    def predict(self, data, **predict_kwargs):
        start = time.time()
        y = self.model.predict(data, **predict_kwargs)
        y = ProductionModel.postprocess(y)
        # cast blob name
        blob_name = self.parser.cast_filename()
        # connect to blob
        self.connection.connect_to_file(blob_name)
        # download data
        logs = self.connection.download()
        # parse log string
        out_text = self.parser.cast_log_string(logs, data, y, start)
        end = time.time()
        # upload data
        self.connection.upload(out_text)
        # return response
        return y
