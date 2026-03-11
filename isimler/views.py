from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
import environ
import json
import requests
from django.db.models import Q, F
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.utils.html import strip_tags

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


def turkce_to_ingilizce(kelime):
    harf_haritasi = {
        'ç': 'c',
        'ö': 'o',
        'ğ': 'g',
        'ş': 's',
        'ı': 'i',
        'ü': 'u'
        # Diğer karakterler için de eşlemeleri ekleyin
    }
    ingilizce_kelime = ''
    for harf in kelime:
        if harf in harf_haritasi:
            ingilizce_kelime += harf_haritasi[harf]
        else:
            ingilizce_kelime += harf
    return ingilizce_kelime


# kullanici_metni = "Çalışma Örneği"
# ingilizce_metin = turkce_to_ingilizce(kullanici_metni)
# print(ingilizce_metin)  # Çıktı: "Calisma Ornegi"


def create_unique_title_slug(title):
    slug = slugify(title)
    unique_slug = slug
    num = 1
    while Post.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug


# Create your views here.
def home(request):
    Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kadin")
    kadin = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
        '-olusturma_tarihi')[:3]

    Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="saglik")
    saglik = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
        '-olusturma_tarihi')[:3]

    Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="cocuk")
    cocuk = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
        '-olusturma_tarihi')[:3]

    title = "Erkek Bebek İsimleri ve Kız Bebek İsimleri Anlamları"
    h1 = "En Popüler Kız Bebek İsimleri ve Erkek Bebek İsimleri Anlamları"
    description = "ErkekBebekisimleri ile hayalinizdeki ismi bulun! Anlamlı, nadir, modern ve trend isimler arasından seçim yapın. Bebeğinizin ismi, kişiliğini yansıtsın."
    keywords = "erkek bebek isimleri,erkek isimleri,kız bebek isimleri,kız isimleri,anlamlı isimler,nadir isimler,modern isimler,trend isimler,isim anlamları,oğlum için isim,kızım için isim,isim önerileri,bebek isimleri rehberi,en güzel erkek bebek isimleri,en güzel kız bebek isimleri"
    yazar = "Yüksek Teknoloji"
    resim = "https://teknolojibucket.s3.amazonaws.com/static/assets/logo/logo.webp"

    from django.db.models import Sum
    toplam_isim = Post.objects.filter(aktif=True, status="Yayinda").count()
    toplam_goruntuleme = Post.objects.filter(aktif=True, status="Yayinda").aggregate(t=Sum('okunma_sayisi'))['t'] or 0

    context = {
        'title': title,
        'h1': h1,
        'description': description,
        'keywords': keywords,
        'resim': resim,
        'kadin': kadin,
        'saglik': saglik,
        'cocuk': cocuk,
        'toplam_isim': toplam_isim,
        'toplam_goruntuleme': toplam_goruntuleme,
    }
    return render(request, "home.html", context)


def kategori(request):
    if request.resolver_match.url_name == 'kiz':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kiz")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords
        urlsi = "https://www.erkekbebekisimleri.net/kiz-isimleri/"

    elif request.resolver_match.url_name == 'erkek':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords
        urlsi = "https://www.erkekbebekisimleri.net/erkek-isimleri/"

    elif request.resolver_match.url_name == 'unisex':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords
        urlsi = "https://www.erkekbebekisimleri.net/unisex-isimler/"

    elif request.resolver_match.url_name == 'kadin':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kadin")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords
        urlsi = "https://www.erkekbebekisimleri.net/kadin/"

    elif request.resolver_match.url_name == 'saglik':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="saglik")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords
        urlsi = "https://www.erkekbebekisimleri.net/saglik/"

    elif request.resolver_match.url_name == 'cocuk':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="cocuk")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords
        urlsi = "https://www.erkekbebekisimleri.net/cocuk/"

    # Popüler Olanlar
    elif request.resolver_match.url_name == 'pei':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = "Popüler Erkek İsimleri Anlamları ve Analizleri | Bebek İsimleri"
        h1 = "Popüler Erkek Bebek İsimleri ve Anlamları"
        description = "En popüler erkek bebek isimleri ve anlamları. Bebeğiniz için en trend isimler, kişilik analizleri ve numerolojik yorumlar. Bebeğinize mükemmel ismi seçin."
        keywords = "Modern Bebek isimleri, trend isimler, erkek bebek isimleri, anlamlı isimler, bebek isimleri, popüler bebek isimleri"
        urlsi = "https://www.erkekbebekisimleri.net/populer-erkek-isimleri/"

    elif request.resolver_match.url_name == 'pui':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = "Popüler Unisex İsimler Anlamları ve Analizleri | Bebek İsimleri"
        h1 = "Popüler Unisex Bebek İsimleri ve Anlamları"
        description = "En popüler unisex bebek isimleri ve anlamları. Bebeğiniz için en trend isimler, kişilik analizleri ve numerolojik yorumlar. Bebeğinize mükemmel ismi seçin."
        keywords = "Modern Bebek isimleri, trend isimler, unisex bebek isimleri, anlamlı isimler, bebek isimleri, popüler bebek isimleri"
        urlsi = "https://www.erkekbebekisimleri.net/populer-unisex-isimler/"

    elif request.resolver_match.url_name == 'pki':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kiz")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = "Popüler Kız İsimleri Anlamları ve Analizleri | Bebek İsimleri"
        h1 = "Popüler Kız Bebek İsimleri ve Anlamları"
        description = "En popüler kız bebek isimleri ve anlamları. Bebeğiniz için en trend isimler, kişilik analizleri ve numerolojik yorumlar. Bebeğinize mükemmel ismi seçin."
        keywords = "Modern Bebek isimleri, trend isimler, kız bebek isimleri, anlamlı isimler, bebek isimleri, popüler bebek isimleri"
        urlsi = "https://www.erkekbebekisimleri.net/populer-kiz-isimleri/"


    # Çok Görüntü Olanlar
    elif request.resolver_match.url_name == 'ecgei':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
        TumPost = Post.objects.filter(aktif=True,status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-okunma_sayisi')
        title = "En Çok Bakılan Erkek İsimleri Anlamları ve Analizleri | Bebek İsimleri"
        h1 = "En Çok Görüntülenen Erkek İsimleri Anlamları"
        description = "En çok görüntülenen erkek bebek isimleri ve anlamları. Bebeğiniz için en trend isimler, kişilik analizleri ve numerolojik yorumlar. Bebeğinize mükemmel ismi seçin."
        keywords = "Erkek Bebek İsimleri, isimlerin Anlamları, Trend isimler, Kişilik Analizi ve Numeroloji Yorumları, En Çok Görüntülenen Erkek Bebek İsimleri, Trend Erkek Bebek İsimleri,Modern Erkek Bebek İsimleri"
        urlsi = "https://www.erkekbebekisimleri.net/en-cok-goruntulenen-erkek-isimleri/"



    elif request.resolver_match.url_name == 'ecgui':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-okunma_sayisi')
        title = "En Çok Bakılan Unisex İsimler Anlamları ve Analizleri | Bebek İsimleri"
        h1 = "En Çok Görüntülenen Unisex İsimler Anlamları"
        description = "En çok görüntülenen unisex bebek isimleri ve anlamları. Bebeğiniz için en trend isimler, kişilik analizleri ve numerolojik yorumlar. Bebeğinize mükemmel ismi seçin."
        keywords = "Unisex Bebek İsimleri, isimlerin Anlamları, Trend isimler, Kişilik Analizi ve Numeroloji Yorumları, En Çok Görüntülenen Unisex Bebek İsimleri, Trend Unisex Bebek İsimleri, Modern Unisex Bebek İsimleri"
        urlsi = "https://www.erkekbebekisimleri.net/en-cok-goruntulenen-unisex-isimler/"

    elif request.resolver_match.url_name == 'ecgki':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kiz")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-okunma_sayisi')
        title = "En Çok Bakılan Kız İsimler Anlamları ve Analizleri | Bebek İsimleri"
        h1 = "En Çok Görüntülenen Kız İsimleri Anlamları"
        description = "En çok görüntülenen kız bebek isimleri ve anlamları. Bebeğiniz için en trend isimler, kişilik analizleri ve numerolojik yorumlar. Bebeğinize mükemmel ismi seçin."
        keywords = "Kız Bebek İsimleri, isimlerin Anlamları, Trend isimler, Kişilik Analizi ve Numeroloji Yorumları, En Çok Görüntülenen Kız Bebek İsimleri, Trend Kız Bebek İsimleri,Modern Kız Bebek İsimleri"
        urlsi = "https://www.erkekbebekisimleri.net/en-cok-goruntulenen-kiz-isimleri/"

    else:
        return HttpResponse("Geçersiz kategori.", status=404)

    paginator = Paginator(TumPost, 9)  # 9 içerik göstermek için
    page_number = request.GET.get('sayfa')
    TumPost = paginator.get_page(page_number)

    if page_number is not None and str(page_number) != "1":
        title = f"{title} - Sayfa {page_number}"
        description = f"{description} - Sayfa {page_number}"

    context = {
        'title': title,
        'H1': h1,
        'description': description,
        'keywords': keywords,
        'Post_Kategorisi': Post_Kategorisi,
        'TumPost': TumPost,
        'urlsi': urlsi,
    }

    return render(request, "list.html", context)


def slug_dispatcher(request, post_slug):
    """Tek catch-all: önce HayvanKategori dene, bulamazsa Post'a düş."""
    try:
        kat = HayvanKategori.objects.get(slug=post_slug, aktif=True)
        return hayvan_kategori_liste(request, post_slug)
    except HayvanKategori.DoesNotExist:
        return enderun(request, post_slug)


def enderun(request, post_slug):
    PostEndrun = get_object_or_404(Post, aktif=True, status="Yayinda", slug=post_slug)
    Post.objects.filter(pk=PostEndrun.pk).update(okunma_sayisi=F('okunma_sayisi') + 1)
    soru_cevap = None
    benzer_isimler = PostEndrun.Benzerisimler.split(',') if PostEndrun.Benzerisimler else []
    isim_durumu = []

    benzer_isimler_clean = [i.strip().lower() for i in benzer_isimler if i.strip()]
    existing_posts = Post.objects.filter(
        isim__in=benzer_isimler_clean, aktif=True, status="Yayinda"
    ).select_related('Post_Turu')
    existing_map = {post.isim: post for post in existing_posts}

    for isim in benzer_isimler:
        isim = isim.strip()
        if not isim:
            continue
        benzer_post = existing_map.get(isim.lower())
        if benzer_post:
            isim_durumu.append({
                'isim': isim,
                'exists': True,
                'slug': benzer_post.slug,
                'cinsiyet': benzer_post.Post_Turu.short_title
            })
        else:
            isim_durumu.append({
                'isim': isim,
                'exists': False,
                'slug': None,
                'cinsiyet': None
            })

    if PostEndrun.sss:
        sss = PostEndrun.sss.split("|")
        soru_cevap = [item.split("::") for item in sss]

    # todo tüm içeriği json için veriyorum
    contents = [PostEndrun.icerik1, PostEndrun.icerik2, PostEndrun.icerik3, PostEndrun.icerik4, PostEndrun.icerik5,
                PostEndrun.icerik6, PostEndrun.icerik7]
    articleBody = strip_tags(' '.join(filter(None, contents)))

    # todo tüm resimleri json için veriyorum (mutlak URL)
    resimler = []
    if PostEndrun.resim:
        resimler.append(request.build_absolute_uri(PostEndrun.resim.url))
    if PostEndrun.resim2:
        resimler.append(request.build_absolute_uri(PostEndrun.resim2.url))
    if PostEndrun.resim3:
        resimler.append(request.build_absolute_uri(PostEndrun.resim3.url))
    # if PostEndrun.resim4:
    #    resimler.append(PostEndrun.resim4.url)
    if not resimler:  # Eğer resimler listesi boşsa
        resimler.append("https://teknolojibucket.s3.amazonaws.com/static/assets/logo/logo.webp")

    context = {
        'icerik': PostEndrun,
        'soru_cevap': soru_cevap,
        'isim_durumu': isim_durumu,
        'articleBody': articleBody,
        'resimler': resimler,
        'icerik_resim_abs': (request.build_absolute_uri(PostEndrun.resim.url) if PostEndrun.resim else ''),
    }

    return render(request, "enderun.html", context)


def arama(request):
    # Hem GET hem POST desteklenir; q veya fulltext parametresi ile arama
    query = (
        request.GET.get('q')
        or request.GET.get('fulltext')
        or request.POST.get('q')
        or request.POST.get('fulltext')
        or ''
    )
    gender = request.GET.get('gender') or request.POST.get('gender') or '1'

    if gender == '1':  # Unisex (varsayılan)
        Cinsiyet = "Unisex"
        posts = Post.objects.filter(isim__icontains=query, Post_Turu__short_title='unisex', aktif=True,
                                    status="Yayinda")
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")
    elif gender == '2':  # Erkek
        Cinsiyet = "Erkek"
        posts = Post.objects.filter(isim__icontains=query, Post_Turu__short_title='erkek', aktif=True,
                                    status="Yayinda")
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
    elif gender == '3':  # Kız
        Cinsiyet = "Kız"
        posts = Post.objects.filter(isim__icontains=query, Post_Turu__short_title='kiz', aktif=True,
                                    status="Yayinda")
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kiz")
    else:
        return HttpResponse(
            'Lütfen Formu Kullanarak Tekrar Deneyin. <a href="{}" class="btn btn-primary">Ana Sayfaya Dönmek için Tıklayın.</a>'.format(
                reverse('home')))


    paginator = Paginator(posts, 12)  # Her sayfada 12 sonuç göster
    page_number = request.GET.get('sayfa')
    TumPost = paginator.get_page(page_number)

    title = f"{query} ile gelen arama sonuçları | Erkek Bebek İsimleri"
    H1 = f"{query} ile Yapılan Aramada Bulunan İsimler ve Anlamları"
    description = f"{query} ile gelen arama sonuçları anlamları tüm detayları | Güncel Erkek Bebek İsimleri ve Kız Bebek İsimleri"
    keywords = f"Erkek Bebek İsimleri, Çocuk isimleri, erkek isimleri, isimlerin anlamları, kız isimleri, kız bebek isimleri, modern isimler, yabancı isimler"

    if not posts:
        H1 = f"{query} ile Hiç Bir {Cinsiyet} İsmi Bulunamadı Lütfen Farklı Bir Seçenek ile Deneyin! "

    if page_number is not None:
        title = f"{title} - Sayfa {page_number}"
        description = f"{description} - Sayfa {page_number}"

    # Canonical temel URL (sayfasız)
    base_search_url = f"{request.scheme}://{request.get_host()}/ara/?q={query}&gender={gender}"

    context = {
        'title': title,
        'H1': H1,
        'description': description,
        'keywords': keywords,
        'Post_Kategorisi': Post_Kategorisi,
        'TumPost': TumPost,
        'urlsi': base_search_url,
        'noindex': True,
        'is_search': True,
    }

    return render(request, 'list.html', context)


def gizlilik(request):
    title = "Gizlilik erkekbebekisimleri.net | Bilgilerinizin Korunması"
    description = "erkekbebekisimleri.net gizlilik politikası Kişisel bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin. Gizliliğiniz bizim için en önemlidir."
    keywords = "Gizlilik Politikası, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "erkekbebekisimleri.net Gizlilik Politikası: Kişisel Bilgileriniz Güvende"
    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'gizlilik.html', context)


