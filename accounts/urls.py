from rest_framework.routers import DefaultRouter
from accounts.views import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [] + router.urls