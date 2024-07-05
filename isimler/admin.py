from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "yazar", "okunma_sayisi", "seo_check", "status", "olusturma_tarihi", "guncelleme_tarihi", "editor","banner","aktif",)#"get_hikayeKategorisi", "get_masalKategorisi",
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("status","aktif","banner","editor",)
    list_editable = ("status","aktif","banner","editor",)


    def seo_check(self, obj):
        checks = []

        # Title check
        title_length = len(obj.title)
        if 50 <= title_length <= 60:
            checks.append(format_html('<span style="color: green;">Title: {}/50-60</span>', title_length))
        else:
            checks.append(format_html('<span style="color: red;">Title: {}/50-60</span>', title_length))

        # H1 check
        h1_length = len(obj.h1)  # Replace 'h1' with the actual field name for your H1
        if 20 <= h1_length <= 70:
            checks.append(format_html('<span style="color: green;">H1: {}/20-70</span>', h1_length))
        else:
            checks.append(format_html('<span style="color: red;">H1: {}/20-70</span>', h1_length))

        # Keywords check
        keywords = obj.keywords.split(",")
        keywords_length = len(keywords)
        if 5 <= keywords_length <= 15:  # Assuming you want between 1 and 10 keywords
            checks.append(format_html('<span style="color: green;">Keywords: {}/5-15</span>', keywords_length))
        else:
            checks.append(format_html('<span style="color: red;">Keywords: {}/5-15</span>', keywords_length))

        # Meta description check
        description_length = len(obj.description)
        if 130 < description_length <= 155:
            checks.append(
                format_html('<span style="color: green;">Meta Description: {}/130-155</span>', description_length))
        else:
            checks.append(
                format_html('<span style="color: red;">Meta Description: {}/130-155</span>', description_length))

        title_words = obj.title.split(" ")
        if len(title_words) != len(set(title_words)):
            checks.append(format_html('<span style="color: red;">Title: Mükkerer kelimeler var</span>'))
        else:
            checks.append(format_html('<span style="color: green;">Title: Süpersin Hepsi Uniq</span>'))

        # H1 duplicate words check
        h1_words = obj.h1.split(" ")  # Replace 'h1' with the actual field name for your H1
        if len(h1_words) != len(set(h1_words)):
            checks.append(format_html('<span style="color: red;">H1: Mükkerer kelimeler var</span>'))
        else:
            checks.append(format_html('<span style="color: green;">H1: Süpersin Hepsi Uniq</span>'))

        return format_html("<br>".join(checks))

    seo_check.short_description = 'SEO'


admin.site.register(Post, PostAdmin)



class allNamesAdmin(admin.ModelAdmin):
    list_display = ("isim", "Durum", )
    search_fields = ("isim",)
    list_filter = ("Durum", "Cinsiyet",)

admin.site.register(allname, allNamesAdmin)


class KategoriAdmin(admin.ModelAdmin):
    list_display = ("Title", "slug", "description", "keywords", "aktif",)
    prepopulated_fields = {'slug': ('Title',)}
    search_fields = ("Title",)
    list_filter = ("aktif",)
    list_editable = ("aktif",)

admin.site.register(PostKategori, KategoriAdmin)

class iletisimAdmin(admin.ModelAdmin):
    list_display = ("email",)


admin.site.register(iletisimmodel, iletisimAdmin)