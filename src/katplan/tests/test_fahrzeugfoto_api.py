# import tempfile
# import os

# from PIL import Image

# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse

# from rest_framework import status
# from rest_framework.test import APIClient

# from core.models import Fahrzeug, FahrzeugFoto

# # from katplan.serializers import FahrzeugSerializer, FahrzeugFotoSerializer


# FAHRZEUGFOTOS_URL = reverse('katplan:fahrzeugfoto-list')


# def image_upload_url(fahrzeugfoto_id):
#     """Return URL for fahrzeugfoto image upload"""
#     return reverse('katplan:fahrzeugfoto-upload-image', 
#                    args=[fahrzeugfoto_id])


# def sample_fahrzeug():
#     return Fahrzeug.objects.create(
#         kuerzel='T0001',
#         name='Test'
#     )

# def sample_fahrzeugfoto():
#     return FahrzeugFoto.objects.create(
#         fahrzeug=sample_fahrzeug()
#     )


# class FahrzeugFotoImageUploadTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'user@michael-web.at',
#             'testpass'
#         )
#         self.client.force_authenticate(self.user)
#         self.fahrzeugfoto = sample_fahrzeugfoto()

#     def tearDown(self):
#         self.fahrzeugfoto.file.delete()

#     def test_upload_image_to_fahrzeugfoto(self):
#         """Test uploading an image to fahrzeugfoto"""
#         # url = image_upload_url(self.fahrzeugfoto.id)
#         with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
#             img = Image.new('RGB', (10, 10))
#             img.save(ntf, format='JPEG')
#             ntf.seek(0)
#             res = self.client.post(FAHRZEUGFOTOS_URL, {'fahrzeug': sample_fahrzeug, 
#                                    'file': ntf}, format='multipart')

#         self.fahrzeugfoto.refresh_from_db()

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn('file', res.data)
#         self.assertTrue(os.path.exists(self.fahrzeug.file.path))

#     def test_upload_image_bad_request(self):
#         """Test uploading an invalid image"""
#         # url = image_upload_url(self.fahrzeugfoto.id)
#         res = self.client.post(FAHRZEUGFOTOS_URL, {'fahrzeug': sample_fahrzeug, 
#                                'file': 'notimage'}, format='multipart')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
