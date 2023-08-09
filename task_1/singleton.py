class Singleton:
    connection_string: str

    def __init__(self, cls):
        self._cls = cls

    def Instance(self, connection_string: str):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls(connection_string)
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `Instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)
