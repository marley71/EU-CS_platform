from ckeditor.widgets import CKEditorWidget
from django.contrib.gis import forms
from django.shortcuts import get_object_or_404
from django_select2.forms import Select2MultipleWidget
from django_select2 import forms as s2forms
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import ugettext_lazy as _
from geopy.geocoders import Nominatim, options
from geopy.exc import GeocoderServiceError
from .models import Project, Topic, Status, Keyword, FundingBody, ProjectCountry
from .models import ParticipationTask, GeographicExtend, HasTag, DifficultyLevel, TranslatedProject, Provincia
from organisations.models import Organisation
from localita.models import Localita
from django.utils import timezone
from django.conf import settings
import json
import os


#from provincia.models import Provincia



STATO_TYPE_CHOICES = [
    ('completato', 'Completato'),
    ('non-ancora-iniziato', 'Non ancora iniziato'),
    ('sospeso', 'Sospeso'),
]

# TODO: Fix this to be an env variable
geolocator = Nominatim(user_agent="eu-citizen-science-platform")


class ProjectGeographicLocationForm(forms.Form):
    projectGeographicLocation = forms.MultiPolygonField(
        required=False,
        widget=forms.OSMWidget(attrs={
            'map_width': '800px',
            'map_height': '400px',
            'default_lat': 41.8719,  # Latitudine dell'Italia
            'default_lon': 12.5674,  # Longitudine dell'Italia
            'default_zoom': 5,  # Zoom specifico
        }),
        label=(' '))


