from django.contrib.auth.models import User, Group
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, CharField, ValidationError

class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=6)
    role = CharField(write_only=True, required=False)  # optional: default student
    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role", "student").lower()
        user = User.objects.create_user(**validated_data)  # hashes password
        grp, _ = Group.objects.get_or_create(name=role)
        user.groups.add(grp)
        return user

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """POST /api/auth/register/  {'username','email','password','role?'}"""
    ser = RegisterSerializer(data=request.data)
    if ser.is_valid():
        user = ser.save()
        return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)
    return Response(ser.errors, status=400)

class MeSerializer(ModelSerializer):
    role = CharField(source="groups.first.name", read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "role"]

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """GET /api/auth/me/ → current user profile (uses JWT)"""
    return Response(MeSerializer(request.user).data)