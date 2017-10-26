class RealTimeSignalData:
    def __init__(self, _timestamp, _message_id, _signal_name, _signal_value):
        self.timestamp = _timestamp
        self.message_id = _message_id
        self.signal_name = _signal_name
        self.signal_value = _signal_value