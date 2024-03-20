class VirtualComputerEnvironment:
    def __init__(self):
        self.current_directory = "/"
        self.files_in_directory = {"documents": "folder", "example.txt": "file"}
        self.is_file_open = False

    def list_files(self):
        """Lists files in the current directory."""
        for file_name, file_type in self.files_in_directory.items():
            print(f"{file_name} ({file_type})")

    def open_file(self, file_name):
        """Opens a file if it exists."""
        if file_name in self.files_in_directory:
            print(f"Opening {file_name}...")
            self.is_file_open = True
        else:
            print("File not found.")

    def close_file(self):
        """Closes the currently open file."""
        if self.is_file_open:
            print("File closed.")
            self.is_file_open = False
        else:
            print("No file is open.")
