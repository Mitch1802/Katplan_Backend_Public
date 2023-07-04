from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Modul

from katplan.serializers import ModulSerializer


MODULE_URL = reverse('katplan:modul-list')


class PublicModuleApiTests(TestCase):
    """Test the publicly available modul API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(MODULE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateModuleApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_module(self):
        """Test retrieving tags"""
        Modul.objects.create(
            bezeichnung='Test',
            kuerzel='A',
            icon='name',
            reihenfolge=0
        )

        res = self.client.get(MODULE_URL)

        module = Modul.objects.all().order_by('-reihenfolge')
        serializer = ModulSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
