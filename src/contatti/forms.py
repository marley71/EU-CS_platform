from .models import Contatto
from django.contrib.gis import forms
from django.utils.translation import ugettext_lazy as _

class ContattoForm(forms.Form):

    # Main information
    def __init__(self, *args, **kwargs):
        super(ContattoForm, self).__init__(*args, **kwargs)

    # return all fields from project_name_en, project_name_es, etc.
    # def get_description_fields(self):
    #     for field_name in self.fields:
    #         return [self[field_name] for field_name in self.fields if field_name.startswith('description_')]

    # def getTassonomie():
    #     nomefile = str(settings.BASE_DIR) + '/../resources/tassonomie.json'
    #     if not os.path.exists(nomefile):
    #         return []
    #
    #     with open(nomefile, 'r') as f:
    #         scelte_data = json.load(f)
    #     tassonomie = []
    #     # Trasforma in formato tuple di tuple (value, label)
    #     for item in scelte_data:
    #         tassonomie.append((item['id'], item['nome']))
    #         if 'children' in item:
    #             for child in item['children']:
    #                 tassonomie.append((child['id'], "----" + child['nome']))
    #                 # tassonomie.append((child['id'], child['nome']))
    #                 if 'children' in child:
    #                     for child1 in child['children']:
    #                         tassonomie.append((child1['id'], '--------' + child1['nome']))
    #     return tassonomie


    nome = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(),
        help_text=_('Please provide your name'),
        label=_('contact name') ,)
    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(),
        help_text=_('Please provide your telephone number'),
        label=_('telephone number') ,)

    email = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        help_text=_('Please provide your email address'),
        label=_('email address') ,)


    messaggio = forms.CharField(
        max_length=200,
        widget=forms.Textarea(),
        help_text=_('Please provide your message'),
        label=_('Scrivi qui') ,)

    ''' Save function '''

    def save(self):
        pk = self.data.get('projectID', '')
        messaggio = self.data['messaggio']
        email = self.data['email']
        nome = self.data['nome']
        # projectGeographicLocation = self.data['projectGeographicLocation']
        telefono = self.data.get('telefono')

        if (pk):
            contatto = get_object_or_404(Contatto, id=pk)
            self.updateFields(
                contatto,
                messaggio,
                email,
                nome,
                telefono)
        else:
            contatto = self.createContatto(
                messaggio,
                email,
                nome,
                telefono)

        # user = args.user
        # if user.is_staff == False:
        #     project.dateUpdated = timezone.now()
        #     project.save()
        # else:
        #     if project.dateUpdated is None:
        #         project.dateUpdated = timezone.now()
        #     else:
        #         project.dateUpdated = project.dateUpdated



        contatto.save()

        return contatto.id


    def createContatto(
            self,
            messaggio,
            email,
            nome,
            telefono):
        return Contatto(
            messaggio = messaggio,
            email=email,
            nome=nome,
            telefono=telefono,
        )

    def updateFields(
            self, contatto, messaggio,
                email,
                nome,
                telefono):
        contatto.nome = nome
        contatto.email = email
        contatto.messaggio = messaggio
        contatto.telefono = telefono