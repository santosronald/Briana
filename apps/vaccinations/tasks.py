from mutacion.celery import app
from push_notifications.models import GCMDevice
from ..control.models import UserChild

__author__ = 'klaatu'
from .models import AppliedVaccine
from django.utils.timezone import localtime, now


@app.task
def days_before_expire_applied_vaccine():
    msg = ''
    applied_vaccines = AppliedVaccine.objects.all()
    for applied_vaccine in applied_vaccines:
        applied_vaccine_next_date = applied_vaccine.next_applied_date
        if (int((applied_vaccine_next_date - localtime(now()).date()).days)) == 3 and (not applied_vaccine.applied):
            msg = 'Faltan 3 días para aplicar {0} a {1}'.format(applied_vaccine.vaccine.name,
                                                                applied_vaccine.child.get_fullname())
        elif (int((applied_vaccine_next_date - localtime(now()).date()).days)) == 2 and (not applied_vaccine.applied):
            msg = 'Falta 2 día para aplicar {0} a {1}'.format(applied_vaccine.vaccine.name,
                                                              applied_vaccine.child.get_fullname())
        elif (int((applied_vaccine_next_date - localtime(now()).date()).days)) == 1 and (not applied_vaccine.applied):
            msg = 'Falta 1 día para aplicar {0} a {1}'.format(applied_vaccine.vaccine.name,
                                                              applied_vaccine.child.get_fullname())
        if msg != '':
            user_childs = UserChild.objects.filter(child=applied_vaccine.child)
            for user_child in user_childs:
                devices = GCMDevice.objects.filter(user=user_child.relative)
                devices.send_message(msg,
                                     extra={"child_id": user_child.child.id, "applied_vaccine_id": applied_vaccine.id,
                                            "type": "days_before_expired"})
            msg = ''


@app.task
def expired_applied_vaccine():
    msg = ''
    applied_vaccines = AppliedVaccine.objects.all()
    for applied_vaccine in applied_vaccines:
        applied_vaccine_next_date = applied_vaccine.next_applied_date
        if (int((localtime(now()).date() - applied_vaccine_next_date).days)) > 0 and (not applied_vaccine.applied):
            msg = 'Ya venció {0} para {1}'.format(applied_vaccine.vaccine.name,
                                                  applied_vaccine.child.get_fullname())
        elif (int((applied_vaccine_next_date - localtime(now()).date()).days)) == 0 and (not applied_vaccine.applied):
            msg = 'Hoy debes aplicar {0} a {1}'.format(applied_vaccine.vaccine.name,
                                                       applied_vaccine.child.get_fullname())
        if msg != '':
            user_childs = UserChild.objects.filter(child=applied_vaccine.child)
            for user_child in user_childs:
                devices = GCMDevice.objects.filter(user=user_child.relative)
                devices.send_message(msg,
                                     extra={"child_id": user_child.child.id, "applied_vaccine_id": applied_vaccine.id,
                                            "type": "expired"})
            msg = ''
