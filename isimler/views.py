from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
import environ
import json
import requests

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

    elif request.resolver_match.url_name == 'erkek':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords

    elif request.resolver_match.url_name == 'unisex':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords

    elif request.resolver_match.url_name == 'kadin':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kadin")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords

    elif request.resolver_match.url_name == 'saglik':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="saglik")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords

    elif request.resolver_match.url_name == 'cocuk':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="cocuk")
        TumPost = Post.objects.filter(aktif=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = Post_Kategorisi.Title
        h1 = Post_Kategorisi.h1
        description = Post_Kategorisi.description
        keywords = Post_Kategorisi.keywords

    # Popüler Olanlar
    elif request.resolver_match.url_name == 'pei':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = "Popüler Erkek İçerikleri"
        h1 = "Popüler Erkek İçerikleri"
        description = "En popüler erkek içeriklerini burada bulabilirsiniz."
        keywords = "popüler erkek, trend erkek, erkek haberleri"

    elif request.resolver_match.url_name == 'pui':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = "Popüler Unisex İçerikler"
        h1 = "Popüler Unisex İçerikler"
        description = "En popüler unisex içeriklerini burada bulabilirsiniz."
        keywords = "popüler unisex, trend unisex, unisex haberleri"

    elif request.resolver_match.url_name == 'pki':
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kiz")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-olusturma_tarihi')
        title = "Popüler Kız İçerikleri"
        h1 = "Popüler Kız İçerikleri"
        description = "En popüler kız içeriklerini burada bulabilirsiniz."
        keywords = "popüler kız, trend kız, kız haberleri"


    # Çok Görüntü Olanlar
    elif request.resolver_match.url_name == 'ecgei':
        # Otomobil haberleri için kod
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            'okunma_sayisi')
        title = "Popüler Kız İçerikleri"
        h1 = "Popüler Kız İçerikleri"
        description = "En popüler kız içeriklerini burada bulabilirsiniz."
        keywords = "popüler kız, trend kız, kız haberleri"

    elif request.resolver_match.url_name == 'ecgui':
        # Otomobil haberleri için kod
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-okunma_sayisi')
        title = "Popüler Kız İçerikleri"
        h1 = "Popüler Kız İçerikleri"
        description = "En popüler kız içeriklerini burada bulabilirsiniz."
        keywords = "popüler kız, trend kız, kız haberleri"

    elif request.resolver_match.url_name == 'ecgki':
        # Teknoloji haberleri için kod
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kiz")
        TumPost = Post.objects.filter(aktif=True, Trend=True, status="Yayinda", Post_Turu=Post_Kategorisi).order_by(
            '-okunma_sayisi')
        title = "Popüler Kız İçerikleri"
        h1 = "Popüler Kız İçerikleri"
        description = "En popüler kız içeriklerini burada bulabilirsiniz."
        keywords = "popüler kız, trend kız, kız haberleri"

    paginator = Paginator(TumPost, 9)  # 9 içerik göstermek için
    page_number = request.GET.get('sayfa')
    TumPost = paginator.get_page(page_number)

    if page_number is None:
        title = f"{title}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Sayfa {page_number}"

    context = {
        'title': title,
        'H1': h1,
        'description': description,
        'keywords': keywords,
        'Post_Kategorisi': Post_Kategorisi,
        'TumPost': TumPost,
    }

    return render(request, "list.html", context)


def enderun(request, post_slug):
    PostEndrun = get_object_or_404(Post, aktif=True, status="Yayinda", slug=post_slug)
    PostEndrun.okunma_sayisi += 1
    PostEndrun.save(update_fields=['okunma_sayisi', 'SosyalKare', 'banner', 'editor', 'indexing', 'facebook', 'twitter',
                                   'pinterest', 'Trend'])
    soru_cevap = None

    benzer_isimler = PostEndrun.Benzerisimler.split(',') if PostEndrun.Benzerisimler else []

    isim_durumu = []

    for isim in benzer_isimler:
        isim = isim.strip()
        try:
            benzer_post = Post.objects.get(isim=isim.lower())
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
        soru_cevap = [item.split("=") for item in sss]

    # todo tüm içeriği json için veriyorum
    contents = [PostEndrun.icerik1, PostEndrun.icerik2, PostEndrun.icerik3, PostEndrun.icerik4, PostEndrun.icerik5,
                PostEndrun.icerik6, PostEndrun.icerik7]
    articleBody = ' '.join(filter(None, contents))

    # todo tüm resimleri json için veriyorum
    resimler = []
    if PostEndrun.resim:
        resimler.append(PostEndrun.resim.url)
    if PostEndrun.resim2:
        resimler.append(PostEndrun.resim2.url)
    if PostEndrun.resim3:
        resimler.append(PostEndrun.resim3.url)
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
    }

    return render(request, "enderun.html", context)


