# from django import template

# register = template.Library()

# @register.filter
# def div(value, arg):
#     try:
#         return int(value) // int(arg)
#     except (ValueError, ZeroDivisionError):
#         return 0

# @register.filter
# def modulo(value, arg):
#     try:
#         return int(value) % int(arg)
#     except (ValueError, ZeroDivisionError):
#         return 0
from django import template

register = template.Library()

# @register.filter(name='to_feet')
# def to_feet(value):
#     return value * 3.28084