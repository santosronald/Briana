from rest_framework.pagination import PageNumberPagination
from .models import Center
from .serializers import ListCenterSerializer, RetrieveCenterSerializer
from rest_framework import generics


class ListCenterAPIView(generics.ListAPIView):
    serializer_class = ListCenterSerializer
    queryset = Center.objects.all()
    pagination_class = PageNumberPagination


class RetrieveCenterAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveCenterSerializer
    queryset = Center.objects.all()