class ProjectForm(forms.Form):

    # class Meta:
    #     model = Project
    #     fields = ['tipo_pubblico']
    # Main information
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for lang_code in settings.MODELTRANSLATION_LANGUAGES:
            self.fields[f'description_{lang_code}'] = forms.CharField(
                max_length=3000,
                widget=CKEditorWidget(config_name='frontpage'),
                help_text=_('Please provide a description of your project here (max 3000 characters).'),
                label=lang_code,
                required=lang_code == settings.MODELTRANSLATION_DEFAULT_LANGUAGE,
            )

            self.fields[f'aim_{lang_code}'] = forms.CharField(
                max_length=3000,
                widget=CKEditorWidget(config_name='frontpage'),
                help_text=_('Please provide the aim of your project here (max 3000 characters).'),
                label=lang_code,
                required=lang_code == settings.MODELTRANSLATION_DEFAULT_LANGUAGE
            )
            self.fields[f'how_to_participate_{lang_code}'] = forms.CharField(
                max_length=3000,
                widget=CKEditorWidget(config_name='frontpage'),
                help_text=_('Please describe how people can get involved in the project (max 3000 characters).'),
                label=lang_code,
                required=lang_code == settings.MODELTRANSLATION_DEFAULT_LANGUAGE,
            )
            self.fields[f'equipment_{lang_code}'] = forms.CharField(
                max_length=3000,
                widget=CKEditorWidget(config_name='frontpage'),
                help_text=_('Please indicate any required or suggested equipment to be used in the project (max 3000 characters).'),
                label=lang_code,
                required=False,
            )
        self.fields['tipo_pubblico'].widget.attrs.update({
            'onchange': 'tipo_pubblicoChange(this.value)'
        })
        # if hasattr(self.instance, 'tipo_pubblico') and self.instance.tipo_pubblico:
        #     # ottieni il valore del campo, es. "a;b;c;"
        #     val_str = self.instance.tipo_pubblico or ''
        #     # Splitta e pulisci
        #     selected = [v for v in val_str.split(';') if v]
        #     self.fields['tipo_pubblico'].initial = selected

    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Quando salvi, combini le scelte in stringa separata
    #     scelte = cleaned_data.get('tipo_pubblico', [])
    #     # Concatena le scelte con ';'
    #     val_str = ';'.join(scelte) + ';' if scelte else ''
    #     # Assegna al campo del modello
    #     self.instance.tipo_pubblico = val_str
    #     return cleaned_data

    # return all fields from project_name_en, project_name_es, etc.
    def get_description_fields(self):
        for field_name in self.fields:
            return [self[field_name] for field_name in self.fields if field_name.startswith('description_')]
        
    def get_aim_fields(self):
        for field_name in self.fields:
            return [self[field_name] for field_name in self.fields if field_name.startswith('aim_')]
        
    def get_how_to_participate_fields(self):
        for field_name in self.fields:
            #print(self.fields)
            return [self[field_name] for field_name in self.fields if field_name.startswith('how_to_participate_')]

    def get_equipment_fields(self):
        for field_name in self.fields:
            return [self[field_name] for field_name in self.fields if field_name.startswith('equipment_')]

    def getTassonomie():
        nomefile = str(settings.BASE_DIR) + '/../resources/tassonomie.json'
        if not os.path.exists(nomefile):
            return []

        with open(nomefile, 'r') as f:
            scelte_data = json.load(f)
        tassonomie = []
        # Trasforma in formato tuple di tuple (value, label)
        for item in scelte_data:
            tassonomie.append((item['id'], item['nome']))
            if 'children' in item:
                for child in item['children']:
                    tassonomie.append((child['id'], "----" + child['nome']))
                    #tassonomie.append((child['id'], child['nome']))
                    if 'children' in child:
                        for child1 in child['children']:
                            tassonomie.append((child1['id'], '--------' + child1['nome']))
        return tassonomie

    type = forms.ChoiceField(
        choices=settings.TIPO_PROGETTO,
        initial='attivita',
        label=_('Project-type'),
        widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
        help_text=_('Please provide the type of the project.'))

    inaturalist = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(),
        help_text=_('Please provide the link of inaturalist data. Left blank if no data in inaturalist.'),
        label=_('Inaturalist data'),)
    risultati = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(),
        help_text=_('Please provide the link to project result.'),
        label=_('Project-result'),)
    tipo_pubblico = forms.MultipleChoiceField(
        choices=settings.TIPO_PUBBLICO,
        #initial='ricercatori',
        #widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
        widget=forms.CheckboxSelectMultiple,
        help_text=_('Please indicate project audience type'),
        label=_('Audience type'),
        required=True
    )
    tipo_pubblico_altro = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        help_text=_('Please provide the name of the project.'),
        label=_('Project-name'))


    project_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        help_text=_('Please provide the name of the project.'),
        label=_('Project-name'))

    url = forms.URLField(
        max_length=200,
        widget=forms.TextInput(),
        label=_('URL'),
        required=False,
        help_text=_('Please provide the URL to an external website of the project.'))

    citizen_science_aspects_description = forms.CharField(
        widget=CKEditorWidget(config_name='frontpage'),
        # help_text=_('Please describe the citizen science aspect(s) of the project and the link of the project to '
        #             'citizen science using the '
        #             '<a href="https://zenodo.org/communities/citscicharacteristics" target="_blank">ECSA '
        #             'Characteristics of Citizen Science</a> and the <a href="https://zenodo.org/record/5127534#.YzQQNEzP2Um" target="_blank">ECSA 10 '
        #             'Principles of Citizen Science</a>. What you introduce in this text field will not appear '
        #             'on the platform; it is just for moderation purposes (max 2000 characters).'),
        help_text = _("Please describe the citizen science aspect(s)"),
        max_length=2000,
        label=_('Description of citizen science aspects'))

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_("Activity status"),
        widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
        help_text=_('Please, select the status of your project.'))

    # localita = forms.ModelChoiceField(
    #     queryset=Localita.objects.all(),
    #     label=_("Località"),
    #     widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
    #     help_text=_('Please, select località of your project.'))

    # provincia = forms.ModelChoiceField(
    #     queryset=Provincia.objects.all().order_by('nome'),
    #     label=_("Provincia"),
    #     widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
    #     help_text=_('Please, select provincia of your project.'))

    provincia = forms.ModelMultipleChoiceField(
        queryset=Provincia.objects.all(),
        widget=Select2MultipleWidget(),
        help_text=_(
            'Please select the project provincia(s) or field(s) of science.'),
        # required=False,
        label=_("Provincia"))

    latitude = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial=41.85
    )
    longitude = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial=12.45
    )
