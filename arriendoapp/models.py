from django.db import models
from django.contrib.auth.models import User

# Modelo para la región
class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para la comuna
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Modelo para el tipo de inmueble
class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para el usuario
class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rut = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='arrendatario')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.tipo_usuario}"
    
# Modelo para el inmueble        
class Inmueble(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.PositiveIntegerField()
    m2_totales = models.PositiveIntegerField()
    estacionamientos = models.PositiveIntegerField()
    habitaciones = models.PositiveIntegerField()
    banos = models.PositiveIntegerField()
    direccion = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE)
    precio_arriendo = models.PositiveIntegerField()
    arrendador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    imagen_principal = models.ImageField(upload_to='inmuebles/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.comuna.nombre} - {self.arrendador}"

# Modelo para la solicitud de arriendo
class SolicitudArriendo(models.Model):
    arrendatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes')
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='solicitudes')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    mensaje = models.TextField(blank=True)

    def __str__(self):
        return f'Solicitud de {self.arrendatario.Usuario.username} para {self.inmueble.nombre}'
