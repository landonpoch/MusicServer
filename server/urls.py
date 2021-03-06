from django.conf.urls import patterns, url

from server import views

urlpatterns = patterns('',
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^artists$', views.artists, name='artists'),
    url(r'^albums$', views.albums, name='albums'),
    url(r'^libraries$', views.libraries, name='libraries'),
    url(r'^create_library$', views.create_library, name='create_library'),
    url(r'^search$', views.search, name='search'),
    url(r'^get_random_songs$', views.get_random_songs, name='get_random_songs'),
    url(r'^search_songs$', views.search_songs, name='search_songs'),
    url(r'^stream_song$', views.stream_song, name='stream_song'),
    #url(r'^test$', views.test, name='test'),
)
