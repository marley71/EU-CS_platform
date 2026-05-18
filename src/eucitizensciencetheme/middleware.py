from .models import Footer, Main, TopBar
from django.template.response import TemplateResponse
from pages.models import Pages
from projects.models import BDSWeek
import logging

logger = logging.getLogger(__name__)

class TopBarMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if isinstance(response, TemplateResponse):
            print(TopBar.objects.all())
            response.context_data['topbar_items'] = TopBar.objects.all()
            response.context_data['platform_name'] = Main.objects.first().platform_name
            response.context_data['bdsweek_years'] = (
                BDSWeek.objects.order_by('-anno').values_list('anno', flat=True).distinct()
            )
        return response
    
class FooterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_template_response(self, request, response):
        # do this only if the response is a TemplateResponse
        if isinstance(response, TemplateResponse):
            response.context_data['footer'] = Footer.objects.first()
            response.context_data['footerPages'] = Pages.objects.filter(id__in=(1,2,3)).order_by("id")

        return response

class ThemeSelectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("here")
    
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if isinstance(response, TemplateResponse):
            response.context_data['theme'] = 'eucitizensciencetheme'
            print('Theme selected: eucitizensciencetheme')
        return response