from django.contrib import admin
from django.urls import path, include
from hotel.views import CustomTokenObtainPairView, UserCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("hotel.urls")),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/', UserCreateView.as_view(), name='token_obtain_pair')
]