#     stato = forms.ChoiceField(
#         choices=STATO_TYPE_CHOICES,
#         widget=forms.Select(attrs={'class': 'js-example-basic-single'}),
#         help_text=_('Please indicate project status'),
#         label=_('Status type'),
#         required=True
#     )
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        widget=s2forms.ModelSelect2TagWidget(
            search_fields=['keyword__icontains'],
            attrs={
                #'data-url': '/path/to/your/tag-search-url/',
                'data-token-separators': '[","]'}),
        required=True,
        help_text=_(
            'Please select or enter 2-3 keywords separated by commas or by pressing enter.'),
        label=_('Keywords'))

    # Useful information to classify the project
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=False,
        label=_("Closest approximate start date of the project"))

    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=False,
        label=_("Approximate end date of the project"))

    topic = forms.MultipleChoiceField(
        #queryset=Topic.objects.all(),
        choices= getTassonomie(),
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
#                 'style': 'max-height: 300px; overflow-y: auto;'
                'style': 'margin-right:5px;'
            }
        ), #Select2MultipleWidget(),
        #help_text=_(
        #    'Please select the project topic(s) or field(s) of science.'),
        #required=False,
        label=''#_("Topic")
        )

    # topic = forms.ModelMultipleChoiceField(
    #     queryset=Topic.objects.all(),
    #     widget=Select2MultipleWidget(),
    #     help_text=_(
    #         'Please select the project topic(s) or field(s) of science.'),
    #     #required=False,
    #     label=_("Topic"))


    hasTag = forms.ModelMultipleChoiceField(
        queryset=HasTag.objects.all(),
        widget=Select2MultipleWidget(),
        help_text=_('Please select the tags that apply to your project.'),
        required=False,
        label=_("Tags"))

    # Participation information
    participationTask = forms.ModelMultipleChoiceField(
        queryset=ParticipationTask.objects.all(),
        widget=Select2MultipleWidget(),
        help_text=_('Please select the task(s) undertaken by participants.'),
        required=False,
        label=_("Participation task"))

    difficultyLevel = forms.ModelChoiceField(
        queryset=DifficultyLevel.objects.all(),
        widget=forms.Select(),
        help_text=_('Please select the difficulty level.'),
        required=False,
        label=_("Difficulty level"))

    # Project location
    geographicextend = forms.ModelMultipleChoiceField(
        queryset=GeographicExtend.objects.all(),
        widget=Select2MultipleWidget(),
        help_text=_('Please indicate the spatial scale of the project'),
        required=False,
        label=_("Geographic extend"))

    projectlocality = forms.CharField(
        max_length=300,
        widget=forms.TextInput(),
        required=False,
        label=_("Project locality"),
        help_text=_('Please describe the locality of the project, in terms of where the main participant '
                    'activities take place. E.g. in your backyard, parks in London, rivers in Europe, '
                    'online globally, etc.'))

    projectGeographicLocation = forms.MultiPolygonField(
        required=False,
        widget=forms.OSMWidget(attrs={
            'map_width': '800px',
            'map_height': '400px',
            'default_lat': 41.8719,  # Latitudine dell'Italia
            'default_lon': 12.5674,  # Longitudine dell'Italia
            'default_zoom': 5,  # Zoom specifico
        }),
        label=_("Project geographic location"))

    aree = forms.CharField(
        #max_length=100,
        widget=forms.Textarea(),
        help_text=_(
            "Please insert project's areas"),
        required=False,
        label=_("Project areas"))
    # projectCountry = forms.ModelMultipleChoiceField(
    #     queryset=ProjectCountry.objects.all(),
    #     widget=Select2MultipleWidget(),
    #     label=_("Countries involved"),
    #     required=False,
    #     help_text=_('Select all countries where the project is active.'))

    # Contact and hosts details
    contact_person = forms.CharField(
        max_length=100,
        widget=forms.TextInput(),
        help_text=_(
            'Please name the contact person or contact point of the project.'),
        required=False,
        label=_("Public contact point"))

    contact_person_email = forms.EmailField(
        required=False,
        widget=forms.TextInput(),
        help_text=_(
            'Please provide the email address of the contact person or contact point.'),
        label=_("Contact point email"))

    mainOrganisation = forms.ModelChoiceField(
        queryset=Organisation.objects.all(),
        widget=s2forms.ModelSelect2Widget(
            model=Organisation,
            search_fields=['name__icontains', ]),
        help_text=_(
            'Please select the organisation coordinating the project. If not listed, '
            'please add it <a href="/new_organisation" target="_blank">here</a> '
            'before submitting the project'),
        label=_('Lead organisation / coordinator'),
        required=False)

    organisation = forms.ModelMultipleChoiceField(
        queryset=Organisation.objects.all(),
        widget=s2forms.ModelSelect2MultipleWidget(
            model=Organisation,
            search_fields=['name__icontains']),
        help_text=_(
            'Please select other organisation(s) participating in the project. If not listed,'
            'please add it <a href="/new_organisation" target="_blank">here</a> '
            'before submitting the project'),
        label=_("Other Organisations"),
        required=False)

    # Funding information
    funding_body = forms.ModelMultipleChoiceField(
        queryset=FundingBody.objects.all(),
        widget=s2forms.Select2TagWidget(
            attrs={'data-token-separators': '[","]'}
        ),
        help_text=_('Please enter the funding agencies of the project (e.g. European Commission)<br />'
                    'Select them from the list or add your own <b>ended by comma or pressing enter</b>.'),
        required=False,
        label=_("Funding body"))

    funding_program = forms.CharField(
        max_length=500,
        widget=forms.TextInput(),
        label=_("Funding programme"),
        help_text=_(
            'Please indicate the name of the programme that funds or funded the project.'),
        required=False)

    # Images
    image1 = forms.ImageField(
        required=False,
        label=_("Image for the thumbnail profile"),
        help_text=_('It will be resized to 600x400 pixels'),
        widget=forms.FileInput)

    x1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height1 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    withImage1 = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    image_credit1 = forms.CharField(
        max_length=300,
        required=False,
        label=_("Thumbnail credit, if applicable"))

    image2 = forms.ImageField(
        required=False,
        label=_("Project logo"),
        help_text=_('It will be resized to 600x400 pixels)'),
        widget=forms.FileInput)
    x2 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y2 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width2 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height2 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    withImage2 = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    image_credit2 = forms.CharField(
        max_length=300,
        required=False,
        label=_("Logo credit, if applicable"))

    image3 = forms.ImageField(
        required=False,
        label=_("Image for the profile heading"),
        help_text=_('It will be resized to 1100x400 pixels'),
        widget=forms.FileInput)
    x3 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y3 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width3 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height3 = forms.FloatField(widget=forms.HiddenInput(), required=False)
    withImage3 = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    image_credit3 = forms.CharField(
        max_length=300,
        required=False,
        label=_("Heading image credit, if applicable"))

    logo = forms.ImageField(
        required=False,
        label=_("Logo progetto/attività"),
        help_text=_('It will be resized to 1100x400 pixels'),
        widget=forms.FileInput)
    xlogo = forms.FloatField(widget=forms.HiddenInput(), required=False)
    ylogo = forms.FloatField(widget=forms.HiddenInput(), required=False)
    widthlogo = forms.FloatField(widget=forms.HiddenInput(), required=False)
    heightlogo = forms.FloatField(widget=forms.HiddenInput(), required=False)
    withImagelogo = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)
    logo_credit = forms.CharField(
        max_length=300,
        required=False,
        label=_("Heading logo credit, if applicable"))

    # Others, some of them unused
    host = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter the name of the institution hosting or coordinating the project'}),
        required=False)
    participatingInaContest = forms.BooleanField(
        required=False,
        label=_('I want to participate in the #MonthOfTheProjects and agree to be contacted via email if the'
                'project I am submitting wins the contest.'
                '<a href="/blog/2021/05/31/june-monthoftheprojects-eu-citizenscience/"> Learn more here!</a>'))
    # Custom fields
    title = forms.CharField(max_length=100, required=False)
    paragraph = forms.CharField(widget=SummernoteWidget(), required=False)

    ''' Save function '''

    def save(self, args, images, cFields, mainOrganisationFixed):
        pk = self.data.get('projectID', '')
        start_dateData = self.data['start_date']
        end_dateData = self.data['end_date']
        projectlocality = self.data['projectlocality']
        #projectGeographicLocation = self.data['projectGeographicLocation']
        projectGeographicLocation = self.data.get('projectGeographicLocation')
        status = get_object_or_404(Status, id=self.data['status'])
        if (self.data['difficultyLevel']):
            difficultyLevel = get_object_or_404(
                DifficultyLevel, id=self.data['difficultyLevel'])
        else:
            difficultyLevel = None
        if (self.data['mainOrganisation']):
            mainOrganisation = get_object_or_404(
                Organisation, id=self.data['mainOrganisation'])
        else:
            mainOrganisation = None

        doingAtHome = False
        if ('doingAtHome' in self.data and self.data['doingAtHome'] == 'on'):
            doingAtHome = True

        participatingInaContest = False
        if ('participatingInaContest' in self.data and self.data['participatingInaContest'] == 'on'):
            participatingInaContest = True

        if (pk):
            project = get_object_or_404(Project, id=pk)
            if project.hidden:
                project.hidden = False
            self.updateFields(
                project,
                status,
                difficultyLevel,
                doingAtHome,
                mainOrganisation,
                projectlocality,
                projectGeographicLocation)
        else:
            project = self.createProject(
                status,
                difficultyLevel,
                doingAtHome,
                projectGeographicLocation,
                participatingInaContest,
                mainOrganisation,
                projectlocality,
                args)

        if start_dateData:
            project.start_date = start_dateData
        if end_dateData:
            project.end_date = end_dateData

        if (images[0] != '/'):
            project.image1 = images[0]
        if (images[1] != '/'):
            project.image2 = images[1]
        if (images[2] != '/'):
            project.image3 = images[2]
        if (images[3] != '/'):
            project.logo = images[3]

        if self.data.get('aree',None):
            project.aree = self.data.get('aree')
        else:
            project.aree = None
        #print("immagini progetto")
        #print(images)
        user = args.user
        if user.is_staff == False:
            project.dateUpdated = timezone.now()
            project.save()
        else:
            if project.dateUpdated is None:
                project.dateUpdated = timezone.now()
            else:
                project.dateUpdated = project.dateUpdated
        project.tipo_pubblico = self.data['tipo_pubblico']
        project.tipo_pubblico_altro = self.data['tipo_pubblico_altro']
