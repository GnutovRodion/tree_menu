from django.urls import path
from django.contrib import admin
from menu.views import draw_menu

app_name = 'app_menu'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:menu_name>/', draw_menu, name='draw_menu'),
]
