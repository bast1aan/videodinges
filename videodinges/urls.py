"""videodinges URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import include

from . import testviews, views

_urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^(?P<slug>[\w-]+).html', views.video)
]

_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

for i in testviews.__all__:
	_urlpatterns.append(url(r'^test/{}$'.format(i), testviews.__dict__[i]))

if settings.URL_BASE:
	urlpatterns = [url(r'^{}/'.format(settings.URL_BASE), include(_urlpatterns))]
else:
	urlpatterns = _urlpatterns
