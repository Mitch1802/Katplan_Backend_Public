import uuid
import os
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


def dokument_file_path(instance, filename):
    """Generate file path for new dokument file"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('dokumente/', filename)


def fahrzeug_image_file_path(instance, filename):
    """Generate file path for new fahrzeug image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('fahrzeugfotos/', filename)


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Creates and saves a new super user"""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_verwaltung = True
        user.is_benutzerverwaltung = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports username"""
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verwaltung = models.BooleanField(default=False)
    is_benutzerverwaltung = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta: 
        verbose_name = ("Benutzer")
        verbose_name_plural = ("Benutzer")
        ordering = ('-username',)


class Modul(models.Model):
    """Modul object"""
    bezeichnung = models.CharField(max_length=255, help_text='Help Text')
    kuerzel = models.CharField(max_length=5)
    icon = models.CharField(max_length=50)
    reihenfolge = models.IntegerField(null=True)
    permissions = models.JSONField(null=True, default=list)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bezeichnung


class Katastrophe(models.Model):
    """Katastrophe object"""
    kuerzel = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    beschreibung = models.TextField(blank=True)
    rollen = models.JSONField(null=True, default=list)
    massnahmen = models.JSONField(null=True, default=list)
    gefahren = models.JSONField(null=True, default=list)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gefahr(models.Model):
    """Gefahr object"""
    kuerzel = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    beschreibung = models.TextField(blank=True)
    ausloeser = models.CharField(max_length=255, blank=True)
    feld1Name = models.CharField(max_length=255, blank=True)
    feld1Value = models.CharField(max_length=255, blank=True)
    feld2Name = models.CharField(max_length=255, blank=True)
    feld2Value = models.CharField(max_length=255, blank=True)
    feld3Name = models.CharField(max_length=255, blank=True)
    feld3Value = models.CharField(max_length=255, blank=True)
    feld4Name = models.CharField(max_length=255, blank=True)
    feld4Value = models.CharField(max_length=255, blank=True)
    feld5Name = models.CharField(max_length=255, blank=True)
    feld5Value = models.CharField(max_length=255, blank=True)
    folgen = models.CharField(max_length=255, blank=True)
    gefahren = models.CharField(max_length=255, blank=True)
    rollen = models.JSONField(null=True, default=list)
    massnahmen = models.JSONField(null=True, default=list)
    dokumente = models.JSONField(null=True, default=list)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Massnahme(models.Model):
    """Massnahme object"""
    kuerzel = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    beschreibung = models.TextField(blank=True)
    kategorie = models.CharField(max_length=255, blank=True)
    verantwortung = models.CharField(max_length=255, blank=True)
    verstaendigung = models.JSONField(null=True, default=list)
    staerke = models.IntegerField(null=True)
    fahrzeuge = models.JSONField(null=True, default=list)
    feld1Name = models.CharField(max_length=255, blank=True)
    feld1Value = models.CharField(max_length=255, blank=True)
    feld2Name = models.CharField(max_length=255, blank=True)
    feld2Value = models.CharField(max_length=255, blank=True)
    feld3Name = models.CharField(max_length=255, blank=True)
    feld3Value = models.CharField(max_length=255, blank=True)
    feld4Name = models.CharField(max_length=255, blank=True)
    feld4Value = models.CharField(max_length=255, blank=True)
    feld5Name = models.CharField(max_length=255, blank=True)
    feld5Value = models.CharField(max_length=255, blank=True)
    durchfuehrung = models.TextField(blank=True)
    rueckbau = models.TextField(blank=True)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Rolle(models.Model):
    """Rolle object"""
    kuerzel = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    beschreibung = models.TextField(blank=True)
    erreichbarkeit = models.JSONField(null=True, default=list)
    notruf = models.CharField(max_length=255, blank=True)
    aufgaben = models.TextField(blank=True)
    verstaendigung = models.JSONField(null=True, default=list)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Kontakt(models.Model):
    """Kontakt object"""
    kuerzel = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    funktion = models.CharField(max_length=255, blank=True)
    telefon = models.CharField(max_length=255, blank=True)
    telefon2 = models.CharField(max_length=255, blank=True)
    telefon3 = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Dokument(models.Model):
    """Dokument object"""
    kuerzel = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    file = models.FileField(null=True, upload_to=dokument_file_path)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)  # Call the "real" delete() method.


@receiver(models.signals.pre_save, sender=Dokument)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Fahrzeug(models.Model):
    """Fahrzeug object"""
    kuerzel = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    fahrzeug = models.BooleanField(default=False)
    anhaenger = models.BooleanField(default=False)
    type = models.CharField(max_length=255, blank=True)
    lenkerberechtigung = models.CharField(max_length=1, blank=True)
    stationierung = models.CharField(max_length=255, blank=True)
    personenkapazitaet = models.IntegerField(null=True)
    treibstoff = models.CharField(max_length=50, blank=True)
    nutzlast = models.IntegerField(null=True)
    ladebordwand = models.BooleanField(default=False)
    ladekran = models.BooleanField(default=False)
    wassertank = models.CharField(max_length=255, blank=True)
    wassertankAbnehmbar = models.BooleanField(default=False)
    geschlossenerAufbau = models.BooleanField(default=False)
    wechselaufbau = models.TextField(blank=True)
    anhaengervorrichtung = models.CharField(max_length=255, blank=True)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FahrzeugFoto(models.Model):
    """Database model for picture of fahrzeuge"""
    fahrzeug = models.ForeignKey(Fahrzeug, on_delete=models.CASCADE)
    file = models.FileField(null=True,
                            upload_to=fahrzeug_image_file_path, max_length=255)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)  # Call the "real" delete() method.


class KMaterial(models.Model):
    """KMaterial object"""
    artikel = models.CharField(max_length=255)
    bemerkung = models.CharField(max_length=255, blank=True)
    menge = models.IntegerField(null=True)
    stationierungsort = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.artikel
