from program import Program

def main():
    print("Start")
    #The first 2 parameters are msg_id, sig_name by which to filter the display of real-time data
    #The next 2 params are the paths of the file containing the dbc definition file (in json) and the data trace
    program = Program('c000003', 'TSC1EMSTECU_EngReqTrq_HR', 'data/convereted_dbc_to_json.json', "data/trace.asc")

    #program.plot()
    program.get_reduced_list_of_signal_data()

if __name__ == "__main__":
    main()