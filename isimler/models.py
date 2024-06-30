from django.db import models
from tinymce.models import HTMLField
from erkek.custom_storages import ImageSettingStorage

status_cho = (
    ("Taslak", "Taslak"),
    ("Hazir", "Hazir"),
    ("Yayinda", "Yayinda"),
    ("oto", "oto"),
    ("manuel", "manuel"),
)

HELP_TEXTS = {
    "title": "Masal Hiyenin başlığını girin.",
    "h1": "İçeriğin H1 Seo uyumlu girilmesi Lazım.",
    "Model": "Modele göre sılanma ve konumlandırılma olacaktır.",
    "yazar": "Şiiri yazan kullanıcıyı seçin.",
    "slug": "Şiirin URL'de görünecek kısmını girin.",
    "kategorisi": "Şiirin kategorisini seçin.",
    "resim": "800 x 400",
    "icerik": "Şiirin içeriğini girin.",
    "kapak_resmi": "Anasayfa Resim",
    "status": "Şiirin durumunu seçin.",
    "aktif": "Şiirin aktif olup olmadığını belirtin.",
    "meta_title": "Sayfanın meta başlığını girin.",
    "meta_description": "Sayfanın meta açıklamasını girin.",
    "keywords": "Sayfanın anahtar kelimelerini \" Virgül '  ' \" ile ayrınız. ",
    "banner": "Ana Sayfadaki büyük resim alanında ögrünür",
    "small_banner": "Ana sayfada küçük resimlerde görünür.",
    "hakkinda": "Şiir hakkında anlatılmak istenen.",
    "Acikalama": "Kullanıcının işlem durumunu gösterir.",
    "Story Catagory": "Hikayenin kategorisi",
    "Wp-TG": "Whatsapp ve Telegramda paylaş",
}


def kapak_resmi_upload_to(instance, filename):
    # Dosya adını değiştir
    yeni_ad = f"{instance.slug}"
    # Dosya uzantısını koru
    uzanti = filename.split('.')[-1]
    # Yeni dosya adını döndür
    return f"kapak_resimleri/{yeni_ad}.{uzanti}"

