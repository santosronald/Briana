from django.contrib.auth.models import PermissionsMixin, BaseUserManager, \
    AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        user = self.model(email=email, is_active=True, is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, blank=True, validators=[
        RegexValidator(regex='^.{8}$', message="El dni debe ser de 8 números")])
    celphone = PhoneNumberField(blank=True, null=True)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def get_fullname(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Child(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    birth_date = models.DateField()
    dni = models.CharField(max_length=8, unique=True, validators=[
        RegexValidator(regex='^.{8}$', message="El dni debe ser de 8 números")])
    photo = models.ImageField(upload_to='control', null=True, blank=True)
    apgar = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1,
                              choices=(('M', 'Masculino'), ('F', 'Femenino')))
    related_family = models.ManyToManyField(User, through='UserChild',
                                            related_name='children')
    relationship = models.CharField(max_length=20)

    def get_fullname(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "Niño"
        verbose_name_plural = "Niños"

    def __str__(self):
        return u'{0}-{1}'.format(self.first_name, self.last_name)


class Control(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    child = models.ForeignKey(Child, related_name='controls')
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    head_circumference = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Control"
        verbose_name_plural = "Controles"
        ordering = ("-created_at",)

    def __str__(self):
        return u'{0}'.format(self.child)


class UserChild(models.Model):
    child = models.ForeignKey(Child, related_name='relations')
    relative = models.ForeignKey(User, related_name='relations')
    relationship = models.CharField(max_length=20)
    is_representative = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('child', 'relative')


class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    child = models.ForeignKey(Child, related_name='requests')
    representative = models.ForeignKey(User, related_name='received_request')
    applicant = models.ForeignKey(User, related_name='sent_requests')
    relationship = models.CharField(max_length=20)
    status = models.CharField(max_length=1, choices=(
        ("A", "Accepted"), ("D", "Denied"), ("N", "None")))
    response_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = "-created_at",


class Stimulation(models.Model):
    month = models.CharField(verbose_name='Mes', max_length=2, choices=(
        ('1', '1 mes'), ('2', '2 meses'), ('3', '3 meses'), ('4', '4 meses'),
        ('5', '5 meses'), ('6', '6 meses'), ('7', '7 meses'), ('8', '8 meses'),
        ('9', '9 meses'), ('10', '10 meses'), ('11', '11 meses'),
        ('12', '12 meses'), ('14', '14 meses'), ('16', '16 meses'),
        ('18', '18 meses'), ('20', '20 meses'), ('22', '22 meses'),
        ('24', '24 meses'), ('30', '30 meses'), ('36', '36 meses'),
        ('48', '48 meses'),))
    name = models.CharField(max_length=150, verbose_name='Nombre')

    class Meta:
        ordering = "month",
        verbose_name = "Estimulación"
        verbose_name_plural = "Estimulaciones"

    def __str__(self):
        return u'{0}-{1}'.format(self.name, self.month)


class ChildStimulation(models.Model):
    child = models.ForeignKey(Child, related_name='stimulations')
    stimulation = models.ForeignKey(Stimulation, related_name='stimulations')
    status = models.BooleanField(default=False)

    class Meta:
        ordering = 'stimulation',
        unique_together = ('child', 'stimulation')


class Message(models.Model):
    image = models.ImageField(verbose_name='imagen', upload_to='messages',
                              null=True, blank=True)
    text = models.TextField(verbose_name='Texto')
    url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = ('Mensajes')
        verbose_name = ('Mensaje')

    def __str__(self):
        return u'{0}'.format(self.text)
