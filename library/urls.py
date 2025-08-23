from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowViewSet, UserViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"users", UserViewSet)
router.register(r"borrows", BorrowViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
