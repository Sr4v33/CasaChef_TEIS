class UserDomainError(Exception):
    """Base exception for user domain."""
    pass


class UserNotFoundError(UserDomainError):

    """Exception raised when a user is not found."""
    pass


class UserAlreadyExistsError(UserDomainError):
    """Exception raised when trying to create a user that already exists."""
    pass


class InvalidEmailError(UserDomainError):
    """Exception raised when email format is invalid."""
    pass


class InvalidPasswordError(UserDomainError):
    """Exception raised when password doesn't meet requirements."""
    pass


class AuthenticationError(UserDomainError):
    """Exception raised when authentication fails."""
    pass


class AuthorizationError(UserDomainError):
    """Exception raised when user lacks required permissions."""
    pass


class UserValidationError(UserDomainError):
    """Exception raised when user data validation fails."""
    pass


class UserDeleteError(UserDomainError):
    """Exception raised when user deletion fails."""
    pass
