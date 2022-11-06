from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="range")
def filter_range(start, end):
    try:
        return range(start, end)
    except:
        return []


@register.filter(name="pretty_time")
def filter_pretty_time(value):
    try:
        hours = value // 60
        minutes = value % 60
        result = ""
        if hours != 0:
            result += str(hours) + "h "
        if minutes != 0:
            result += str(minutes) + "min"
        return result
    except:
        return ""


@register.filter(name="pretty_profit")
def filter_pretty_profit(value):
    try:
        """
        millions = value / 1000000
        if millions > 0:
            return "$" + "{:.2f}".format(millions) + " millions"
        else:
            return "$" + str(value)
        """
        return "${:,.2f}".format(value)
    except:
        return ""
