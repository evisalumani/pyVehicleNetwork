class RealTimeData:
    def __init__(self, _timestamp, _message_id, _raw_values):
        self.timestamp = _timestamp
        self.message_id = _message_id
        self.raw_values = _raw_values
        self.rt_signal_data = []