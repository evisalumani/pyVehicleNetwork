import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import functools
from helpers import Helpers

class Program:
    def __init__(self, _msg_id, _sig_name, _dbc_filepath, _trace_filepath):
        print("Program Class")
        self.msg_id = _msg_id
        self.sig_name = _sig_name
        self.dbc_filepath = _dbc_filepath
        self.trace_filepath = _trace_filepath
        self.rt_signal_data = []
        self.startup()

    def startup(self):
        Helpers.extract_message_and_signal_definition_from_dbc_file(self.dbc_filepath)
        self.rt_signal_data = Helpers.extract_trace_data_from_file(self.trace_filepath)

    def filter_by_msgid_signalname(self, x):
        return x.message_id == self.msg_id and x.signal_name == self.sig_name

    def filter(self):
        return list(filter(self.filter_by_msgid_signalname, self.rt_signal_data))

    def map_timestamp(self, x):
        return x.timestamp

    def map_signal_value(self, x):
        return x.signal_value

    # Plotting
    def plot(self):
        filtered_signals = self.filter() #filtered signals

        x_values = np.array(list(map(self.map_timestamp, filtered_signals)))
        y_values = np.array(list(map(self.map_signal_value, filtered_signals)))

        print("X-values")
        print(x_values[0:10])

        print("Y-values")
        print(y_values[0:10])

        plt.figure()
        plt.cla()  # ?

        plt.plot(x_values, y_values, label="Signal")
        plt.xlabel("timestamp")
        plt.ylabel("signal value")
        plt.legend(loc=1)
        plt.show()
        
    def get_dataframe_from_signal_data(self):
        list_signal_values = self.get_reduced_list_of_signal_data()
        return pd.DataFrame([s.to_dict() for s in list_signal_values])

    def get_reduced_list_of_signal_data(self):
        #TODO: takes too long if only self.rt_signal_data is considered
        test = [sig_data.do_magic() for sig_data in self.rt_signal_data[0:5]]
        test_reduced = functools.reduce(list.__add__, test)
        return test_reduced