from template_manager import set_template, get_current_template, template_manager_ui
from utils import console_output, logging


def handle_template_set(args):
    if args.path:
        logging.info(f"Setting template: {args.path}")
        set_template(args.path)
    else:
        console_output("Error: Path to template file is required for 'set' action.", 'error')

def handle_template_get(args):
    current_template = get_current_template()
    console_output(f"Current template: {current_template or 'Not set'}")

def handle_template_manage(args):
    template_manager_ui()

def handle_create(args):
    logging.info(f"Creating new file with function {args.function_name} from {args.source_file}")
    # TODO: Implement create_file function


def handle_template(args):
    template_actions = {
        'set': handle_template_set,
        'get': handle_template_get,
        'manage': handle_template_manage
    }
    action_handler = template_actions.get(args.action)
    if action_handler:
        action_handler(args)
    else:
        console_output(f"Unknown template action: {args.action}", 'error')
