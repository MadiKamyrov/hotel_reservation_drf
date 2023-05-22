from hotel import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('category', views.CategoryViewSet)
router.register('room', views.RoomViewSet)
router.register('pricing', views.PricingViewSet)
router.register('reservation', views.ReservationViewSet)

urlpatterns = [

]
urlpatterns += router.urls
