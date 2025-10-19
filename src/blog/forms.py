from django import forms
from django.shortcuts import get_object_or_404
from django.db import models
from django.utils.translation import ugettext_lazy as _
from organisations.models import Organisation
from projects.models import Project
from .models import Post
from django_select2 import forms as s2forms
import pytz
from datetime import datetime, timedelta
from django.utils import timezone

EVENT_TYPE_CHOICES = [
    ('online', 'On-line event'),
    ('face-to-face', 'Face-to-face event'),
    ('hybrid', 'Hybrid event'),
]


class PostForm(forms.Form):
    STATUS = (
        (0, "Non Approvato"),
        (1, "Approvato"),
    )
    STICKY = (
        (0, "No"),
        (1, "Yes")
    )

    # def __init__(self, *args, **kwargs):
    #     self.initial_data['data'] = self.initial_data['data'] if self.initial_data['data'] else timezone.now

    image = forms.ImageField(
        required=False,
        label=_("Image for the thumbnail profile"),
        help_text=_('It will be resized to 600x400 pixels'),
        widget=forms.FileInput)

    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    withImage = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False)

    created_on = models.DateTimeField()
    title = forms.CharField(
            max_length=200,
            widget=forms.TextInput(),
            help_text=_('Please write the title of the blog.'),
            label=_('Title'))
    data = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=True,
        #initial=self.initial['data'] if self.initial['data'] else timezone.now,
        label=_("Please write the data of the blog."))
    # slug = forms.CharField(
    #     max_length=200,
    #     widget=forms.TextInput(),
    #     help_text=_('Please insert slug of the blog.'),
    #     label=_('Slug'))
    # excerpt = forms.CharField(
    #     max_length=200,
    #     widget=forms.TextInput(),
    #     help_text=_('Please insert excerpt of the blog.'),
    #     label=_('Excerpt'))
    # author e updated_on
    content = forms.CharField(widget=forms.Textarea(), max_length = 3000,
            help_text=_('Please add a brief description of the post.'),
            label=_('Description'))
    status = forms.ChoiceField(choices=STATUS, initial=0, widget=forms.Select(attrs={'class' : 'form-control'}),
                               help_text=_('Please indicate the status of the blog.'), label=_('Status'))
    # sticky = forms.ChoiceField(choices=STICKY, initial=0, widget=forms.Select(attrs={'class' : 'form-control'}),
    #                            help_text=_('Please indicate if the blog is in original language.'), label=_('Language'))


    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance')
    #     if instance:
    #             event_type = 'online' if instance.online_event else 'physical'
    #             kwargs['initial'] = kwargs.get('initial', {})
    #             kwargs['initial']['event_type'] = event_type
    #     super().__init__(*args, **kwargs)
    
    def save(self, args,images):
        resolver_match = args.resolver_match
        pk = resolver_match.kwargs.get('pk')
        #pk = self.data.get('id', '')
        print('blog data',self.data['data'],'blod id',pk,args)
        # hour = self.data['hour']
        # if hour == '':
        #     hour = None
        if pk:
            updated_on = timezone.make_aware(datetime.now())
            post = get_object_or_404(Post, id=pk)
            post.title = self.data['title']
            post.content = self.data['content']
            post.data = self.data['data']
            #post.slug = self.data['slug']
            post.updated_on = updated_on
            post.status = self.data['status']
            #post.excerpt=self.data['excerpt']
            #post.sticky=self.data['sticky']
            post.author=args.user
        else:
            #date_object = datetime.strptime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            # Assicurati che l'oggetto datetime sia consapevole del fuso orario
            created_on = timezone.make_aware(datetime.now())
            post = Post(
                title=self.data['title'],
                content=self.data['content'],
                #slug=self.data['slug'],
                created_on=created_on,
                updated_on=created_on,
                status=self.data['status'],
                #excerpt=self.data['excerpt'],
                #sticky=self.data['sticky'],
                author=args.user
            )
        if (images[0] != '/' and images[0] != ''):
            post.image = images[0]
        post.slug = self.data['title'].replace(' ', '-') + '-' + self.data['data']
        post.save()
        return post