class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FileList(metaclass=Singleton):
    def __init__(self):
        self._saved_files = []

    @property
    def saved_files(self):
        return self._saved_files

    def append_to_list(self, file_path):
        self._saved_files.append(file_path)
        print(self._saved_files)

