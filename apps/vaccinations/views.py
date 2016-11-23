from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .models import Vaccine
from .permissions import CanSeeAppliedVaccines, CanSeeAppliedVaccine



class ListVaccinesAPIView(generics.ListAPIView):
    serializer_class = ListVaccinesSerializer
    pagination_class = PageNumberPagination
    queryset = Vaccine.objects.all()



class ListAppliedVaccinesAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, CanSeeAppliedVaccines)
    serializer_class = ListAppliedVaccinesSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return AppliedVaccine.objects.filter(child=self.kwargs['child_pk'])



class RetrieveAppliedVaccineAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, CanSeeAppliedVaccine)
    serializer_class = RetrieveAppliedVaccineSerializer
    queryset = AppliedVaccine.objects.all()


class UpdateAppliedVaccineAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, CanSeeAppliedVaccine)
    serializer_class = UpdateAppliedVaccineSerializer
    queryset = AppliedVaccine.objects.all()


class ListCentersRelatedToVaccineAPIView(generics.ListAPIView):
    serializer_class = ListCentersRelatedToVaccineSerializer

    def get_queryset(self):
        return Center.objects.filter(related_vaccines=self.kwargs['pk'])


class ListDiseasesRelatedToVaccineAPIView(generics.ListAPIView):
    serializer_class = ListDiseasesRelatedToVaccineSerializer

    def get_queryset(self):
        return Disease.objects.filter(related_vaccines=self.kwargs['pk'])
