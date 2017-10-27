from realTimeSignalData import RealTimeSignalData
import functools

class RealTimeData:
    def __init__(self, _timestamp, _message_id, _raw_values):
        self.timestamp = _timestamp
        self.message_id = _message_id
        self.raw_values = _raw_values
        self.rt_signal_data = [] #list of RealTimeSignalData objects

    def map_to_timestamp_message_id(self):
        return {"timestamp": self.timestamp, "message_id": self.message_id}

    def map_to_separate_signal_per_message(self, signal):
        return RealTimeSignalData(self.timestamp, self.message_id, signal["signal_name"], signal["signal_value"])

    def map_to_signal_data(self, sig_datum):
        return {"signal_name": sig_datum.signal_name, "signal_value": sig_datum.signal_value}

    def magic(self, signal_data):
        signal_values = [self.map_to_signal_data(sig_datum) for sig_datum in signal_data]
        return [self.map_to_separate_signal_per_message(sig) for sig in signal_values]

    def get_reduced_list_of_signal_data(self):
        test = list(map(self.magic, self.rt_signal_data))
        #test = self.magic()
        print(test[0])
        # test_reduced = functools.reduce(list.__add__, test)
        # print[test_reduced[0]]
        # return test_reduced