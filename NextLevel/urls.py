
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Misiones.views import home_redirect
from django.views.generic import TemplateView
urlpatterns = [
    path('', home_redirect),
    path('', include('Misiones.urls')),
    path('admin/', admin.site.urls),

     # URL para el Service Worker
    path('sw.js',TemplateView.as_view(template_name='sw.js', content_type='application/javascript'),name='sw.js'),
    path('manifest.json',TemplateView.as_view(template_name='manifest.json', content_type='application/json'),name='manifest.json'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)