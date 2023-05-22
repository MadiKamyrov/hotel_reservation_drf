from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Category, Room, Pricing, Reservation, User
from .permissions import IsAuthor
from .serializers import CategorySerializer, RoomSerializer, PricingSerializer, ReservationSerializer, \
    CustomTokenObtainPairSerializer, UserSerializer, TokenSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('category').all()
    serializer_class = RoomSerializer


class PricingViewSet(viewsets.ModelViewSet):
    queryset = Pricing.objects.select_related('category').all()
    serializer_class = PricingSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthor, ]
    queryset = Reservation.objects.select_related('room').all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TokenObtainPairWithUserView(TokenObtainPairView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        token_serializer = TokenSerializer({
            'access': response.data['access'],
            'refresh': response.data['refresh'],
            'user': user_data
        })

        return Response(token_serializer.data)

