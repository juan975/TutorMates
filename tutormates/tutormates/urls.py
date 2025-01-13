
from django.contrib import admin
from django.urls import path, include
from tutoring.views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('account/', include('tutoring.urls'))
]
