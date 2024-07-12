import json
import logging
from utils import exit_menu_action, setup_logger, console_output, get_menu_input, get_user_input, generate_options_string, menu_display
import os
import shutil

# Ścieżka do katalogu z szablonami
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
# Ścieżka do pliku konfiguracyjnego
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config', 'template_config.json')


# Basic
def ensure_templates_dir():
    """Ensure templates dir exists"""
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)
        logging.info(f"Created templates directory: {TEMPLATES_DIR}")

def load_config():
    """Loading templates configuration."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)
    logging.info(f"Loaded templates configuration from {CONFIG_FILE}")
    return {"current_template": None}

def save_config(config):
    """ templates configuration."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file)
    logging.info(f"Saved templates configuration in {config_file}")

def set_template(template_name):
    """Set current template."""
    ensure_templates_dir()
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        logging.error(f"Template {template_name} does not exist.")
        return False
    
    config = load_config()
    config["current_template"] = template_name
    save_config(config)
    logging.info(f"Set current template to: {template_name}")
    return True

def get_current_template():
    """Retrieves the name of the currently set template."""
    config = load_config()
    current_template = config.get("current_template")
    if current_template:
        logging.info(f"Current template: {current_template}")
    else:
        logging.info("No template currently set.")
    return current_template

def list_templates():
    """Zwraca listę dostępnych szablonów."""
    ensure_templates_dir()
    templates = [templates for templates in os.listdir(TEMPLATES_DIR) if templates.endswith('.py')]
    logging.info(f"Znaleziono {len(templates)} szablonów.")
    return templates

def add_template(template_name, content):
    """Dodaje nowy szablon."""
    # TODO - Zabespieczyć funckję przed naspisaniem bez zgody użytkownika
    ensure_templates_dir()
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if os.path.exists(template_path):
        logging.warning(f"Template {template_name} already exists. Overwriting.")
    
    with open(template_path, 'w') as template_file:
        template_file.write(content)
    logging.info(f"Added new template: {template_name}")
    return True

def remove_template(template_name):
    """Usuwa istniejący szablon."""
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        logging.error(f"Template {template_name} does not exist.")
        return False
    
    os.remove(template_path)
    logging.info(f"Removed template: {template_name}")
    
    # If deleted template was currently set, we reset configuration
    config = load_config()
    if config.get("current_template") == template_name:
        config["current_template"] = None
        save_config(config)
        logging.info("Reset current template setting.")
    
    return True

def functions_test():
    if __name__ == "__main__":

        print(f"{os.path.basename(__file__)}.py working! ")
        logging.debug(f"{os.path.basename(__file__)}.py working! ")
        logging.debug(f"Logger working for template_manager.py")

        print("Dostępne szablony:", list_templates())
        
        add_template("example_template.py", "# To jest przykładowy szablon\n\ndef example_function():\n    pass")
        print("Dostępne szablony po dodaniu:", list_templates())
        
        set_template("example_template.py")
        print("Aktualny szablon:", get_current_template())
        
        remove_template("example_template.py")
        print("Dostępne szablony po usunięciu:", list_templates())

def template_manager_ui():

    def display_available_templates(templates):
            print()
            current_template = get_current_template()
            print("Available templates:")
            for i, template in enumerate(templates, 1):
                print(f"{i}. {template}")
            print(f"Current template: {current_template}")
            print()

    def is_valid_template_choice(choice, num_templates):
            return choice.isdigit() and 1 <= int(choice) <= num_templates

    def list_templates_action():
        templates = list_templates()
        if templates:
            display_available_templates(templates)
            
            logging.info(f"Listed {len(templates)} templates")
        else:
            console_output("No templates available.")
            
        logging.info("Entered template management interface") 
  
    def set_current_template_action():

        templates = list_templates()
        if not templates:
            console_output("No templates available to set.")
            return

        display_available_templates(templates)
        sub_menu_options = generate_options_string(templates)
        template_choice = get_menu_input(f"Choose template number from {sub_menu_options}: ")
        
        if not is_valid_template_choice(template_choice, len(templates)):
            console_output(f"Invalid template choice: {template_choice}")
            return

        selected_template = templates[int(template_choice) - 1]
        if set_template(selected_template):
            console_output(f"Successfully set template to: {template_choice}. {selected_template}")
        else:
            console_output("Failed to set template.", 'error')

    def add_new_template_action():
        template_path = get_user_input("Enter the path to the file you want to use as a template: ")
        
        if not os.path.exists(template_path):
            console_output(f"File not found: {template_path}", "error")
            return

        if not template_path.endswith('.py'):
            console_output("Warning: The file does not have a .py extension. It may not be a Python file.", "warning")
        
        template_name = os.path.basename(template_path)
        destination_path = os.path.join(TEMPLATES_DIR, template_name)
        logging.debug(f"Destination_path : {destination_path}")

        try:
            shutil.copy2(template_path, destination_path)
            console_output(f"Successfully added template: {template_name}")
        except Exception as e:
            console_output(f"Failed to add template: {str(e)}", "error")

    def remove_template_action():
        templates = list_templates()
        if not templates:
            console_output("No templates available to remove.")
            return

        display_available_templates(templates)
        sub_menu_options = generate_options_string(templates)
        template_choice = get_menu_input(f"Choose template number to remove from {sub_menu_options}: ")
        
        if not is_valid_template_choice(template_choice, len(templates)):
            console_output(f"Invalid template choice: {template_choice}")
            return

        template_to_remove = templates[int(template_choice) - 1]
        if remove_template(template_to_remove):
            console_output(f"Successfully removed template: {template_choice}. {template_to_remove}")
        else:
            console_output("Failed to remove template.", 'error')

    
    
    
    # Order of setting templates_numer, current_template, template_manager_actions,menu_options matter!
    templates_numer = len(list_templates())
    current_template = get_current_template()

    template_manager_actions = {
    'L': (f"List templates | {templates_numer} ", list_templates_action),
    'S': (f"Set current template | {current_template or 'Not set'}", set_current_template_action),
    'A': ("Add new template", add_new_template_action),
    'R': ("Remove template", remove_template_action),
    'E': ("Exit", lambda: exit_menu_action("Exiting Template Manager. Goodbye!"))
    }

    menu_options = generate_options_string(template_manager_actions)

    menu_display('Template Manager', template_manager_actions)
    while True:
        choice = get_menu_input(f'Press key from {menu_options}: ')
        action = template_manager_actions.get(choice)

        if action:
            description, func = action
            result = func()  
            if result is True:
                break
        else:
            console_output(f"Option {choice} does not exist. Please try again.",'warning')

if __name__ == "__main__":
    setup_logger()
    logging.debug(f"Logger working for template_manager.py")
    template_manager_ui()








































































