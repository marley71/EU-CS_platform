from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import urlencode
from django.conf import settings
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.template.response import TemplateResponse

class PostList(generic.ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = urlencode(query_params)
        return context
    queryset = Post.objects.filter(status=1).order_by('-sticky', '-created_on')
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
    text = "Nuovo evento"
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/blog')
        else:
            print(form.errors)
    return TemplateResponse(request, 'new_post.html', {
        'form': form,
        'user': user,
        'text': text,
        'user_agent': settings.USER_AGENT})
