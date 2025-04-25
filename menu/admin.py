from django.contrib import admin

from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_editable = ('name',)
    ordering = ('name',)
    search_fields = ('name__icontains',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'menu')
    list_filter = ('menu',)
    search_fields = (
        'title__icontains',
        'parent__name_icontains',
        'menu__name__icontains'
    )
