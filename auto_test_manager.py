import os
import time



# ------------------------ dictionary -----------------------------------------------------
# path dictionary
dic_path = {
        "all": "pytest -v",
        "tests": "pytest testFolder/ -v",
        "t": "pytest testFolder/test_main_1.py -v",
        "login": "pytest test_login_suite.py -v",
        "teams": "pytest test_teams_page_suite.py -v",
        "exit": "exit"
}

welcome_msg = "--------- Welcome To The Auto-Test Manager -------------"

instructions = [
    "Please Enter Command:",
    "all - run all suites",
    "login - run login suite only",
    "teams - run teams suite",
    "tests - run ALL mini-tests",
    "t - run ONE mini-test",
    "exit - to quit"
]

logger_input_msg = "Do you want to save log? y/n"

#####################################################################################################################


# generates log file name - 'Test type'+'current_time'.txt in 'logs' folder
def get_timestamp_log_file_name(text):
    epochtime = str(time.time())
    filename = epochtime.replace(".","")
    print(filename)
    stamp = text + filename + ".txt"
    txt = ">logs/" + stamp
    return txt


# print instructions
def show_instructions():
    print("---------------------------------------------------------------------------")
    for line in instructions:
        print(line)
    print("---------------------------------------------------------------------------")


# print invalid error
def invalid_command():
    print("***************************************************************************")
    print("Error: must enter valid command")
    print("***************************************************************************")


# main
def run_manager_input():
    print(welcome_msg)
    while True:
        show_instructions()
        # read user input - test type
        text = input("")
        if(len(text) > 0):
            if text in dic_path:
                # find the right command in dictionary
                arg = dic_path[text]
                if(text == "exit"):
                    exit()
            else:
                invalid_command()
                continue
            while True:
                # get user input - save log or not
                print(logger_input_msg)
                log = input("")
                if (log == "y" or log == "n"):
                    break
                else:
                    invalid_command()
            if (log == "y"):
                arg = arg + " " + get_timestamp_log_file_name(text)
            # execute the command
            os.system(arg)
            print("Manager performed - ", arg)
        else:
            invalid_command()


run_manager_input()
