class FileOperator:

    def __init__(self, filepath, mode):
        self.filepath = filepath
        self.file = None
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()
