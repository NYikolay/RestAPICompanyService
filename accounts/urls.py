from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from accounts.views import AdminUserCreation, CompanyView, WorkersViewSet, UpdateProfileView

router = DefaultRouter()
router.register(r'users', AdminUserCreation, basename='users')
router.register(r'company', CompanyView, basename='company')
router.register(r'workers', WorkersViewSet, basename='workers')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile_update/<int:pk>/', UpdateProfileView.as_view(), name='worker_update')
]

urlpatterns += router.urls
