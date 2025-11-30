from fastapi import HTTPException, status

"""
Custom Users Exceptions
"""
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

class UserInvalidCredentials(UserError):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid email or password"

"""
Custom JWT Exceptions
"""
class JwtError(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "JWT error"

class JwtRefreshTokenNotFound(JwtError):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Refresh token is missing"

class JwtRefreshTokenExpired(JwtError):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Refresh token has expired"

class JwtRefreshTokenInvalid(JwtError):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid refresh token"
    
class JwtRefreshTokenRevoked(JwtError):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Refresh token has been revoked"

class JwtRefreshTokenCompromised(JwtError):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Refresh token has been compromised"

class JwtInvalidAccessToken(JwtError):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Invalid access token"

class JwtAccessTokenExpired(JwtError):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Access token has expired"
