from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Massnahme

from katplan.serializers import MassnahmeSerializer


MASSNAHMEN_URL = reverse('katplan:massnahme-list')


def sample_massnahme():
    return Massnahme.objects.create(
        kuerzel='T0001',
        name='Test'
    )


def detail_url(massnahme_id):
    """Return massnahme detail URL"""
    return reverse('katplan:massnahme-detail', args=[massnahme_id])


class PublicMassnahmeApiTests(TestCase):
    """Test the publicly available massnahme API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(MASSNAHMEN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMassnahmeApiTests(TestCase):
    """Test the authorized user massnahme API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_massnahme(self):
        """Test retrieving massnahme"""
        sample_massnahme()

        res = self.client.get(MASSNAHMEN_URL)

        module = Massnahme.objects.all().order_by('-kuerzel')
        serializer = MassnahmeSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_massnahme_successful(self):
        """Test creating massnahme"""
        payload = {
            'kuerzel': 'T1',
            'name': 'Text',
            'beschreibung': '...'
        }
        res = self.client.post(MASSNAHMEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        massnahme = Massnahme.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(massnahme, key))

    def test_create_invalid_massnahme(self):
        """Test the invalid creation"""
        payload = {'name': ''}
        res = self.client.post(MASSNAHMEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_massnahme(self):
        """Test updating a massnahme with patch"""
        massnahme = sample_massnahme()

        payload = {'name': 'Testpatch'}
        url = detail_url(massnahme.id)
        self.client.patch(url, payload)

        massnahme.refresh_from_db()
        self.assertEqual(massnahme.name, payload['name'])

    def test_full_update_massnahme(self):
        """Test updating a massnahme with put"""
        massnahme = sample_massnahme()

        payload = {'kuerzel': 'P1', 'name': 'Testpatch'}
        url = detail_url(massnahme.id)
        self.client.put(url, payload)

        massnahme.refresh_from_db()
        self.assertEqual(massnahme.kuerzel, payload['kuerzel'])
        self.assertEqual(massnahme.name, payload['name'])

    def test_delete_successfull(self):
        """Test the deleting"""
        massnahme = sample_massnahme()

        url = detail_url(massnahme.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