def arama(request):
    query = request.POST.get('fulltext')
    gender = request.POST.get('gender')
    # query = request.GET.get('fulltext')
    # gender = request.GET.get('gender')

    if gender == '1':  # Unisex
        Cinsiyet = "Unisex"
        posts = Post.objects.filter(isim__icontains=query, Post_Turu__short_title='unisex', aktif=True,
                                    status="Yayinda")
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="kiz")
    elif gender == '2':  # Erkek
        Cinsiyet = "Erkek"
        posts = Post.objects.filter(isim__icontains=query, Post_Turu__short_title='erkek', aktif=True,
                                    status="Yayinda")
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="erkek")
    elif gender == '3':  # Kız
        Cinsiyet = "Kız"
        posts = Post.objects.filter(isim__icontains=query, Post_Turu__short_title='kiz', aktif=True,
                                    status="Yayinda")
        Post_Kategorisi = get_object_or_404(PostKategori, aktif=True, short_title="unisex")

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

    context = {
        'title': title,
        'H1': H1,
        'description': description,
        'keywords': keywords,
        'Post_Kategorisi': Post_Kategorisi,
        'TumPost': TumPost,
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
    description = "erkekbebekisimleri.net iletişim politikası Kişisel bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin. Gizliliğiniz bizim için en önemlidir."
    keywords = "iletişim Politikası, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "erkekbebekisimleri.net Gizlilik Politikası: Kişisel Bilgileriniz Güvende"

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


def hakkinda(request):
    title = "Hakkımızda erkekbebekisimleri.net | Erkek Bebek isimleri"
    description = "erkekbebekisimleri.net Hakkımızda bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin. Gizliliğiniz bizim için en önemlidir."
    keywords = "Gizlilik Politikası, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "erkekbebekisimleri.net Gizlilik Politikası: Kişisel Bilgileriniz Güvende"
    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'hakkimizda.html', context)


def cerez(request):
    title = "Çerez Politikamız erkekbebekisimleri.net | Erkek isimleri"
    description = "erkekbebekisimleri.net gizlilik politikası Kişisel bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin. Gizliliğiniz bizim için en önemlidir."
    keywords = "Gizlilik Politikası, erkekbebekisimleri.net, Kişisel Bilgiler, Veri Koruma, Kullanıcı Gizliliği"
    h1 = "erkekbebekisimleri.net Gizlilik Politikası: Kişisel Bilgileriniz Güvende"
    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'cerez.html', context)


def kullanim(request):
    title = "Kullanım erkekbebekisimleri.net | Bilgilerinizin Korunması"
    description = "erkekbebekisimleri.net gizlilik politikası Kişisel bilgilerinizin nasıl korunduğunu ve kullanıldığını öğrenin. Gizliliğiniz bizim için en önemlidir."
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



        isimsonuc = allname(isim=isim,  aciklama=aciklama, Durum=Durum, Cinsiyet=Cinsiyet)
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
        Post_Turu = request.POST.get('Post_Turu')
        title = f"{isim.capitalize()} İsminin Anlamı Nedir? {isim.capitalize()} Adının Özellikleri Nelerdir?"
        h1 = f"{isim.capitalize()} İsminin Anlamı Ve Tüm Kişilik Özellikleri Nelerdir ?"
        slug = f"{isim.lower()} İsminin Anlami nedir ?"



        Post_Turu_Gelen = PostKategori.objects.get(short_title=Post_Turu)

        yeni_Slug = create_unique_title_slug(slug)
        isimekle = Post(title=title, slug=yeni_Slug, h1=h1, isim=isim,kisaanlam=kisaaciklama, Post_Turu=Post_Turu_Gelen, icerik1=icerik1, icerik2=icerik2)
        isimekle.save()

        allname.objects.filter(id=GelenID).update(Durum="Tamamlandi")

        if isimekle.id is None:
            return HttpResponse("Post kaydedilemedi.")
        else:
            return HttpResponse("Şükürler Olsun Post başarıyla kaydedildi. ID: " + str(isimekle.id))