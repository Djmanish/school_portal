from django import template

register = template.Library()

@register.simple_tag
def get_attendance_percentage(total, present):
    percentage = (present*100)/total
    percentage =round(percentage, 2)

    return percentage




