
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView

from users.filters import PaymentFilter
from users.models import Payment, CustomUser
from users.serializers import PaymentSerializer, UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer





class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
