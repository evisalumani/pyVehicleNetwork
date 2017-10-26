#import program as Program
from program import Program
from helpers import Helpers

def main():
    print("Hello World")
    #msg_id, sig_name
    program = Program('c000003', 'TSC1EMSTECU_EngReqTrq_HR')

    Helpers.get_message_and_signal_definition_from_file()
    Helpers.extract_all_messages()
    Helpers.extract_traces_from_file()

    program.plot()

if __name__ == "__main__":
    main()