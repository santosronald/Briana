from django.db import models
from ..centers.models import Center
from ..control.models import Child


class Disease(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')

    class Meta:
        verbose_name = "Enfermedad"
        verbose_name_plural = 'Enfermedades'

    def __str__(self):
        return '{0}'.format(self.name)


class Vaccine(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre')
    dose = models.CharField(verbose_name='Dosis', max_length=1,
                            choices=(("1", "First dose"), ("2", "Second dose"), ("3", "Third dose")))
    after_months = models.PositiveSmallIntegerField(verbose_name='Mes')
    details = models.TextField(verbose_name='Detalles')
    effects = models.TextField(verbose_name='Efectos')
    recommendation = models.TextField(verbose_name='Recomendaciones')
    related_diseases = models.ManyToManyField(Disease, related_name='related_vaccines',
                                              verbose_name='Emfermedades Relacionadas')
    related_centers = models.ManyToManyField(Center, related_name='related_vaccines',
                                             verbose_name='Centros de Vacunación')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        unique_together = ("name", "dose")
        ordering = ('order',)

    def __str__(self):
        return u'{0}-{1}'.format(self.name, self.dose)


class AppliedVaccine(models.Model):
    child = models.ForeignKey(Child, related_name='history')
    vaccine = models.ForeignKey(Vaccine, related_name='applied_vaccines')
    applied = models.BooleanField(default=False)
    required = models.BooleanField(default=True)
    month = models.PositiveSmallIntegerField()
    applied_date = models.DateField(null=True, blank=True)
    next_applied_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('child', 'vaccine')
        ordering = ('vaccine',)

    def __str__(self):
        return u'{0}-{1}'.format(self.vaccine, self.child)
