class RealTimeSignalData:
    def __init__(self, _timestamp, _message_id, _signal_name, _signal_value):
        self.timestamp = _timestamp
        self.message_id = _message_id
        self.signal_name = _signal_name
        self.signal_value = _signal_value
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'message_id': self.message_id,
            'signal_name': self.signal_name,
            'signal_value': self.signal_value
        }