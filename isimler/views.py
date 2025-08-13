from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
import environ
import json
import requests
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_GET

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
    resim = "resimurlsi gelecek buraya"

    context = {
        'title': title,
        'h1': h1,
        'description': description,
        'keywords': keywords,
        'resim': resim,
        'kadin': kadin,
        'saglik': saglik,
        'cocuk': cocuk,
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

    paginator = Paginator(TumPost, 9)  # 9 içerik göstermek için
    page_number = request.GET.get('sayfa')
    TumPost = paginator.get_page(page_number)

    if page_number is None:
        title = f"{title}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Sayfa {page_number}"
        h1 = f"{h1} - Sayfa {page_number}"

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


def enderun(request, post_slug):
    PostEndrun = get_object_or_404(Post, aktif=True, status="Yayinda", slug=post_slug)
    PostEndrun.okunma_sayisi += 1
    PostEndrun.save(update_fields=['okunma_sayisi', 'banner', 'editor', 'indexing', 'facebook', 'twitter',
                                   'pinterest', 'Trend'])
    soru_cevap = None
    benzer_isimler = PostEndrun.Benzerisimler.split(',') if PostEndrun.Benzerisimler else []
    isim_durumu = []

    for isim in benzer_isimler:
        isim = isim.strip()
        try:
            benzer_post = Post.objects.get(isim=isim.lower(), aktif=True, status="Yayinda")
            isim_durumu.append({
                'isim': isim,
                'exists': True,
                'slug': benzer_post.slug,
                'cinsiyet': benzer_post.Post_Turu.short_title
            })
        except Post.DoesNotExist:
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
    articleBody = ' '.join(filter(None, contents))

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
    print(posts)

    title = f"{query} ile gelen arama sonuçları | Erkek Bebek İsimleri"
    H1 = f"{query} ile Yapılan Aramada Bulunan İsimler ve Anlamları"
    description = f"{query} ile gelen arama sonuçları anlamları tüm detayları | Güncel Erkek Bebek İsimleri ve Kız Bebek İsimleri"
    keywords = f"Erkek Bebek İsimleri, Çocuk isimleri, erkek isimleri, isimlerin anlamları, kız isimleri, kız bebek isimleri, modern isimler, yabancı isimler"

    if not posts:
        H1 = f"{query} ile Hiç Bir {Cinsiyet} İsmi Bulunamadı Lütfen Farklı Bir Seçenek ile Deneyin! "

    if page_number is None:
        title = f"{title}"
        H1 = f"{H1}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        H1 = f"{H1}"
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


robots_txt_content = """
User-agent: *
Allow: /
Sitemap: https://www.erkekbebekisimleri.net/sitemap.xml/
"""

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
    h1 = "erkekbebekisimleri.net Çeverez Politikası Kişisel Bilgileriniz Güvende"
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
        post.save(update_fields=['okunma_sayisi', 'banner', 'editor', 'indexing', 'facebook', 'twitter',
                                 'pinterest', 'Trend'])
        return HttpResponse(f"https://www.erkekbebekisimleri.net/{post.slug}/")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def facebook_var_mi(request):
    post = Post.objects.filter(facebook=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.facebook = False
        if post.isim:
            icerik = f"{post.isim} İsminin Gizli Anlamı Nedir? Öğrenince Şaşıracaksınız! İsminin Sırrı Nedir? #bebekisimleri"
        else:
            icerik = f"{post.ozet}"
        if not icerik:
            icerik = f"{post.h1}"
        post.save(update_fields=['okunma_sayisi', 'banner', 'editor', 'indexing', 'facebook', 'twitter',
                                 'pinterest', 'Trend'])
        return HttpResponse(f"https://www.erkekbebekisimleri.net/{post.slug}/!={icerik}")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def twitter_var_mi(request):
    post = Post.objects.filter(twitter=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.twitter = False
        hashtag = "#bebekisimleri"
        if post.isim:
            icerik = f"{post.isim.capitalize()} İsminin Gizli Anlamı Nedir? Öğrenince Şaşıracaksınız! İsminin Sırrı Nedir?"
        else:
            icerik = f"{post.h1}"
        if not icerik:
            icerik = f"{post.h1}"
        post.save(update_fields=['okunma_sayisi', 'banner', 'editor', 'indexing', 'facebook', 'twitter',
                                 'pinterest', 'Trend'])
        return HttpResponse(f"https://www.erkekbebekisimleri.net/{post.slug}/!={icerik} {hashtag}")
    else:
        return HttpResponse("Paylaşılacak Twitter içerik bulunamadı")


@csrf_exempt
def pinterest_var_mi(request):
    post = Post.objects.filter(pinterest=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.pinterest = False
        icerik = post.title
        if not icerik:
            icerik = "Bebek İsimleri"
        post.save(update_fields=['okunma_sayisi', 'banner', 'editor', 'indexing', 'facebook', 'twitter',
                                 'pinterest', 'Trend'])
        return HttpResponse(
            f"https://www.erkekbebekisimleri.net/{post.slug}/!={post.kisaanlam} Anlamına gelmektedir. Daha fazla bebek ismi için bizi takip edin!={post.title}!={post.Post_Turu.short_title}!={post.resim.url}")
    else:
        return HttpResponse("post bulunamadı.")