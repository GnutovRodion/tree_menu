from django import template

from menu.models import MenuItem


register = template.Library()

@register.simple_tag
def draw_menu(menu_name):
    menu_items = MenuItem.objects.filter(
        title=menu_name
    ).select_related('parent').order_by('order')
    html = '<ul>'
    for item in menu_items:
        html += render_menu_item(item, menu_name)
    html += '</ul>'
    return html


def render_menu_item(item, menu_name):
    html = f'<li><a href="{item.get_absolute_url()}">{item.name}</a>'
    if item.children.exists():
        html += '<ul>'
        for child in item.children.all().order_by('order'):
            html += render_menu_item(child, menu_name)
        html += '</ul>'
    html += '</li>'
    return html
