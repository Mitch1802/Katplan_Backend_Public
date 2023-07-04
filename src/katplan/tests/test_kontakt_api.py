from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Kontakt

from katplan.serializers import KontaktSerializer


KONTAKTE_URL = reverse('katplan:kontakt-list')


def sample_kontakt():
    return Kontakt.objects.create(
        kuerzel='T0001',
        name='Test'
    )


def detail_url(kontakt_id):
    """Return kontakt detail URL"""
    return reverse('katplan:kontakt-detail', args=[kontakt_id])


class PublicKontaktApiTests(TestCase):
    """Test the publicly available kontakt API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(KONTAKTE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateKontaktApiTests(TestCase):
    """Test the authorized user kontakt API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_kontakt(self):
        """Test retrieving kontakt"""
        sample_kontakt()

        res = self.client.get(KONTAKTE_URL)

        module = Kontakt.objects.all().order_by('-kuerzel')
        serializer = KontaktSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_kontakt_successful(self):
        """Test creating kontakt"""
        payload = {
            'kuerzel': 'T1',
            'name': 'Text'
        }
        res = self.client.post(KONTAKTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        kontakt = Kontakt.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(kontakt, key))

    def test_create_invalid_kontakt(self):
        """Test the invalid creation"""
        payload = {'name': ''}
        res = self.client.post(KONTAKTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_kontakt(self):
        """Test updating a kontakt with patch"""
        kontakt = sample_kontakt()

        payload = {'name': 'Testpatch'}
        url = detail_url(kontakt.id)
        self.client.patch(url, payload)

        kontakt.refresh_from_db()
        self.assertEqual(kontakt.name, payload['name'])

    def test_full_update_kontakt(self):
        """Test updating a kontakt with put"""
        kontakt = sample_kontakt()

        payload = {'kuerzel': 'P1', 'name': 'Testpatch'}
        url = detail_url(kontakt.id)
        self.client.put(url, payload)

        kontakt.refresh_from_db()
        self.assertEqual(kontakt.kuerzel, payload['kuerzel'])
        self.assertEqual(kontakt.name, payload['name'])

    def test_delete_successfull(self):
        """Test the deleting"""
        kontakt = sample_kontakt()

        url = detail_url(kontakt.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
