from functools import wraps
from todo_app.models import User


# def requires_auth(session=None):
#     """Auth handler"""
#     def is_logged_in_wrapper(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             """
#             Ensures a user is logged in or returns error

#             Parameterss:
#                 session(dict):
#                     - flask session object

#             returns
#                 id(str):
#                     - logged in users id
#             """
#             user = session.get("user")

#             if not user:
#                 raise CustomError("Unauthorized", 401, "You are not logged in")
#             user_id = user.get("id")
#             return f(user_id, *args, **kwargs)

#         return wrapper

#     return is_logged_in_wrapper