class PostKategori(models.Model):
    Title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    h1 = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField( blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    keywords = models.CharField(max_length=255,blank=True,null=True,help_text=HELP_TEXTS["keywords"])
    short_title = models.CharField(max_length=255, blank=True)
    resim1 = models.ImageField(upload_to=kapak_resmi_upload_to,
                               storage=ImageSettingStorage(),
                               help_text=HELP_TEXTS["resim"], null=True, blank=True)
    aktif = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Post Kategori"
    def __str__(self):
        return self.short_title
class Post(models.Model):
    YAZARLAR = [
        ('Melih ÖZKAŞ', 'Melih ÖZKAŞ'),
        ('Hava ÖZKAŞ', 'Hava ÖZKAŞ'),
        ('Ebru GÜNEŞ', 'Ebru GÜNEŞ'),
    ]


    Tur = [
        ('isim', 'isim'),
        ('blog', 'blog'),
    ]

    Jsonu = [
        ('Article', 'Article'),
        ('NewsArticle', 'NewsArticle'),
        ('BlogPosting', 'BlogPosting'),
    ]

    Cinsiyetler = [
        ('Kız', 'Kız'),
        ('Erkek', 'Erkek'),
        ('Unisex', 'Unisex'),
        ('Bekleniyor', 'Bekleniyor'),
    ]


    title = models.CharField(max_length=255, help_text=HELP_TEXTS["title"])
    slug = models.SlugField(max_length=255, unique=True, blank=True,help_text=HELP_TEXTS["slug"])
    h1 = models.CharField(max_length=255,blank=True, help_text=HELP_TEXTS["h1"])
    isim = models.CharField(max_length=255,blank=True, help_text="Sadece ismin kendisi küçük harflerle")
    Post_Turu = models.ForeignKey(PostKategori, null=True, on_delete=models.SET_NULL)
    Post_type = models.CharField(max_length=255, choices=Jsonu, null=True, default="Article")
    yazar = models.CharField(max_length=255, choices=YAZARLAR, null=True,blank=True)
    Kuran = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    Caiz = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    kisaanlam = models.TextField(blank=True, null=True)
    Benzerisimler = models.TextField(blank=True, null=True)
    icerik1 = HTMLField(null=True, blank=True, help_text="ismin uzun anlamı kökeni vs...")
    icerik2 = HTMLField(null=True, blank=True, help_text="ismin kişilik özellikleri")
    icerik3 = HTMLField(null=True, blank=True, help_text="isminde ki ünlü isimler!")
    icerik4 = HTMLField(null=True, blank=True)
    icerik5 = HTMLField(null=True, blank=True)
    icerik6 = HTMLField(null=True, blank=True)
    icerik7 = HTMLField(null=True, blank=True)
    sss = models.TextField(blank=True, null=True)
    ozet = models.TextField(blank=True, null=True)

    #resim = models.ImageField(upload_to='images/', blank=True, null=True)
    #resim2 = models.ImageField(upload_to='images/', blank=True, null=True)
    #resim3 = models.ImageField(upload_to='images/', blank=True, null=True)

    resim = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["resim"], null=True, blank=True)
    resim2 = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["resim"], null=True, blank=True)
    resim3 = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["resim"], null=True, blank=True)
    resim4 = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["resim"], null=True, blank=True)
    resim5 = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["resim"], null=True, blank=True)
    resim6 = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["resim"], null=True, blank=True)


    youtube = models.URLField(blank=True)
    youtube2 = models.URLField(blank=True)
    youtube3 = models.URLField(blank=True)
    twitterwidget = models.TextField(blank=True, null=True)
    twitterwidget2 = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True,verbose_name="Meta Açıklama",help_text=HELP_TEXTS["meta_description"])
    keywords = models.CharField(max_length=255,blank=True,verbose_name="Anahtar Kelimeler",help_text=HELP_TEXTS["keywords"])
    yayin_tarihi = models.DateTimeField(null=True, blank=True, help_text="Postanın yayınlanacağı tarih ve saat")
    status = models.CharField(max_length=10, choices=status_cho, default="Taslak", help_text=HELP_TEXTS["status"])
    Trend = models.BooleanField(default=False, help_text="Ana Sayfada Popülerde Çıkar!")
    aktif = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    indexing = models.BooleanField(default=True, help_text="Indexlensin mi?")
    banner = models.BooleanField(default=False, help_text=HELP_TEXTS["banner"])
    editor = models.BooleanField(default=False,help_text=HELP_TEXTS["small_banner"])
    facebook = models.BooleanField(default=True, help_text="Facebook da Paylaşılsın mı ?")
    twitter = models.BooleanField(default=True, help_text="twitter da Paylaşılsın mı ?")
    pinterest = models.BooleanField(default=True, help_text="twitter da Paylaşılsın mı ?")
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    Kaynak_Linki = models.URLField(blank=True, null=True)
    Kaynak_Follow = models.TextField(blank=True, null=True)
    Kaynak_NoFollow = models.TextField(blank=True, null=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Post"
    def __str__(self):
        return self.title







class allname(models.Model):

    Durumlar = [
        ('Beklemede', 'Beklemede'),
        ('Yolda', 'Yolda'),
        ('Tamamlandı', 'Tamamlandı'),
    ]

    Cinsiyetler = [
        ('Kız', 'Kız'),
        ('Erkek', 'Erkek'),
        ('Unisex', 'Unisex'),
        ('B', 'B'),
    ]

    isim = models.CharField(max_length=255, unique=True, help_text=HELP_TEXTS["title"])
    aciklama = models.TextField(null=True)
    Durum = models.CharField(max_length=255, choices=Durumlar, null=True, default="Beklemede")
    Cinsiyet = models.CharField(max_length=255, choices=Cinsiyetler, null=True, default="B")

    class Meta:
        verbose_name_plural = "Tüm isimler"
    def __str__(self):
        return self.isim



class iletisimmodel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255,blank=True,null=True,help_text=HELP_TEXTS["keywords"])
    icerik = models.TextField( blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "iletişim Formu"
    def __str__(self):
        return self.email

