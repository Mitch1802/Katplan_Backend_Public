from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Rolle

from katplan.serializers import RolleSerializer


ROLLEN_URL = reverse('katplan:rolle-list')


def sample_rolle():
    return Rolle.objects.create(
        kuerzel='T0001',
        name='Test'
    )


def detail_url(rolle_id):
    """Return rolle detail URL"""
    return reverse('katplan:rolle-detail', args=[rolle_id])


class PublicRolleApiTests(TestCase):
    """Test the publicly available rolle API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(ROLLEN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRolleApiTests(TestCase):
    """Test the authorized user rolle API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_rolle(self):
        """Test retrieving rolle"""
        sample_rolle()

        res = self.client.get(ROLLEN_URL)

        module = Rolle.objects.all().order_by('-kuerzel')
        serializer = RolleSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_rolle_successful(self):
        """Test creating rolle"""
        payload = {
            'kuerzel': 'T1',
            'name': 'Text',
            'beschreibung': '...'
        }
        res = self.client.post(ROLLEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        rolle = Rolle.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(rolle, key))

    def test_create_invalid_rolle(self):
        """Test the invalid creation"""
        payload = {'name': ''}
        res = self.client.post(ROLLEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_rolle(self):
        """Test updating a rolle with patch"""
        rolle = sample_rolle()

        payload = {'name': 'Testpatch'}
        url = detail_url(rolle.id)
        self.client.patch(url, payload)

        rolle.refresh_from_db()
        self.assertEqual(rolle.name, payload['name'])

    def test_full_update_rolle(self):
        """Test updating a rolle with put"""
        rolle = sample_rolle()

        payload = {'kuerzel': 'P1', 'name': 'Testpatch'}
        url = detail_url(rolle.id)
        self.client.put(url, payload)

        rolle.refresh_from_db()
        self.assertEqual(rolle.kuerzel, payload['kuerzel'])
        self.assertEqual(rolle.name, payload['name'])

    def test_delete_successfull(self):
        """Test the deleting"""
        rolle = sample_rolle()

        url = detail_url(rolle.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
