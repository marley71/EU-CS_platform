from django.urls import path, include
from django.conf.urls import url
from . import views

''' Paths of eucitizensciencetheme, in alphabetical order '''
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("call/", views.call, name="call"),
    path("call_ambassadors/", views.call_ambassadors, name="call_ambassadors"),
    path("criteria/", views.criteria, name="criteria"),
    path("development", views.development, name="development"),
    path("ecs_project/", views.ecs_project, name="ecs_project"),
    path("ecs_project/ambassadors", views.ecs_project_ambassadors, name="ecs_project_ambassadors"),
    path("ecs_project/ecs_codesign_process", views.ecs_project_codesign, name="ecs_project_codesign"),
    path("faq/", views.faq, name="faq"),   
    path("final_event/", views.final_event, name="final_event"),
    path("final_launch/", views.final_launch, name="final_launch"),
    path('get_projects/', views.get_projects, name='get_projects'),
    path('get_projects_webmapp/', views.get_projects_webmapp, name='get_projects_webmapp'),
    path('get_projects_webmapp/progetti-nazionali', views.get_projects_webmapp(type='pn'), name='get_projects_webmapp_pn'),
    path('get_projects_webmapp/progetti-regionali', views.get_projects_webmapp, name='get_projects_webmapp_pr'),
    path('get_projects_webmapp/progetti-locali', views.get_projects_webmapp, name='get_projects_webmapp_pl'),
    path('get_projects_webmapp/attivita-nazionali', views.get_projects_webmapp, name='get_projects_webmapp_an'),
    path('get_projects_webmapp/attivita-regionali', views.get_projects_webmapp, name='get_projects_webmapp_ar'),
    path('get_projects_webmapp/attivita-locali', views.get_projects_webmapp, name='get_projects_webmapp_al'),
    path('get_organisations/', views.get_organisations, name='get_organisations'),
    path("imprint/", views.imprint, name="imprint"),
    path("moderation/", views.moderation, name="moderation"),
    path("moderation_quality_criteria/", views.moderation_quality_criteria, name="moderation_quality_criteria"),
    path("policy_brief/", views.policy_brief, name="policy_brief"),
    path("policy_maker_event_2021/", views.policy_maker_event_2021, name="policy_maker_event_2021"),
    path("privacy/", views.privacy, name="privacy"),
    path("map/", views.projects_map, name="map"),
    path("bdsweek_map/", views.bdsweek_projects_map, name="bdsweek_map"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("terms/", views.terms, name="terms"),
    path("translations/", views.translations, name="translations"),
    path("test/", views.test, name="test"),
    path("test2/", views.test2, name="test2"),
    


]