from django.urls import path
from .views import RegisterView, ActivationView, ForgotPasswordView, ForgotPasswordCompleteView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns =[
    path('register/', RegisterView.as_view()),
    path('activate/<str:email>/<str:activation_code>', ActivationView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(' /', ForgotPasswordView.as_view()),
    path('forg_pas_con/', ForgotPasswordCompleteView.as_view()),
    path('change_pass/', ChangePasswordView.as_view()),
]