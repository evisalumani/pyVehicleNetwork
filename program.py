import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from helpers import Helpers
import itertools

class Program:
    def __init__(self, _msg_id, _sig_name, _dbc_filepath, _trace_filepath):
        self.msg_id = _msg_id
        self.sig_name = _sig_name
        self.dbc_filepath = _dbc_filepath
        self.trace_filepath = _trace_filepath
        self.rt_signal_data = []
        self.message_definitions = []
        self.startup()

    def startup(self):
        Helpers.extract_message_and_signal_definition_from_dbc_file(self.dbc_filepath)
        self.message_definitions = Helpers.message_definitions
        self.rt_signal_data = Helpers.extract_trace_data_from_file(self.trace_filepath)

    def filter_by_msgid_signalname(self, x):
        return x.message_id == self.msg_id and x.signal_name == self.sig_name

    def filter(self):
        return list(filter(self.filter_by_msgid_signalname, self.rt_signal_data))

    def map_timestamp(self, x):
        return x.timestamp

    def map_signal_value(self, x):
        return x.signal_value

    def key_signal_name(self, rt_signal_data):
        return rt_signal_data.signal_name

    def group_messages_by_signal_name(self, message_id):
        #filter by message id; remove 0x prefix
        filtered_rt_signal_data = list(filter(lambda rt: rt.message_id == message_id, self.rt_signal_data))

        print('#filtered signals', len(filtered_rt_signal_data))

        #the key to group by is signal_name
        #group by signal name
        groups = []
        uniquekeys = []

        sorted_rt_signal_data = sorted(filtered_rt_signal_data, key=self.key_signal_name)
        for k, g in itertools.groupby(sorted_rt_signal_data, key=self.key_signal_name):
            groups.append(list(g))  # Store group iterator as a list
            uniquekeys.append(k)

        #Plotting directly from inside the above loop doesn't work due to lazy evaluation
        #plot signal
        for i in range(0, len(uniquekeys)):
            self.plot_signal_values(uniquekeys[i], groups[i])

    def plot_signal_values(self, signal_name, signal_values):
        #TODO: is sorting by timestamp needed?
        x_values = np.array(list(map(self.map_timestamp, signal_values)))
        y_values = np.array(list(map(self.map_signal_value, signal_values)))

        #display for testing purposes
        print(signal_name)
        print("X-values")
        print(x_values[0:10])

        print("Y-values")
        print(y_values[0:10])

        plt.figure()
        plt.cla()  # ?

        plt.plot(x_values, y_values, label=signal_name)
        plt.xlabel("timestamp")
        plt.ylabel("signal value")
        plt.legend(loc=1)
        plt.show()

    # Plotting the signal which is provided with the Program object
    def plot(self):
        self.plot_signal_values('Test signal', self.filter())
        
    def get_dataframe_from_signal_data(self):
        return pd.DataFrame([s.to_dict() for s in self.rt_signal_data])

    def get_message_defitions_dict_for_widget(self):
        return {msg.name: msg.message_id for msg in self.message_definitions}