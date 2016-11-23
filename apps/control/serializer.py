from django.contrib.auth import authenticate, login
from push_notifications.models import GCMDevice
from requests.exceptions import HTTPError
from rest_framework.authtoken.models import Token
from apps.vaccinations.models import Vaccine, AppliedVaccine
from .models import User, Child, Control, UserChild, Request, Stimulation, ChildStimulation, Message
from rest_framework import serializers
from apps.vaccinations.serializers import add_months


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'dni', 'celphone')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate_dni(self, dni):
        if dni and User.objects.filter(dni=dni).exists():
            raise serializers.ValidationError("Este DNI ya fue registrado")
        try:
            int(dni)
            return dni
        except:
            raise serializers.ValidationError('Dni must be int')

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], dni=validated_data['dni']
                                   )

        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class HasChildSerializer(serializers.ModelSerializer):
    has_child = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('has_child',)

    def get_has_child(self, obj):
        return UserChild.objects.filter(relative=obj).exists()


class UpdateChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('id', 'first_name', 'last_name', 'apgar', 'gender', 'relationship', 'dni')

    def update(self, instance, validated_data):
        instance = super(UpdateChildSerializer, self).update(instance, validated_data)
        request = self.context.get('request')
        user_child = UserChild.objects.get(child=instance.id, relative=request.user)
        user_child.relationship = instance.relationship
        user_child.save()
        return instance


class DeleteChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class RetrieveChildSerializer(serializers.ModelSerializer):
    relationship = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = ('id', 'first_name', 'last_name', 'apgar', 'gender', 'photo', 'relationship')

    def get_relationship(self, obj):
        request = self.context.get("request")
        return UserChild.objects.get(child=obj, relative=request.user).relationship


class ChildrenSerializer(serializers.ModelSerializer):
    applied_vaccines_quantity = serializers.SerializerMethodField()
    relationship = serializers.SerializerMethodField()

    class Meta:
        model = Child
        field = ('id', 'first_name', 'last_name', 'gender', 'relationship', 'applied_vaccines_quantity')

    def get_applied_vaccines_quantity(self, obj):
        return str(obj.history.filter(applied=True).count()) + " de " + str(Vaccine.objects.all().count()) + " vacunas"

    def get_relationship(self, obj):
        request = self.context.get("request")
        return UserChild.objects.get(child=obj, relative=request.user).relationship


class FilterChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={"blank": "Este campo es obligatorio"})
    password = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        self.user_cache = authenticate(email=attrs["email"], password=attrs["password"])
        if not self.user_cache:
            raise serializers.ValidationError("Invalid login")
        return attrs

    def get_user(self):
        return self.user_cache


class FacebookLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        request = self.context.get("request")
        self.user_cache = None
        try:
            self.user_cache = request.backend.do_auth(attrs.get("access_token"))
            return attrs
        except HTTPError:
            raise serializers.ValidationError("Invalid facebook token")

    def get_user(self):
        return self.user_cache


class CreateControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ("id", "weight", "height", "head_circumference", "date")

    def create(self, validated_data):
        view = self.context['view']
        child = Child.objects.get(id=view.kwargs['pk'])
        control = Control.objects.create(child=child, **validated_data)
        return control


class DeleteControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control


class UpdateControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ("id", "weight", "height", "head_circumference", "date")


class ListControlsSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField()

    class Meta:
        model = Control
        fields = ('id', 'date', 'weight', 'height', 'head_circumference', 'birth_date',)

    def get_birth_date(self, obj):
        return obj.child.birth_date


class CreateChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('id', 'first_name', 'last_name', 'birth_date', 'dni', 'apgar', 'gender')


class UpdateChildPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('photo',)


class CreateUserChildRepresentativeSerializer(serializers.ModelSerializer):
    child = CreateChildSerializer()

    class Meta:
        model = UserChild
        fields = ('child', 'relationship')

    def create(self, validated_data):
        child_vd = validated_data.pop('child')
        child = Child.objects.create(relationship=validated_data['relationship'], **child_vd)
        request = self.context.get('request')
        user_child = UserChild.objects.create(child=child, is_representative=True, relative=request.user,
                                              **validated_data)
        vaccines = Vaccine.objects.all()
        for vaccine in vaccines:
            vacc = AppliedVaccine.objects.create(month=vaccine.after_months, child=child, vaccine=vaccine)
            vacc.next_applied_date = add_months(child.birth_date, vaccine.after_months)
            vacc.save()
        stimulations = Stimulation.objects.all()
        for stimulation in stimulations:
            ChildStimulation.objects.create(stimulation=stimulation, child=child)
        return user_child


class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('child', 'relationship')

    def validate_child(self, value):
        user_child = UserChild.objects.filter(child=value, is_representative=True).first()
        if not user_child:
            raise serializers.ValidationError("Child doesn't have a representative")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        if UserChild.objects.filter(child=attrs.get("child"), relative=request.user, is_representative=True).exists():
            raise serializers.ValidationError("You can't send a request to yourself")
        elif Request.objects.filter(child=attrs.get("child"), applicant=request.user, status="A").exists():
            raise serializers.ValidationError("User already related to child")
        elif Request.objects.filter(child=attrs.get("child"), applicant=request.user, status="N").exists():
            raise serializers.ValidationError("Unanswered response")
        return attrs


class RequestsSerializer(serializers.ModelSerializer):
    child_fullname = serializers.SerializerMethodField()
    applicant_fullname = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Request
        fields = (
            'id', 'child', 'applicant', 'relationship', 'status', 'child_fullname', 'applicant_fullname', 'updated_at')

    def get_child_fullname(self, obj):
        return obj.child.get_fullname()

    def get_applicant_fullname(self, obj):
        return obj.applicant.get_fullname()


class ResponseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'status')

    def update(self, instance, validated_data):
        instance = super(ResponseRequestSerializer, self).update(instance, validated_data)
        if instance.status == "A":
            UserChild.objects.create(child=instance.child, relative=instance.applicant,
                                     relationship=instance.relationship)
            devices = GCMDevice.objects.filter(user=instance.applicant)
            devices.send_message(
                "{0} ha acceptado tu solicitud sobre {1}".format(instance.applicant.get_fullname(),
                                                                 instance.child.get_fullname()),
                extra={"child_id": instance.child.id, "type": "ok_request"})
        elif instance.status == "D":
            if UserChild.objects.filter(relative=instance.applicant, child=instance.child).exists():
                UserChild.objects.get(relative=instance.applicant, child=instance.child).delete()
            instance.delete()
        return instance


class ListChildStimulationsSerializer(serializers.ModelSerializer):
    month = serializers.CharField(source="stimulation.month")
    name = serializers.CharField(source="stimulation.name")

    class Meta:
        model = ChildStimulation
        exclude = ("child", "stimulation")


class UpdateChildStimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildStimulation
        fields = ('status',)


class ListMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message


class GCMDeviceSerializer(serializers.ModelSerializer):
    registration_id = serializers.CharField()
    device_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_registration_id(self, attr):
        user = getattr(self.context.get("request"), "user")
        if self.Meta.model.objects.filter(registration_id=attr, user=user):
            raise serializers.ValidationError("El usuario ya registró este dispositivo")
        return attr

    class Meta:
        model = GCMDevice
        fields = ("id", "name", "date_created", "device_id", "registration_id")
