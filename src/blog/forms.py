from django import forms
from django.shortcuts import get_object_or_404
from django.db import models
from django.utils.translation import ugettext_lazy as _
from organisations.models import Organisation
from projects.models import Project
from .models import Post
from django_select2 import forms as s2forms
import pytz


EVENT_TYPE_CHOICES = [
    ('online', 'On-line event'),
    ('face-to-face', 'Face-to-face event'),
    ('hybrid', 'Hybrid event'),
]


class PostForm(forms.Form):
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )
    STICKY = (
        (0, "No"),
        (1, "Yes")
    )

    image = models.ImageField(max_length=200, default='default_blog.png')
    created_on = models.DateTimeField()

    title = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            help_text=_('Please write the title of the blog.'),
            label=_('Title'))

    slug = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        help_text=_('Please insert slug of the blog.'),
        label=_('Slug'))
    excerpt = forms.CharField(
        max_length=200,
        widget=forms.TextInput(),
        help_text=_('Please insert excerpt of the blog.'),
        label=_('Excerpt'))
    # author e updated_on
    content = forms.CharField(widget=forms.Textarea(), max_length = 3000,
            help_text=_('Please add a brief description of the post.'),
            label=_('Description'))
    status = forms.ChoiceField(choices=STATUS, initial=0, widget=forms.Select(attrs={'class' : 'form-control'}), help_text=_('Please indicate the language of the event.'), label=_('Language'))
    sticky = forms.ChoiceField(choices=STICKY, initial=0, widget=forms.Select(attrs={'class' : 'form-control'}), help_text=_('Please indicate the language of the event.'), label=_('Language'))


    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance')
    #     if instance:
    #             event_type = 'online' if instance.online_event else 'physical'
    #             kwargs['initial'] = kwargs.get('initial', {})
    #             kwargs['initial']['event_type'] = event_type
    #     super().__init__(*args, **kwargs)
    
    def save(self, args):
        pk = self.data.get('blogID', '')
        # hour = self.data['hour']
        # if hour == '':
        #     hour = None
        if pk:
            post = get_object_or_404(Post, id=pk)
            post.title = self.data['title']
            post.description = self.data['description']
            post.place = self.data['place']
            post.country = self.data['country']
            post.start_date = self.data['start_date']
            post.end_date = self.data['end_date']
            #post.hour = hour
            post.timezone=self.data['timezone']
            post.language=self.data['language']
            post.url = self.data['url']
            post.event_type = self.data['event_type']
            post.latitude = self.data['latitude']
            post.longitude = self.data['longitude']
            post.creator=args.user
            post.project = self.cleaned_data['project']
            post.mainOrganisation = self.cleaned_data['mainOrganisation']
            post.organisations.set(self.cleaned_data['organisations'])
        else:
            post = Post(
                title=self.data['title'],
                description=self.data['description'],
                place=self.data['place'],
                country=self.data['country'],
                start_date=self.data['start_date'],
                end_date=self.data['end_date'],
                #hour=hour,
                timezone=self.data['timezone'],
                language=self.data['language'],
                url=self.data['url'],
                latitude=self.data['latitude'],
                longitude=self.data['longitude'],
                event_type=self.data['event_type'],
                creator=args.user
            )
            post.save()
            post.project = self.cleaned_data['project']
            post.mainOrganisation = self.cleaned_data['mainOrganisation']
            post.organisations.set(self.cleaned_data['organisations'])

        post.save()
