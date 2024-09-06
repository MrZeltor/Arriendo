from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from .forms import InmuebleForm, CrearUsuarioForm, UsuarioEditForm, SolicitudArriendoForm
from .models import Inmueble, Comuna, SolicitudArriendo, Usuario, Region

# Vista para obtener las comunas según la región seleccionada
def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

# Vista para listar todos los inmuebles
def lista_inmuebles(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'lista_inmuebles.html', {'inmuebles': inmuebles})

# Vista para mostrar el detalle de un inmueble
def detalle_inmueble(request, inmueble_id):
    # Obtiene el inmueble con el ID proporcionado, o devuelve un 404 si no se encuentra (test)
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    return render(request, 'detalle_inmueble.html', {'inmueble': inmueble})

def buscar_inmuebles(request):
    query = request.GET.get('q', '')
    inmuebles = Inmueble.objects.filter(nombre__icontains=query)
    data = list(inmuebles.values('id', 'nombre', 'imagen_principal', 'precio_arriendo', 'region', 'comuna'))
    return JsonResponse({'inmuebles': data})
# Vista perfil
@login_required
def perfil(request):
    try:
        user = request.user.usuario
        inmuebles = Inmueble.objects.filter(arrendador=user)
    except Usuario.DoesNotExist:
        return redirect('login')
    return render(request, 'perfil.html', {'usuario': user, 'inmuebles': inmuebles})

# Vista inicio
def inicio(request):
    return render(request, 'inicio.html')

# Vista para crear un nuevo usuario
def crear_usuario(request):
    form = CrearUsuarioForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'Usuario creado exitosamente. Por favor, inicia sesión.')
        return redirect('login')
    return render(request, 'crear_usuario.html', {'form': form})


# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('lista_inmuebles')
        messages.error(request, 'Credenciales incorrectas')
    return render(request, 'login.html')

# Vista para editar el perfil del usuario
@login_required
def editar_perfil(request):
    # Obtiene el perfil del usuario actual
    usuario = request.user.usuario
    
    # Crea un formulario para editar el perfil, usando datos POST si están disponibles
    form = UsuarioEditForm(request.POST or None, instance=usuario)
    
    # Verifica si el formulario es válido
    if form.is_valid():
        # Guarda los cambios en el perfil del usuario
        form.save()
        
        # Actualiza el correo electrónico del usuario asociado
        usuario.user.email = form.cleaned_data.get('email')
        usuario.user.save()
        
        # Muestra un mensaje de éxito
        messages.success(request, 'Perfil actualizado exitosamente.')
        
        # Redirige al perfil del usuario
        return redirect('perfil')
    
    # Renderiza el formulario en la plantilla si no se envían datos POST
    return render(request, 'editar_perfil.html', {'form': form})

# Vista para agregar un nuevo inmueble
@login_required
def agregar_inmueble(request):
    form = InmuebleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        inmueble = form.save(commit=False)
        inmueble.arrendador = request.user.usuario
        inmueble.save()
        if request.user.usuario.tipo_usuario == 'arrendatario':
            request.user.usuario.tipo_usuario = 'arrendador'
            request.user.usuario.save()
        messages.success(request, 'Inmueble agregado exitosamente.')
        return redirect('perfil')
    return render(request, 'agregar_inmueble.html', {'form': form})

# Vista para actualizar un inmueble
@login_required
def actualizar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendador=request.user.usuario)
    form = InmuebleForm(request.POST or None, request.FILES or None, instance=inmueble)
    if form.is_valid():
        form.save()
        messages.success(request, 'Inmueble actualizado exitosamente.')
        return redirect('perfil')
    return render(request, 'actualizar_inmueble.html', {'form': form, 'inmueble': inmueble})

# Vista para borrar un inmueble
@login_required
def borrar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, arrendador=request.user.usuario)
    if request.method == 'POST':
        inmueble.delete()
        messages.success(request, 'Inmueble borrado exitosamente.')
        return redirect('perfil')
    return render(request, 'borrar_inmueble.html', {'inmueble': inmueble})

# Vista para solicitar el arriendo de un inmueble
@login_required
def solicitar_arriendo(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    form = SolicitudArriendoForm(request.POST or None)
    if form.is_valid():
        solicitud = form.save(commit=False)
        solicitud.arrendatario = request.user.usuario
        solicitud.inmueble = inmueble
        solicitud.save()
        messages.success(request, 'Solicitud enviada exitosamente.')
        return redirect('detalle_inmueble', inmueble_id=inmueble.id)
    return render(request, 'solicitar_arriendo.html', {'form': form, 'inmueble': inmueble})

# Vista para ver las solicitudes de arriendo
@login_required
def ver_solicitudes(request):
    usuario = request.user.usuario
    inmuebles = Inmueble.objects.filter(arrendador=usuario)
    if inmuebles.exists():
        solicitudes = SolicitudArriendo.objects.filter(inmueble__in=inmuebles)
    else:
        messages.info(request, 'No tienes inmuebles para arrendar.')
        return redirect('perfil')
    return render(request, 'ver_solicitudes.html', {'solicitudes': solicitudes})
