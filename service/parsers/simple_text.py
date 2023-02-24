import datetime
import io
import re
import time

import pandas as pd

from service.service.parsers.abstract import AbstractParser


class SimpleTextParser(AbstractParser):

    def __init__(self, config, *args, **kwargs):
        self.config = config

    def cast_filename(self):
        setattr(self, 'current_time', datetime.datetime.now())
        return f"{self.current_time.day}-{self.current_time.month}-{self.current_time.year}.txt"

    def cast_log_string(self, logs, data, y, start):
        input_string = f"Time {self.current_time.hour}-{self.current_time.minute}-{self.current_time.second}, Features:"
        for i, value in enumerate(data[0]): input_string += f" {self.config['feature_names'][i]} - {str(value)}"
        input_string += f", Prediction: {str(y)} \n"
        logs += input_string
        logs += f"<{str(round(time.time() - start, 5))}>"
        out_text = io.StringIO(logs)
        return out_text

    def sting_to_data(self, string, *args, **kwargs):
        if not isinstance(string, str):
            string = string.decode()
        string = string.split('\n')[1:-1]
        data = {'time': [], 'pred': [], 'response_time': []}
        for i, feature in enumerate(self.config['feature_names']): data[feature] = []
        for log in string:
            if log == '': continue
            log_list = log.split('>')[1]
            log_list = log_list.split(',')
            # getting time
            hour = log_list[0].split(' ')[-1]
            data['time'].append(datetime.datetime.strptime(hour, '%H-%M-%S'))
            values = re.findall(r'\d+', log_list[1])
            for i, feature in enumerate(self.config['feature_names']):
                data[feature].append(float(values[i]))
            data['pred'].append(int(log_list[-1].split(":")[-1]))
            data['response_time'].append(float(log.split('>')[0].replace('<', '')))
        return pd.DataFrame(data)
