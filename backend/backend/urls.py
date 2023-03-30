from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

admin.site.site_header = 'Администрирование проекта Foodgram'
admin.site.index_title = 'Меню'
admin.site.site_title = 'Администрирование проекта Foodgram'
