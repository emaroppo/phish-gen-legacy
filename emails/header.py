class EMailHeader:
    def __init__(
        self,
        **kwargs,
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Header: {self.__dict__}"
