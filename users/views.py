from .models import User
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

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
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['id']
  http_method_names = ['get']

  def list(self, requset, *args, **kwargs):
    queryset = self.queryset
    serializer = self.get_serializer(queryset, many=True)

    response_data = {
      'status': 'success',
      'message': 'Список пользователей успешно сформирован',
      'data':serializer.data
    }

    return response_data