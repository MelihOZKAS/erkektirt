"""
URL configuration for erkek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from isimler.views import *
from django.conf import settings
from django.conf.urls.static import static
from .sitemaps import *
from django.contrib.sitemaps.views import index, sitemap

sitemaps = {
    'Erkekisimleri': erkekisimleri,
    'Kizisimleri': kizisimleri,
    'Unisexisimler': unisexisimleri,
    'kadin': kadin,
    'cocuk': cocuk,
    'saglik': saglik,
}

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("", home, name="home"),
                  path('tinymce/', include('tinymce.urls')),
                  path('ara/', arama, name='ara'),
                  path("erkek-isimleri/", kategori, name="erkek"),
                  #path("erkek-bebek-isimleri/", kategori, name="erkek"),
                  path("kiz-isimleri/", kategori, name="kiz"),
                  #path("kiz-bebek-isimleri/", kategori, name="kiz"),
                  path("unisex-isimler/", kategori, name="unisex"),
                  path("kadin/", kategori, name="kadin"),
                  path("saglik/", kategori, name="saglik"),
                  path("cocuk/", kategori, name="cocuk"),
                  path("populer-erkek-isimleri/", kategori, name="pei"),
                  path("populer-kiz-isimleri/", kategori, name="pki"),
                  path("populer-unisex-isimler/", kategori, name="pui"),
                  path("en-cok-goruntulenen-erkek-isimleri/", kategori, name="ecgei"),
                  path("en-cok-goruntulenen-kiz-isimleri/", kategori, name="ecgki"),
                  path("en-cok-goruntulenen-unisex-isimler/", kategori, name="ecgui"),
                  path("kisaisimekle/", kisaisimekle, name="kisaisimekle"),
                  path("ai-cek/", aicek, name="aicek"),
                  path("iletisim/", iletisim, name="iletisim"),
                  path("hakkimizda/", hakkinda, name="hakkimizda"),
                  path("cerez-politikasi/", cerez, name="cerez"),
                  path("gizlilik-politikasi/", gizlilik, name="gizlilik-politikasi"),
                  path("kullanim-sartlari/", kullanim, name="kullanim-sartlari"),
                  path('sitemap.xml/', index, {'sitemaps': sitemaps}),
                  path('sitemap-<section>.xml/', sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
                  path('<str:post_slug>/', enderun, name='post-getir'),  # Blog Git
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
