from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inmuebles/', views.lista_inmuebles, name='lista_inmuebles'),
    path('inmueble/<int:inmueble_id>/', views.detalle_inmueble, name='detalle_inmueble'),
    path('perfil/', views.perfil, name='perfil'),
    path('buscar_inmuebles/', views.buscar_inmuebles, name='buscar_inmuebles'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('agregar_inmueble/', views.agregar_inmueble, name='agregar_inmueble'),
    path('actualizar_inmueble/<int:inmueble_id>/', views.actualizar_inmueble, name='actualizar_inmueble'),
    path('borrar_inmueble/<int:inmueble_id>/', views.borrar_inmueble, name='borrar_inmueble'),
    path('obtener_comunas/', views.obtener_comunas, name='obtener_comunas'),
    path('solicitar_arriendo/<int:inmueble_id>/', views.solicitar_arriendo, name='solicitar_arriendo'),
    path('ver_solicitudes/', views.ver_solicitudes, name='ver_solicitudes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
