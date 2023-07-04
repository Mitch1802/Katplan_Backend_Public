from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Fahrzeug

from katplan.serializers import FahrzeugSerializer


FAHRZEUGE_URL = reverse('katplan:fahrzeug-list')


def sample_fahrzeug():
    return Fahrzeug.objects.create(
        kuerzel='T0001',
        name='Test'
    )


def detail_url(fahrzeug_id):
    """Return fahrzeug detail URL"""
    return reverse('katplan:fahrzeug-detail', args=[fahrzeug_id])


class PublicFahrzeugApiTests(TestCase):
    """Test the publicly available fahrzeug API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(FAHRZEUGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFahrzeugApiTests(TestCase):
    """Test the authorized user fahrzeug API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_fahrzeug(self):
        """Test retrieving fahrzeug"""
        sample_fahrzeug()

        res = self.client.get(FAHRZEUGE_URL)

        module = Fahrzeug.objects.all().order_by('-kuerzel')
        serializer = FahrzeugSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_fahrzeug_successful(self):
        """Test creating fahrzeug"""
        payload = {
            'kuerzel': 'T1',
            'name': 'Text'
        }
        res = self.client.post(FAHRZEUGE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        fahrzeug = Fahrzeug.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(fahrzeug, key))

    def test_create_invalid_fahrzeug(self):
        """Test the invalid creation"""
        payload = {'name': ''}
        res = self.client.post(FAHRZEUGE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_fahrzeug(self):
        """Test updating a fahrzeug with patch"""
        fahrzeug = sample_fahrzeug()

        payload = {'name': 'Testpatch'}
        url = detail_url(fahrzeug.id)
        self.client.patch(url, payload)

        fahrzeug.refresh_from_db()
        self.assertEqual(fahrzeug.name, payload['name'])

    def test_full_update_fahrzeug(self):
        """Test updating a fahrzeug with put"""
        fahrzeug = sample_fahrzeug()

        payload = {'kuerzel': 'P1', 'name': 'Testpatch'}
        url = detail_url(fahrzeug.id)
        self.client.put(url, payload)

        fahrzeug.refresh_from_db()
        self.assertEqual(fahrzeug.kuerzel, payload['kuerzel'])
        self.assertEqual(fahrzeug.name, payload['name'])

    def test_delete_successfull(self):
        """Test the deleting"""
        fahrzeug = sample_fahrzeug()

        url = detail_url(fahrzeug.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
