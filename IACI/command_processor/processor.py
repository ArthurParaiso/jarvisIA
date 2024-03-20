# command_processor/processor.py

class CommandProcessor:
    def __init__(self, environment):
        self.environment = environment

    def process_command(self, action):
        """Executes an action in the virtual environment based on the AI's decision."""
        if action == 'list_files':
            self.environment.list_files()
        elif action == 'open_file':
            # This example assumes a specific file to simplify interaction.
            self.environment.open_file('example.txt')
        elif action == 'close_file':
            self.environment.close_file()
        else:
            print("Unknown action. No command executed.")

