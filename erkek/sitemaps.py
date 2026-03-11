from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from isimler.models import *

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = 'https'

    def items(self):
        return [
            'home',
            'erkek', 'kiz', 'unisex', 'kadin', 'saglik', 'cocuk',
            'pei', 'pki', 'pui',
            'ecgei', 'ecgki', 'ecgui',
            'hakkimizda', 'gizlilik-politikasi', 'kullanim-sartlari', 'iletisim',
            'hayvan-ana',
        ]

    def location(self, item):
        return reverse(item)


class HayvanKategoriSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return HayvanKategori.objects.filter(aktif=True)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])


class HayvanIsimSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return HayvanIsim.objects.filter(aktif=True)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hayvan-detay', args=[obj.slug])

class erkekisimleri(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        PostKategorisi = PostKategori.objects.get(short_title="erkek")
        return Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=PostKategorisi)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])

class kizisimleri(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        PostKategorisi = PostKategori.objects.get(short_title="kiz")
        return Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=PostKategorisi)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])


class unisexisimleri(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        PostKategorisi = PostKategori.objects.get(short_title="unisex")
        return Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=PostKategorisi)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])

class kadin(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        PostKategorisi = PostKategori.objects.get(short_title="kadin")
        return Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=PostKategorisi)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])



class cocuk(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        PostKategorisi = PostKategori.objects.get(short_title="cocuk")
        return Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=PostKategorisi)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])


class saglik(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        PostKategorisi = PostKategori.objects.get(short_title="saglik")
        return Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=PostKategorisi)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])