from django.conf.urls import patterns, url


urlpatterns = patterns(
    'blog.views',
    url(r'^$', 'post', {'slug': None}, name='post'),
    url(r'^(?P<slug>.*?)/$', 'post', name='post'),
)
