# from urllib import response

from django.shortcuts import get_object_or_404

# from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, FormParser, \
    MultiPartParser

from core.models import Modul, Katastrophe, Gefahr, Massnahme, \
    Rolle, Dokument, KMaterial, Kontakt, \
    Fahrzeug, FahrzeugFoto

from katplan import serializers


class ModulViewSet(viewsets.ModelViewSet):
    """Manage module in the database"""
    serializer_class = serializers.ModulSerializer
    queryset = Modul.objects.all().order_by('-reihenfolge').reverse()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        mod_queryset = self.filter_queryset(self.get_queryset())
        mod_serializer = self.get_serializer(mod_queryset, many=True)

        kat_queryset = Katastrophe.objects.all()
        gef_queryset = Gefahr.objects.all()
        mas_queryset = Massnahme.objects.all()
        rol_queryset = Rolle.objects.all()
        kon_queryset = Kontakt.objects.all()
        dok_queryset = Dokument.objects.all()
        fahr_queryset = Fahrzeug.objects.all()
        fahrf_queryset = FahrzeugFoto.objects.all()
        kmat_queryset = KMaterial.objects.all()

        kat_serializer = serializers.KatastropheSerializer(
            kat_queryset, many=True)
        gef_serializer = serializers.GefahrSerializer(gef_queryset, many=True)
        mas_serializer = serializers.MassnahmeSerializer(
            mas_queryset, many=True)
        rol_serializer = serializers.RolleSerializer(rol_queryset, many=True)
        kon_serializer = serializers.KontaktSerializer(kon_queryset, many=True)
        dok_serializer = serializers.DokumentSerializer(
            dok_queryset, many=True)
        fahr_serializer = serializers.FahrzeugSerializer(
            fahr_queryset, many=True)
        fahrf_serializer = serializers.FahrzeugFotoSerializer(
            fahrf_queryset, many=True)
        kmat_serializer = serializers.KMaterialSerializer(
            kmat_queryset, many=True)

        return Response({
            'modul': 'Modul',
            'modulDaten': mod_serializer.data,
            'katastrophen': kat_serializer.data,
            'gefahren': gef_serializer.data,
            'massnahmen': mas_serializer.data,
            'rollen': rol_serializer.data,
            'kontakte': kon_serializer.data,
            'dokumente': dok_serializer.data,
            'fahrzeuge': fahr_serializer.data,
            'kmaterial': kmat_serializer.data,
            'gkatastrophen': kat_serializer.data,
            'ggefahren': gef_serializer.data,
            'gmassnahmen': mas_serializer.data,
            'grollen': rol_serializer.data,
            'gkontakte': kon_serializer.data,
            'gfahrzeuge': fahr_serializer.data,
            'gfahrzeugfotos': fahrf_serializer.data
        })


class KatastropheViewSet(viewsets.ModelViewSet):
    """Manage katastrophe in the database"""
    serializer_class = serializers.KatastropheSerializer
    queryset = Katastrophe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        kat_queryset = self.filter_queryset(self.get_queryset())
        gef_queryset = Gefahr.objects.all()
        rol_queryset = Rolle.objects.all()
        mas_queryset = Massnahme.objects.all()

        kat_serializer = self.get_serializer(kat_queryset, many=True)
        gef_serializer = serializers.GefahrSerializer(gef_queryset, many=True)
        rol_serializer = serializers.RolleSerializer(rol_queryset, many=True)
        mas_serializer = serializers.MassnahmeSerializer(
            mas_queryset, many=True)

        return Response({
            'modul': 'Katastrophen',
            'modulDaten': kat_serializer.data,
            'gefahren': gef_serializer.data,
            'rollen': rol_serializer.data,
            'massnahmen': mas_serializer.data
        })

    def retrieve(self, request, pk=None):
        kat_queryset = self.filter_queryset(self.get_queryset())
        gef_queryset = Gefahr.objects.all()
        rol_queryset = Rolle.objects.all()
        mas_queryset = Massnahme.objects.all()

        kat_check = get_object_or_404(kat_queryset, pk=pk)

        kat_serializer = self.get_serializer(kat_check)
        gef_serializer = serializers.GefahrSerializer(gef_queryset, many=True)
        rol_serializer = serializers.RolleSerializer(rol_queryset, many=True)
        mas_serializer = serializers.MassnahmeSerializer(
            mas_queryset, many=True)

        return Response({
            'modulDaten': kat_serializer.data,
            'gefahren': gef_serializer.data,
            'rollen': rol_serializer.data,
            'massnahmen': mas_serializer.data
        })


class GefahrViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Gefahren"""
    serializer_class = serializers.GefahrSerializer
    queryset = Gefahr.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        gef_queryset = self.filter_queryset(self.get_queryset())
        mas_queryset = Massnahme.objects.all()
        rol_queryset = Rolle.objects.all()
        dok_queryset = Dokument.objects.all()

        gef_serializer = self.get_serializer(gef_queryset, many=True)
        mas_serializer = serializers.MassnahmeSerializer(
            mas_queryset, many=True)
        rol_serializer = serializers.RolleSerializer(
            rol_queryset, many=True)
        dok_serializer = serializers.DokumentSerializer(
            dok_queryset, many=True)

        return Response({
            'modul': 'Gefahren',
            'modulDaten': gef_serializer.data,
            'massnahmen': mas_serializer.data,
            'rollen': rol_serializer.data,
            'dokumente': dok_serializer.data
        })

    def retrieve(self, request, pk=None):
        gef_queryset = self.filter_queryset(self.get_queryset())
        mas_queryset = Massnahme.objects.all()
        rol_queryset = Rolle.objects.all()
        dok_queryset = Dokument.objects.all()

        gef_check = get_object_or_404(gef_queryset, pk=pk)

        gef_serializer = self.get_serializer(gef_check)
        mas_serializer = serializers.MassnahmeSerializer(
            mas_queryset, many=True)
        rol_serializer = serializers.RolleSerializer(
            rol_queryset, many=True)
        dok_serializer = serializers.DokumentSerializer(
            dok_queryset, many=True)

        return Response({
            'modulDaten': gef_serializer.data,
            'massnahmen': mas_serializer.data,
            'rollen': rol_serializer.data,
            'dokumente': dok_serializer.data
        })


class MassnahmeViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Massnahmen"""
    serializer_class = serializers.MassnahmeSerializer
    queryset = Massnahme.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        mas_queryset = self.filter_queryset(self.get_queryset())
        kon_queryset = Kontakt.objects.all()
        fahr_queryset = Fahrzeug.objects.all()

        mas_serializer = self.get_serializer(mas_queryset, many=True)
        kon_serializer = serializers.KontaktSerializer(kon_queryset, many=True)
        fahr_serializer = serializers.FahrzeugSerializer(
            fahr_queryset, many=True)

        return Response({
            'modul': 'Massnahmen',
            'modulDaten': mas_serializer.data,
            'kontakte': kon_serializer.data,
            'fahrzeuge': fahr_serializer.data
        })

    def retrieve(self, request, pk=None):
        mas_queryset = self.filter_queryset(self.get_queryset())
        kon_queryset = Kontakt.objects.all()
        fahr_queryset = Fahrzeug.objects.all()

        mas_check = get_object_or_404(mas_queryset, pk=pk)

        mas_serializer = self.get_serializer(mas_check)
        kon_serializer = serializers.KontaktSerializer(kon_queryset, many=True)
        fahr_serializer = serializers.FahrzeugSerializer(
            fahr_queryset, many=True)

        return Response({
            'modulDaten': mas_serializer.data,
            'kontakte': kon_serializer.data,
            'fahrzeuge': fahr_serializer.data
        })


class RolleViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Rollen"""
    serializer_class = serializers.RolleSerializer
    queryset = Rolle.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        rol_queryset = self.filter_queryset(self.get_queryset())
        kon_queryset = Kontakt.objects.all()

        rol_serializer = self.get_serializer(rol_queryset, many=True)
        kon_serializer = serializers.KontaktSerializer(kon_queryset, many=True)

        return Response({
            'modul': 'Rollen',
            'modulDaten': rol_serializer.data,
            'kontakte': kon_serializer.data
        })

    def retrieve(self, request, pk=None):
        rol_queryset = self.filter_queryset(self.get_queryset())
        kon_queryset = Kontakt.objects.all()

        rol_check = get_object_or_404(rol_queryset, pk=pk)

        rol_serializer = self.get_serializer(rol_check)
        rolG_serializer = self.get_serializer(rol_queryset, many=True)
        kon_serializer = serializers.KontaktSerializer(kon_queryset, many=True)

        return Response({
            'modulDaten': rol_serializer.data,
            'rollen': rolG_serializer.data,
            'kontakte': kon_serializer.data
        })


class KontaktViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Kontakte"""
    serializer_class = serializers.KontaktSerializer
    queryset = Kontakt.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'modul': 'Kontakte',
            'modulDaten': serializer.data
        })

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())

        check = get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(check)

        return Response({
            'modulDaten': serializer.data
        })


class DokumentViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Dokumente"""
    parser_classes = (MultiPartParser, FormParser, )
    serializer_class = serializers.DokumentSerializer
    queryset = Dokument.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_class = (FileUploadParser,)

    def list(self, request, *args):
        dok_queryset = self.filter_queryset(self.get_queryset())
        dok_serializer = self.get_serializer(dok_queryset, many=True)

        return Response({
            'modul': 'Dokumente',
            'modulDaten': dok_serializer.data
        })

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        check = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(check)

        return Response({
            'modulDaten': serializer.data
        })

    # def post(self, request, *args, **kwargs):
    #     file_serializer = self.serializer_class(data=request.data)

    #     if file_serializer.is_valid():
    #         file_serializer.save()
    #         return Response({'modulDaten': file_serializer.data},
    #                         status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(file_serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
    
    # def destroy(self, request, pk=None):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # check = get_object_or_404(queryset, pk=pk)
    #     serializer = self.get_serializer(queryset)

    #     return Response({
    #         'modulDaten': serializer.data
    #     })


class FahrzeugViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating Fahrzeuge"""
    serializer_class = serializers.FahrzeugSerializer
    queryset = Fahrzeug.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        fahr_queryset = self.filter_queryset(self.get_queryset())

        fahr_serializer = self.get_serializer(fahr_queryset, many=True)

        return Response({
            'modul': 'Fahrzeuge',
            'modulDaten': fahr_serializer.data
        })

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        check = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(check)

        fotos_queryset = FahrzeugFoto.objects.filter(fahrzeug=pk)
        fotos_serializer = serializers.FahrzeugFotoSerializer(
            fotos_queryset, many=True)

        return Response({
            'modulDaten': serializer.data,
            'fotos': fotos_serializer.data
        })


class FahrzeugFotoViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating FahrzeugFoto"""
    serializer_class = serializers.FahrzeugFotoSerializer
    queryset = FahrzeugFoto.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_class = (FileUploadParser,)

    # Post
    def create(self, request, *args, **kwargs):
        file_serializer = self.serializer_class(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            fzg = file_serializer.data["fahrzeug"]
            fotos_queryset = FahrzeugFoto.objects.filter(fahrzeug=fzg)
            fotos_serializer = serializers.FahrzeugFotoSerializer(
                fotos_queryset, many=True)

            return Response({'modulDaten': fotos_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = FahrzeugFoto.objects.all()
        filterColoumn = self.request.query_params.get('fahrzeug')
        if filterColoumn is not None:
            queryset = queryset.filter(fahrzeug=filterColoumn)
        return queryset

    def get(self, request):
        fahr_queryset = self.queryset(self.get_queryset())
        fahr_serializer = self.get_serializer(fahr_queryset, many=True)

        return Response({
            'modul': 'FahrzeugFotos',
            'modulDaten': fahr_serializer.data
        })

    def list(self, request):
        fahr_queryset = self.filter_queryset(self.get_queryset())
        fahr_serializer = self.get_serializer(fahr_queryset, many=True)

        return Response({
            'modul': 'FahrzeugFotos',
            'modulDaten': fahr_serializer.data
        })

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        check = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(check)

        return Response({
            'modulDaten': serializer.data
        })


class KMaterialViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating KMaterial"""
    serializer_class = serializers.KMaterialSerializer
    queryset = KMaterial.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        mat_queryset = self.filter_queryset(self.get_queryset())

        mat_serializer = self.get_serializer(mat_queryset, many=True)

        return Response({
            'modul': 'KMaterial',
            'modulDaten': mat_serializer.data
        })

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())

        check = get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(check)

        return Response({
            'modulDaten': serializer.data
        })
