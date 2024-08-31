from .models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework.response import Response

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