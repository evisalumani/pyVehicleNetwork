import matplotlib.pyplot as plt
import numpy as np

class Program:
    def __init__(self, _msg_id, _sig_name):
        print("Program Class")
        self.msg_id = _msg_id
        self.sig_name = _sig_name
        self.rt_signal_data = []

    def filter_by_msgid_signalname(self, x):
        return x.message_id == self.msg_id and x.signal_name == self.sig_name

    def filter(self):
        return list(filter(self.filter_by_msgid_signalname, self.rt_signal_data))

    #Plotting
    map_timestamp = lambda x: x.timestamp
    map_signal_value = lambda x: x.signal_value

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