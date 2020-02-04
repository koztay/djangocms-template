from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.static import serve

from backend import settings
from backend.error_handler.views import collect_500_error_user_feedback_view


urlpatterns = [
    url(r'^captcha/', include('captcha.urls')), # required by aldryn-forms
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^', include('cms.urls')),
)


handler500 = collect_500_error_user_feedback_view


def sentry_trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = urlpatterns + [
    path('sentry-debug/', sentry_trigger_error),
]



if settings.env.is_dev():
    urlpatterns = urlpatterns + staticfiles_urlpatterns() + [
        url(
            r'^media/(?P<path>.*)$',
            serve,
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True,
            },
        ),
    ]
