import csv
import logging
import os

def get_logger_path():
    log_file_name = f"onebite_log.csv"
    this_app_catalog = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(this_app_catalog, log_file_name)

    return log_file_path

def setup_logger(level='debug'):
    log_file_path = get_logger_path()
    print(f"Log file path: {log_file_path}")
    logging.basicConfig(level=level.upper(),
                        format='%(asctime)s,%(levelname)s,%(name)s,%(funcName)s,%(message)s,%(pathname)s:%(lineno)d',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(log_file_path, mode='a', encoding='utf-8')])
    return

def initialize_logger(level='debug', program_name='onebite'):

    log_file_path = get_logger_path()

    # Overwriting log file and adding headers to the CSV file
    with open(log_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["Timestamp", "Level", "Module", "Function", "Message", "Path:Line"])
    
    setup_logger()
    # First log entries
    logging.info(f"Program {program_name} started!")
    logging.info(f"Log file configuration completed successfully. Logger level {level}.")
    logging.info(f"Log file path:{log_file_path}")
    
    return log_file_path

def console_output(message, level='info'):
    """
    Logs a message and prints it to the console.
    
    Args:
        message (str): The message to log and print.
        level (str): The logging level ('debug', 'info', 'warning', 'error', 'critical').
    """
    log_levels = {
        'debug': logging.debug,
        'info': logging.info,
        'warning': logging.warning,
        'error': logging.error,
        'critical': logging.critical
    }
    log_message = message.replace(',',';')
    log_func = log_levels.get(level.lower(), logging.info)
    log_func(log_message)
    print(f"{message}")
    print()

def get_user_input(prompt, log_message=None):
    """
    Gets user input and logs it.
    
    Args:
        prompt (str): The prompt to display to the user.
        log_message (str, optional): A custom log message. If None, the prompt is used.
    
    Returns:
        str: The user's input.
    """
    user_input = str(input(prompt))
    if log_message is None:
        log_message = f"User input for '{prompt}': {user_input}"
    logging.info(log_message)
    return user_input

def get_menu_input(prompt, log_message=None):
    """
    Gets user input for manu choice and logs it.
    Input is raised to upper case.
    
    Args:
        prompt (str): The prompt to display to the user.
        log_message (str, optional): A custom log message. If None, the prompt is used.
    
    Returns:
        str: The user's input.
    """
    user_input = str(input(prompt)).upper()
    if log_message is None:
        log_message = (f"User input for '{prompt}': {user_input}").replace(',',';')
    logging.info(log_message)
    return user_input

def menu_heading(menu_title):
        width = 100
        border_symbol = '-'

        print("\n" + border_symbol * width)
        print(f"{menu_title}")
        print(border_symbol * width)

def generate_options_string(options):
        if isinstance(options, dict):
            return ','.join(f"[{key}]" for key in options.keys())
        elif isinstance(options, list):
            return ','.join(f"[{i+1}]" for i in range(len(options)))
        else:
            return str(options)

def menu_display(menu_title, menu_actions):
     menu_heading(menu_title)
     for key, (description, _) in menu_actions.items():
          print((f"[{key}] to {description}"))
     print()

def exit_menu_action(message):
        console_output(f"{message}")
        return True     


# if __name__ == "__main__":
#     setup_logger()
#     logging.debug(f"Logger working for utils.py")
    
# #    choice = get_user_input("Enter yout choice: ")
#     console_output(f"Test konsoli ,,,,;;;;")

















