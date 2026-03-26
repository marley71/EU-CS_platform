from django.contrib import admin
from .models import (Project, Topic, Status, ApprovedProjects, FollowedProjects,
                     Provincia, HasTag, DifficultyLevel, ParticipationTask, HelpText, ProjectCountry, BDSWeek)
from .forms import STATO_TYPE_CHOICES
from django import forms
from django.db import models
from django_select2.forms import Select2MultipleWidget
from django_ckeditor_5.fields import CKEditor5Widget
from modeltranslation.admin import TabbedTranslationAdmin
from django.utils.translation import ugettext_lazy as _
#from provincia.models import Provincia
from django.core.exceptions import ValidationError
from django.http import Http404

from localita.models import Localita


class DifficultyLevelAdmin(TabbedTranslationAdmin):
    list_display = ('difficultyLevel',)
    pass

class ProjectFormA(forms.ModelForm):
    topic = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(), widget=Select2MultipleWidget, required=False)
    provincia = forms.ModelMultipleChoiceField(queryset=Provincia.objects.all(), widget=Select2MultipleWidget, required=False)
    stato = forms.ChoiceField(
        choices=STATO_TYPE_CHOICES,
        widget=forms.Select(),
        help_text=_('Please indicate project status'),
        label=_('Status type'),
        required=True
    )
    # provincia = forms.ModelChoiceField(
    #     queryset=Provincia.objects.all().order_by('nome'),
    #     label=_("Provincia"),
    #     widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
    #     help_text=_('Please, select provincia of your project.'))
    # projectCountry = forms.ModelChoiceField(
    #     queryset=ProjectCountry.objects.all(),
    #     widget=forms.Select,
    # )
    class Meta:
        model = Project
        exclude = ('origin',)

class HasTagAdmin(TabbedTranslationAdmin):
    list_display = ('hasTag',)
    pass

class ParticipationTaskAdmin(TabbedTranslationAdmin):
    list_display = ('participationTask',)
    pass

class ProjectAdmin(TabbedTranslationAdmin):
    list_filter = ('creator', 'status', )
    form = ProjectFormA
    exclude = ('projectCountry', 'projectlocality', 'projectGeographicLocation','localita' )
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }

    def save_model(self, request, obj, form, change):
        # Calcola il valore di price (ad esempio, impostalo a un valore arbitrario)
        localita = None
        if obj.provincia is not None and obj.provincia.first():
            localita = Localita.objects.get(name=obj.provincia.first().regione)

        if localita == None:
            raise Http404("Località non trovata.")
        obj.localita = localita
        super().save_model(request, obj, form, change)
    pass

class StatusAdmin(TabbedTranslationAdmin):
    list_display = ('status',)
    pass

class TopicAdmin(TabbedTranslationAdmin):
    list_display = ('topic',)
    pass

class HelpTextAdmin(TabbedTranslationAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }
    pass

class ProjectCountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country', 'latitude', 'longitude')
    search_fields = ('country_name', 'country')  # Asumiendo que 'country' es un campo accesible

admin.site.register(DifficultyLevel, DifficultyLevelAdmin)
admin.site.register(HasTag, HasTagAdmin)
admin.site.register(ParticipationTask, ParticipationTaskAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCountry, ProjectCountryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(HelpText, HelpTextAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(ApprovedProjects)
admin.site.register(FollowedProjects)
admin.site.register(BDSWeek)

