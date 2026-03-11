# Hayvan İsimleri Seed Verisi - Gemini Prompt

Bu prompt'u Gemini'ye vererek isim listesini genişletebilirsin.

## Prompt

```
Bu Django projesindeki hayvan isimleri seed verisini genişletmeni istiyorum.

DOSYA: isimler/views.py
FONKSİYON: hepsini_ekle (satır 751)
İÇİNDEKİ LİSTE: isim_data (satır 791'den başlıyor)

FORMAT:
Her isim bir tuple:
("isim", "anlam", "cinsiyet", ["kategori-slug-listesi"])

- isim: küçük harf, türkçe karakter olabilir
- anlam: kısa açıklama
- cinsiyet: "erkek", "disi" veya "unisex"
- kategori slugları: ismin ait olduğu kategoriler

MEVCUT KATEGORİ SLUG'LARI:
- kopek-isimleri
- kedi-isimleri
- kus-isimleri
- balik-isimleri
- hamster-isimleri
- tavsan-isimleri
- kaplumbaga-isimleri
- at-isimleri
- papagan-isimleri
- yilan-isimleri

MEVCUT İSİMLER (TEKRARLAMA):
boncuk, pamuk, karamel, tarçın, zeytin, aslan, buddy, lucky, max, bella, çakıl, fıstık, kaplan, kurt, duman, paşa, prenses, çomar, karabas, findik, zeus, luna, rocky, daisy, charlie, toby, maya, oscar, sasha, rex, tekir, minnak, pati, miyav, ponçik, simba, cleo, whiskers, misty, tiger, nala, garfield, bıdık, maviş, tüylü, siyah, sarman, çiçek, melek, tırnak, cıvıl, tüy, melodí, tweety, kanarya, bulut, şeker, limon, rüzgar, cennet, şakrak, mavimsi, gonca, vivaldi, mozart, pırıl, nemo, dory, goldie, mercan, dalga, inci, okyanus, yıldız, atlas, neptün, pul, kumsal, turkuaz, deniz, marina, ceviz, çıtır, topik, minik, kurabiye, badem, nugget, peluş, susam, lokum, pofuduk, mısır, yerfıstığı, papatyam, havuç, tüfek, kar, zıpzıp, yonca, cotton, bunny, toffee, oreo, latte, tüylüş, ninja, yavaş, tank, kaya, zümrüt, çakıltaşı, yeşil, sheldon, turbo, bilge, donatello, rafaello, yıldırım, fırtına, şahlan, küheylan, alaca, doru, gökhan, cesur, sultan, kraliçe, yelen, karayel, bora, akın, polly, lori, rio, koko, bıcırık, geveze, pranga, yeşilçam, amazon, pikaçu, zazu, iago, kobra, nagini, medusa, venom, python, jade, gölge, zehir, ipek, slyther, basilisk, onyx

KURALLAR:
1. isimler/views.py dosyasındaki isim_data listesine eklenecek şekilde sadece Python tuple listesi ver
2. Yukarıdaki mevcut isimleri tekrarlama
3. Her kategoride en az 30 YENİ isim olsun
4. Birden fazla kategoriye uygun isimler varsa birden fazla slug ekle
5. Türkçe isimler ağırlıklı olsun ama yabancı isimler de olabilir
6. Çıktıyı direkt kopyalayıp isim_data listesinin sonuna yapıştırabileyim
7. En az 300 YENİ isim ekle
```

## Notlar

- Gemini'den gelen çıktıyı `isim_data` listesinin sonuna (968. satır civarı, `]` kapanışından önce) yapıştır
- `/hepsini-ekle/` URL'ine gidince `get_or_create` kullandığı için mevcut isimler tekrar eklenmez
- JSON endpoint: `/hayvan-json/` tüm veriyi döner
