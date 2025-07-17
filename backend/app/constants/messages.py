class Registration:
    SUCCESS = (
        "Registration successful! Check your inbox for an email validation message."
    )
    FAILURE = "Registration failed. Please try again."
    DUPE_USER = "Username or email already exists"


class Errors:
    GENERIC = "Something went wrong"
    BAD_TOKEN = "Token is expired or was never recorded."
    DBCOMMIT = "Database commit failure!"


class Verification:
    SENT = "Verification email sent. Please check your inbox."
    ALREADY_VERIFIED = "Your email address is already verified."
    INVALID_OR_EXPIRED = "This verification link is invalid or has expired."
    SUCCESS = "Your email has been successfully verified."


class Resend:
    RATE_LIMITED = "You’ve recently requested a verification email. Please wait before trying again."
    NOT_ELIGIBLE = "We couldn’t resend a verification email for this account."
    SUCCESS = "A new verification email has been sent."


class Auth:
    INVALID_CREDENTIALS = "Incorrect username or password."
    INACTIVE_ACCOUNT = "Your account is not active yet. Please verify your email."
    LOGIN_SUCCESS = "Welcome back!"