def iletisim(request):
    title = "iletişim erkekbebekisimleri.net | Bilgilerinizin Korunması"
    description = "erkekbebekisimleri.net iletişim politikası Kişisel bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin."
    keywords = "iletişim Politikası, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "İletişim"

    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': f"{env('RECAPTCHA_PRIVATE_KEY')}",
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            name = request.POST.get('name')
            email = request.POST.get('email')
            icerik = request.POST.get('message')

            iletisim_obj = iletisimmodel(name=name, email=email, icerik=icerik)
            iletisim_obj.save()

            return HttpResponse(
                'İletişim istediğinizi Kaydettik. <a href="{}" class="btn btn-primary">Ana Sayfaya Dönmek için Tıklayın.</a>'.format(
                    reverse('home')))

    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'iletisim.html', context)


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")


robots_txt_content = """User-agent: *
Allow: /
Sitemap: https://www.erkekbebekisimleri.net/sitemap.xml/
""".lstrip()

@require_GET
def ads(request):
    return HttpResponse(ads_content, content_type="text/plain")


ads_content = """google.com, pub-7065951693101615, DIRECT, f08c47fec0942fa0"""

def hakkinda(request):
    title = "Hakkımızda erkekbebekisimleri.net | Erkek Bebek isimleri"
    description = "erkekbebekisimleri.net Hakkımızda bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin. Gizliliğiniz bizim için en önemlidir."
    keywords = "Hakkımızda, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "erkekbebekisimleri.net Hakkımızda     Kişisel Bilgileriniz Güvende"
    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'hakkimizda.html', context)


def cerez(request):
    title = "Çerez Politikamız erkekbebekisimleri.net | Erkek isimleri"
    description = "erkekbebekisimleri.net çerez politikası Kişisel bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin."
    keywords = "çerez Politikası, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "erkekbebekisimleri.net Çerez Politikası Kişisel Bilgileriniz Güvende"
    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'cerez.html', context)


def kullanim(request):
    title = "Kullanım erkekbebekisimleri.net | Bilgilerinizin Korunması"
    description = "erkekbebekisimleri.net Kullanım politikası Kişisel bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin. Gizliliğiniz bizim için en önemlidir."
    keywords = "Kullanım Politikası, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "erkekbebekisimleri.net Kullanım Politikası Kişisel Bilgileriniz Güvende"
    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'kullanim.html', context)


@csrf_exempt
def kisaisimekle(request):
    if request.method == 'POST':
        # Gelen POST isteğindeki değerleri alın
        isim = request.POST.get('isim')
        aciklama = request.POST.get('aciklama')
        Durum = request.POST.get('Durum')
        Cinsiyet = request.POST.get('Cinsiyet')

        isimsonuc = allname(isim=isim, aciklama=aciklama, Durum=Durum, Cinsiyet=Cinsiyet)
        isimsonuc.save()
        if isimsonuc.id is None:
            return HttpResponse("Post kaydedilemedi.")
        else:
            return HttpResponse("Post başarıyla kaydedildi. ID: " + str(isimsonuc.id))


@csrf_exempt
def aicek(request):
    if request.method == 'POST':
        mahsul_cek = allname.objects.filter(Durum="Hazirla").first()
        if mahsul_cek is not None:
            mahsul_cek.Durum = "Yolda"
            mahsul_cek.save()
            Sonucu = f"{mahsul_cek.pk}|={mahsul_cek.isim}|={mahsul_cek.aciklama}|={mahsul_cek.Cinsiyet}"
            return HttpResponse(Sonucu)
        else:
            return HttpResponse("Mahsul bulunamadı")
    else:
        return HttpResponse("Geçersiz istek", status=400)


@csrf_exempt
def aiadd(request):
    if request.method == 'POST':
        # Gelen POST isteğindeki değerleri alın
        GelenID = request.POST.get('GelenID')
        icerik1 = request.POST.get('icerik1')
        icerik2 = request.POST.get('icerik2')
        kisaaciklama = request.POST.get('kisaaciklama')
        isim = request.POST.get('isim')
        benzer = request.POST.get('benzer')
        unlu = request.POST.get('unlu')
        Post_Turu = request.POST.get('Post_Turu')
        title = f"{isim.capitalize()} İsminin Anlamı Nedir? {isim.capitalize()} Adının Özellikleri Nelerdir?"
        h1 = f"{isim.capitalize()} İsminin Anlamı Ve Tüm Kişilik Özellikleri Nelerdir ?"
        slug = f"{isim.lower()} İsminin Anlami nedir ?"
        desc = f"{isim.lower()} isminin anlamı ve özellikleri, {isim.lower()} kuranda geçiyor mu, {isim.lower()} caiz mi, tüm modern bebek isimleri, anlamları ve kişilik özellikleri"
        keys = f"{isim.lower()} ismi anlamı,{isim.lower()} isminin anlamı,{isim.lower()} isminin özellikleri,{isim.lower()} isminin kökeni,{isim.lower()} ismi Kuranda geçiyor mu,{isim.lower()} ismi meşhur olanlar,{isim.lower()} ne demek,{isim.lower()} ismi caiz mi,bebek isimleri,modern isimler,erkek isimleri,kız isimleri,erkek bebek isimleri,kız bebek isimleri"

        Post_Turu_Gelen = PostKategori.objects.get(short_title=Post_Turu)

        yeni_Slug = create_unique_title_slug(slug)
        isimekle = Post(title=title, slug=yeni_Slug, h1=h1, isim=isim, Benzerisimler=benzer, kisaanlam=kisaaciklama,
                        description=desc, keywords=keys, Post_Turu=Post_Turu_Gelen, icerik1=icerik1, icerik2=icerik2,
                        icerik3=unlu)
        isimekle.save()

        allname.objects.filter(id=GelenID).update(Durum="Tamamlandı")

        if isimekle.id is None:
            return HttpResponse("Post kaydedilemedi.")
        else:
            return HttpResponse("Şükürler Olsun Post başarıyla kaydedildi. ID: " + str(isimekle.id))


def oto_Paylas(request):
    post = Post.objects.filter(
        Q(status="oto") & (Q(yayin_tarihi__lte=timezone.now()) | Q(yayin_tarihi=None))).first()
    if post is not None:

        if post.Kuran:
            kuransonuc = f"Evet {post.isim.capitalize()} İsmi Kuranı Kerimde Geçer."
        else:
            kuransonuc = f"Maalesef {post.isim.capitalize()} İsmi Kuranı Kerimde Geçmemektedir."
        if post.Caiz:
            caizsonuc = f"Evet {post.isim.capitalize()} İsmi Caizdir."
        else:
            caizsonuc = f"Maalesef {post.isim.capitalize()} İsmi Caiz Değildir."


        if post.isim:
            sssSonuc = f"{post.isim.capitalize()} isminin anlamı nedir ?::{post.kisaanlam.capitalize()} anlamına gelmektedir.|{post.isim.capitalize()} ismi kuranda geçiyor mu ?::{kuransonuc}|{post.isim.capitalize()} ismi caiz mi ?::{caizsonuc}|{post.isim.capitalize()} isminin cinseyeti nedir?::Genel olarak {post.isim.capitalize()} ismi {post.Post_Turu.short_title.capitalize()} ismi olarak kullanılmaktadır. "
            post.sss = sssSonuc
        post.status = "Yayinda"
        post.aktif = True
        post.olusturma_tarihi = timezone.now()  # eklenme tarihini güncelle
        post.save()
        return HttpResponse(f'Şükürler Olsun "{post.title}" Paylaşıldı.')
    else:
        return HttpResponse('Paylaşılacak Post Bulunamadı.')


