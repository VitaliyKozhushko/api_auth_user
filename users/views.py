from .models import User
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer, ActualUserSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class RegistrationView(generics.CreateAPIView):
  queryset = User.objects.all()
  permission_classes = [AllowAny]
  serializer_class = RegisterSerializer

  def create(self, request, *args, **kwargs):
    serializer =self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    headers = self.get_success_headers(serializer.data)
    response_data = {
      'status':'success',
      'message': 'Пользователь успешно зарегистрирован',
      'data': {
        'user_id': user.id,
        'login': user.username,
        'phone': user.phone,
        'email': user.email
      }
    }
    return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class UsersViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.filter(is_superuser=False)
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]
  http_method_names = ['get']

  @method_decorator(cache_page(60 * 15))
  def list(self, requset, *args, **kwargs):
    queryset = self.queryset
    serializer = self.get_serializer(queryset, many=True)

    response_data = {
      'status': 'success',
      'message': 'Список пользователей успешно сформирован',
      'data':serializer.data
    }

    return Response(response_data)

class UserDetailView(generics.RetrieveUpdateAPIView):
  queryset = User.objects.all()
  serializer_class = ActualUserSerializer
  permission_classes = [IsAuthenticated]
  lookup_field = 'id'

  def get_object(self):
    user = super().get_object()
    if self.request.user != user:
      raise PermissionError("Вы можете просматривать и редактировать только свои данные")
    return user

class ChangePasswordView(generics.UpdateAPIView):
  model = User
  serializer_class = ChangePasswordSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self, queryset=None):
    return self.request.user

  def update(self, request, *args, **kwargs):
    user = self.get_object()
    serializer = self.get_serializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    if not user.check_password(serializer.validated_data['old_password']):
      return Response({'old_password': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(serializer.validated_data['new_password'])
    user.save()
    return Response({'detail': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)