from django.conf.urls import patterns, url


urlpatterns = patterns(
    'works.views',
    url(r'^(?P<slug>.*?)/$', 'work', name='work'),
)
