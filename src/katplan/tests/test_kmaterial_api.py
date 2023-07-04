from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import KMaterial

from katplan.serializers import KMaterialSerializer


KATASTROPHE_URL = reverse('katplan:kmaterial-list')


def sample_kmaterial():
    return KMaterial.objects.create(
        artikel='Test'
    )


def detail_url(kmaterial_id):
    """Return kmaterial detail URL"""
    return reverse('katplan:kmaterial-detail', args=[kmaterial_id])


class PublicKMaterialApiTests(TestCase):
    """Test the publicly available kmaterial API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(KATASTROPHE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateKMaterialApiTests(TestCase):
    """Test the authorized user kmaterial API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_kmaterial(self):
        """Test retrieving kmaterial"""
        sample_kmaterial()

        res = self.client.get(KATASTROPHE_URL)

        module = KMaterial.objects.all().order_by('-artikel')
        serializer = KMaterialSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_kmaterial_successful(self):
        """Test creating kmaterial"""
        payload = {
            'artikel': 'T1',
            'bemerkung': '...'
        }
        res = self.client.post(KATASTROPHE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        kmaterial = KMaterial.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(kmaterial, key))

    def test_create_invalid_kmaterial(self):
        """Test the invalid creation"""
        payload = {'artikel': ''}
        res = self.client.post(KATASTROPHE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_kmaterial(self):
        """Test updating a kmaterial with patch"""
        kmaterial = sample_kmaterial()

        payload = {'artikel': 'Testpatch'}
        url = detail_url(kmaterial.id)
        self.client.patch(url, payload)

        kmaterial.refresh_from_db()
        self.assertEqual(kmaterial.artikel, payload['artikel'])

    def test_full_update_kmaterial(self):
        """Test updating a kmaterial with put"""
        kmaterial = sample_kmaterial()

        payload = {'artikel': 'Testpatch'}
        url = detail_url(kmaterial.id)
        self.client.put(url, payload)

        kmaterial.refresh_from_db()
        self.assertEqual(kmaterial.artikel, payload['artikel'])

    def test_delete_successfull(self):
        """Test the deleting"""
        kmaterial = sample_kmaterial()

        url = detail_url(kmaterial.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
