# from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(username='test', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):

    def test_create_user_with_username_successful(self):
        """Test creating a new user with an username is successful"""
        username = 'test'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_username(self):
        """Test creating user with no username raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # @patch('uuid.uuid4')
    # def test_recipe_file_name_uuid(self, mock_uuid):
    #     """Test that image is saved in the correct location"""
    #     uuid = 'test-uuid'
    #     mock_uuid.return_value = uuid
    #     file_path = models.recipe_image_file_path(None, 'myimage.jpg')

    #     exp_path = f'uploads/recipe/{uuid}.jpg'
    #     self.assertEqual(file_path, exp_path)

    def test_modul_str(self):
        """Test the modul string respresentation"""
        modul = models.Modul.objects.create(
            bezeichnung='Test',
            kuerzel='A',
            icon='icon',
            reihenfolge=0
        )

        self.assertEqual(str(modul), modul.bezeichnung)

    def test_katastrophe_str(self):
        """Test the katastrophe string respresentation"""
        katastrophe = models.Katastrophe.objects.create(
            kuerzel='K01',
            name='Test',
            beschreibung='Text',
            rollen=[],
            massnahmen=[],
            gefahren=[]
        )

        self.assertEqual(str(katastrophe), katastrophe.name)

    def test_gefahr_str(self):
        """Test the gefahr string respresentation"""
        gefahr = models.Gefahr.objects.create(
            kuerzel='T0001',
            name='Test',
            beschreibung='Text'
        )

        self.assertEqual(str(gefahr), gefahr.name)

    def test_massnahme_str(self):
        """Test the massnahme string respresentation"""
        massnahme = models.Massnahme.objects.create(
            kuerzel='T0001',
            name='Test',
            beschreibung='Text'
        )

        self.assertEqual(str(massnahme), massnahme.name)

    def test_rolle_str(self):
        """Test the rolle string respresentation"""
        rolle = models.Rolle.objects.create(
            kuerzel='T0001',
            name='Test',
            beschreibung='Text'
        )

        self.assertEqual(str(rolle), rolle.name)

    def test_kontakt_str(self):
        """Test the kontakt string respresentation"""
        kontakt = models.Kontakt.objects.create(
            kuerzel='T0001',
            name='Test'
        )

        self.assertEqual(str(kontakt), kontakt.name)

    def test_dokument_str(self):
        """Test the dokument string respresentation"""
        dokument = models.Dokument.objects.create(
            kuerzel='T0001',
            name='Test'
        )

        self.assertEqual(str(dokument), dokument.name)

    def test_fahrzeug_str(self):
        """Test the fahrzeug string respresentation"""
        fahrzeug = models.Fahrzeug.objects.create(
            kuerzel='T0001',
            name='Test'
        )

        self.assertEqual(str(fahrzeug), fahrzeug.name)

    def test_kmaterial_str(self):
        """Test the kmaterial string respresentation"""
        kmaterial = models.KMaterial.objects.create(
            artikel='Test',
            menge=0
        )

        self.assertEqual(str(kmaterial), kmaterial.artikel)
