from rest_framework.routers import DefaultRouter
from .views import MetroLineViewSet, StationViewSet, PositionViewSet, AdvertisementViewSet, AdvertisementArchiveViewSet, get_me, ExpiredAdvertisementViewSet, Stationimage
from django.urls import path
router = DefaultRouter()
router.register(r'lines', MetroLineViewSet)
router.register(r'stations', StationViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'advertisements-archive', AdvertisementArchiveViewSet)
router.register(r'tugashi-advertisements', ExpiredAdvertisementViewSet, basename='tugashi-advertisements')


urlpatterns = router.urls + [
    path('me/', get_me, name='get_me'), 
    path("stations/<int:pk>/update-image/", Stationimage.as_view(), name="station-update-image"),

]


