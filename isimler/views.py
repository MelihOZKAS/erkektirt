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

    if page_number is not None:
        title = f"{title} - Sayfa {page_number}"
        description = f"{description} - Sayfa {page_number}"
        h1 = f"{h1} - Sayfa {page_number}"
        urlsi = f"{urlsi}?sayfa={page_number}"

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