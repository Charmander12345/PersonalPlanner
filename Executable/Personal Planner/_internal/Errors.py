class UnknownAccountError(Exception):
    def __init__(self,message = "The account does not exist.") -> None:
        self.message = message
        super().__init__(message)

class AccountsFileNotFoundError(Exception):
    def __init__(self, message="The accounts file does not exist or is damaged.") -> None:
        self.message = message
        super().__init__(message)

class PasswordIncorrectError(Exception):
    def __init__(self, message="The provided password is incorrect.") -> None:
        super().__init__(message)

class AccountAlreadyExistsError(Exception):
    def __init__(self, message="The accounts already exists.") -> None:
        self.message = message
        super().__init__(message)

class AccountDataNotFoundError(Exception):
    def __init__(self, message="The account file cound not be found.") -> None:
        super().__init__(message)