@csrf_exempt
def indexing_var_mi(request):
    post = Post.objects.filter(indexing=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.indexing = False
        post.save(update_fields=['indexing'])
        return HttpResponse(f"https://www.erkekbebekisimleri.net/{post.slug}/")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def facebook_var_mi(request):
    post = Post.objects.filter(facebook=True, aktif=True, status="Yayinda").first()
    if post is not None:
        post.facebook = False
        if post.isim:
            icerik = f"{post.isim} İsminin Gizli Anlamı Nedir? Öğrenince Şaşıracaksınız! İsminin Sırrı Nedir? #bebekisimleri"
        else:
            icerik = f"{post.ozet}"
        if not icerik:
            icerik = f"{post.h1}"
        post.save(update_fields=['facebook'])
        return HttpResponse(f"https://www.erkekbebekisimleri.net/{post.slug}/!={icerik}")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def twitter_var_mi(request):
    post = Post.objects.filter(twitter=True, aktif=True, status="Yayinda").first()
    if post is not None:
        post.twitter = False
        hashtag = "#bebekisimleri"
        if post.isim:
            icerik = f"{post.isim.capitalize()} İsminin Gizli Anlamı Nedir? Öğrenince Şaşıracaksınız! İsminin Sırrı Nedir?"
        else:
            icerik = f"{post.h1}"
        if not icerik:
            icerik = f"{post.h1}"
        post.save(update_fields=['twitter'])
        return HttpResponse(f"https://www.erkekbebekisimleri.net/{post.slug}/!={icerik} {hashtag}")
    else:
        return HttpResponse("Paylaşılacak Twitter içerik bulunamadı")


@csrf_exempt
def pinterest_var_mi(request):
    post = Post.objects.filter(pinterest=True, aktif=True, status="Yayinda").first()
    if post is not None:
        post.pinterest = False
        icerik = post.title
        if not icerik:
            icerik = "Bebek İsimleri"
        post.save(update_fields=['pinterest'])
        return HttpResponse(
            f"https://www.erkekbebekisimleri.net/{post.slug}/!={post.kisaanlam} Anlamına gelmektedir. Daha fazla bebek ismi için bizi takip edin!={post.title}!={post.Post_Turu.short_title}!={post.resim.url}")
    else:
        return HttpResponse("post bulunamadı.")


# ==========================================
# HAYVAN İSİMLERİ
# ==========================================

def hayvan_kategori_liste(request, kategori_slug):
    kat = get_object_or_404(HayvanKategori, slug=kategori_slug, aktif=True)
    isimler_qs = HayvanIsim.objects.filter(kategoriler=kat, aktif=True)

    cinsiyet = request.GET.get('cinsiyet')
    if cinsiyet in ('erkek', 'disi', 'unisex'):
        isimler_qs = isimler_qs.filter(cinsiyet=cinsiyet)

    harf = request.GET.get('harf')
    if harf:
        isimler_qs = isimler_qs.filter(isim__istartswith=harf)

    paginator = Paginator(isimler_qs, 12)
    page_number = request.GET.get('sayfa')
    page_obj = paginator.get_page(page_number)

    title = kat.title
    h1 = kat.h1 or kat.title
    description = kat.description
    keywords = kat.keywords

    if page_number is not None:
        title = f"{title} - Sayfa {page_number}"
        description = f"{description} - Sayfa {page_number}"

    tum_kategoriler = HayvanKategori.objects.filter(aktif=True)

    context = {
        'title': title,
        'H1': h1,
        'description': description,
        'keywords': keywords,
        'kategori': kat,
        'isimler': page_obj,
        'tum_kategoriler': tum_kategoriler,
        'secili_cinsiyet': cinsiyet or '',
        'secili_harf': harf or '',
        'urlsi': f"https://www.erkekbebekisimleri.net/{kat.slug}/",
    }
    return render(request, 'hayvan/liste.html', context)


def hayvan_isim_detay(request, isim_slug):
    isim_obj = get_object_or_404(HayvanIsim, slug=isim_slug, aktif=True)
    HayvanIsim.objects.filter(pk=isim_obj.pk).update(okunma_sayisi=F('okunma_sayisi') + 1)

    kategoriler = isim_obj.kategoriler.filter(aktif=True)
    benzer = HayvanIsim.objects.filter(
        kategoriler__in=kategoriler, aktif=True
    ).exclude(pk=isim_obj.pk).distinct()[:12]

    context = {
        'isim': isim_obj,
        'kategoriler': kategoriler,
        'benzer_isimler': benzer,
        'title': isim_obj.title,
        'description': isim_obj.description,
        'keywords': isim_obj.keywords,
    }
    return render(request, 'hayvan/detay.html', context)


def hayvan_ana_sayfa(request):
    kategoriler = HayvanKategori.objects.filter(aktif=True)
    son_eklenen = HayvanIsim.objects.filter(aktif=True).order_by('-olusturma_tarihi')[:6]
    populer = HayvanIsim.objects.filter(aktif=True).order_by('-okunma_sayisi')[:6]

    context = {
        'title': 'Hayvan İsimleri - Evcil Hayvanınız İçin En Güzel İsimler',
        'H1': 'Evcil Hayvanınız İçin En Güzel İsimler',
        'description': 'Köpek, kedi, kuş, balık ve daha fazlası için en güzel hayvan isimleri.',
        'keywords': 'hayvan isimleri, köpek isimleri, kedi isimleri, kuş isimleri, balık isimleri',
        'kategoriler': kategoriler,
        'son_eklenen': son_eklenen,
        'populer': populer,
    }
    return render(request, 'hayvan/ana_sayfa.html', context)


@require_GET
def hayvan_json(request):
    """Tüm hayvan kategorileri ve isimleri JSON olarak döner."""
    from django.http import JsonResponse
    kategoriler = HayvanKategori.objects.filter(aktif=True).prefetch_related('isimler')
    data = []
    for kat in kategoriler:
        isimler = kat.isimler.filter(aktif=True).values('isim', 'slug', 'anlam', 'cinsiyet', 'okunma_sayisi')
        data.append({
            'kategori': kat.title,
            'slug': kat.slug,
            'h1': kat.h1,
            'description': kat.description,
            'ikon': kat.ikon,
            'url': f'https://www.erkekbebekisimleri.net/{kat.slug}/',
            'isim_sayisi': kat.isimler.filter(aktif=True).count(),
            'isimler': list(isimler),
        })
    return JsonResponse({'kategoriler': data, 'toplam_kategori': len(data)}, json_dumps_params={'ensure_ascii': False})


def hepsini_ekle(request):
    """Hayvan kategorileri ve isimlerini toplu ekler."""

    # ── KATEGORİLER ──
    kategori_data = [
        {"title": "Köpek İsimleri", "slug": "kopek-isimleri", "ikon": "bi-award", "sira": 1,
         "h1": "En Güzel Köpek İsimleri", "description": "Erkek ve dişi köpekler için en güzel, en popüler köpek isimleri listesi.", "keywords": "köpek isimleri, erkek köpek isimleri, dişi köpek isimleri"},
        {"title": "Kedi İsimleri", "slug": "kedi-isimleri", "ikon": "bi-heart", "sira": 2,
         "h1": "En Güzel Kedi İsimleri", "description": "Erkek ve dişi kediler için en tatlı, en popüler kedi isimleri listesi.", "keywords": "kedi isimleri, erkek kedi isimleri, dişi kedi isimleri"},
        {"title": "Kuş İsimleri", "slug": "kus-isimleri", "ikon": "bi-feather", "sira": 3,
         "h1": "En Güzel Kuş İsimleri", "description": "Muhabbet kuşu, papağan ve kanarya için en güzel kuş isimleri.", "keywords": "kuş isimleri, muhabbet kuşu isimleri, papağan isimleri"},
        {"title": "Balık İsimleri", "slug": "balik-isimleri", "ikon": "bi-water", "sira": 4,
         "h1": "En Güzel Balık İsimleri", "description": "Akvaryum balıkları ve japon balıkları için en güzel balık isimleri.", "keywords": "balık isimleri, akvaryum balığı isimleri, japon balığı isimleri"},
        {"title": "Hamster İsimleri", "slug": "hamster-isimleri", "ikon": "bi-emoji-smile", "sira": 5,
         "h1": "En Güzel Hamster İsimleri", "description": "Hamsterınız için en tatlı ve en sevimli hamster isimleri listesi.", "keywords": "hamster isimleri, erkek hamster isimleri, dişi hamster isimleri"},
        {"title": "Tavşan İsimleri", "slug": "tavsan-isimleri", "ikon": "bi-flower1", "sira": 6,
         "h1": "En Güzel Tavşan İsimleri", "description": "Tavşanınız için en sevimli ve anlamlı tavşan isimleri listesi.", "keywords": "tavşan isimleri, erkek tavşan isimleri, dişi tavşan isimleri"},
        {"title": "Kaplumbağa İsimleri", "slug": "kaplumbaga-isimleri", "ikon": "bi-shield", "sira": 7,
         "h1": "En Güzel Kaplumbağa İsimleri", "description": "Kaplumbağanız için en güzel ve anlamlı kaplumbağa isimleri.", "keywords": "kaplumbağa isimleri, su kaplumbağası isimleri"},
        {"title": "At İsimleri", "slug": "at-isimleri", "ikon": "bi-trophy", "sira": 8,
         "h1": "En Güzel At İsimleri", "description": "Atınız için en asil ve güçlü at isimleri listesi.", "keywords": "at isimleri, erkek at isimleri, dişi at isimleri, yarış atı isimleri"},
        {"title": "Papağan İsimleri", "slug": "papagan-isimleri", "ikon": "bi-chat-dots", "sira": 9,
         "h1": "En Güzel Papağan İsimleri", "description": "Papağanınız için en eğlenceli ve konuşkan papağan isimleri.", "keywords": "papağan isimleri, sultan papağanı isimleri, jako isimleri"},
        {"title": "Yılan İsimleri", "slug": "yilan-isimleri", "ikon": "bi-lightning", "sira": 10,
         "h1": "En Güzel Yılan İsimleri", "description": "Evcil yılanınız için en egzotik ve etkileyici yılan isimleri.", "keywords": "yılan isimleri, evcil yılan isimleri"},
    ]

    kategoriler = {}
    eklenen_kat = 0
    for kd in kategori_data:
        obj, created = HayvanKategori.objects.get_or_create(
            slug=kd["slug"],
            defaults=kd
        )
        kategoriler[kd["slug"]] = obj
        if created:
            eklenen_kat += 1

    # ── İSİMLER ──
    # (isim, anlam, cinsiyet, [kategori_slug listesi])
    isim_data = [
        # ═══ KÖPEK İSİMLERİ ═══
        ("boncuk", "Küçük ve değerli, boncuk gibi sevimli", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("pamuk", "Yumuşacık ve beyaz, pamuk gibi", "disi", ["kopek-isimleri", "kedi-isimleri", "tavsan-isimleri"]),
        ("karamel", "Tatlı ve sıcak tonlarda, karamel renkli", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("tarçın", "Sıcak ve baharatlı, tarçın renkli tüylü", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("zeytin", "Doğal ve sade güzellik", "unisex", ["kopek-isimleri", "kedi-isimleri", "kus-isimleri", "balik-isimleri"]),
        ("aslan", "Güçlü ve cesur, aslan yürekli", "erkek", ["kopek-isimleri"]),
        ("buddy", "En iyi arkadaş, sadık dost", "erkek", ["kopek-isimleri"]),
        ("lucky", "Şanslı ve neşeli", "erkek", ["kopek-isimleri"]),
        ("max", "En büyük, en güçlü", "erkek", ["kopek-isimleri"]),
        ("bella", "Güzel, zarif ve hoş", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("çakıl", "Küçük taş gibi sert ve dayanıklı", "erkek", ["kopek-isimleri"]),
        ("fıstık", "Küçük ama enerjik, minik fıstık", "disi", ["kopek-isimleri", "kedi-isimleri", "hamster-isimleri"]),
        ("kaplan", "Güçlü ve yırtıcı, kaplan gibi cesur", "erkek", ["kopek-isimleri"]),
        ("kurt", "Vahşi ve özgür, kurt gibi sadık", "erkek", ["kopek-isimleri"]),
        ("duman", "Gizemli ve gri tonlarında", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("paşa", "Asil ve heybetli, paşa gibi görkemli", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("prenses", "Zarif ve nazlı, bir prenses gibi", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("çomar", "Geleneksel Türk çoban köpeği ismi", "erkek", ["kopek-isimleri"]),
        ("karabas", "Kara başlı, geleneksel köpek ismi", "erkek", ["kopek-isimleri"]),
        ("findik", "Küçük, yuvarlak ve sevimli", "disi", ["kopek-isimleri", "kedi-isimleri", "hamster-isimleri"]),
        ("zeus", "Tanrıların kralı, güçlü ve heybetli", "erkek", ["kopek-isimleri"]),
        ("luna", "Ay gibi parlak ve güzel", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("rocky", "Kayalar gibi sağlam ve güçlü", "erkek", ["kopek-isimleri"]),
        ("daisy", "Papatya gibi taze ve sevimli", "disi", ["kopek-isimleri", "tavsan-isimleri"]),
        ("charlie", "Neşeli, eğlenceli ve oyuncu", "erkek", ["kopek-isimleri"]),
        ("toby", "Sadık ve sevecen dost", "erkek", ["kopek-isimleri"]),
        ("maya", "Gizemli ve büyüleyici", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("oscar", "Cesur ve soylu savaşçı", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("sasha", "İnsanların koruyucusu", "disi", ["kopek-isimleri"]),
        ("rex", "Kral, hükümdar", "erkek", ["kopek-isimleri"]),

        # ═══ KEDİ İSİMLERİ ═══
        ("tekir", "Çizgili ve geleneksel kedi ismi", "unisex", ["kedi-isimleri"]),
        ("minnak", "Küçücük ve çok tatlı", "disi", ["kedi-isimleri"]),
        ("pati", "Sevimli patileriyle bilinen", "unisex", ["kedi-isimleri"]),
        ("miyav", "Kedilerin sesi gibi tatlı", "unisex", ["kedi-isimleri"]),
        ("ponçik", "Tombul ve sevimli, ponçik gibi", "unisex", ["kedi-isimleri", "hamster-isimleri"]),
        ("simba", "Aslan kral, cesur ve güçlü", "erkek", ["kedi-isimleri"]),
        ("cleo", "Kleopatra'dan esinlenilmiş, asil", "disi", ["kedi-isimleri"]),
        ("whiskers", "Bıyıklı ve meraklı", "erkek", ["kedi-isimleri"]),
        ("misty", "Sisli ve gizemli güzellik", "disi", ["kedi-isimleri"]),
        ("tiger", "Kaplan gibi çizgili ve güçlü", "erkek", ["kedi-isimleri"]),
        ("nala", "Aslan kralın sadık yoldaşı", "disi", ["kedi-isimleri"]),
        ("garfield", "Turuncu ve sevimli, tembel kedi", "erkek", ["kedi-isimleri"]),
        ("bıdık", "Ufacık ve çok sevimli", "unisex", ["kedi-isimleri", "hamster-isimleri"]),
        ("maviş", "Mavi gözlü güzel", "disi", ["kedi-isimleri", "kus-isimleri"]),
        ("tüylü", "Kabarık ve yumuşak tüylü", "unisex", ["kedi-isimleri"]),
        ("siyah", "Gece gibi kara ve gizemli", "unisex", ["kedi-isimleri"]),
        ("sarman", "Sarı-turuncu tüylü kedi", "erkek", ["kedi-isimleri"]),
        ("çiçek", "Çiçek gibi güzel ve zarif", "disi", ["kedi-isimleri", "tavsan-isimleri"]),
        ("melek", "Melek gibi uslu ve güzel", "disi", ["kedi-isimleri", "tavsan-isimleri"]),
        ("tırnak", "Sivri tırnaklı ve oyuncu", "erkek", ["kedi-isimleri"]),

        # ═══ KUŞ İSİMLERİ ═══
        ("cıvıl", "Cıvıl cıvıl öten, neşeli kuş", "unisex", ["kus-isimleri"]),
        ("tüy", "Hafif ve zarif, tüy gibi", "unisex", ["kus-isimleri"]),
        ("melodí", "Güzel ezgiler söyleyen", "disi", ["kus-isimleri"]),
        ("tweety", "Sevimli ve sarı, çizgi film karakteri", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("kanarya", "Sarı ve güzel sesli", "unisex", ["kus-isimleri"]),
        ("bulut", "Özgür ve hafif, bulut gibi uçan", "unisex", ["kus-isimleri", "kedi-isimleri", "tavsan-isimleri"]),
        ("şeker", "Tatlı ve sevimli, şeker gibi", "disi", ["kus-isimleri", "hamster-isimleri", "tavsan-isimleri"]),
        ("limon", "Sarı ve ferahlatıcı", "unisex", ["kus-isimleri", "balik-isimleri"]),
        ("rüzgar", "Hızlı ve özgür, rüzgar gibi", "erkek", ["kus-isimleri", "at-isimleri"]),
        ("cennet", "Cennet kuşu gibi güzel", "disi", ["kus-isimleri"]),
        ("şakrak", "Neşeyle şakıyan, canlı ve enerjik", "unisex", ["kus-isimleri"]),
        ("mavimsi", "Mavi tonlarında güzel kuş", "unisex", ["kus-isimleri"]),
        ("gonca", "Henüz açmamış gül, zarif", "disi", ["kus-isimleri"]),
        ("vivaldi", "Müzikal ve sanatsal", "erkek", ["kus-isimleri", "papagan-isimleri"]),
        ("mozart", "Büyük müzisyen gibi sesli", "erkek", ["kus-isimleri", "papagan-isimleri"]),
        ("pırıl", "Pırıl pırıl parlayan", "disi", ["kus-isimleri"]),

        # ═══ BALIK İSİMLERİ ═══
        ("nemo", "Kayıp balık, maceraperest", "erkek", ["balik-isimleri"]),
        ("dory", "Unutkan ama sevimli mavi balık", "disi", ["balik-isimleri"]),
        ("goldie", "Altın sarısı japon balığı", "disi", ["balik-isimleri"]),
        ("mercan", "Deniz mercanı gibi renkli", "disi", ["balik-isimleri"]),
        ("dalga", "Deniz dalgası gibi hareketli", "unisex", ["balik-isimleri"]),
        ("inci", "Denizin incisi gibi değerli", "disi", ["balik-isimleri", "kedi-isimleri"]),
        ("okyanus", "Derin ve engin, okyanus gibi", "erkek", ["balik-isimleri"]),
        ("yıldız", "Deniz yıldızı gibi parlak", "disi", ["balik-isimleri", "kedi-isimleri", "kopek-isimleri"]),
        ("atlas", "Güçlü ve dayanıklı", "erkek", ["balik-isimleri"]),
        ("neptün", "Denizler tanrısı", "erkek", ["balik-isimleri"]),
        ("pul", "Balık pulu gibi parlak", "unisex", ["balik-isimleri"]),
        ("kumsal", "Sahil ve deniz kokusu", "unisex", ["balik-isimleri"]),
        ("turkuaz", "Turkuaz mavi renk gibi", "unisex", ["balik-isimleri"]),
        ("deniz", "Engin ve derin", "unisex", ["balik-isimleri", "kedi-isimleri"]),
        ("marina", "Denizle ilgili, liman güzeli", "disi", ["balik-isimleri"]),

        # ═══ HAMSTER İSİMLERİ ═══
        ("ceviz", "Küçük ve yuvarlak, ceviz gibi", "unisex", ["hamster-isimleri"]),
        ("çıtır", "Çıtır çıtır kemiren, sevimli", "disi", ["hamster-isimleri"]),
        ("topik", "Yuvarlak ve top gibi", "erkek", ["hamster-isimleri"]),
        ("minik", "Küçücük ve sevimli", "unisex", ["hamster-isimleri", "tavsan-isimleri"]),
        ("kurabiye", "Tatlı ve yuvarlak, kurabiye gibi", "disi", ["hamster-isimleri"]),
        ("badem", "Badem gözlü ve zarif", "disi", ["hamster-isimleri", "kedi-isimleri"]),
        ("karamel", "Tatlı ve sıcak tonlarda", "disi", ["hamster-isimleri"]),
        ("nugget", "Küçük altın parçası", "erkek", ["hamster-isimleri"]),
        ("peluş", "Peluş oyuncak gibi yumuşak", "unisex", ["hamster-isimleri", "tavsan-isimleri"]),
        ("susam", "Küçücük ama lezzetli", "unisex", ["hamster-isimleri"]),
        ("lokum", "Türk lokumu gibi tatlı", "disi", ["hamster-isimleri"]),
        ("pofuduk", "Kabarık ve yumuşacık", "unisex", ["hamster-isimleri", "tavsan-isimleri"]),
        ("mısır", "Mısır tanesi gibi sarı ve minik", "unisex", ["hamster-isimleri"]),
        ("yerfıstığı", "Yerfıstığı seven sevimli kemirgen", "unisex", ["hamster-isimleri"]),

        # ═══ TAVŞAN İSİMLERİ ═══
        ("papatyam", "Papatya gibi beyaz ve masum", "disi", ["tavsan-isimleri"]),
        ("havuç", "Havuç seven sevimli tavşan", "unisex", ["tavsan-isimleri"]),
        ("tüfek", "Hızlı koşan, çevik tavşan", "erkek", ["tavsan-isimleri"]),
        ("kar", "Bembeyaz ve saf, kar gibi", "unisex", ["tavsan-isimleri", "kedi-isimleri"]),
        ("zıpzıp", "Zıplayan ve oyuncu", "unisex", ["tavsan-isimleri"]),
        ("yonca", "Şanslı yonca yaprağı", "disi", ["tavsan-isimleri"]),
        ("cotton", "Pamuk gibi beyaz ve yumuşak", "disi", ["tavsan-isimleri"]),
        ("bunny", "Sevimli küçük tavşan", "disi", ["tavsan-isimleri"]),
        ("toffee", "Karamel şeker gibi tatlı", "unisex", ["tavsan-isimleri"]),
        ("oreo", "Siyah beyaz, kurabiye gibi", "unisex", ["tavsan-isimleri", "hamster-isimleri", "kedi-isimleri"]),
        ("latte", "Sütlü kahve rengi, yumuşak", "disi", ["tavsan-isimleri", "kedi-isimleri"]),
        ("tüylüş", "Tüylü ve sevimli tavşan", "unisex", ["tavsan-isimleri"]),

        # ═══ KAPLUMBAĞA İSİMLERİ ═══
        ("ninja", "Ninja kaplumbağalar gibi cesur", "erkek", ["kaplumbaga-isimleri"]),
        ("yavaş", "Ağır ama emin adımlarla", "unisex", ["kaplumbaga-isimleri"]),
        ("tank", "Zırhı gibi sağlam kabuk", "erkek", ["kaplumbaga-isimleri"]),
        ("kaya", "Kaya gibi sert ve dayanıklı", "erkek", ["kaplumbaga-isimleri"]),
        ("zümrüt", "Yeşil zümrüt gibi değerli", "disi", ["kaplumbaga-isimleri"]),
        ("çakıltaşı", "Irmak kenarındaki yuvarlak taş", "unisex", ["kaplumbaga-isimleri"]),
        ("yeşil", "Doğanın rengi, huzurlu", "unisex", ["kaplumbaga-isimleri"]),
        ("sheldon", "Kabuklu dostun adı", "erkek", ["kaplumbaga-isimleri"]),
        ("turbo", "Hızlı kaplumbağa, sürpriz hız", "erkek", ["kaplumbaga-isimleri"]),
        ("bilge", "Yaşlı ve bilge, sabırlı", "unisex", ["kaplumbaga-isimleri"]),
        ("donatello", "Ninja kaplumbağa, sanatçı ruhlu", "erkek", ["kaplumbaga-isimleri"]),
        ("rafaello", "Ninja kaplumbağa, savaşçı", "erkek", ["kaplumbaga-isimleri"]),

        # ═══ AT İSİMLERİ ═══
        ("yıldırım", "Şimşek gibi hızlı ve güçlü", "erkek", ["at-isimleri"]),
        ("fırtına", "Fırtına gibi güçlü ve coşkulu", "erkek", ["at-isimleri"]),
        ("şahlan", "Şahlanan, asil ve görkemli", "erkek", ["at-isimleri"]),
        ("küheylan", "Soylu Arap atı", "erkek", ["at-isimleri"]),
        ("alaca", "Alacalı, renkli tüylü at", "disi", ["at-isimleri"]),
        ("doru", "Doru renkli, kahverengi at", "erkek", ["at-isimleri"]),
        ("gökhan", "Göklerin hükümdarı", "erkek", ["at-isimleri"]),
        ("cesur", "Korkusuz ve yiğit", "erkek", ["at-isimleri", "kopek-isimleri"]),
        ("sultan", "Hükümdar, asil ve güçlü", "erkek", ["at-isimleri", "kopek-isimleri"]),
        ("kraliçe", "Asil ve zarif dişi at", "disi", ["at-isimleri"]),
        ("yelen", "Yeleli ve görkemli", "erkek", ["at-isimleri"]),
        ("karayel", "Kuzeyden esen güçlü rüzgar", "erkek", ["at-isimleri"]),
        ("bora", "Sert ve soğuk rüzgar gibi güçlü", "erkek", ["at-isimleri"]),
        ("akın", "Hızlı ve durdurulamaz", "erkek", ["at-isimleri"]),

        # ═══ PAPAĞAN İSİMLERİ ═══
        ("polly", "Klasik papağan ismi, konuşkan", "disi", ["papagan-isimleri"]),
        ("lori", "Renkli ve neşeli papağan", "disi", ["papagan-isimleri"]),
        ("rio", "Renkli ve tropik, maceraperest", "erkek", ["papagan-isimleri", "kus-isimleri"]),
        ("koko", "Zeki ve konuşkan papağan", "unisex", ["papagan-isimleri"]),
        ("bıcırık", "Çok konuşan, cıvıl cıvıl", "unisex", ["papagan-isimleri"]),
        ("geveze", "Çok konuşmayı seven", "unisex", ["papagan-isimleri"]),
        ("pranga", "Güçlü gagalı ve kararlı", "erkek", ["papagan-isimleri"]),
        ("yeşilçam", "Yeşil tüylü papağan", "unisex", ["papagan-isimleri"]),
        ("amazon", "Amazon ormanlarının güzeli", "disi", ["papagan-isimleri"]),
        ("pikaçu", "Sarı ve enerjik, sevimli", "unisex", ["papagan-isimleri", "kus-isimleri"]),
        ("zazu", "Aslan kral filminden, sadık kuş", "erkek", ["papagan-isimleri", "kus-isimleri"]),
        ("iago", "Aladdin filminden, kurnaz papağan", "erkek", ["papagan-isimleri"]),

        # ═══ YILAN İSİMLERİ ═══
        ("kobra", "Güçlü ve heybetli yılan", "erkek", ["yilan-isimleri"]),
        ("nagini", "Harry Potter'dan gizemli yılan", "disi", ["yilan-isimleri"]),
        ("medusa", "Mitolojik yılan saçlı varlık", "disi", ["yilan-isimleri"]),
        ("venom", "Zehirli ve güçlü", "erkek", ["yilan-isimleri"]),
        ("python", "Büyük ve güçlü piton yılanı", "erkek", ["yilan-isimleri"]),
        ("jade", "Yeşim taşı gibi yeşil ve değerli", "disi", ["yilan-isimleri"]),
        ("gölge", "Sessiz ve gizemli, gölge gibi", "unisex", ["yilan-isimleri", "kedi-isimleri"]),
        ("zehir", "Güçlü ve etkileyici", "erkek", ["yilan-isimleri"]),
        ("ipek", "Pürüzsüz ve zarif, ipek gibi", "disi", ["yilan-isimleri"]),
        ("slyther", "Kayarak hareket eden, çevik", "erkek", ["yilan-isimleri"]),
        ("basilisk", "Mitolojik dev yılan", "erkek", ["yilan-isimleri"]),
        ("onyx", "Siyah ve parlak değerli taş", "unisex", ["yilan-isimleri", "kedi-isimleri"]),

        # YENI KÖPEK İSİMLERİ
        ("bozkurt", "Mitolojik ulu kurt", "erkek", ["kopek-isimleri"]),
        ("asena", "Dişi kurt", "disi", ["kopek-isimleri"]),
        ("toros", "Yüce dağ", "erkek", ["kopek-isimleri", "at-isimleri"]),
        ("bobi", "Sevecen", "erkek", ["kopek-isimleri"]),
        ("maskot", "Şanslı", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("apollo", "Yunan tanrısı", "erkek", ["kopek-isimleri", "at-isimleri"]),
        ("aşil", "Yenilmez", "erkek", ["kopek-isimleri"]),
        ("bingo", "Mutluluk", "unisex", ["kopek-isimleri"]),
        ("snoop", "Meraklı", "erkek", ["kopek-isimleri"]),
        ("rambo", "Savaşçı", "erkek", ["kopek-isimleri"]),

        # YENİ KEDİ İSİMLERİ
        ("pişmaniye", "Tel tel beyaz", "unisex", ["kedi-isimleri", "tavsan-isimleri"]),
        ("lili", "Masum", "disi", ["kedi-isimleri"]),
        ("tırmık", "Pati atan", "unisex", ["kedi-isimleri"]),
        ("zilli", "Hareketli", "disi", ["kedi-isimleri"]),
        ("yoda", "Bilge bakışlı", "erkek", ["kedi-isimleri"]),
        ("kekik", "Ufak tefek", "unisex", ["kedi-isimleri"]),
        ("poğaça", "Tombul", "unisex", ["kedi-isimleri"]),
        ("simit", "Kıvrılıp yatan", "unisex", ["kedi-isimleri"]),
        ("dumanlı", "Gri renkli", "unisex", ["kedi-isimleri"]),
        ("minnoş", "Çok sevimli", "unisex", ["kedi-isimleri", "tavsan-isimleri"]),

        # YENİ KUŞ İSİMLERİ
        ("cicikuş", "Sevimli kuş", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("kanat", "Bağımsız", "erkek", ["kus-isimleri"]),
        ("nefes", "Hayat veren", "unisex", ["kus-isimleri"]),
        ("zıpır", "Taklacı", "erkek", ["kus-isimleri"]),
        ("yankı", "Sesçi", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("dudu", "Diller döken", "disi", ["kus-isimleri", "papagan-isimleri"]),
        ("seher", "Erken öten", "disi", ["kus-isimleri"]),
        ("mavi", "Mavi renkli", "unisex", ["kus-isimleri", "balik-isimleri", "papagan-isimleri"]),
        ("juju", "Sevimli ses", "unisex", ["kus-isimleri"]),
        ("neşeli", "Her zaman öten", "unisex", ["kus-isimleri"]),

        # YENİ BALIK İSİMLERİ
        ("beta", "Savaşçı", "erkek", ["balik-isimleri"]),
        ("lepistes", "Çok renkli", "unisex", ["balik-isimleri"]),
        ("çupra", "İştahlı", "unisex", ["balik-isimleri"]),
        ("ıstakoz", "Kırmızı", "erkek", ["balik-isimleri"]),
        ("kalamar", "Esnek", "unisex", ["balik-isimleri"]),
        ("karides", "Zıplayan", "unisex", ["balik-isimleri"]),
        ("dalgıç", "Dipte yüzen", "erkek", ["balik-isimleri"]),
        ("pusula", "Yolunu bilen", "unisex", ["balik-isimleri"]),
        ("hamsi", "Çok hızlı", "unisex", ["balik-isimleri"]),
        ("yunus", "Dostane", "erkek", ["balik-isimleri"]),

        # YENİ HAMSTER İSİMLERİ
        ("cüzdan", "Yiyecek saklayan", "unisex", ["hamster-isimleri"]),
        ("pinpon", "Beyaz ufak", "unisex", ["hamster-isimleri"]),
        ("tetris", "Her yere sığan", "unisex", ["hamster-isimleri"]),
        ("scooter", "Çok hızlı", "erkek", ["hamster-isimleri"]),
        ("atari", "Durmak bilmeyen", "unisex", ["hamster-isimleri"]),
        ("çekirdek", "En sevdiği", "unisex", ["hamster-isimleri", "kus-isimleri"]),
        ("fırfır", "Yerinde duramayan", "unisex", ["hamster-isimleri"]),
        ("kemirgen", "Sürekli kemiren", "erkek", ["hamster-isimleri"]),
        ("tıknaz", "Tombul", "erkek", ["hamster-isimleri"]),
        ("kaşar", "Peynir seven", "unisex", ["hamster-isimleri"]),

        # YENİ TAVŞAN İSİMLERİ
        ("seksek", "Hoplayan", "unisex", ["tavsan-isimleri"]),
        ("hoppala", "Sıçrayan", "unisex", ["tavsan-isimleri"]),
        ("kaçak", "Sürekli sıvışan", "erkek", ["tavsan-isimleri"]),
        ("çimen", "Yeşillik", "disi", ["tavsan-isimleri"]),
        ("beyaz", "Lekesiz", "unisex", ["tavsan-isimleri"]),
        ("zıpzıp", "Sürekli zıplayan", "unisex", ["tavsan-isimleri"]),
        ("ponpon", "Yuvarlak", "unisex", ["tavsan-isimleri"]),
        ("puf", "Yumuşacık", "unisex", ["tavsan-isimleri"]),
        ("lola", "Sevimli", "disi", ["tavsan-isimleri"]),
        ("marul", "Yeşillik seven", "unisex", ["tavsan-isimleri", "kaplumbaga-isimleri"]),

        # YENİ KAPLUMBAĞA İSİMLERİ
        ("çiko", "Büyük ve yaşlı", "erkek", ["kaplumbaga-isimleri"]),
        ("kayaalp", "Sert zırhlı", "erkek", ["kaplumbaga-isimleri"]),
        ("zırh", "Korunaklı", "unisex", ["kaplumbaga-isimleri"]),
        ("tosun", "İri yarı", "erkek", ["kaplumbaga-isimleri"]),
        ("gezgin", "Sürekli dolaşan", "unisex", ["kaplumbaga-isimleri"]),
        ("nene", "Yaşlı görünümlü", "disi", ["kaplumbaga-isimleri"]),
        ("dede", "Uzun ömürlü", "erkek", ["kaplumbaga-isimleri"]),
        ("miskin", "Uyuyan", "unisex", ["kaplumbaga-isimleri"]),
        ("dodo", "Eğlenceli isim", "erkek", ["kaplumbaga-isimleri"]),
        ("yeşilay", "Parlak yeşil", "unisex", ["kaplumbaga-isimleri"]),

        # YENİ AT İSİMLERİ
        ("şimal", "Kuzeyden", "disi", ["at-isimleri"]),
        ("tayyar", "Uçan", "erkek", ["at-isimleri"]),
        ("sürat", "Hız", "unisex", ["at-isimleri"]),
        ("boran", "Fırtına", "erkek", ["at-isimleri"]),
        ("kırat", "Beyaz", "erkek", ["at-isimleri"]),
        ("yağız", "Siyah", "erkek", ["at-isimleri"]),
        ("rüzgargülü", "Hızlı", "disi", ["at-isimleri"]),
        ("şampiyon", "Yarış kazanan", "erkek", ["at-isimleri"]),
        ("tayfun", "Şiddetli", "erkek", ["at-isimleri"]),
        ("pegasus", "Kanatlı", "erkek", ["at-isimleri"]),

        # YENİ PAPAĞAN İSİMLERİ
        ("mucize", "Şaşırtan", "disi", ["papagan-isimleri"]),
        ("şair", "Konuşan", "erkek", ["papagan-isimleri"]),
        ("maşallah", "Güzel", "unisex", ["papagan-isimleri"]),
        ("renkli", "Çok renkli", "unisex", ["papagan-isimleri"]),
        ("jak", "Jako türü", "erkek", ["papagan-isimleri"]),
        ("sultan", "Sultan papağanı", "disi", ["papagan-isimleri"]),
        ("ara", "Ara türü", "disi", ["papagan-isimleri"]),
        ("kakadu", "İbikli", "unisex", ["papagan-isimleri"]),
        ("mango", "Sarı turuncu", "unisex", ["papagan-isimleri"]),
        ("ıslık", "İslık çalan", "erkek", ["papagan-isimleri"]),

        # YENİ YILAN İSİMLERİ
        ("sürgün", "Kayarak ilerleyen", "erkek", ["yilan-isimleri"]),
        ("boğucu", "Saran", "erkek", ["yilan-isimleri"]),
        ("slither", "Sürünerek", "unisex", ["yilan-isimleri"]),
        ("tıss", "Ses", "unisex", ["yilan-isimleri"]),
        ("piton", "Büyük", "erkek", ["yilan-isimleri"]),
        ("boa", "Büyük yılan", "erkek", ["yilan-isimleri"]),
        ("engerek", "Zehirli", "disi", ["yilan-isimleri"]),
        ("kaygan", "Pullu", "unisex", ["yilan-isimleri"]),
        ("şerit", "Çizgili", "unisex", ["yilan-isimleri"]),
        # YENİ EKLENEN 200 İSİM

        # KÖPEK İSİMLERİ (+20)
        ("mars", "Savaşçı ve cesur, korumacı ruh", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("gofret", "Tatlı, kahverengi ve çıtır ufaklık", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("tarzan", "Ormanlar kralı, doğayı seven", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("kahve", "Sıcak bir koyu ton, uyku sever", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("baron", "Saygın, ağırbaşlı, asil duruş", "erkek", ["kopek-isimleri"]),
        ("balina", "İri yarı, devasa cüsseli ve çok iştahlı", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("badem", "Tatlı, uslu, bal gözlü ve uysal", "disi", ["kopek-isimleri", "kedi-isimleri", "tavsan-isimleri"]),
        ("moka", "Hem tatlı hem uyanık, kahvemsi", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("duman", "Gidenin arkasından süzülen sessizlik", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("cesi", "Çok cesur ve gözü pek", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("ares", "Korkusuz, evi kollayan savaş tanrısı", "erkek", ["kopek-isimleri"]),
        ("lokum", "Lokum gibi pofuduk, bembeyaz ve tatlı", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("hera", "Gururlu, evini sahiplenen baş tanrıça", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("zorro", "Maskeli yüz hattına sahip siyahlı kahraman", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("susam", "Sarı, krem gibi açık kahve, ufak ve leziz", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("poyraz", "Serin bir esinti gibi ferah ve güçlü rüzgar", "erkek", ["kopek-isimleri", "at-isimleri"]),
        ("hector", "Zırhlı, sarsılmaz, heybetli kapı bekçisi", "erkek", ["kopek-isimleri"]),
        ("yaman", "Yaramazlıkta üstüne olmayan zeki ufaklık", "erkek", ["kopek-isimleri", "kedi-isimleri"]),
        ("kuki", "Sıcacık fırından çıkmış bir kalp hırsızı kurabiye", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("efe", "Başı dik, gururlu, memleket sevdalısı sokak çocuğu", "erkek", ["kopek-isimleri"]),

        # KEDİ İSİMLERİ (+20)
        ("macaron", "Renkli hevesli şık Fransız beyefendi/hanımefendisi", "unisex", ["kedi-isimleri"]),
        ("şurup", "Yapışkan sırnaşık, şifalı dostluk veren", "unisex", ["kedi-isimleri"]),
        ("rüya", "Uykucu rüyalar perisi bir melek", "disi", ["kedi-isimleri", "kopek-isimleri"]),
        ("fındıkkıran", "Yaramazlık yaparken sürekli bir şeyleri ısıran", "erkek", ["kedi-isimleri"]),
        ("safir", "Değerli maviş gözlere sahip kıymetli maden", "unisex", ["kedi-isimleri", "kus-isimleri"]),
        ("gece", "Zifiri karanlık ortamda bile parlayan avcı", "unisex", ["kedi-isimleri", "kopek-isimleri", "at-isimleri"]),
        ("şans", "Eve girdikten sonra bolluk getirdiğine inanılan melek", "unisex", ["kedi-isimleri", "kopek-isimleri"]),
        ("çorap", "Dört pati de farklı renk ayaklık giymiş çoraplı çocuk", "unisex", ["kedi-isimleri", "kopek-isimleri"]),
        ("safari", "Vahşi doğasına geri dönmek isteyen vahşi avcı", "unisex", ["kedi-isimleri"]),
        ("mochi", "Dolgun pembe beyaz suratlı yapışkan asya tatlısı", "unisex", ["kedi-isimleri"]),
        ("sütlaç", "Sütte yıkanmış gibi bembeyaz kar topu", "unisex", ["kedi-isimleri"]),
        ("mırnav", "Konuşmayı çok seven ve mırıl mırıl gezen", "unisex", ["kedi-isimleri"]),
        ("düğme", "Ufacık kömür karası pıt bir burna sahip şirin", "unisex", ["kedi-isimleri"]),
        ("kül", "Sessiz sakin ev köşesinde soba başında uyuyan gri ufaklık", "unisex", ["kedi-isimleri"]),
        ("cadı", "Küçük bir süpürgesi eksik hiperaktif yaramaz dişi", "disi", ["kedi-isimleri"]),
        ("böcek", "Oradan oraya koşan ele avuca sığmayan çılgın fırlama", "unisex", ["kedi-isimleri", "kopek-isimleri"]),
        ("cappuccino", "Sütlü köpüklü rahatlatıcı pufidi kış uykucusu", "unisex", ["kedi-isimleri", "kopek-isimleri"]),
        ("tozlu", "Sokak çocuğu hissiyatlı gizemli kül rengi şirin", "unisex", ["kedi-isimleri"]),
        ("şeftali", "Pembe tatlı bir yanak gibi şeftali esintisi dişi sultanı", "disi", ["kedi-isimleri"]),
        ("minnoş", "Annesinin en sevdiği küçük gözbebeği bebeği", "disi", ["kedi-isimleri", "kopek-isimleri"]),

        # KUŞ İSİMLERİ (+20)
        ("bahar", "Canlı bir mevsim neşesi yayan, tomurcuk çiçek", "disi", ["kus-isimleri"]),
        ("ufuk", "Gözleri uzaklara bakan uçmayı bekleyen kaptan", "erkek", ["kus-isimleri"]),
        ("alisa", "Zarif narin uzun kanatlarıyla büyüleyici masal kahramanı", "disi", ["kus-isimleri"]),
        ("güneş", "Günün ilk ışıkları ile cıvıldayan sapsarı tatlı yıldız", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("şarkı", "Kafesinde her gün yeni bir konsere uyanan maestro", "disi", ["kus-isimleri"]),
        ("damla", "Ufacık narin su zerresi gibi maviş huzur", "disi", ["kus-isimleri"]),
        ("özgür", "Kafes sevmeyen kapılar açılınca durmayan asil ruh", "erkek", ["kus-isimleri", "papagan-isimleri"]),
        ("kivi", "Tüyleri meyve kadar tatlı yeşil şirin çocuk", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("çisil", "Su sıçratan fırlama ıslak ve heyecanlı şakıyan dost", "disi", ["kus-isimleri"]),
        ("limoni", "Sarı renkte ekşi ama çok ferah ufak yaz esintisi", "unisex", ["kus-isimleri"]),
        ("bülbül", "En dokunaklı şakımalara eşlik eden ince saz aşığı", "erkek", ["kus-isimleri"]),
        ("sümbül", "Erkenci tomurcuk açan gözkamaştıran orkide pembesi-mavisi", "disi", ["kus-isimleri"]),
        ("gül", "Klasik aşk sembolü evin tatlı nazlı gülü", "disi", ["kus-isimleri"]),
        ("yakamoz", "Parlayarak göz alan denizde oynaşan ışık yansıması", "unisex", ["kus-isimleri", "balik-isimleri"]),
        ("aydın", "Eve neşe ve nur getiren aydınlık zihniyet", "erkek", ["kus-isimleri"]),
        ("nağme", "Kafesteki yalnızlığından şikayet edip dert çalan kemancı", "disi", ["kus-isimleri"]),
        ("nota", "Tek heceli komik uyarılarıyla hep hareketli maestro", "disi", ["kus-isimleri"]),
        ("su", "Berrak dupduru mavi gökyüzü yansımalı saf melek", "disi", ["kus-isimleri", "balik-isimleri"]),
        ("hür", "Bağımsızlık ilan etmiş parmak ısıran korkusuz efe", "erkek", ["kus-isimleri", "papagan-isimleri"]),
        ("asuman", "Bulutlardan inip gelen gökyüzünün masmavi narin sefiri", "disi", ["kus-isimleri"]),

        # BALIK İSİMLERİ (+20)
        ("köpük", "Su üstünde çılgınca salınan beyaz renkli minik hava yastığı", "unisex", ["balik-isimleri"]),
        ("siren", "Duyan herkesi akvaryuma kitleyen güzel efsuncu denizkızı", "disi", ["balik-isimleri"]),
        ("balon", "Patlak gözlü karnı şişko tatlı ve tombik", "unisex", ["balik-isimleri"]),
        ("akıntı", "Akvaryum motorunda hızlıca süzülen inatçı şampiyon", "unisex", ["balik-isimleri"]),
        ("nehir", "Suyun gücünü taşıyan asil mavi yüzgeçli güzellik", "disi", ["balik-isimleri"]),
        ("ırmak", "Beli kırk büküm uzun ve tatlı görünümlü kraliçe", "disi", ["balik-isimleri"]),
        ("girdap", "Etrafında suyu döndüren obur iştahlı lider", "erkek", ["balik-isimleri"]),
        ("şila", "Yüzgeçleri dans eder gibi salınan kız", "disi", ["balik-isimleri"]),
        ("çakıl", "Kumların arasında yatan renkli hareketsiz zeki", "unisex", ["balik-isimleri"]),
        ("kaya", "Öyle sabit duran ki dipteki yosun kaplı efendi balık", "erkek", ["balik-isimleri", "kaplumbaga-isimleri"]),
        ("vatoz", "Uzay gemisi gibi tüm camda süzülen gizemli gezgin", "erkek", ["balik-isimleri"]),
        ("jaws", "Köpekbalığı edası taşıyan minik asabi akvaryum kabadayısı", "erkek", ["balik-isimleri"]),
        ("sushi", "Hınzır dostların hep ağzını sulandıran pembe neşeli maskot", "unisex", ["balik-isimleri"]),
        ("havyar", "Pahalı gösterişli siyah parlayan nadide bir mücevher", "unisex", ["balik-isimleri"]),
        ("pirana", "Hep yem atılmasını bekleyen vahşi görünümlü atik efendi", "erkek", ["balik-isimleri"]),
        ("yakut", "Kıpkırmızı göz alıcı yüzgeçleri olan kraliyet soyundan gelen", "unisex", ["balik-isimleri"]),
        ("zümrüt", "Parlak yeşil nehir dibinden gelme değerli bir sırdaş", "unisex", ["balik-isimleri"]),
        ("amber", "Sarımtırak kehribar gibi güneşte parlayan büyü", "disi", ["balik-isimleri"]),
        ("poyraz", "Kuzeyden esen soğuk hava fırtınası hızında akvaryum fatihi", "erkek", ["balik-isimleri"]),
        ("zorro", "Cam kenarında sürekli kendini saklayıp pusu atan maskeli dost", "erkek", ["balik-isimleri"]),

        # HAMSTER İSİMLERİ (+20)
        ("mikro", "Gözle bile görülmeyecek kadar narin ufacık pıt", "erkek", ["hamster-isimleri"]),
        ("cebo", "Sempatik yaramaz cep boy canavar", "erkek", ["hamster-isimleri"]),
        ("kumbara", "Yanak içlerine bütün sülalesinin yemeğini doldurabilen pufuk", "unisex", ["hamster-isimleri"]),
        ("tombiş", "İri yarı yuvarlak göbiş bir minnoş top", "unisex", ["hamster-isimleri"]),
        ("ufaklık", "Minik zeki fırlama köşebaşı kaçakçısı", "unisex", ["hamster-isimleri"]),
        ("fıstıki", "Yeşil sarı renkte hafif asabi ve kabuk soyan inatçı", "unisex", ["hamster-isimleri"]),
        ("fındık", "Kabuklu fındık gibi sert kahverengi tatlı iştahlı", "unisex", ["hamster-isimleri"]),
        ("cüce", "Pamuk prensesin 7 yoldaşından ufacık bodur bir maskot", "erkek", ["hamster-isimleri"]),
        ("bıdık", "Evin ufak tatlı şapşik fıtı fıtısı", "unisex", ["hamster-isimleri"]),
        ("cips", "Kıtır kıtır ses çıkarıp kemiren çekirdek delisi hırsız", "unisex", ["hamster-isimleri"]),
        ("topaç", "Hızlı bir tekerlekte dönerek enerjisini asla atamayan maratoncu", "erkek", ["hamster-isimleri"]),
        ("tekerlek", "Çarkta bütün gün durmayan ev faresi klasiği", "unisex", ["hamster-isimleri"]),
        ("pırtık", "Tüyleri kabarık kıpır kıpır ufacık stres topu", "unisex", ["hamster-isimleri"]),
        ("susam", "Bir kurabiyenin üstündeki sevimli yalnız nokta", "unisex", ["hamster-isimleri"]),
        ("leblebi", "Yuvarlak bej sevimli tost", "unisex", ["hamster-isimleri"]),
        ("piko", "Çok küçük minik heceleri kısa yaramaz kaçıran tüy yumağı", "erkek", ["hamster-isimleri"]),
        ("tombo", "Tombulluğundan tekerleğe sığamayıp uzanan uyuz miskin", "erkek", ["hamster-isimleri"]),
        ("peynir", "Tatlı farenin sarımtırak en iyi rüya menüsü dost", "unisex", ["hamster-isimleri"]),
        ("şişko", "Yanakları yoruluncaya kadar depolamacı iştahlı dombili", "erkek", ["hamster-isimleri"]),
        ("karam", "Koyu karamel bitter arası çikolata kıvamı melek", "unisex", ["hamster-isimleri"]),

        # TAVŞAN İSİMLERİ (+20)
        ("pamuk", "Beyaz uzun kulaklı yumuşacık uyku sever sevimli bulut", "unisex", ["tavsan-isimleri"]),
        ("havuç", "Tombul yanaklı sürekli yeşillik turuncu sebze arayan fırlama", "unisex", ["tavsan-isimleri"]),
        ("kuyruk", "Minicik bir ponpondan ibaret hızlı seken sevgidolu yürek", "unisex", ["tavsan-isimleri"]),
        ("bugs", "Ünlü çizgi dizi komik arsız korkusuz geveze maskotu", "erkek", ["tavsan-isimleri"]),
        ("zıpzıp", "Durmadan sürekli arka ayaklarına vuran havada taklacı enerjik", "unisex", ["tavsan-isimleri"]),
        ("ponpon", "Düğme burun ve bir topak kuyrukla kendini ezdirebilecek şirin", "unisex", ["tavsan-isimleri"]),
        ("uzunkulak", "Gözünün önünü kapatacak denli upuzun sevimli kulak dedektifi", "unisex", ["tavsan-isimleri"]),
        ("kartopu", "Soğuk ama içi sımsıcak saf bembeyaz yumuşak melek", "unisex", ["tavsan-isimleri"]),
        ("puf", "Yastık gibi rahatına düşkün pufidi", "unisex", ["tavsan-isimleri"]),
        ("thumper", "Bambi filmindeki meşhur fırlama şirin arka ayakçı", "erkek", ["tavsan-isimleri"]),
        ("yumoş", "Koku deterjanından fırlama bulut köpük gibi yumuşak masumiyet", "unisex", ["tavsan-isimleri"]),
        ("alaca", "Rengarenk karmakarışık iki tatlı lekesi olan alaca doğa misafiri", "unisex", ["tavsan-isimleri"]),
        ("hop", "Zıplayan seken koşarak yanına süzülen neşeli yaramaz tüy", "unisex", ["tavsan-isimleri"]),
        ("kadife", "Tüylerinin pürüzsüzlüğü ve sevimliliği dokunmaktan vazgeçilmeyen hatun", "disi", ["tavsan-isimleri"]),
        ("sakız", "Beyaz tatlı çiğnedikçe sünen uzayan kıkırdayan şekerli damla", "unisex", ["tavsan-isimleri"]),
        ("tüytop", "Pıtırak gibi her yana yuvarlanan tüy yumağı enerji küpü küçük efe", "unisex", ["tavsan-isimleri"]),
        ("kıtır", "Havuç yedikçe evi inleten obur kemirgen tatlı hırsız faremsi", "unisex", ["tavsan-isimleri"]),
        ("roket", "Adımlarıyla arkasında toz bulutu bırakan jetgiller koşucusu tavşancık", "erkek", ["tavsan-isimleri"]),
        ("cici", "Sıcacık kucakta uymaya bayılan bebek gibi şirin hanımefendi kız", "disi", ["tavsan-isimleri"]),
        ("nane", "Serin bir nefes kadar tazeleyici kıpır kıpır oyuncu ve ferahlatıcı sevimli", "disi", ["tavsan-isimleri"]),

        # KAPLUMBAĞA İSİMLERİ (+20)
        ("tosbağa", "Evin neşesi ama bir o kadar da miskin yavaş gezenti tatlışı", "unisex", ["kaplumbaga-isimleri"]),
        ("ninja", "Film kahramanı korkusuz dövüşçü göz bandajlı ve inatçı yeşil dost", "erkek", ["kaplumbaga-isimleri"]),
        ("kabuk", "Ne zaman kızsa veya korksa direkt kocaman şapkasının altına pusan maskot", "unisex", ["kaplumbaga-isimleri"]),
        ("zırhlı", "Mermer gibi bir ev taşıyan sırtındaki yükünden asla usanmayan kalkanlı arkadaş", "erkek", ["kaplumbaga-isimleri"]),
        ("tank", "Ağır ve devasa ama duruşu her defasında etkileyici yürüyen komik şirin", "erkek", ["kaplumbaga-isimleri"]),
        ("ağır", "Hantallığı komik duran adımlarını sanki on saatte izlediğimiz miskin dede", "erkek", ["kaplumbaga-isimleri"]),
        ("yaşlı", "Sanki iki yüz yıldır bu dünyada yaşıyor bilgelikte sınır tanımayan guru asil", "erkek", ["kaplumbaga-isimleri"]),
        ("bilge", "Uzak dünyaları biliyormuşçasına sakin kendi halinde huzurlu bir üstad sevecen", "unisex", ["kaplumbaga-isimleri", "kus-isimleri"]),
        ("fıstık", "Kabuğunda taze yeşil çimen tonlarıyla bezeli küçük bir sırça köşkü ev ahalisi", "unisex", ["kaplumbaga-isimleri"]),
        ("çamur", "Islak serin toprak üstünde güneşlenmeye bayılan doğanın toprak çocuğu asabi", "unisex", ["kaplumbaga-isimleri"]),
        ("gölge", "Gece bile fark edimeyen köşe bucak uyku sever ışıkta kalmayı sevmeyen sevimli saklambaççı", "unisex", ["kaplumbaga-isimleri"]),
        ("dinazor", "Eski çağlardan günümüze kadar yaşamış pre-historic t-rex komedisini sunan asabi heybet", "erkek", ["kaplumbaga-isimleri"]),
        ("mermer", "Yeşil gri ve oldukça serin kabuğu ile tam bir ev mücevheri taşıyan tatlı cankurtaran", "unisex", ["kaplumbaga-isimleri"]),
        ("taş", "Kayaların üzerinde güneşlenirken ne taşı var ne kendi var sadece huzuru izleyen asil tembel", "erkek", ["kaplumbaga-isimleri"]),
        ("kaktüs", "Kabuğu dikenli kaba ama içi çok sulu tatlı kıvrak narin kaktüs gülü dişil heybet", "unisex", ["kaplumbaga-isimleri"]),
        ("franklin", "Masal kahramanlarını seven bir çocuğun kendi sevimli ilk arkadaşı masum dost masalı", "erkek", ["kaplumbaga-isimleri"]),
        ("leonardo", "Gerçek bir kılıç ustası edasıyla akşama kadar elini şıklatan yeşil kahreden asil dost", "erkek", ["kaplumbaga-isimleri"]),
        ("kral", "Tüm akvaryum/bahçeye hükmeden başını dimdik göğe kaldıran bir otorite komutan ve hükümdar", "erkek", ["kaplumbaga-isimleri"]),
        ("şanslı", "Tüm kazalara yaramazlıklara rağmen uzun ömür getiren sağlamlık şifa mucizevi canavar", "unisex", ["kaplumbaga-isimleri"]),
        ("tıstıs", "Nefes alışında kızdığında burun fışkırtan eğlenceli tatlı bela sevilesi bir gülle kumpir", "unisex", ["kaplumbaga-isimleri"]),

        # AT İSİMLERİ (+20)
        ("destan", "Savaş meydanlarında bile korkusuz koşan dilden dile aktarılmış efsane", "erkek", ["at-isimleri"]),
        ("kocabey", "Cüssesi boyundan büyük heybetli ulu atalara yakışır ulu şampiyon paşa", "erkek", ["at-isimleri"]),
        ("karayel", "Kuzeyden esen dondurucu ve sert simsiyah parlayan yarış fırtınası efsanesi", "erkek", ["at-isimleri"]),
        ("göktuğ", "Göklerden aldığı yetkiyle şaha kalkan ufkumuza bayrağını diken yiğit cesur asil zerafet", "erkek", ["at-isimleri"]),
        ("hedef", "Şampiyon olmak dışında odaklanmayan, jokeyiyle yarışan hız küpü azim anıtı beygir efsanesi", "erkek", ["at-isimleri"]),
        ("zafer", "Ulaşılmaz bitiş çizgisini birinci yırtarak geçmiş hep kazanan mutlak otorite şampiyon safkan ezelî", "erkek", ["at-isimleri"]),
        ("kahraman", "Kötü günde hızır gibi uçarak yetilmiş bir halk efsanesi ve kahramanların daimi bineği kabadayı efsane", "erkek", ["at-isimleri"]),
        ("asil", "Duruşu asil kanı soylu boynu kıvrık bembeyaz doru güzel bir evlat ve kanatkar yoldaş gurur", "erkek", ["at-isimleri", "kopek-isimleri"]),
        ("hürrem", "Narince naz yapan süslü padişahların kıymetlisi oyuncu ve güler yüzlü neşesi dillerde kıymetli sırma saçlı efsunlu inci", "disi", ["at-isimleri"]),
        ("çil", "Kestane renginde komik şirin noktaları olan dağ gibi sevilesi minyatür yaramaz bir inatçı midilli afacan cüce", "unisex", ["at-isimleri"]),
        ("batur", "Cesur savaşan, gözüpek bükülmez batur korkusuz komutan hakanlık ruhlu ulu heybet şaha kalkmış dev alp kaya", "erkek", ["at-isimleri"]),
        ("tay", "Taylığında ele avuca sığmayan fırlama tıpıdık genç ruhlu afacan atılgan neşeli şımarık nazlı küçük melek evlat narin", "unisex", ["at-isimleri"]),
        ("süvari", "Gökte süzülen bulutlar arasına yeleleri karışan savaş atı cenk beyfendisi mert cengaver er", "erkek", ["at-isimleri"]),
        ("vural", "Adımlarıyla yerleri sarsan bir kasırga gibi sert asil acımasız kabadayı asrın gücü yenilmez komutan padişah heybeti", "erkek", ["at-isimleri"]),
        ("kemer", "Gösterişli koşumları seven daima birinci sıraya kurulan yarışta toz yutturan şımarık asil zengin kupa fatihi şahlanmış cengaver", "erkek", ["at-isimleri"]),
        ("yüce", "Erişilmez asalet ulu duruş gururlu mağrur hiç bir zorluktan korkmayan efendi padişah dağ dağları deviren kasırga fırtınası", "erkek", ["at-isimleri"]),
        ("alper", "Cengaver yürekli güçlü orduları kovalayan yaman ve bir ok gibi rüzgarda şahlanan destansı efsane gürz kılıç yiğit asker", "erkek", ["at-isimleri"]),
        ("şahin", "Kartal şahin kadar hızlı ve acımasız, yelesi jilet gibi avcı bir yarış koşucusu dondurucu heybet fatihin amansız askeri yiğit efendi", "erkek", ["at-isimleri"]),
        ("doğa", "Vahşi ve asi yabani huylu tabiat ana yeşilliğin asil kraliçesi orman fatihi serbest süzülen gökyüzünün kızı masal perisi gülü", "disi", ["at-isimleri"]),
        ("efehan", "Dağ efe yiğit lider şah efelerin şahı zeybek gibi heybetli onurlu efsane zafere namzet yoldaş sadık alp duruş destan öyküsü ulu heybet asil duruşu padişah efe ruh", "erkek", ["at-isimleri"]),

        # PAPAĞAN İSİMLERİ (+20)
        ("geveze", "Sus ağzından sular akan her sese tepki yaramaz vır vır eden şımarık söz erbabı ev neşesi akşama kadar diller döken dırdırcı sırnaşık dedektif maskot eğlenceli tatlı canavar ufak cümbüş", "unisex", ["papagan-isimleri"]),
        ("bıcırık", "Ses çıkaran cıvıl cıvıl durmayan ciyak tatlı bela evin eğlencesi çikita papağan canayakın fırlama zıpır yaramaz yerinde durmaz heceli söz dağarcığına sahip arsız komik bebeksi şirin bir top", "unisex", ["papagan-isimleri"]),
        ("korsan", "Omuzlarda gezmeye ve tek kaşı gözükür gibi yaramaz asabi ama bir o kadar da tül yumağı uykucu can dost cıvıl efendi karadeniz deniz korsanı gemi yoldaşı tayfa fatihi fırtına dost ev neşesi", "erkek", ["papagan-isimleri"]),
        ("şakrak", "Neşeli gülen yüzü güldüren müzikli melodi orkestra ustası palamut ceviz şampiyonu tatlı yiyip diller döken asil bey hanım", "unisex", ["papagan-isimleri"]),
        ("şeker", "Rengarenk tatlı şeker dilli bal gibi şurup nazlı pembe kırmızı şurup gibi akide pembesi", "disi", ["papagan-isimleri", "kus-isimleri"]),
        ("vırvır", "Durmayan gagasından cıyak eksik olmayan vıdı vıdı efendi hanımı kız çingene pembik şirin maskar", "unisex", ["papagan-isimleri"]),
        ("çıtçıt", "Hep bir şeyleri çıtlatan kırıcı oyuncak kıran tatlı şapşik sevecen zıplayan cıvıl ufaklık", "unisex", ["papagan-isimleri"]),
        ("akıllı", "Tüm evin isimlerini ezberleyip telefon çalınca 'alo' diyen ev profesörü zeki asil dahi cümbüşü profesörü zekası cin afacan deha komik profesör", "unisex", ["papagan-isimleri"]),
        ("bilmiş", "Her şeye hece ile cevap itiraz eden bilmiş huysuz neşeli dır dır eden papa şımarık şirin inatçı asabi filozof komik bilgin şıpırcık tatlı kız hanım hanımcık inatçı afacan uleması dahi tatlı hoca komedyen artist yetenekli", "unisex", ["papagan-isimleri"]),
        ("papa", "Papağanın sevimli sempatik kısaltması tatlış ufak tatöş efsane şefik sevimli komik maskot minik", "erkek", ["papagan-isimleri"]),
        ("lori", "Renkli alacalı kırmızı mavi masmavi orman kaçkını rengarenk yaz asilzadesi nazlı kız efsunlu melek tatlı şurup pembe yanaklı", "disi", ["papagan-isimleri"]),
        ("tropik", "Kocaman gagası egzotik ormanların kralı şahane orkide yaz güneşi cıvıltı deniz okyanus efsunu tropik meyve fatihi", "unisex", ["papagan-isimleri"]),
        ("jungle", "Vahşi Amazon yağmur ormanlarından çıkagelen sırnaşık avazı çıktığı kadar ciyaklayan cıvıldak komik asil komutan deli neşeli çingene ruh diller dökücü afacan tüy yumak tatlı yeşillik sır sır orman kral fırtına dırdırcı yeşil", "unisex", ["papagan-isimleri"]),
        ("zazu", "Filmlerdeki geveze bilmiş efendinin asil yoldaşı korkak neşeli şımarık huysuz", "erkek", ["papagan-isimleri"]),
        ("kaptan", "Gemiyi omuzda idare eden rotasını senin saçına çizen afacan denizci cesur paşa yiğit komik yoldaş tatlı fırtına", "erkek", ["papagan-isimleri"]),
        ("cici", "Cici kuş demesiyle her kalbi çalan uslu hanımefendi süslü kokoş neşeli kıkır kız pembe yanak efsane melek pamuk efsanevi güzellik şeker pare nur tanesi afrodit peri heves masum ceylan gül gonca sırma kılıç perisi minnak", "disi", ["papagan-isimleri"]),
        ("göztepe", "Sarı kırmızı renk cümbüşü taraftar heyecanı neşeli", "erkek", ["papagan-isimleri"]),
        ("fener", "Sarı mavi lacivert aşkıyla cıvıldayan maç izlemeyi seven afacan", "erkek", ["papagan-isimleri"]),
        ("bestekar", "Melodileri kendi üreten ritmik müzik ustası kompoze asil sanatçı şurup", "unisex", ["papagan-isimleri"]),
        ("cümbüş", "Renk cümbüşü evin cümbüş eğlence festival komedi tiyatro maskot efsane standup afacan oyuncu maskara eğlence tiyatro yetenek artist şovmen komedyen fırlama zıpır güler cıvıl asabi şen kahkaha fırtına", "unisex", ["papagan-isimleri"]),

        # YILAN İSİMLERİ (+20)
        ("sinsi", "Sessiz hareket eden gizlenmeyi seven avcı gizemli dedektif", "unisex", ["yilan-isimleri"]),
        ("hayalet", "Saydam tenli gibi süzülen ruhvari görkem asil melek beyaz", "unisex", ["yilan-isimleri"]),
        ("neon", "Parlak şeritleri ışık gibi renk cümbüşü fosforlu avcı", "unisex", ["yilan-isimleri"]),
        ("fosfor", "Canlı efsane karanlıkta göz alır avcı tehlikeli renk güzel", "unisex", ["yilan-isimleri"]),
        ("kral", "Heybeti kobra asaleti gücü asil bey avcı kral başkumandan efendi", "erkek", ["yilan-isimleri"]),
        ("çöl", "Kum rengi sakin susuzluk asil bilge ihtiyar kum kurdu", "unisex", ["yilan-isimleri"]),
        ("sahra", "Kum asil kraliçesi kavurucu ama efsunlu güzel sıcak dişi kum perisi asil", "disi", ["yilan-isimleri"]),
        ("sfenks", "Mısır piramidinde yatan efsane tanrı asaleti sır sır küpü sfenks mısır kraliçesi", "unisex", ["yilan-isimleri"]),
        ("apophis", "Eski inanışlardan kargaşa ve gücün heybeti tanrı efsun kral ezel mutlak korku destan efsane karabasan devasa canavar", "erkek", ["yilan-isimleri"]),
        ("orochi", "Efsane çok başlı güçlü ejderha destanı mitsel gücü yenilmez ihtiyar canavar ormanların gizli cankurtaran asilzade gücü destansı ejder tanrı avcı ninja samuray", "erkek", ["yilan-isimleri"]),
        ("ejder", "Korku salan pul pul kaplı ejder yürek asil ateş aalevi cesur asil kumandan hırçın gücü fırtına kükreyen alev topu asilzade canavarı uykulu miskin", "erkek", ["yilan-isimleri"]),
        ("kıvrım", "Oynaşık şekilli sarmaşık tatlı esnek oyun hamuru şirin dans eden ritmik", "unisex", ["yilan-isimleri"]),
        ("halka", "Daire daire desenli şirin oyuncu güzel benekli fırlama desen", "unisex", ["yilan-isimleri"]),
        ("ip", "Sıpsıska ip gibi sürten kıvrılan efsun komik şirin iplikçik tel", "unisex", ["yilan-isimleri"]),
        ("kalın", "Hamile gibi obur tombik ağır yavaş miskin uyuz kocaman tank dombili canavar kabadayı iri boğa et", "erkek", ["yilan-isimleri"]),
        ("pulu", "Parlayan narin pul pulları efsun gümüş narin dişi pırıtıl parlak tatlı", "unisex", ["yilan-isimleri"]),
        ("deri", "Yeni ceket giymiş manken şık zerafet soylu artist karizma komik havalı", "unisex", ["yilan-isimleri"]),
        ("düğümlü", "Kendi kendine dolaşmış beceriksiz komik fırlama sapsıkı obur yün oyun şirin tembel dolaşık saç afacan yaramaz tatlı belası deli divane inat şımarık sarsak zıpır", "unisex", ["yilan-isimleri"]),
        ("fay", "Uzun ince bir hat fay kırığı sismik hareket eden sessiz avcı uzun ince zerafet şapşik asabi hantal minnoş uzun çubuk efsun inatçı", "unisex", ["yilan-isimleri"]),
        ("lazer", "Keskin bakan parlak efsun av gözlü sinsi kırmızı avcı hırçın izleyici komando ninja ışık hızlı acımasız roket deli fişeng yılan sinsi asabi ateş asabi heyecan kıpır hiperaktif", "erkek", ["yilan-isimleri"]),

        # YENİ EKLENEN +200 ÇOK DAHA ŞİRİN İSİM

        # KÖPEK İSİMLERİ (+20)
        ("bonibon", "Rengarenk tatlı şeker gibi enerji küpü", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("ponçik", "Yumuşacık hamur işi gibi sıkılası melek", "unisex", ["kopek-isimleri", "kedi-isimleri", "hamster-isimleri"]),
        ("bıdık", "Kısa bacaklı paytak yürüyüşlü masum dost", "erkek", ["kopek-isimleri"]),
        ("şuşu", "Bol tüylü gösterişli kokoş güzellik", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("pati", "Beyaz çoraplı ufak minik ayaklarıyla koşturan", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("puding", "Tatlı yumuşak obur kucak delisi", "unisex", ["kopek-isimleri", "hamster-isimleri"]),
        ("karam", "Bitter çikolata kıvamında asil siyah evlat", "erkek", ["kopek-isimleri"]),
        ("fırça", "Saçları taranmaktan hiç hoşlanmayan asi", "unisex", ["kopek-isimleri"]),
        ("leydi", "Asaletiyle evi yöneten küçük hanımefendi", "disi", ["kopek-isimleri"]),
        ("maço", "Boyundan büyük köpeklere kafa tutan fırlama", "erkek", ["kopek-isimleri"]),
        ("pufi", "Pamuk şeker gibi rüzgarda uçacak kadar narin", "unisex", ["kopek-isimleri", "tavsan-isimleri"]),
        ("şurup", "Yaralara merhem olan canayakın terapi dostu", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("kaptan", "Evde her şeye burnunu sokan meraklı denizci", "erkek", ["kopek-isimleri"]),
        ("pırlanta", "Parıltısıyla göz alan eve şans getiren lüks", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("cips", "Sürekli mama kabından kıtırkıtır ses çıkaran", "unisex", ["kopek-isimleri"]),
        ("zeytin", "Kara gözlü ufacık tefecik içi dolu fıçıcık", "unisex", ["kopek-isimleri", "kedi-isimleri"]),
        ("misket", "Yuvalak boncuk gözleriyle kalbi eriten cici", "unisex", ["kopek-isimleri"]),
        ("sosis", "Uzun ince gövdeli hiperaktif dachshund sevdası", "erkek", ["kopek-isimleri"]),
        ("sütlaç", "Beyaz sarı karışımı fırınlanmış tatlı kase", "disi", ["kopek-isimleri", "kedi-isimleri"]),
        ("tarçın", "Turuncu tüyleriyle sıcaklık veren baharat güzeli", "unisex", ["kopek-isimleri", "kedi-isimleri"]),

        # KEDİ İSİMLERİ (+20)
        ("miya", "En ufak şeyde şikayet eden tatlı mızmız", "disi", ["kedi-isimleri"]),
        ("pıtır", "Arkasında ayak sesleri bırakarak gezen gölge", "unisex", ["kedi-isimleri"]),
        ("zilli", "Boynundaki pembe ziliyle evi inleten güzellik", "disi", ["kedi-isimleri"]),
        ("tırmık", "Oyunu hep ciddiye alan keskin patili usta avcı", "erkek", ["kedi-isimleri"]),
        ("kumpir", "Patates gibi içi dolu şişko göbekli keyifçi", "unisex", ["kedi-isimleri"]),
        ("mantı", "Sarımsaklı yoğurt gibi sırnaşan lezzetli hamur", "unisex", ["kedi-isimleri"]),
        ("duman", "Sokaktan sahiplenilmiş gri karizmatik sokak kedisi", "erkek", ["kedi-isimleri"]),
        ("çilek", "Pembe burunlu kıpkırmızı tasmalı evin tatlısı", "disi", ["kedi-isimleri"]),
        ("kekik", "Ufacık bitki gibi her yere sızıp yatan rahatsız", "unisex", ["kedi-isimleri"]),
        ("simit", "Yuvarlak şekil alıp uymaya bayılan gevreklik", "unisex", ["kedi-isimleri"]),
        ("ayran", "Çalkalandıkça köpüren ama bembeyaz saflık", "unisex", ["kedi-isimleri"]),
        ("pekmez", "Sağlık veren yapış yapış karanlık güzel dost", "unisex", ["kedi-isimleri"]),
        ("yoda", "Büyük kulaklı ufacık gövdeli bilge canavar", "erkek", ["kedi-isimleri"]),
        ("korsan", "Tek gözlü asilzade sokak savaşçısı efsane", "erkek", ["kedi-isimleri"]),
        ("şeftali", "Tüysüz kediler veya açık somon renkli narin dişi", "disi", ["kedi-isimleri"]),
        ("irmik", "Kum rengi altın sarısı şahane tüylü prens", "erkek", ["kedi-isimleri"]),
        ("cadı", "Gece ansızın ayak parmağına saldıran fırlama", "disi", ["kedi-isimleri"]),
        ("macaron", "Lüks tatlı gibi asil duruşlu kibirli güzellik", "unisex", ["kedi-isimleri"]),
        ("paşa", "Evdeki en iyi koltuğu babasının malı gibi sahiplenen", "erkek", ["kedi-isimleri"]),
        ("sırdaş", "Ağlarken gelip gözyaşı yalayan en iyi arkadaş", "unisex", ["kedi-isimleri"]),

        # KUŞ İSİMLERİ (+20)
        ("cicikuş", "Konuşmayı ilk öğrendiği kelimeyle meşhur papağan", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("pıtpıt", "Uçmaya çalışırken duvarlara hafif çarpan minik", "unisex", ["kus-isimleri"]),
        ("kanat", "Kafes dışında saatlerce tavan turlayan özgür efe", "erkek", ["kus-isimleri"]),
        ("pırpır", "Küçük cüssesiyle evin neşe küpü motor misali", "unisex", ["kus-isimleri"]),
        ("fasıl", "Canı sıkıldıkça en güzel melodileri çığran sanatçı", "erkek", ["kus-isimleri"]),
        ("tıktık", "Kafes demirini kemirerek isyan eden baterist", "unisex", ["kus-isimleri"]),
        ("nida", "Sabah alarmından önce öten tiz sesli bülbül", "disi", ["kus-isimleri"]),
        ("yaprak", "Yeşil sarı renk cümbüşüyle doğa harikası", "disi", ["kus-isimleri"]),
        ("mızıkçı", "Yem yemeyip sağa sola fırlatan isyankar prens", "erkek", ["kus-isimleri"]),
        ("zıpır", "Tellerin arasından ters asılıp uyuyan fırlama", "erkek", ["kus-isimleri"]),
        ("yankı", "Islık çalınıca peşinden aynısını öten deha", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("neşe", "Eve gelen herkesi cıvıltısıyla karşılayan evrak", "disi", ["kus-isimleri"]),
        ("dudu", "Tatlı dilli kırmızı gagalı ev perisi orman yıldızı", "disi", ["kus-isimleri", "papagan-isimleri"]),
        ("mehtap", "Parlak sarı aya benzeyen lutino türü cennet kuşu", "disi", ["kus-isimleri"]),
        ("seher", "Şafak sökerken öten sessizliği bozan güzel ötüşlü", "disi", ["kus-isimleri"]),
        ("bumerang", "Uçsa bile dönüp omuz başa inen sadık yoldaş", "erkek", ["kus-isimleri"]),
        ("mermi", "Kafes kapısı açıldığında roket gibi fırlayan sülün", "erkek", ["kus-isimleri"]),
        ("kivi", "Tüyleri meyve gibi tatlı ve ekşi bir sırnaşık", "unisex", ["kus-isimleri", "papagan-isimleri"]),
        ("limon", "Limon sarısı muhabbet kuşu evlat aşkı masum", "unisex", ["kus-isimleri"]),
        ("cennet", "Her baktığında güzelliğiyle mest eden cennet kuşu", "disi", ["kus-isimleri"]),

        # BALIK İSİMLERİ (+20)
        ("beta", "Tek başına bir akvaryum isteyen asabi savaşçı", "erkek", ["balik-isimleri"]),
        ("lepistes", "Kuyruk sallaması şölen yaratan milyon renkli afacan", "unisex", ["balik-isimleri"]),
        ("lüfer", "Gümüş gibi parlayan avcı balık edasında asil geyik", "erkek", ["balik-isimleri"]),
        ("kalkan", "Dipteki yassı yüzeylerde kumlanan enteresan kamuflajcı", "erkek", ["balik-isimleri"]),
        ("ıstakoz", "Kırmızı renkli akvaryum fatihi gösteriş sevdalısı", "erkek", ["balik-isimleri"]),
        ("yengeç", "Kaba görünüşlü kabuklu yürüyüş asil pınarı saklambaç", "erkek", ["balik-isimleri"]),
        ("karides", "Saydam pembe akvaryun neşe kaynağı temizlik robotu", "unisex", ["balik-isimleri"]),
        ("dalgıç", "Devamlı bitkilerin ardına dalış yapan izci ufaklık", "erkek", ["balik-isimleri"]),
        ("pusula", "Ne atarsan hangi yönde atarsan anında koşan iştahlı", "unisex", ["balik-isimleri"]),
        ("şamandıra", "Yemek bekleken su tepesinde su kabarcığı yutan şişko", "unisex", ["balik-isimleri"]),
        ("dümenci", "Bütün lepistesleri ardından sürükleyen alfa maskot", "erkek", ["balik-isimleri"]),
        ("midye", "Pipo fitrenin yanında hiç uyanmayan miskin kabuklu", "disi", ["balik-isimleri"]),
        ("hamsi", "Suda cıva gibi süzülen incecik minicik hiperaktif fırtına", "unisex", ["balik-isimleri"]),
        ("yunus", "Ciclid türünden en nazik gülücük atan canayakın dost", "erkek", ["balik-isimleri"]),
        ("fenerci", "Karanlıkta parıldayan kedi gözü gibi fosforlu yakut", "erkek", ["balik-isimleri"]),
        ("marlin", "Çizgili atik yüzüşüyle akvaryum krallığında soylu efsane", "erkek", ["balik-isimleri"]),
        ("yakut", "Kıymetli kırmızı kan rengi japon güzelliği nar tanesi", "disi", ["balik-isimleri"]),
        ("zümrüt", "Yeşili bitkilere saklanan tatlı asil amazon mücevheri", "unisex", ["balik-isimleri"]),
        ("amber", "Portakal ağacından kopmuş canlı yaz meyvesi neşesi", "disi", ["balik-isimleri"]),
        ("köpük", "Hava taşının üstünden oynamayan beyaz yüzgeç minnoş", "unisex", ["balik-isimleri"]),

        # HAMSTER İSİMLERİ (+20)
        ("pinpon", "Beyaz top misali akşama kadar zıplayan komik sporcu", "unisex", ["hamster-isimleri"]),
        ("tetris", "En dar oyuklara bile iki şekil atarak sığabilen kurnaz", "unisex", ["hamster-isimleri"]),
        ("cüzdan", "Ödül mamasını zula yapıp iki yanağını taşıran zengin", "unisex", ["hamster-isimleri"]),
        ("scooter", "Kafes terası ve tekerlek arasında depar atan motor", "erkek", ["hamster-isimleri"]),
        ("atari", "Retro oyuncak gibi çok cana yakın tıkır tıkır sesli kaset", "unisex", ["hamster-isimleri"]),
        ("lümen", "Gözleri gece olunca pırıl pırıl aydınlanan kömürlük", "unisex", ["hamster-isimleri"]),
        ("joule", "Bütün enerjisini harcayıp iki saniye sonra yemek bekleyen", "erkek", ["hamster-isimleri"]),
        ("palamut", "Meşe gibi renk harmonisinde saklanan tombik kuruyemiş", "unisex", ["hamster-isimleri"]),
        ("kozalak", "Kendini kamufle edip talaş yığınında uyuklayan sonbahar", "unisex", ["hamster-isimleri"]),
        ("tomruk", "O kadar şişti ki artık merdiveni zor tırmanan ayıcık", "erkek", ["hamster-isimleri"]),
        ("leblebitozu", "Yedikçe ağzı sulandıran sapsarı tüylü sarışın şapşik", "unisex", ["hamster-isimleri"]),
        ("nohut", "Eli kadar kalıbıyla yüreği kocaman minyatür uslu efe", "unisex", ["hamster-isimleri"]),
        ("bulgur", "Tanecik yemeğini sabırla didik didik eden hamarat şef", "unisex", ["hamster-isimleri"]),
        ("tost", "Uyuduğu yerlere kaşar gibi sünük yatıp kalan gevrek", "unisex", ["hamster-isimleri"]),
        ("kese", "Torba misali bir köşede duran sevimli büzüşük kese", "unisex", ["hamster-isimleri"]),
        ("dirhem", "Kilosu tartıda on numara şampiyon ufak narin dirhemcik", "unisex", ["hamster-isimleri"]),
        ("okka", "Minik bir okkalık ağırlığı boyundan büyük dev fare komedi", "erkek", ["hamster-isimleri"]),
        ("paten", "Evcil hayvan topunun içinde evin dört tarafı gezentisi patenci", "unisex", ["hamster-isimleri"]),
        ("kalori", "Günde kaç elma kaç çekirdek tüketebileceği meçhul obur bebek", "unisex", ["hamster-isimleri"]),
        ("meşe", "Odun gibi sert uşak tırmanıcı pösteki meşe yumağı sarılması şahane", "erkek", ["hamster-isimleri"]),

        # TAVŞAN İSİMLERİ (+20)
        ("seksek", "Çimlerde adım atmayıp hep ip atlar gibi zıp zıp giden şımarık", "unisex", ["tavsan-isimleri"]),
        ("hoppala", "Sevinince binkies yapan şaşkın bebek gülücük perisi uçuşu", "unisex", ["tavsan-isimleri"]),
        ("kaçak", "Kafes açık kalır kalmaz mutfağa marul çalan profesör fırlama", "erkek", ["tavsan-isimleri"]),
        ("çimen", "Yeşillikleri o kadar sever ki adı bile doğadan bir bitkicik dişi", "disi", ["tavsan-isimleri"]),
        ("tepe", "Evin en yüksek yeri neresiyse çıkıp çevreyi dikizleyen avcı kulak", "erkek", ["tavsan-isimleri"]),
        ("menekşe", "Göz alıcı kokusu ve görüntüsü bir hanımefendi zarif masum", "disi", ["tavsan-isimleri"]),
        ("karanfil", "Lop tavşanı cinsi şüphesiz kıvırcık tatlı ve hoş nane fırtına asil", "disi", ["tavsan-isimleri"]),
        ("zambak", "Uzun narin kulak yapılı çok uzağı bile duyan zarif beyaz prens", "disi", ["tavsan-isimleri"]),
        ("turp", "Kıpkırmızı şirin gözleri dombili vücuduyla aşırı komik ufaklık tüy asabi", "erkek", ["tavsan-isimleri"]),
        ("beyaz", "Pamuk pamuğu tertemiz beyazlık tüy saflık masum melek yastık puf", "unisex", ["tavsan-isimleri"]),
        ("bıyık", "Titreyen burnu kocaman anten fırfırlı sevimli afacan kabadayı", "erkek", ["tavsan-isimleri"]),
        ("patpat", "Yere arka ayağıyla tehlike uyarısı yapan pat pat şapşik asabi efe", "unisex", ["tavsan-isimleri"]),
        ("takla", "Keyfi yerindeyken ters dönüp yatan oyuncu gülücük atan maskara fırlama", "erkek", ["tavsan-isimleri"]),
        ("tırsık", "Misafir gelince hemen yatağın altına topuklayan sevimli uysal nazik afacan", "erkek", ["tavsan-isimleri"]),
        ("kütküt", "Heyecanlanınca mırıldanan kalp çarpısı şefkatle sevilmesi muhtaç can evlat", "unisex", ["tavsan-isimleri"]),
        ("havana", "Havana purosu misali tatlı kahve tonu gizemli bir şık kankito serserilik tatlı", "disi", ["tavsan-isimleri"]),
        ("angora", "Pek kabarık tüy yumağı angora şahane lüks ve havalı moda ikonu yün bulut nazlı", "disi", ["tavsan-isimleri"]),
        ("tüysüz", "Kısa tüy sevimli azı çok yapan uyanık ve fırlama kedi köpek düşmanı heybet orman efendisi", "erkek", ["tavsan-isimleri"]),
        ("badibadi", "Yaralanmış gibi masum paytak can yakıcı kafa sürten kucak ebabı sarsak güzel uysal dost", "unisex", ["tavsan-isimleri"]),
        ("maral", "Geyik gibi uzun asil bacak korkak gözler vahşi güzelliğin harmanı zarif şık masum", "disi", ["tavsan-isimleri"]),

        # KAPLUMBAĞA İSİMLERİ (+20)
        ("çiko", "Yanağı iki yana şişik tombiş neşeli kırmızı yanak su kaplumbağası şirin efe", "erkek", ["kaplumbaga-isimleri"]),
        ("kayaalp", "Sırtında devasa çadır gibi zırh çok dayanıklı korkusuz vatansever inatçı komutan adam", "erkek", ["kaplumbaga-isimleri"]),
        ("zırh", "Tüm dünya gelse yıkılmayan kalkan muhafız sessiz saklanmacı defansif taktik şövalye efendisi puf", "unisex", ["kaplumbaga-isimleri"]),
        ("panzer", "Etrafı esip gürleyen tank hantal kaba ama komikleri komiği komedyen ağır çekim asil şapşik afacan", "erkek", ["kaplumbaga-isimleri"]),
        ("kapşon", "Şapka içerisine gizlenen pısırık mahçup yüz ifadeli gizem merak utangaç dert çekingen kaplumbaşa", "unisex", ["kaplumbaga-isimleri"]),
        ("tosun", "Tosbağa babası efe kabadayı yemeğe ilk dadanan göbek efe reisi efendi puf adam kocaman tank komutan", "erkek", ["kaplumbaga-isimleri"]),
        ("bilgin", "Akvaryumdaki şelaleyi saatlerce izleyen felsefik adam kütüphane faresi okuyan bilen komik şapşik adam bilge", "erkek", ["kaplumbaga-isimleri"]),
        ("gezgin", "Güneşlenen yer taş bile olsa durmayıp odayı arşınlayan yürüyüşcü maraton fırlama tursit maceraperest seyahat asil", "unisex", ["kaplumbaga-isimleri"]),
        ("nene", "Hep esneyip ağzını açan sevimli yaşlı babaanne yüzlü kırışık minnoş çikolata efsane sevgi yumağı dert ana", "disi", ["kaplumbaga-isimleri"]),
        ("dede", "Dinlenen huzur uyuklayan horlayan ağır ağır nefes komik minik can yoldaşı uzun fıçı şirin baston dede ihtiyar", "erkek", ["kaplumbaga-isimleri"]),
        ("karpuz", "Çizik sarı kırmızı turuncu desenlerle bezeli komik dış görünüm meyve obur dev ufak tefek can tatlı", "unisex", ["kaplumbaga-isimleri"]),
        ("kavun", "Bal gibi rengi tatlı miskin sırt sapsarı sevimli pıt efsune tatlı yiyik şirin masum efsane canavar ufak fıçı", "unisex", ["kaplumbaga-isimleri"]),
        ("yapraklı", "Doğa bitki marul yeşil falan görünce dellenen aç iştah vejetaryen efe zırh şövalye ağabey dev kaplumbağa efsun", "unisex", ["kaplumbaga-isimleri"]),
        ("sedef", "Sedef parlayan alt tarafı asil deniz melek inci güzeli beyaz pembe parıltı süs porselen incelik hanımefendi kız şahane asil perisi", "disi", ["kaplumbaga-isimleri"]),
        ("porselen", "Fırfır ince narin kırılacak gibi tırnaklı güzellik süs salon adamı nazik ince zarif nazlı sinsi uysal güzellik peri", "unisex", ["kaplumbaga-isimleri"]),
        ("beton", "Toslasa da kafeskendisine vız gelen kaba saba heybet şah komutan güçlü korkusuz t-rex dinazor hantal inat", "erkek", ["kaplumbaga-isimleri"]),
        ("kiremit", "Soğuk ama içi koruyan yalıtım dış duvar kaba kırmızı renk yanan inat şirin hırçın güçlü savunma uysallığı efsane adam", "unisex", ["kaplumbaga-isimleri"]),
        ("şövalye", "Zırh içerisinde ev koruyucu tapınak şah gürz komutan padişah can suyu ulu dev kabadayı heybet ulu puf", "erkek", ["kaplumbaga-isimleri"]),
        ("tırtıl", "Boyundan sürünerek ufacık cıvıl ayak yapraklardan atlayan şapşik bebek kelebek olmadan afacan", "unisex", ["kaplumbaga-isimleri"]),
        ("feryat", "Aç kaldığını duyurmak çırpınan suda heyecan ses fırlama bela uyuz sır sır can ciğer dost arkadaş hür neşe", "unisex", ["kaplumbaga-isimleri"]),

        # AT İSİMLERİ (+20)
        ("şimal", "Kuzey yeli kutup dondurucu buz gücü dağ yıkılmaz asi serinkanlı kış zerafeti rüzgargülü beyaz peri hanım çoban asil peri", "disi", ["at-isimleri"]),
        ("barın", "Koruyan himaye eden vatan bekçisi alp asil dağ yüce kabadayı efsane güç timsali komutan asilzade bey soylu", "erkek", ["at-isimleri"]),
        ("tayyar", "Uçan uçucu kanat takmış göğe ok yayı fırtına mermi alev hür uçan yiğit kahraman destan paşa ok yeli dev gibi heybet efe fırtınası", "erkek", ["at-isimleri"]),
        ("sürat", "Ferrari gibi piste inince acımaz tozu dumana motor rüzgar ivmesi hız timsali mermi hız sınır kural inatçı sürat arabası yoldaş efendi at", "unisex", ["at-isimleri"]),
        ("boran", "Çakan şimşek karanlık kara bulut gücü doğa yeli korkusuz güç amansız yenilmez ulu efe batur alp cesur amansız yenilgi kara dev gaddar ulu kral", "erkek", ["at-isimleri"]),
        ("kırat", "Bembeyaz mermer asil destansı melek ulu temiz duru inci nur parıltı ulu görkem heybetli komutan binici yoldaşı kılıç efendi paşası yiğiti süvari bineği", "erkek", ["at-isimleri"]),
        ("yağız", "Parlak siyah doru ulu komando korku maskeli güçlü şövalye kaplan zırhı karanlık efsane destan bükülmez ordu ejderi korkusuz canavar ejder", "erkek", ["at-isimleri"]),
        ("rüzgargülü", "Esinti ile oynayan fırfır oyuncu afacan taze hava çayır aşığı peri kızı dişi uysal yele duman pembe inci elmas taze nazlı tatlı nazik dişi gülü evlat kız", "disi", ["at-isimleri"]),
        ("şampiyon", "Kupa birinci kürsü kalkan zafer namağlup ulu tek kral fatih asil destan efsane komutan şah zafer gürleyen alkış tozu yele", "erkek", ["at-isimleri"]),
        ("tayfun", "Durulmaz coşkun felaket asabi yaman yenilmez kabadayı yeli bora esintisi ordu kılıç keskin alp çavuş asker can", "erkek", ["at-isimleri"]),
        ("pegasus", "Kanatları efsane mit Yunan gökyüzü heybet koca bembeyaz ihtiyar ulu destan efsane asilzade uçan dev at kabadayı perisi orman perisi uçucu fırfır at heybet melek", "erkek", ["at-isimleri"]),
        ("gülbeyaz", "Beyaz gül kokusu misafiri çayır prensesi yele örgü uzun nur ten inci kılıcı asil şık güzel pırlanta", "disi", ["at-isimleri"]),
        ("türbey", "Türklük ulu bey makam ordu hakan sultan komutan fatih efsun alp cesaret onur kılıcı vatan ok gücü alp", "erkek", ["at-isimleri"]),
        ("kordüğüm", "Açılmaz karışık asabi sarsılmaz dev çözülmez kara bulut dev sarp inat kayalık hırçın gücü fırlama mermi zırh adam kılıç ordu", "erkek", ["at-isimleri"]),
        ("mahmuz", "Dürtü cesaret tetik hazır anlık ordu hızlı fırlayan heyecan mermi koşucu alp asabi", "erkek", ["at-isimleri"]),
        ("dikbaş", "Eğilmeyen itaat sevmeyen inat şımarık yaramaz kafa asabi efe", "erkek", ["at-isimleri"]),
        ("soylu", "Kral aileyi asil şecere zengin kupa zafer altın madalya ulu ihtişam görkem cengaver kılıç", "erkek", ["at-isimleri"]),
        ("rüzgarkızı", "Meltem esintisi ince narin çayır dişi hafif", "disi", ["at-isimleri"]),
        ("beypazarı", "Anadolu yiğit komik yerel vatanşafak efe maden suyu esintisi şirin", "erkek", ["at-isimleri"]),
        ("karabaş", "Siyah çene kafa uyumlu gelenek paşa dost sadık beygir", "erkek", ["at-isimleri"]),

        # PAPAĞAN İSİMLERİ (+20)
        ("mucize", "Şaşırtıcı kelime zeka asıl sihir efsun afacan yetenek", "disi", ["papagan-isimleri"]),
        ("şair", "Dize dize öten ezgi melodi bülbül söz dehası", "erkek", ["papagan-isimleri"]),
        ("maşallah", "Göz değmesi nazarlara karşı heybet güzellik", "unisex", ["papagan-isimleri"]),
        ("renkli", "Meyve cümbüş boya fırça tablo tüy efsane şık kokoş", "unisex", ["papagan-isimleri"]),
        ("jak", "Jako klasiği gri zeka küpü geveze bilge dırdırcı şapşik", "erkek", ["papagan-isimleri"]),
        ("sultan", "Ağa saray eşraf ibik kukuleta kırmızı turuncu güzellik kraliçe dudu", "disi", ["papagan-isimleri"]),
        ("ara", "Macaw şaheser orman devi güçlü can", "disi", ["papagan-isimleri"]),
        ("kakadu", "Sürekli başını diken asabi telaş heyecan cıngar gürültü beyaz melek asil maskara", "unisex", ["papagan-isimleri"]),
        ("mango", "Sapsarı mis tatlı sulu renk afacan portakal turunç tatlı kız şirin", "unisex", ["papagan-isimleri"]),
        ("ananas", "Tepe görkem saç fırfır komik iştahlı obur", "unisex", ["papagan-isimleri"]),
        ("ıslık", "Şarkı çağıran zil fırlama ıslıkçı melodik", "erkek", ["papagan-isimleri"]),
        ("fıstık", "Bembeyaz veya yemyeşil kuruyemiş", "unisex", ["papagan-isimleri"]),
        ("korsanbey", "Tek göz kapalı kabadayı tayfa başı", "erkek", ["papagan-isimleri"]),
        ("prens", "Yeşil kafesten asil bakış prens yele yakışıklı erkek can", "erkek", ["papagan-isimleri"]),
        ("yakışıklı", "Kıymet ayna karşısı sürekli can yakıcı güzellik kokoş erkek", "erkek", ["papagan-isimleri"]),
        ("çingene", "Heryere zıplayan hareket renk", "disi", ["papagan-isimleri"]),
        ("cadoloz", "Isıran kafa yedi cadı dır dır gaga afacan fıtı", "disi", ["papagan-isimleri"]),
        ("fırıldak", "Akşama dönen fırfır yelpaze çark takla oyun", "unisex", ["papagan-isimleri"]),
        ("hacıyatmaz", "Devrilmeyen uykucu asil", "unisex", ["papagan-isimleri"]),
        ("baterist", "Yem kabına vuran orkestracı gürültü", "erkek", ["papagan-isimleri"]),

        # YILAN İSİMLERİ (+20)
        ("sürgün", "Sürünen ceza sürgün yalnız afacan yaman ulu", "erkek", ["yilan-isimleri"]),
        ("boğucu", "Saran sevgi nefes kesen dostluk efsun devasa", "erkek", ["yilan-isimleri"]),
        ("slither", "Film afacan sümüksü kayan kertenkele narin fırlama afacan", "unisex", ["yilan-isimleri"]),
        ("tıss", "Tıslama nefes asabi yaman koruyucu ninja kobra efsun", "unisex", ["yilan-isimleri"]),
        ("piton", "Piton gücü şımarık tatlı sarsılmaz iri obur etobur", "erkek", ["yilan-isimleri"]),
        ("boa", "Küçük ama fıçı dev obur avcı kalın hantal canavar gülle", "erkek", ["yilan-isimleri"]),
        ("engerek", "Tehlike sinsi gizli fırlama zehir orman kum", "disi", ["yilan-isimleri"]),
        ("kaygan", "Elden kaçan ele avuca esnek elastik yaramaz kıvrak afacan", "unisex", ["yilan-isimleri"]),
        ("şerit", "Yoldaki çizgi ince pürüzsüz hat karizmatik adam siyah", "unisex", ["yilan-isimleri"]),
        ("çizgili", "Kavun karpuz şablon şemsiye afacan tiyatro pijama renkli", "unisex", ["yilan-isimleri"]),
        ("sihir", "Büyülü afrodit gizem şahane şaşı efsun cadı gizil peri", "disi", ["yilan-isimleri"]),
        ("kıvrık", "Kat kat uyuyan şekil rulo börek", "unisex", ["yilan-isimleri"]),
        ("rüya", "Dalgın miskin", "disi", ["yilan-isimleri"]),
        ("gaddar", "Acemi oyuncu şapşik", "erkek", ["yilan-isimleri"]),
        ("çölcü", "Kum fırtına", "erkek", ["yilan-isimleri"]),
        ("saklambaç", "Sürekli kuyu bulan", "unisex", ["yilan-isimleri"]),
        ("giz", "Görünmez asil", "unisex", ["yilan-isimleri"]),
        ("sarmal", "Helezon iplik", "unisex", ["yilan-isimleri"]),
        ("zincir", "Demir misali kobra", "erkek", ["yilan-isimleri"]),
        ("kamçı", "Şaklayan kabadayı ulu", "erkek", ["yilan-isimleri"]),
    ]

    eklenen_isim = 0
    atlanan_isim = 0
    for isim, anlam, cinsiyet, kat_sluglar in isim_data:
        # karamel gibi tekrar eden isimleri atla (ilk eklenende M2M'e eklenir)
        obj, created = HayvanIsim.objects.get_or_create(
            isim=isim,
            defaults={
                "anlam": anlam,
                "cinsiyet": cinsiyet,
            }
        )
        # Kategorileri ekle (varsa da M2M'e ekle)
        for ks in kat_sluglar:
            if ks in kategoriler:
                obj.kategoriler.add(kategoriler[ks])

        if created:
            eklenen_isim += 1
        else:
            atlanan_isim += 1

    toplam_isim = HayvanIsim.objects.count()
    toplam_kat = HayvanKategori.objects.count()

    return HttpResponse(
        f"<h2>Hayvan İsimleri Yüklendi!</h2>"
        f"<p><b>Kategoriler:</b> {eklenen_kat} yeni eklendi / {toplam_kat} toplam</p>"
        f"<p><b>İsimler:</b> {eklenen_isim} yeni eklendi, {atlanan_isim} zaten vardı / {toplam_isim} toplam</p>"
        f"<p><a href='/hayvan-isimleri/'>Hayvan İsimlerine Git &rarr;</a></p>"
    )