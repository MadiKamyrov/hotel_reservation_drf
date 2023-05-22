from django.contrib.auth import get_user_model
from django.test import TestCase

from hotel.models import Reservation, Category, Room

User = get_user_model()


class MyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category_data = {
            "id": 2,
            "name": "Люкс",
            "description": "Лучший люкс в городе"
        }

        Category.objects.create(**category_data)
        category = Category.objects.get(id=2)

        room_data = {
            "category": category,
            "number": 25,
            "floor": 1
        }

        Room.objects.create(**room_data)

        user_data = {
            "username": "Madi",
            "password": 12345
        }

        User.objects.create(**user_data)

        data = {
            "room_id": Room.objects.last().id,
            "user_id": User.objects.last().id,
            "customer_name": "username",
            "arrival_date": "2023-01-03",
            "departure_date": "2023-02-03",
            "price": 10 or 10.99

        }
        cls.reservation = Reservation.objects.create(**data)

    def test_room(self):
        self.assertEqual(self.reservation.room.category, Category.objects.first())

    def test_user(self):
        return self.assertEqual(self.reservation.user, User.objects.first())

    def test_customer_name(self):
        return self.assertEqual(self.reservation.customer_name, "username")

    def test_arrival_date(self):
        return self.assertEqual(self.reservation.arrival_date, "2023-01-03")

    def test_departure_date(self):
        return self.assertEqual(self.reservation.departure_date, "2023-02-03")

    def test_price(self):
        return self.assertEqual(self.reservation.price, 10 or 10.99)
