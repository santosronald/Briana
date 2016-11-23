from django.core.urlresolvers import resolve
from rest_framework.permissions import BasePermission
from apps.control.models import UserChild
from apps.vaccinations.models import AppliedVaccine

__author__ = 'klaatu'


class CanSeeAppliedVaccines(BasePermission):
    def has_permission(self, request, view):
        return UserChild.objects.filter(child=view.kwargs["child_pk"],relative=request.user).exists()


class CanSeeAppliedVaccine(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (UserChild.objects.filter(child=view.kwargs["child_pk"],relative=request.user).exists() and AppliedVaccine.objects.filter(
            child=view.kwargs["child_pk"], id=view.kwargs["pk"]).exists())
