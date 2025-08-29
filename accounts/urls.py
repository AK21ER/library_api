from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/login/", LoginView.as_view(), name="login"),
]
urlpatterns += router.urls
