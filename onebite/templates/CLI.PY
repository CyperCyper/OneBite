from utils import initialize_logger
import argparse
import logging


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
    template_command.add_argument("action", choices=["set", "get"], help="Action to perform on template")
    template_command.add_argument("path", nargs="?", help="Path to template file (for 'set' action)")
    logging.info(f"Template command cereated!")

    # Creating create command
    create_command = subcommands.add_parser("create", help="Create new file with extracted function")
    create_command.add_argument("source_file", help="Source file containing the function")
    create_command.add_argument("function_name", help="Name of the function to extract")
    logging.info(f"Create command created!")

    user_comamand_input = command_parser.parse_args()

    if user_comamand_input.command == "template":
        if user_comamand_input.action == "set":
            logging.info(f"Setting template: {user_comamand_input.path}")
            # TODO: Implement set_template function
        elif user_comamand_input.action == "get":
            logging.info("Getting current template")
            # TODO: Implement get_template function
    elif user_comamand_input.command == "create":
        logging.info(f"Creating new file with function {user_comamand_input.function_name} from {user_comamand_input.source_file}")
        # TODO: Implement create_file function

if __name__ == "__main__":
    main()

