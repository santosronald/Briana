from django.core.mail import send_mail
from django.db.models import Q
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from rest_framework import generics, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from social.apps.django_app.utils import psa
from .serializer import *
from .permissions import *


class IndexView(TemplateView):
    template_name = 'index.html'


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class HasChildAPIView(generics.RetrieveAPIView):
    serializer_class = HasChildSerializer

    def get_object(self):
        return self.request.user


class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveUserSerializer

    def get_object(self):
        return self.request.user


class CreateControlAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, CanSeeChild)
    serializer_class = CreateControlSerializer


class ListControlsAPIView(generics.ListAPIView):
    serializer_class = ListControlsSerializer
    permission_classes = (IsAuthenticated, CanSeeChild)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Control.objects.filter(child=self.kwargs['pk'])


class DeleteControlAPIView(generics.DestroyAPIView):
    serializer_class = DeleteControlSerializer
    permission_classes = IsAuthenticated, CanDeleteUpdateControlChild
    queryset = Control.objects.all()


class UpdateControlAPIView(generics.UpdateAPIView):
    serializer_class = UpdateControlSerializer
    permission_classes = IsAuthenticated, CanDeleteUpdateControlChild
    queryset = Control.objects.all()


class RetrieveChildAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveChildSerializer
    queryset = Child.objects.all()
    permission_classes = (IsAuthenticated, CanSeeChild)


class ChildrenAPIView(generics.ListAPIView):
    serializer_class = ChildrenSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return self.request.user.children.all()


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class MobileLoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class FacebookMobileLoginAPI(MobileLoginAPI):
    serializer_class = FacebookLoginSerializer

    @method_decorator(psa('facebook-mobile-login'))
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookMobileLoginAPI, self).dispatch(request, *args, **kwargs)


class CreateUserChildRepresentativeAPIView(generics.CreateAPIView):
    # permission_classes = IsAuthenticated,
    serializer_class = CreateUserChildRepresentativeSerializer


class UpdateChildAPIView(generics.UpdateAPIView):
    permission_classes = IsAuthenticated, IsRepresentative
    serializer_class = UpdateChildSerializer
    queryset = Child.objects.all()


class DeleteChildAPIView(generics.DestroyAPIView):
    permission_classes = IsAuthenticated, IsRepresentative
    serializer_class = DeleteChildSerializer
    queryset = Child.objects.all()


class UpdateChildPhotoAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, CanSeeChild)
    serializer_class = UpdateChildPhotoSerializer
    queryset = Child.objects.all()


class CreateRequestAPIView(generics.CreateAPIView):
    serializer_class = CreateRequestSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        vd = serializer.validated_data
        parent = UserChild.objects.filter(child=vd.get("child"), is_representative=True).first().relative
        req = serializer.save(representative=parent, applicant=self.request.user, status="N")
        devices = GCMDevice.objects.filter(user=parent)
        child_name = vd.get("child").get_fullname()
        devices.send_message(
            "{0} ha solicitado permisos para acceder a los datos de {1}".format(self.request.user.get_fullname(),
                                                                                child_name),
            extra={"request_id": req.id, "type": "request"})


class ObtainRequestsAPIView(generics.ListAPIView):
    serializer_class = RequestsSerializer

    def get_queryset(self):
        return self.request.user.received_request.all().filter(Q(status="N") | Q(status="A"))


class ResponseRequestAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, CanResponseRequests)
    serializer_class = ResponseRequestSerializer
    queryset = Request.objects.all()


class FilterChildrenAPIView(generics.ListAPIView):
    queryset = Child.objects.all()
    serializer_class = FilterChildrenSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('dni',)


class ListChildStimulationAPIView(generics.ListAPIView):
    serializer_class = ListChildStimulationsSerializer
    pagination_class = PageNumberPagination

    # permission_classes = IsAuthenticated, CanSeeChild

    def get_queryset(self):
        return ChildStimulation.objects.filter(child=self.kwargs['pk'])


class UpdateChildStimulationAPIView(generics.UpdateAPIView):
    serializer_class = UpdateChildStimulationSerializer
    permission_classes = IsAuthenticated, CanModifyStimulation
    queryset = ChildStimulation.objects.all()


class ListMessagesAPIView(generics.ListAPIView):
    serializer_class = ListMessagesSerializer
    queryset = Message.objects.all().order_by('?')[:4]


class RegisterGCMDeviceAPI(generics.CreateAPIView):
    serializer_class = GCMDeviceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        registration_id = serializer.validated_data.get("registration_id")
        device = GCMDevice.objects.filter(registration_id=registration_id).first()
        if device:
            device.user = self.request.user
            device.name = self.request.user.first_name + self.request.user.last_name
            device.device_id = vd.get("device_id")
            device.save()
            return Response(GCMDeviceSerializer(device).data, status=status.HTTP_201_CREATED)
        else:
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@csrf_exempt
def mail_indotic(self):
    if self.POST.get('tipo').lower() == "contacto":
        email = 'contacto@indotic.com'
    else:
        email = 'proyectos@indotic.com'
    send_mail('{}'.format(self.POST.get('asunto')),
              '''
                    Nombre: {}
                    Empresa: {}
                    Web: {}
                    Email de Contacto: {}
                    Teléfono: {}
                    Tipo de Consulta: {}
                    Detalle: {}
                    '''.format(self.POST.get('nombre'), self.POST.get('empresa'), self.POST.get('web'),
                               self.POST.get('email'), self.POST.get('telefono'), self.POST.get('tipo'),
                               self.POST.get('detalle')), 'anderdl007@gmail.com', [email],
              fail_silently=False)
    return HttpResponse(status=200)
