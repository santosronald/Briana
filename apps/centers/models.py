from django.db import models
from django.contrib.gis.db.models import PointField

CENTERS_TYPE_CHOICES = (
    ('HOSPITAL', 'Hospital'), ('CLINIC', 'Clinica'), ('POSTA', 'Posta'),
    ('OTHER', 'Otro'))


class Center(models.Model):
    center_type = models.CharField(verbose_name='Tipo de Centro',max_length=10, choices=CENTERS_TYPE_CHOICES)
    name = models.CharField(verbose_name='Nombre',max_length=100)
    address = models.CharField(verbose_name='Dirección',max_length=200, blank=True)
    description = models.TextField(verbose_name='descripción')
    location = PointField(u'longitude/latitude', geography=True)
    monday_to_friday = models.CharField(max_length=25,verbose_name='Lunes a Viernes')
    saturday_sunday_holiday = models.CharField(max_length=25,verbose_name='Fines de semana y feriados')

    class Meta:
        verbose_name = "Centro  Medico"
        verbose_name_plural = "Centros Medicos"

    def __str__(self):
        return '{0}'.format(self.name)
