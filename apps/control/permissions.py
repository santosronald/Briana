from rest_framework.permissions import BasePermission
from .models import UserChild, Request, Control, ChildStimulation

__author__ = 'klaatu'


class CanSeeChild(BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserChild.objects.filter(child=obj.id, relative=request.user).exists()


class CanDeleteUpdateControlChild(BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserChild.objects.filter(child=Control.objects.get(id=obj.id).child, relative=request.user).exists()


class CanModifyStimulation(BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserChild.objects.filter(child=ChildStimulation.objects.get(id=obj.id).child,
                                        relative=request.user).exists()


class IsRepresentative(BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserChild.objects.filter(child=obj.id, relative=request.user, is_representative=True)


class CanResponseRequests(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Request.objects.filter(id=obj.id, representative=request.user).exists()
