from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import PaymentListView, UserCreateAPIView, PaymentCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register'),

    path('payments/', PaymentCreateAPIView.as_view(), name='payments'),

]