#         project.stato = self.data['stato']
        project.type = self.data['type']
        project.risultati = self.data['risultati']
        project.inaturalist = self.data['inaturalist']
#         print(self.data.getlist('topic'))

        provinciaId = next(iter(self.data.getlist('provincia')), None)
        #print('PROVINCIAID', provinciaId)
        if provinciaId:
            provincia = Provincia.objects.get(id=provinciaId)
            if provincia:
                localita = Localita.objects.get(name=provincia.regione)
                project.localita = localita
        project.save()

        #project.topic.set(self.data.getlist('topic'))
        project.keywords.set(self.data.getlist('keywords'))
        project.fundingBody.set(self.data.getlist('funding_body'))
        project.participationTask.set(self.data.getlist('participationTask'))
        project.hasTag.set(self.data.getlist('hasTag'))
        project.geographicextend.set(self.data.getlist('geographicextend'))
        project.organisation.set(self.data.getlist('organisation'))
        project.provincia.set(self.data.getlist('provincia'))

        #project.projectCountry.set(self.cleaned_data['projectCountry'])

        for key, value in self.data.items():
            if key.startswith('description_'):
                setattr(project, key, value)
            if key.startswith('aim_'):
                setattr(project, key, value)
            if key.startswith('how_to_participate_'):
                setattr(project, self.to_camel_case(key), value)
            if key.startswith('equipment_'):
                setattr(project, self.to_camel_case(key), value)


        project.save()

        return project.id

    def to_camel_case(self,s):
        parts = s.split('_')
        # Prima parola in minuscolo, le successive capitalizzate
        trs =  parts[0].lower() + ''.join(word.capitalize() for word in parts[1:len(parts)-1]) + '_' + parts[len(parts)-1]
        print(trs)
        return trs

    def createProject(
            self,
            status,
            difficultyLevel,
            doingAtHome,
            projectGeographicLocation,
            participatingInaContest,
            mainOrganisation,
            projectLocality,
            args):
        return Project(
            localita_id = 1,
            creator=args.user,
            name=self.data.get('project_name', ''),
            url=self.data['url'],
            citizen_science_aspects_description=self.data['citizen_science_aspects_description'],
            projectlocality=self.data['projectlocality'],
            mainOrganisation=mainOrganisation,
            author=self.data['contact_person'],
            author_email=self.data['contact_person_email'],
            status=status,
            difficultyLevel=difficultyLevel,
            imageCredit1=self.data['image_credit1'],
            imageCredit2=self.data['image_credit2'],
            imageCredit3=self.data['image_credit3'],
            logoCredit = self.data['logo_credit'],
            fundingProgram=self.data['funding_program'],
            participatingInaContest=participatingInaContest,
            projectGeographicLocation=projectGeographicLocation,
            tipo_pubblico_altro=self.data['tipo_pubblico_altro'],
            latitude=41,
            longitude=11,
        )

    def updateFields(
            self, project, status, difficultyLevel,
            doingAtHome, mainOrganisation, projectLocality, projectGeographicLocation):
        project.name = self.data['project_name']
        project.url = self.data['url']
        project.projectlocality = self.data['projectlocality']
        project.author = self.data['contact_person']
        project.author_email = self.data['contact_person_email']
      
        project.citizen_science_aspects_description = self.data[
            'citizen_science_aspects_description']
        project.status = status
        project.difficultyLevel = difficultyLevel
        project.imageCredit1 = self.data['image_credit1']
        project.imageCredit2 = self.data['image_credit2']
        project.imageCredit3 = self.data['image_credit3']
        project.logoCredit = self.data['logo_credit']
        try :
            #provincia = Provincia.objects.get(id=self.data['provincia'])

            provinciaId = next(iter(self.data.getlist('provincia')), None)
            if provinciaId:
                provincia = Provincia.objects.get(id=provinciaId)
                if provincia:
                    localita = Localita.objects.get(name=provincia.regione)
            #print('Localita trovata')
        except Provincia.DoesNotExist:
            localita = None
            provincia = None

        if localita and provincia:
            project.localita_id = localita.id
            project.provincia.set(self.data.getlist('provincia'))
            #project.add(provincia)
            #project.provincia_id = provincia.id
        project.latitude = self.data['latitude']
        project.longitude = self.data['longitude']
        project.doingAtHome = doingAtHome
        #project.localita
        project.fundingProgram = self.data['funding_program']
        project.mainOrganisation = mainOrganisation
        project.projectGeographicLocation = projectGeographicLocation

        #project.projectCountry.set(self.cleaned_data['projectCountry'])

        for key, value in self.data.items():
            if key.startswith('description_'):
                setattr(project, key, value)
            if key.startswith('aim_'):
                setattr(project, key, value)
            if key.startswith('how_to_participate_'):
                setattr(project, self.to_camel_case(key), value)
            if key.startswith('equipment_'):
                setattr(project, key, value)

        # If there are translations, need to improve them
        project.translatedProject.all().update(needsUpdate=True)

