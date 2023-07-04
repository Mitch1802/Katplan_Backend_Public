from rest_framework import serializers

from core.models import Modul, Katastrophe, Gefahr, Massnahme, \
                        Rolle, Dokument, Fahrzeug, KMaterial, \
                        Kontakt, FahrzeugFoto


class ModulSerializer(serializers.ModelSerializer):
    """Serializer for modul objects"""

    class Meta:
        model = Modul
        fields = '__all__'
        read_only_fields = ('id',)


class KatastropheSerializer(serializers.ModelSerializer):
    """Serializer for katastrophe objects"""

    class Meta:
        model = Katastrophe
        fields = '__all__'
        read_only_fields = ('id',)


class GefahrSerializer(serializers.ModelSerializer):
    """Serializer for gefahr objects"""

    class Meta:
        model = Gefahr
        fields = '__all__'
        read_only_fields = ('id',)


class MassnahmeSerializer(serializers.ModelSerializer):
    """Serializer for massnahme objects"""

    class Meta:
        model = Massnahme
        fields = '__all__'
        read_only_fields = ('id',)


class RolleSerializer(serializers.ModelSerializer):
    """Serializer for rolle objects"""

    class Meta:
        model = Rolle
        fields = '__all__'
        read_only_fields = ('id',)


class KontaktSerializer(serializers.ModelSerializer):
    """Serializer for kontakt objects"""

    class Meta:
        model = Kontakt
        fields = '__all__'
        read_only_fields = ('id',)


class DokumentSerializer(serializers.ModelSerializer):
    """Serializer for dokument objects"""

    class Meta:
        model = Dokument
        fields = '__all__'
        read_only_fields = ('id',)


class FahrzeugSerializer(serializers.ModelSerializer):
    """Serializer for fahrzeug objects"""

    class Meta:
        model = Fahrzeug
        fields = '__all__'
        read_only_fields = ('id',)


class FahrzeugFotoSerializer(serializers.ModelSerializer):
    """ Serializes FahrzeugFotos"""

    class Meta:
        model = FahrzeugFoto
        fields = '__all__'


class KMaterialSerializer(serializers.ModelSerializer):
    """Serializer for kmaterial objects"""

    class Meta:
        model = KMaterial
        fields = '__all__'
        read_only_fields = ('id',)
