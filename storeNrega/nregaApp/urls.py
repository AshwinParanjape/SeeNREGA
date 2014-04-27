from django.conf.urls import url

from nregaApp import views

urlpatterns = [
		    url(r'^$', views.query, name='query'),
		    #url(r'^admJSON$', views.admJSON, name='admJSON'),
		    url(r'^panchayatList/([0-9]+)/$', views.panchayats, name='panchayats'),
		    url(r'^dataretrive/$', views.dataretrive, name='dataretrive'),
			]
