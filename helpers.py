import json
from signalDefinition import SignalDefinition
from messageDefinition import MessageDefinition
from realTimeData import RealTimeData
from realTimeSignalData import RealTimeSignalData

class Helpers:
    message_definitions = [] #definition of CAN message structure (including signals per message) as defined in .dbc file
    rt_data = [] #list of ReatTimeData objects
    rt_signal_data = [] #list of RealTimeSignalData objects
    not_found_message_ids = set() #message ids found in the trace, but not in the message definitions

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
        return hex(dec) #[2:] to remove 0x prefix

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

        cls.message_definitions = list(map(cls.extract_message_definition, data['messages']))

    @classmethod
    def extract_signal_definition(cls, sig):
        signal = SignalDefinition(sig['start_bit'], sig['bit_length'], sig['name'])
        return signal

    @classmethod
    def extract_message_definition(cls, msg):
        message = MessageDefinition(cls.dec_to_hex(msg['id']), msg['name'])
        message.signals = list(map(cls.extract_signal_definition, msg['signals']))
        return message

    """
    Extract real-time data from the trace .asc file
    """
    @classmethod
    def extract_trace_data_from_file(cls, trace_filepath):
        file = open(trace_filepath, "r")
        trace_lines = file.readlines()[3:-1]  # skip the header and the last line

        #TODO: decide which strategy to use: as is, or create a list of RealTimeData objects and return it from here, instead of returning a list of RealTimeSignalData
        """
        data = []
        for trace_line in trace_lines:
            data.append(cls.extract_data_from_trace_lines(trace_line))
        return data
        """
        for trace_line in trace_lines:
            cls.extract_data_from_trace_lines(trace_line) #this call modifies rt_signal_data

        return cls.rt_signal_data

    @classmethod
    def extract_data_from_trace_lines(cls, trace_line):
        data = trace_line.split()
        timestamp = data[0] #message timestamp
        message_id = data[2][:-1]  #message id; remove 'x' in the end
        raw_values = cls.hex_to_binary("".join(data[6:])) #raw bytes containing signal values for this message

        message_definition = cls.get_message_definition_by_id(message_id)

        #check if message_id is found in the message definitions
        if message_definition is None:
            cls.not_found_message_ids.add(message_id)
            return

        #translate the signal values
        cls.translate_raw_signal_values(timestamp, message_id, raw_values, message_definition)

    @classmethod
    def get_message_definition_by_id(cls, _id):
        #_id has no 0x prefix
        for msg in cls.message_definitions:
            if (msg.message_id[2:] == _id):
                return msg

    @classmethod
    def translate_raw_signal_values(cls, timestamp, message_id, raw_values, message_definition):
        rt_data = RealTimeData(timestamp, message_id, raw_values)

        for signal in message_definition.signals:
            bit_value = raw_values[signal.start_bit : signal.start_bit + signal.bit_length]
            signal_data = RealTimeSignalData(timestamp, message_id, signal.name, cls.binary_to_dec(bit_value))

            #update the RealTimeData object by adding the signal value
            rt_data.rt_signal_data.append(signal_data)

            # besides RealTimeData object, create RealTimeSignalData object
            # TODO: figure out if RealTimeSignalData is created here, or when only requested by modifying the RealTimeData object
            # TODO: consider if a RealTimeData object is needed to access the raw_values
            cls.rt_signal_data.append(signal_data)

        #update the list of RealTimeData objects
        cls.rt_data.append(rt_data)