from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Dokument

from katplan.serializers import DokumentSerializer


DOKUMENTE_URL = reverse('katplan:dokument-list')


def sample_dokument():
    return Dokument.objects.create(
        kuerzel='T0001',
        name='Test'
    )


def detail_url(dokument_id):
    """Return dokument detail URL"""
    return reverse('katplan:dokument-detail', args=[dokument_id])


class PublicDokumentApiTests(TestCase):
    """Test the publicly available dokument API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(DOKUMENTE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDokumentApiTests(TestCase):
    """Test the authorized user dokument API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_dokument(self):
        """Test retrieving dokument"""
        sample_dokument()

        res = self.client.get(DOKUMENTE_URL)

        module = Dokument.objects.all().order_by('-kuerzel')
        serializer = DokumentSerializer(module, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["modulDaten"], serializer.data)

    def test_create_dokument_successful(self):
        """Test creating dokument"""
        payload = {
            'kuerzel': 'T1',
            'name': 'Text'
        }
        res = self.client.post(DOKUMENTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        dokument = Dokument.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(dokument, key))

    def test_create_invalid_dokument(self):
        """Test the invalid creation"""
        payload = {'name': ''}
        res = self.client.post(DOKUMENTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_dokument(self):
        """Test updating a dokument with patch"""
        dokument = sample_dokument()

        payload = {'name': 'Testpatch'}
        url = detail_url(dokument.id)
        self.client.patch(url, payload)

        dokument.refresh_from_db()
        self.assertEqual(dokument.name, payload['name'])

    def test_full_update_dokument(self):
        """Test updating a dokument with put"""
        dokument = sample_dokument()

        payload = {'kuerzel': 'P1', 'name': 'Testpatch'}
        url = detail_url(dokument.id)
        self.client.put(url, payload)

        dokument.refresh_from_db()
        self.assertEqual(dokument.kuerzel, payload['kuerzel'])
        self.assertEqual(dokument.name, payload['name'])

    def test_delete_successfull(self):
        """Test the deleting"""
        dokument = sample_dokument()

        url = detail_url(dokument.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
