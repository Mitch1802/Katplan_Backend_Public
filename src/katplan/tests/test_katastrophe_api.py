from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Katastrophe

from katplan.serializers import KatastropheSerializer


KATASTROPHE_URL = reverse('katplan:katastrophe-list')


def sample_katastrophe():
    """Return a sample katastrophe"""
    return Katastrophe.objects.create(
        kuerzel='T0001',
        name='Test',
        beschreibung='Text'
    )


def detail_url(katastrophe_id):
    """Return katastrophe detail URL"""
    return reverse('katplan:katastrophe-detail', args=[katastrophe_id])


class PublicKatastropheApiTests(TestCase):
    """Test the publicly available katastrophe API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(KATASTROPHE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateKatastropheApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_katastrophe(self):
        """Test retrieving tags"""
        sample_katastrophe()

        res = self.client.get(KATASTROPHE_URL)

        katastrophe = Katastrophe.objects.all().order_by('-kuerzel')
        serializer = KatastropheSerializer(katastrophe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_katastrophe_successful(self):
        """Test creating katastrophe"""
        payload = {
            'kuerzel': 'T1',
            'name': 'Text',
            'beschreibung': '...'
        }
        res = self.client.post(KATASTROPHE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        katastrophe = Katastrophe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(katastrophe, key))

    def test_create_invalid_katastrophe(self):
        """Test the invalid creation"""
        payload = {'name': ''}
        res = self.client.post(KATASTROPHE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_katastrophe(self):
        """Test updating a katastrophe with patch"""
        katastrophe = sample_katastrophe()

        payload = {'name': 'Testpatch'}
        url = detail_url(katastrophe.id)
        self.client.patch(url, payload)

        katastrophe.refresh_from_db()
        self.assertEqual(katastrophe.name, payload['name'])

    def test_full_update_katastrophe(self):
        """Test updating a katastrophe with put"""
        katastrophe = sample_katastrophe()

        payload = {'kuerzel': 'P1', 'name': 'Testpatch'}
        url = detail_url(katastrophe.id)
        self.client.put(url, payload)

        katastrophe.refresh_from_db()
        self.assertEqual(katastrophe.kuerzel, payload['kuerzel'])
        self.assertEqual(katastrophe.name, payload['name'])

    def test_delete_successfull(self):
        """Test the deleting"""
        katastrophe = sample_katastrophe()

        url = detail_url(katastrophe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
