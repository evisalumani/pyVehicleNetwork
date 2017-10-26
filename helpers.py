import json
# import signal as Signal
# import message as Message
# import realTimeData as RealTimeData
from signal import Signal
from message import Message
from realTimeData import RealTimeData

class Helpers:
    messages = []
    can_messages = []
    traces = []
    rt_signal_data = []

    @classmethod
    def hex_to_dec(cls, hex):
        return int(hex, 16)

    @classmethod
    def dec_to_hex(cls, dec):
        return hex(dec)[2:]  # remove 0x prefix

    @classmethod
    def get_message_and_signal_definition(cls):
        with open('data/convereted_dbc_to_json.json') as data_file:
            data = json.load(data_file)

        cls.messages = data['messages']

    @classmethod
    def extract_signal(cls, sig):
        signal = Signal(sig['start_bit'], sig['bit_length'], sig['name'])
        return signal

    @classmethod
    def extract_message(cls, msg):
        message = Message(Helpers.dec_to_hex(msg['id']), msg['name'])
        message.signals = list(map(Helpers.extract_signal, msg['signals']))
        return message

    @classmethod
    def extract_all_messages(cls):
        cls.can_messages = list(map(Helpers.extract_message, cls.messages))

    @classmethod
    def extract_traces_from_file(cls):
        file = open("data/trace.asc", "r")
        trace_lines = file.readlines()[3:-1]  # skip the header
        # print(trace_lines[0].split()) #Index #2 (message_id; remove x in the end); #6-13 (data bytes)

        for trace_line in trace_lines:
            cls.traces.append(Helpers.extract_data_from_trace(trace_line))

    @classmethod
    def extract_data_from_trace(cls, trace_line):
        data = trace_line.split()
        timestamp = data[0]
        message_id = data[2][:-1]  # remove 'x' in the end
        values = Helpers.hex_to_binary("".join(data[6:]))

        rtdata = RealTimeData(timestamp, message_id, values)
        return rtdata

    @classmethod
    def hex_to_binary(cls, hex_data):
        h_size = len(hex_data) * 4
        bin_data = (bin(int(hex_data, 16))[2:]).zfill(h_size)
        return bin_data

    @classmethod
    def get_can_message_by_id(cls, _id):
        for msg in cls.can_messages:
            if (msg.message_id == _id):
                return msg