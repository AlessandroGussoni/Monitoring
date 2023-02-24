import json
import os
import sys

import streamlit as st
from streamlit.web import cli as stcli

sys.path.append(__file__)
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from service.service.builders.builders import ConnectionBuilder, ParserBuilder

CONFIG = os.path.join(os.path.dirname(__file__), "..", "app", "config.json")

with open(CONFIG, 'r') as file:
    config = json.load(file)


def main(d_config):
    connection = ConnectionBuilder(config).construct()
    parser = ParserBuilder(config).construct()

    connection.init()
    connection.connect_to_file(parser.cast_filename())
    logs = connection.download()
    data = parser.sting_to_data(logs)

    st.set_page_config(
        page_title="Real-Time Data Science Dashboard",
        page_icon="✅",
        layout="wide",
    )

    st.title("Real-Time Data Science Dashboard")

    if d_config['dashboard']['call_per_minute']:
        st.header('Application perfomance')
        plot_data = data \
            .assign(**{'group_time': [str(d.hour) + '_' + str(d.minute) for d in data.time]}) \
            .group_time.value_counts() \
            .to_frame() \
            .reset_index() \
            .rename({'index': 'minute', 'group_time': 'number_of_call'})
        st.subheader('Numer of call per _minute_ :blue :clock2:')
        st.line_chart(plot_data, x='index', y='group_time')

    if d_config['dashboard']['call_per_minute']:
        st.subheader('Response _time_ :blue :clock4:')
        st.line_chart(data, x='time', y='response_time')

    if d_config['dashboard']['model_statistics']:
        st.header('model statistics')
        kpis = st.columns(d_config['n_classes'])
        number_of_preds = len(data)

        # fill in those three columns with respective metrics or KPIs
        for i, kpi in enumerate(kpis):
            kpi.metric(label=f"% of {i} class",
                       value=round(len(data.loc[data.pred == i]) / number_of_preds, 3))


if __name__ == '__main__':
    if st.runtime.exists():
        main(config)
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
