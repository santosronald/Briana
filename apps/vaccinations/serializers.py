from apps.centers.models import Center
from apps.control.models import Child
from apps.vaccinations.models import Disease

__author__ = 'klaatu'
from rest_framework import serializers
from .models import Vaccine, AppliedVaccine
import datetime
import calendar
from dateutil import relativedelta

'''
Child Age when vaccine was applied
print(relativedelta.relativedelta(instance.applied_date,Child.objects.get(id=int(view.kwargs["child_pk"])).birth_date).years)
print(relativedelta.relativedelta(instance.applied_date,Child.objects.get(id=int(view.kwargs["child_pk"])).birth_date).months)
'''


def add_months(date, months):
    month = date.month - 1 + months
    year = int(date.year + month / 12)
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


class ListVaccinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ('id', 'name', 'dose', 'details', 'effects', 'recommendation', 'after_months')


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        exclude = ('related_diseases', 'related_centers')


class ListAppliedVaccinesSerializer(serializers.ModelSerializer):
    vaccine = VaccineSerializer()

    class Meta:
        model = AppliedVaccine


class RetrieveAppliedVaccineSerializer(serializers.ModelSerializer):
    vaccine = VaccineSerializer()

    class Meta:
        model = AppliedVaccine
        fields = ('id', 'child', 'vaccine', 'applied', 'required', 'applied_date', 'next_applied_date')


class ListCentersRelatedToVaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ('id', 'name', 'center_type', 'address')


class ListDiseasesRelatedToVaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ('name', 'description')


class UpdateAppliedVaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedVaccine
        fields = ('applied_date',)

    def update(self, instance, validated_data):
        instance = super(UpdateAppliedVaccineSerializer, self).update(instance,
                                                                      validated_data)
        view = self.context["view"]
        vaccine_month = instance.vaccine.after_months
        applied_vaccines = AppliedVaccine.objects.filter(
            child=int(view.kwargs["child_pk"]))
        for applied_vaccine in applied_vaccines:
            if applied_vaccine.month > vaccine_month:
                applied_vaccine.next_applied_date = add_months(
                    instance.applied_date,
                    applied_vaccine.month - vaccine_month)
                applied_vaccine.save()
        instance.applied = True
        instance.save()
        return instance
