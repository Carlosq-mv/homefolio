from fastapi import HTTPException, status

class UserError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "User error"

class UserEmailExists(UserError):
    status_code = status.HTTP_409_CONFLICT
    message = "Email already exists"

class UserUsernameExists(UserError):
    status_code = status.HTTP_409_CONFLICT
    message = "Username already exists"

class UserUsernameAndEmailExists(UserError):
    status_code = status.HTTP_409_CONFLICT
    message = "Both username and email already exist"

class UserDoesNotExist(UserError):
    status_code = status.HTTP_404_NOT_FOUND
    message = "User not found"

class NoUsersExists(UserError):
    status_code = status.HTTP_404_NOT_FOUND
    message = "No users found"