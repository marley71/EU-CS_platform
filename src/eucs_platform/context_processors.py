from django.conf import settings


def global_settings(request):
    return {
        'TRANSLATED_LANGUAGES': settings.TRANSLATED_LANGUAGES,
        'TRANSLATED_LANGUAGES_KEY' : settings.TRANSLATED_LANGUAGES_KEY,
    }


def static_version(request):
    return {'STATIC_VERSION': settings.STATIC_VERSION}


def theme(request):
    return {'THEME': settings.THEME}