def getCountryCode(latitude, longitude):
    try:
        location = geolocator.reverse([latitude, longitude], exactly_one=True)
        if len(location.raw) > 1:
            return location.raw['address']['country_code']
        else:
            return ''
    except GeocoderServiceError:
        return ''


''' This is the form to translate projects '''
class ProjectTranslationForm(forms.Form):
    translatedDescription = forms.CharField(
        widget=CKEditorWidget(config_name='frontpage'),
        help_text=_('Please provide a <i>description</i> field translation.'),
        max_length=10000,
        label=_("Description"))

    translatedAim = forms.CharField(
        widget=CKEditorWidget(config_name='frontpage'),
        help_text=_('Please provide an <i>aim</i> field translation.'),
        max_length=10000,
        label=_("Aim"),
        required=True)

    translatedHowToParticipate = forms.CharField(
        widget=CKEditorWidget(config_name='frontpage'),
        help_text=_(
            'Please provide a <i>how to participate</i> field translation.'),
        max_length=10000,
        label=_("How to participate"),
        required=False)

    translatedEquipment = forms.CharField(
        widget=CKEditorWidget(config_name='frontpage'),
        help_text=_(
            'Please provide a <i>translated equipment</i> field translation.'),
        max_length=10000,
        label=_("Needed equipment"),
        required=False)

    def save(self, args):
        project = Project.objects.get(id=self.data.get('projectId'))
        translation = project.translatedProject.filter(
            inLanguage=self.data.get('languageId')).first()

        print(translation)
        if translation:
            TranslatedProject.objects.filter(id=translation.id).delete()
        t1 = TranslatedProject(
            inLanguage=self.data.get('languageId'),
            translatedDescription=self.data.get('translatedDescription'),
            translatedAim=self.data.get('translatedAim'),
            translatedHowToParticipate=self.data.get(
                'translatedHowToParticipate'),
            translatedEquipment=self.data.get('translatedEquipment'),
            needsUpdate=False,
            creator=args.user,
        )
        t1.save()
        project.translatedProject.add(t1)

        user = args.user
        if user.is_staff == False:
            project.dateUpdated = timezone.now()
            project.save()
        else:
            project.dateUpdated = project.dateUpdated
        project.save()


class CustomFieldForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    paragraph = forms.CharField(widget=SummernoteWidget(), required=False)


class ProjectPermissionForm(forms.Form):
    selectedUsers = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial=())
    usersCollection = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial=())
    usersAllowed = forms.MultipleChoiceField(
        choices=(),
        widget=Select2MultipleWidget,
        required=False,
        label=_("Give additional users permission to edit"))

