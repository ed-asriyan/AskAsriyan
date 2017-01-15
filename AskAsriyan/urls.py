"""AskAsriyan URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sign_in/', 'AskAsriyan.views.login_view'),
    url(r'^sign_up/', 'AskAsriyan.views.register_view'),
    url(r'^logout/', 'AskAsriyan.views.logout_view'),
    url(r'^article(?P<article_id>\d+)/', 'AskAsriyan.views.article_view'),
    url(r'^tag/(?P<tag>\w+)/', 'AskAsriyan.views.article_by_tag_list_page_view'),
    url(r'^articles/', 'AskAsriyan.views.article_list_page_view'),
    url(r'^ask/', 'AskAsriyan.views.article_add_view'),
    url(r'^settings/', 'AskAsriyan.views.profile_settings_view'),
    url(r'^$', 'AskAsriyan.views.index_page_view'),
]
