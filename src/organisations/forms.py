from django import forms
from django_select2.forms import Select2MultipleWidget
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from .models import Organisation, OrganisationType
from localita.models import Localita
from projects.forms import getCountryCode
from ckeditor.widgets import CKEditorWidget
from django.conf import settings


class OrganisationForm(forms.Form):
        
    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)
        for lang_code in settings.MODELTRANSLATION_LANGUAGES:
            self.fields[f'description_{lang_code}'] = forms.CharField(
                help_text=_('Please briefly describe the organisation (max 3000 characters).'),
                widget=CKEditorWidget(config_name='frontpage'),
                max_length=3000,
                label=lang_code,
                required=lang_code == settings.MODELTRANSLATION_DEFAULT_LANGUAGE
            )

    def get_description_fields(self):
        for field_name in self.fields:
            return [self[field_name] for field_name in self.fields if field_name.startswith('description_')]
                    
        
    name = forms.CharField(
        max_length=200,
        help_text=_('Please write the name of the organisation.'),
        widget=forms.TextInput(),
        label=_('Name'))
    url = forms.URLField(
        max_length=200,
        label=_('URL'),
        help_text=_(
            'Please provide the URL to the website of the organisation.'),
        widget=forms.TextInput())
    orgType = forms.ModelChoiceField(
        queryset=OrganisationType.objects.all(),
        label=_("Type"),
        help_text=_('Please select one.'),
        widget=forms.Select(attrs={'class': 'js-example-basic-single'}))
    logo = forms.ImageField(
        required=False,
        help_text=_(
            'Please upload the logo of your organisation (.jpg or .png).'),
        widget=forms.FileInput)
    logo_credit = forms.CharField(
        max_length=300,
        required=False,
        label=_("Logo credit, if applicable"))
    image1 = forms.ImageField(
        required=False,
        help_text=_(
            'Please upload the image of your organisation (.jpg or .png).'),
        label=_('Organisation image'),
        widget=forms.FileInput)
    image1Credit = forms.CharField(
        max_length=300,
        required=False,
        label=_("Organisation image credit, if applicable"))

    x_1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y_1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width_1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height_1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    x_logo = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y_logo = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width_logo = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height_logo = forms.FloatField(widget=forms.HiddenInput(), required=False)

    contact_point = forms.CharField(
        max_length=100,
        help_text=_(
            'Please name the contact person or contact point for the organisation.'),
        label=_('Public contact point'),
        widget=forms.TextInput())
    contact_point_email = forms.EmailField(
        max_length=100,
        help_text=_(
            'Please provide the email address of the contact person or '
            'contact point. Note you will need permission to do that.'),
        widget=forms.TextInput(),
        label=_('Contact point email'))
    latitude = forms.DecimalField(
        max_digits=9, decimal_places=6, widget=forms.HiddenInput())
    longitude = forms.DecimalField(
        max_digits=9, decimal_places=6, widget=forms.HiddenInput())
    localita = forms.ModelChoiceField(
        queryset=Localita.objects.all(),
        label=_("Località"),
        widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
        help_text=_('Please, select località of your project.'))

    # TODO: I link this more to be used in others
    def save(self, args, images):
        print("In save")
        pk = self.data.get('organisationID', '')
        orgType = get_object_or_404(OrganisationType, id=self.data['orgType'])
        #localita = get_object_or_404(Localita, id=self.data['localita'])
        if (pk):
            organisation = get_object_or_404(Organisation, id=pk)
            organisation.name = self.data['name']
            organisation.url = self.data['url']
            organisation.orgType = orgType
            organisation.contactPoint = self.data['contact_point']
            organisation.contactPointEmail = self.data['contact_point_email']
            organisation.logoCredit = self.data['logo_credit']
            organisation.latitude = self.data['latitude']
            organisation.longitude = self.data['longitude']
            organisation.localita_id = self.data['localita']
            organisation.image1Credit = self.data['image1Credit']
        else:
            organisation = Organisation(
                name=self.data['name'],
                url=self.data['url'],
                creator=args.user,
                latitude=self.data['latitude'],
                longitude=self.data['longitude'],
                logoCredit=self.data['logo_credit'],
                image1Credit=self.data['image1Credit'],
                orgType=orgType,
                contactPoint=self.data['contact_point'],
                contactPointEmail=self.data['contact_point_email'],
                localita_id=self.data['localita'],
            )
            
        for key, value in self.data.items():
            if key.startswith('description_'):
                setattr(organisation, key, value)
        organisation.save()
        print('Organisation saved',images)
        if (images[0]):
            organisation.logo = images[0]
        if (images[1]):
            organisation.image1 = images[1]

        # TODO: Fix this
        # if len(logo_path):
        #     organisation.logo = logo_path
        # if len(image1_path):
        #     organisation.image1 = image1_path

#        country = getCountryCode(
#            organisation.latitude, organisation.longitude).upper()
#        organisation.country = country
        organisation.save()
        return organisation


class OrganisationPermissionForm(forms.Form):
    selectedUsers = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial=())
    usersCollection = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial=())
    usersAllowed = forms.MultipleChoiceField(
        choices=(),
        widget=Select2MultipleWidget,
        required=False,
        label=_("Give additional users permission to edit"))
