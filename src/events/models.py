from django.db import models
from django.conf import settings
from projects.models import Project
from organisations.models import Organisation
from django.utils import timezone
from django.utils.translation import get_language
from datetime import datetime, timedelta
import pytz

class HelpText(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    paragraph = models.TextField()

class Event(models.Model):
    creator = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True,
            blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    place = models.CharField(max_length=200, blank=True, default='On-line')
    country = models.CharField(null=True, blank=True, max_length=50)
    start_date = models.DateTimeField('Start date')
    end_date = models.DateTimeField('End date')
    hour = models.TimeField(null=True, blank=True)
    language_other = models.CharField(max_length=200, null=True)
    timezone = models.CharField(max_length=100, choices=[(tz, tz) for tz in pytz.all_timezones], default='Europe/Brussels')
    #TODO: reference this to settings
    language = models.CharField(max_length=20, choices=[
        ('NL', 'Dutch'),
        ('EN', 'English'),
        ('ET', 'Estonian'),
        ('FR', 'Français'),
        ('DE', 'German'),
        ('EL', 'Greek'),
        ('HU', 'Hungarian'),
        ('IT', 'Italian'),
        ('LT', 'Lituanian'),
        ('PT', 'Portuguese'),
        ('ES', 'Spanish'),
        ('SV', 'Swedish'),
        ('OT', 'Other'),
    ], default='EN')
    url = models.URLField(max_length=200, blank=True)
    featured = models.BooleanField(null=True, default=False)
    # TODO: This a a fixture
    event_type = models.CharField(max_length=20, choices=[
        ('online', 'On-line'),
        ('face-to-face', 'In presenza'),
        ('hybrid', 'Evento ibrido'),
    ], default='online')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='events_associated')
    mainOrganisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='events_coordinated')
    organisations = models.ManyToManyField(Organisation, blank=True)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.now())
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def language_calc(self):
        if self.language == 'OT': return  self.language_other
        return self.language  #TODO mettere la traduzione

    @property
    def place_calc(self):
        current_language = (get_language() or settings.LANGUAGE_CODE or "en").lower()
        is_italian = current_language.startswith("it")

        online_label = "On-line" if is_italian else "Online"
        hybrid_suffix = " (Ev. ibrido)" if is_italian else " (Hybrid event)"
        presenza_label = "In presenza" if is_italian else "In presence"
        if self.event_type == "online":
            return online_label
        # if self.event_type == "face-to-face":
        #     return self.place
        if self.event_type == "face-to-face":
            return f"{presenza_label}"
        if self.event_type == "hybrid":
            return f"{self.place}{hybrid_suffix}"
        return ""

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title


class ApprovedEvents(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event}'


class UnApprovedEvents(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event}'
