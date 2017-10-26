# import helpers as Helpers
# import realTimeSignalData as RealTimeSignalData
from helpers import Helpers
from realTimeSignalData import RealTimeSignalData

class RealTimeData:
    def __init__(self, _timestamp, _message_id, _raw_values):
        self.timestamp = _timestamp
        self.message_id = _message_id
        self.raw_values = _raw_values
        self.translated_values = []
        self.translate_raw_values()

    def translate_raw_values(self):
        message = Helpers.get_can_message_by_id(self.message_id)
        # TODO: where to check for the message id, here or in the constructor?
        if message is None:
            return

        for signal in message.signals:
            bit_value = self.raw_values[signal.start_bit : signal.start_bit + signal.bit_length]
            #print('bit value:', bit_value)
            self.translated_values.append({'timestamp': self.timestamp, 'signal_name': signal.name, 'signal_value': int(bit_value, 2)})
            Helpers.rt_signal_data.append(RealTimeSignalData(self.timestamp, self.message_id, signal.name, int(bit_value, 2)))