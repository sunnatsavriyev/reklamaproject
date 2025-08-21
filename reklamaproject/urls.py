from rest_framework.routers import DefaultRouter
from .views import MetroLineViewSet, StationViewSet, PositionViewSet, AdvertisementViewSet, AdvertisementArchiveViewSet, get_me
from django.urls import path, include
router = DefaultRouter()
router.register(r'lines', MetroLineViewSet)
router.register(r'stations', StationViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'advertisements-archive', AdvertisementArchiveViewSet)


urlpatterns = router.urls + [
    path('me/', get_me, name='get_me'),  
]


