from django import template

register = template.Library()

@register.filter
def filter_user(comments, user):
    return comments.filter(author=user)


@register.filter
def done_check(num):
    if num == 0:
        return "not done"
    else:
        return "done"

@register.filter
def finish_check(tf):
    if tf:
        return "마감"
    else:
        return "진행중"
