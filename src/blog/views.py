from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import urlencode
from django.conf import settings
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.template.response import TemplateResponse
from PIL import Image
from django.utils import formats
from datetime import datetime, timezone
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
import copy

class PostList(generic.ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = urlencode(query_params)
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Post.objects.order_by('-sticky', '-created_on')
        elif user:
            return Post.objects.filter(Q(status=1) | Q(author_id=user.id)).order_by('-sticky', '-created_on')
        else:
            return Post.objects.filter(status=1).order_by('-sticky', '-created_on')

    template_name = 'blog.html'
    paginate_by = '12'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    user = request.user
    return TemplateResponse(request, 'post_detail.html', {
        'post': post,
        'user': user,
        'user_agent': settings.USER_AGENT})

    #return render(request, 'post_detail.html', {'post': post, "domain": settings.HOST})


def post_review(request, pk):
    return render(request, 'post_review.html', {'postID': pk})


@login_required(login_url='/login')
def new_blog(request):
    user = request.user
    form = PostForm()
    #text = get_object_or_404(HelpText, slug='new-event')
    text = "Nuova notizia"
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            images = setImages(request, form)
            post = form.save(request, images)
            sendBlogEmail(post.id,user)
            return redirect('/blog')
        else:
            print(form.errors)
    return TemplateResponse(request, 'new_post.html', {
        'form': form,
        'user': user,
        'text': text,
        'user_agent': settings.USER_AGENT})

@login_required(login_url='/login')
def edit_blog(request,pk):

    #text = get_object_or_404(HelpText, slug='new-event')
    text = "Modifica notizia"
    blog = None
    user = request.user
    blog = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            images = setImages(request, form)
            form.save(request, images)
            return redirect('/blog')
        else:
            print(form.errors)

    else:
        initial_data = {
            'title': blog.title,
            'content': blog.content,
            'status': blog.status,
            'data':  blog.data, #formats.date_format(blog.data, 'Y-m-d')
        }
        #print(blog.data)
        form = PostForm(initial=initial_data)
    return TemplateResponse(request, 'edit_post.html', {
        'blog' : blog,
        'form': form,
        'user': user,
        'text': text,
        'user_agent': settings.USER_AGENT})

def setImages(request, form):
    #print('setImages')
    images = []
    image_path = saveImage(request, form, 'image')
    images.append(image_path)
    return images


def saveImage(request, form, element):
    image_path = ''
    filepath = request.FILES.get(element, False)
    withImage = form.cleaned_data.get('withImage')
    #print('ref ' + ref + 'withImage' + ref + ' withImage ' + str(withImage)  + ' filepath ' + str(filepath))
    if (filepath):
        x = form.cleaned_data.get('x') if form.cleaned_data.get('x') else 0
        y = form.cleaned_data.get('y') if form.cleaned_data.get('y') else 0
        w = form.cleaned_data.get('width') if form.cleaned_data.get('width') else 600
        h = form.cleaned_data.get('height') if form.cleaned_data.get('height') else 400
        #print(element)
        photo = request.FILES[element]
        image = Image.open(photo)
        cropped_image = image.crop((x, y, w+x, h+y))
        finalSize = (600, 400)
        resized_image = cropped_image.resize(finalSize, Image.Resampling.LANCZOS)

        if (cropped_image.width > image.width):
            size = (abs(int(
                (finalSize[0]-(finalSize[0]/cropped_image.width*image.width))/2)), finalSize[1])
            whitebackground = Image.new(
                mode='RGBA', size=size, color=(255, 255, 255, 0))
            position = ((finalSize[0] - whitebackground.width), 0)
            resized_image.paste(whitebackground, position)
            position = (0, 0)
            resized_image.paste(whitebackground, position)
        if (cropped_image.height > image.height):
            size = (finalSize[0], abs(
                int((finalSize[1]-(finalSize[1]/cropped_image.height*image.height))/2)))
            whitebackground = Image.new(
                mode='RGBA', size=size, color=(255, 255, 255, 0))
            position = (0, (finalSize[1] - whitebackground.height))
            resized_image.paste(whitebackground, position)
            position = (0, 0)
            resized_image.paste(whitebackground, position)

        image_path = saveImageWithPath(resized_image, photo.name)
    elif withImage:
        image_path = '/'
    else:
        image_path = ''

    return image_path


def saveImageWithPath(image, photoName):
    _datetime = formats.date_format(datetime.now(), 'Y-m-d_hhmmss')
    random_num = random.randint(0, 1000)
    image_path = "images/" + _datetime + \
        '_' + str(random_num) + '_' + photoName
    image.save("media/"+image_path)
    return image_path

def sendBlogEmail(pk, user):
    post = get_object_or_404(Post, id=pk)
    subject = '[EU-CITIZEN.SCIENCE] news "%s" has been submitted' % post.title
    message = render_to_string('emails/new_post.html', {
        'username': user.name,
        'domain': settings.HOST,
        'eventTitle': post.title,
        'eventId': pk})
    # to = [user.email]
    to = copy.copy(settings.EMAIL_RECIPIENT_LIST)
    #print(f"Lista TO: {to}")
    #to.append(user.email)
    bcc = copy.copy(settings.EMAIL_RECIPIENT_LIST)
    #print(f"Lista BCC: {bcc}")
    from_email = 'help@eu-cs-platform.dev.it'#settings.EMAIL_FROM_CONTENTS
    email = EmailMessage(subject=subject, body=message,from_email=from_email, to=to, bcc=bcc,)
    email.content_subtype = "html"
    email.send()