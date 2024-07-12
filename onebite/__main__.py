
import logging
from template_manager import template_manager_ui, set_template, get_current_template
from utils import exit_menu_action, generate_options_string, initialize_logger, console_output, get_menu_input, menu_display
import argparse

def main():
    initialize_logger()
    logging.info("Main function started")
    command_parser = argparse.ArgumentParser(
        description="One Bite - Function extraction and template management tool",
        epilog="For more information, see README.md or visit: https://github.com/CyperCyper/OneBite \n")
    subcommands = command_parser.add_subparsers(dest="command", help="Available commands")
    logging.info(f"Parser configuration completed!")

    # Creating template command
    template_command = subcommands.add_parser("template", help="Manage templates")
    template_command.add_argument("action", choices=["set", "get", "manage"], help="Action to perform on template")
    template_command.add_argument("path", nargs="?", help="Path to template file (for 'set' action)")
    logging.info(f"Template command created!")

    # Creating create command
    create_command = subcommands.add_parser("create", help="Create new file with extracted function")
    create_command.add_argument("source_file", help="Source file containing the function")
    create_command.add_argument("function_name", help="Name of the function to extract")
    logging.info(f"Create command created!")

    user_command_input = command_parser.parse_args()

    if user_command_input.command == "template":
        if user_command_input.action == "set":
            if user_command_input.path:
                logging.info(f"Setting template: {user_command_input.path}")
                set_template(user_command_input.path)
            else:
                console_output("Error: Path to template file is required for 'set' action.", 'error')
        elif user_command_input.action == "get":
            current_template = get_current_template()
            console_output(f"Current template: {current_template or 'Not set'}")
        elif user_command_input.action == "manage":
            template_manager_ui()
    elif user_command_input.command == "create":
        logging.info(f"Creating new file with function {user_command_input.function_name} from {user_command_input.source_file}")
        # TODO: Implement create_file function
    else:
        # If no command is provided, run the interactive menu
        main_menu()

def main_menu():

    def create_file_action():
        console_output("Create file functionality not implemented yet.", 'warning')
    

    menu_actions = {
        'T': ("Template management", template_manager_ui),
        'C': ("Create new file", create_file_action),
        'E': ("Exit", lambda: exit_menu_action("Exiting One Bite. Goodbye!"))
    } 

    menu_options = generate_options_string(menu_actions)

    while True:
        menu_display("One Bite - Main Menu", menu_actions)
        
        choice = get_menu_input(f'Press key from {menu_options}: ')
        action = menu_actions.get(choice)

        if action:
            description, func = action
            result = func()  
            if result is True:
                break
        else:
            console_output(f"Option {choice} does not exist. Please try again.",'warning')

if __name__ == "__main__":
    main()