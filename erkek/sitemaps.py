from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from isimler.models import *

class erkekisimleri(Sitemap):
    changefreq = "daily"
    priority = 1.0
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
    priority = 1.0
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
    priority = 1.0
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
    priority = 1.0
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
    priority = 1.0
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
    priority = 1.0
    protocol = 'https'

    def items(self):
        PostKategorisi = PostKategori.objects.get(short_title="saglik")
        return Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=PostKategorisi)

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('post-getir', args=[obj.slug])