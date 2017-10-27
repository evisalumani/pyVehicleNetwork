import json
from signalDefinition import SignalDefinition
from message import Message
from realTimeData import RealTimeData
from realTimeSignalData import RealTimeSignalData

class Helpers:
    message_definitions = [] #definition of CAN message structure (including signals per message) as defined in .dbc file
    rt_signal_data = [] #TODO: remove this, just make use of array of RealTimeData objects

    """
    Conversion methods
    """
    @classmethod
    def hex_to_dec(cls, hex):
        return int(hex, 16)

    @classmethod
    def binary_to_dec(cls, binary_value):
        return int(binary_value, 2)

    @classmethod
    def dec_to_hex(cls, dec):
        return hex(dec)[2:]  # remove 0x prefix

    @classmethod
    def hex_to_binary(cls, hex_data):
        h_size = len(hex_data) * 4
        bin_data = (bin(int(hex_data, 16))[2:]).zfill(h_size)
        return bin_data

    """
    From dbc file (converted to json) extract CAN message definitions and the corresponding singal definitions for each message
    """
    @classmethod
    def extract_message_and_signal_definition_from_dbc_file(cls, dbc_filepath):
        with open(dbc_filepath) as data_file:
            data = json.load(data_file)

        cls.message_definitions = list(map(Helpers.extract_message_definition, data['messages']))

    @classmethod
    def extract_signal_definition(cls, sig):
        signal = SignalDefinition(sig['start_bit'], sig['bit_length'], sig['name'])
        return signal

    @classmethod
    def extract_message_definition(cls, msg):
        message = Message(Helpers.dec_to_hex(msg['id']), msg['name'])
        message.signals = list(map(Helpers.extract_signal_definition, msg['signals']))
        return message

    """
    Extract real-time data from the trace .asc file
    """
    @classmethod
    def extract_trace_data_from_file(cls, trace_filepath):
        file = open(trace_filepath, "r")
        trace_lines = file.readlines()[3:-1]  # skip the header and the last line
        # print(trace_lines[0].split()) #Index #2 (message_id; remove x in the end); #6-13 (data bytes)

        #TODO: create a list of RealTimeData objects and return it from here, instead of returning a list of RealTimeSignalData
        """
        toreturn = []
        for trace_line in trace_lines:
            toreturn.append(Helpers.extract_data_from_trace_lines(trace_line))
        return toreturn
        """
        for trace_line in trace_lines:
            Helpers.extract_data_from_trace_lines(trace_line)

        return cls.rt_signal_data

    @classmethod
    def extract_data_from_trace_lines(cls, trace_line):
        data = trace_line.split()
        timestamp = data[0] #message timestamp
        message_id = data[2][:-1]  #message id; remove 'x' in the end
        raw_values = Helpers.hex_to_binary("".join(data[6:])) #raw bytes containing signal values for this message

        message_definition = cls.get_message_definition_by_id(message_id)

        #TODO: where to check for the message id, here or in the RealTimeData constructor?
        if message_definition is None:
            return

        rtdata = RealTimeData(timestamp, message_id, raw_values)
        #translate the signal values
        rtdata.rt_signal_data = cls.translate_raw_signal_values(timestamp, message_id, raw_values, message_definition)
        return rtdata


    @classmethod
    def get_message_definition_by_id(cls, _id):
        for msg in cls.message_definitions:
            if (msg.message_id == _id):
                return msg

    @classmethod
    def translate_raw_signal_values(cls, timestamp, message_id, raw_values, message_definition):
        rt_signal_data = []
        for signal in message_definition.signals:
            bit_value = raw_values[signal.start_bit : signal.start_bit + signal.bit_length]
            #rtdata.translated_values.append({'timestamp': rtdata.timestamp, 'signal_name': signal.name, 'signal_value': cls.binary_to_dec(bit_value)})
            cls.rt_signal_data.append(RealTimeSignalData(timestamp, message_id, signal.name, cls.binary_to_dec(bit_value)))
            rt_signal_data.append(RealTimeSignalData(timestamp, message_id, signal.name, cls.binary_to_dec(bit_value)))

        return rt_signal_data