from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Gefahr

from katplan.serializers import GefahrSerializer


GEFAHREN_URL = reverse('katplan:gefahr-list')


def sample_gefahr():
    return Gefahr.objects.create(
        kuerzel='T0001',
        name='Test'
    )


def detail_url(gefahr_id):
    """Return gefahr detail URL"""
    return reverse('katplan:gefahr-detail', args=[gefahr_id])


class PublicGefahrApiTests(TestCase):
    """Test the publicly available gefahr API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(GEFAHREN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGefahrApiTests(TestCase):
    """Test the authorized user gefahr API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_gefahr(self):
        """Test retrieving gefahr"""
        sample_gefahr()

        res = self.client.get(GEFAHREN_URL)

        module = Gefahr.objects.all().order_by('-kuerzel')
        serializer = GefahrSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_gefahr_successful(self):
        """Test creating gefahr"""
        payload = {
            'kuerzel': 'T1',
            'name': 'Text',
            'beschreibung': '...'
        }
        res = self.client.post(GEFAHREN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        gefahr = Gefahr.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(gefahr, key))

    def test_create_invalid_gefahr(self):
        """Test the invalid creation"""
        payload = {'name': ''}
        res = self.client.post(GEFAHREN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_gefahr(self):
        """Test updating a gefahr with patch"""
        gefahr = sample_gefahr()

        payload = {'name': 'Testpatch'}
        url = detail_url(gefahr.id)
        self.client.patch(url, payload)

        gefahr.refresh_from_db()
        self.assertEqual(gefahr.name, payload['name'])

    def test_full_update_gefahr(self):
        """Test updating a gefahr with put"""
        gefahr = sample_gefahr()

        payload = {'kuerzel': 'P1', 'name': 'Testpatch'}
        url = detail_url(gefahr.id)
        self.client.put(url, payload)

        gefahr.refresh_from_db()
        self.assertEqual(gefahr.kuerzel, payload['kuerzel'])
        self.assertEqual(gefahr.name, payload['name'])

    def test_delete_successfull(self):
        """Test the deleting"""
        gefahr = sample_gefahr()

        url = detail_url(gefahr.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
