from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def userlinks_list(request, user):
    """
    Include navbar menu list items.
    """
    items = []

    # Set title and login/logout link
    if not user.is_authenticated:
        title = "Not logged in"
        loginout_item = userlinks_login(request)
    else:
        title = user.pretty_username
        loginout_item = userlinks_logout(request)
    if loginout_item:
        items.append(loginout_item)

    extra_items = userlinks_extras(request, user)
    if extra_items and len(extra_items) > 0:
        items += extra_items

    if len(items) == 0:
        return ""

    content = """
        <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                {title}
                <b class="caret"></b>
            </a>
            <ul class="dropdown-menu">
        """
    content = format_html(content, title=escape(title))
    for item in items:
        content += item + "\n"
    content += """
            </ul>
        </li>
    """

    return mark_safe(content)  # noqa: S703, S308 (potential XSS)


def userlinks_login(request):
    try:
        login_url = reverse("rest_framework:login")
        item = '<li><a href="{href}?next={next}">Log in</a></li>'
        return format_html(item, href=login_url, next=escape(request.path))
    except NoReverseMatch:
        pass


def userlinks_logout(request):
    try:
        logout_url = reverse("rest_framework:logout")
        item = '<li><a href="{href}?next={next}">Log out</a></li>'
        return format_html(item, href=logout_url, next=escape(request.path))
    except NoReverseMatch:
        pass


def userlinks_extras(request, user):
    items = []

    items.append('<li><a href="/schema">Schema</a></li>')

    if user.is_staff:
        items.append('<li><a href="/admin">Admin panel</a></li>')

    return items
