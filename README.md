# Home Assistant Türkçe Komutlar

Home Assistant Assist için günlük konuşma Türkçesiyle yazılmış ek cümle paketi: "salonun ışığını açar mısın", "avizeyi yüzde 50 yap", "hangi ışıklar açık", "sesi kıs", "saat kaç".

Home Assistant'ın kendi Türkçe cümlelerinin yerine geçmez, üstüne eklenir. Bulut veya yapay zeka kullanmaz.

*English summary: [below](#english-summary).*

## Neden gerekli?

Home Assistant'ın resmi cümle deposu [home-assistant/intents](https://github.com/home-assistant/intents) Türkçeyi destekler, ama kapsamı dar. İngilizcede 42 niyet (intent, yani komut türü) varken Türkçede 8 tane var: açma, kapatma, sıcaklık okuma ve ayarlama, zamanlayıcı başlatma ve iptali, vazgeçme. Karşılaştırma tarihi: 2026-11-02, inceleme `b1e9b98` numaralı sürüm üzerinde yapıldı.

| Konu | Yerleşik Türkçe | Bu paketle |
|---|---|---|
| Açma, kapatma | Çoğul, yalın emir: "mutfaktaki ışıkları aç" | Tekil, rica, iyelik: "salonun ışığını açar mısın", "salonun avizesini aç" |
| Cümle başı büyük I: "Işıkları kapat" | Tanımaz | Tanır |
| Parlaklık, renk, ışık tonu | Yok | Var |
| Durum sorma ("avize açık mı", "hangi ışıklar açık") | Yok | Var |
| Kat komutları, sahne, script | Yok | Var |
| Perde konumu, fan hızı, süpürge | Yok | Var |
| Müzik, ses | Yok | Var |
| Saat, tarih, hava durumu, alışveriş listesi | Yok | Var |
| Zamanlayıcı duraklatma, süre ekleme, kalan süre | Yok | Var |
| Oda sıcaklığı yanıtı | Gerçek klimada "off derece" der | "23 derece" der |

Paket 26 yeni niyet için cümle ekler, 6 niyeti genişletir. En doğru uzun vadeli yer yine de resmi depodur: [docs/UST_PROJE.md](docs/UST_PROJE.md).

## Kurulum

1. `custom_sentences/tr/` klasöründeki `.yaml` dosyalarını Home Assistant yapılandırmanızda `/config/custom_sentences/tr/` altına kopyalayın. Klasör yoksa oluşturun.
2. **Geliştirici Araçları > Eylemler** bölümünde `conversation.reload` çalıştırın ya da Home Assistant'ı yeniden başlatın.
3. Assist hattınızın dilinin **Türkçe** olduğunu kontrol edin.
4. Cihazlarınızın **Ayarlar > Ses asistanları > Cihazları göster** ekranında Assist'e açık olduğunu kontrol edin. Hava durumu ve script varsayılan olarak kapalıdır; o komutları kullanacaksanız bunları elle açın.
5. **Geliştirici Araçları > Assist** ekranında bir cümle deneyin.

Kaldırmak için aynı dosyaları silin, `conversation.reload` çalıştırın.

Oda adı gerekmeyen komutlar ("ışığı aç", "sesi kıs", zamanlayıcı) sesli asistan cihazı (uydu) üzerinden çalışır, çünkü odayı o cihazdan öğrenir. Yazılı Assist ekranından "salonun ışığını aç" gibi odayı söyleyin.

Oda adları, ek çözümü ve kendi cümlenizi eklemek için: [docs/REHBER.md](docs/REHBER.md).

## Örnek cümleler

Örnekler Salon, Mutfak gibi odalar ve Avize gibi cihazlar varsayar; kendi adlarınızla söyleyin.

| Ne yapar | Örnek |
|---|---|
| Oda ışığı | salonun ışığını aç · mutfağın ışığını söndür · yatak odasındaki lambayı kapat · aç salonun ışığını |
| Rica biçimleri | avizeyi yakabilir misin · kapatsana · söndürür müsün · priz kapansın · yatak odasında ışık kalmasın |
| Kat ve tüm ev | üst kattaki ışıkları kapat · evdeki bütün ışıkları aç · tüm ışıkları kapatır mısın |
| Parlaklık | avizeyi yüzde 50 yap · salonun ışığını %40'a getir · mutfağın ışığını kıs · avizeyi en yükseğe al |
| Renk, ton | avizeyi kırmızı yap · salonun ışığını maviye çevir · abajuru sıcak beyaz yap |
| Sıcaklık | salonun sıcaklığını 22 yap · 22 buçuk derece yap · salon kliması 24 derece yap · salon kaç derece oldu |
| Fan | tavan fanını yüzde 40 yap · tavan fanını durdur · yatak odasının fanını %70'e ayarla |
| Perde | salon perdesini yüzde 30 aç · salonun perdesini yarıya indir · mutfağın panjurunu indir |
| Durum | avize açık mı · salonda açık ışık var mı · hangi ışıklar açık · kaç ışık açık · salonun nemi kaç · mutfakta hareket var mı · ön kapı kilitli mi |
| Müzik, ses | müziği durdur · müziğe devam et · sonraki şarkıya geç · sesi yüzde 30 yap · televizyonun sesini kıs · televizyonu sessize al |
| Süpürge, sahne | robot süpürgeyi başlat · süpürgeyi eve gönder · salonu süpür · film gecesi modunu aç |
| Genel | saat kaç · bugünün tarihi ne · hava nasıl · alışveriş listesine süt ekle · boş ver · teşekkürler |
| Zamanlayıcı | 10 dakikaya zamanlayıcı kur · 1 saat 30 dakikalık zamanlayıcı kur · zamanlayıcıda ne kadar kaldı · zamanlayıcıyı duraklat · zamanlayıcıya 5 dakika ekle |

Birden çok işi birden yapan "iyi geceler", "evden çıkıyorum" gibi komutlar için [examples/otomasyonlar.yaml](examples/otomasyonlar.yaml). Bu dosya örnektir, kurulumun parçası değildir.

## Güvenlik

**Bu paket kapı açan veya alarm kapatan cümle içermez.** Kilit için yalnızca soru var ("ön kapı kilitli mi"). Garaj kapısı için de yeni cümle eklenmedi. Testlerde kilit ve alarm bilerek Assist'e açıldı, paketin hiçbir cümlesi onları değiştirmedi.

**Ama dikkat:** Home Assistant'ın kendi Türkçe cümleleri şunları zaten yapıyor ve bu paket onları kapatamıyor:

- "ön kapının kilidini aç": kilit Assist'e açıksa kilidi **gerçekten açar** (testte görüldü). Kilitler varsayılan olarak Assist'e kapalıdır, biri elle açmış olmalı.
- "garaj kapısını aç": kapıyı açar. **Garaj kapısı perde gibi bir kapak sayıldığı için testte elle açmaya gerek kalmadan Assist'e açıktı.**

Sesli komut kimin konuştuğunu bilmez, pencereden bağıran biri de söyleyebilir. Kilit, alarm ve garaj kapısını Assist'e kapalı tutun, garaj kapınızı özellikle kontrol edin. Bu ayar **Ayarlar > Ses asistanları > Cihazları göster** ekranındadır.

## Test sonuçları

Testler `home-assistant:stable` imajı üzerinde çalıştı (Home Assistant 2026.10.4, intents 2026.10.6, hassil 3.12.1). Sahte cihazlarla, gerçek API üzerinden yapıldı: her cümlede eşleşen niyet ve cihazın son durumu kontrol edildi. Yanıtlar da okundu.

Önemli olan üç ayrı rakam var:

| Ölçüm | Sonuç | Ne anlama geliyor |
|---|---|---|
| **Paketi görmeden yazılmış 60 cümle, ilk çalışma** | **48/60 (%80)** | En dürüst tahmin budur. Paket olmadan aynı cümlelerde 9/60 (%15). |
| Bu paket için yazılmış matris | 170/170 | Kurallar bu cümlelere göre düzeltildi, yüksek çıkması beklenir. Gerçek hayat başarısı sanmayın. |
| Resmi deponun kendi 144 Türkçe test cümlesi | 144/144, paket bozmadı | Paket var olan davranışı başka niyete kaydırmıyor. Eşleşme düzeyinde ölçüldü. |

İlk kör küme 36/60 geçti, kurallar ona göre düzeltildi, sonra yeni yazılmış ikinci kör küme 48/60 geçti. Ardından ikinci kümeye göre de düzeltme yapıldı (şimdi 57/60), yani artık o da kör değildir. Birinci kümede 11 cümle kalıyor; bunların bazıları uyduda çalışan cümlenin uydusuz denenmesi ya da beklenen niyet etiketinin tartışmalı olması yüzünden kalıyor, bazıları desteklenmiyor ("hava nasıl olacak" gibi tahmin soruları).

Matriste paketsiz sonuç 43/170'tir. Eşleşmesi beklenen paket satırlarında (güvenlik, yanlış eşleşme, otomasyon ve üst proje satırları hariç) paketsiz 8/134, paketli 134/134.

Ayrıntılar: [tests/results/](tests/results/). Tekrar çalıştırmak için `python tests/run_tests.py` (Docker ve Python 3 gerekir).

## Sınırlar

- **Gerçek sesle denenmedi.** Testler konuşma tanımanın (STT) çıktısı yerine doğrudan metin gönderir. Türkçe konuşma tanımanın kalitesi burada ölçülmedi, sonuç onun doğruluğuna bağlıdır. Resmi depodaki `languages.yaml` Türkçe için Home Assistant Cloud konuşma tanımayı destekli, yerel Whisper ve Speech-to-Phrase'i desteksiz olarak işaretliyor.
- **Sesli asistan cihazında denenmedi.** Uydu davranışı, sahte bir cihaz kimliğiyle taklit edildi. Sesli yanıt (TTS) denenmedi.
- **Gerçek cihazda denenmedi.** Sahte varlıklar kullanıldı; markaya özgü farklılıklar görülmüş olmaz.
- **Yalnızca 2026.10.4 denendi.** Eski sürümlerde çalışıp çalışmadığı bilinmiyor.
- **Kalıba dayalıdır.** Kalıpta olmayan cümle tanınmaz. Kör testte yaklaşık beş cümleden biri tanınmadı.
- **"Kıs" ve "hızlandır" sabit değerdir.** Home Assistant'ta göreli parlaklık ve fan niyeti yok. "Kıs" %30, "parlat" %100, fan "yavaşlat" %30, "hızlandır" %100 yapar. "Biraz" sözcüğü yok sayılır.
- **Göreli sıcaklık yok.** "Sıcaklığı biraz artır" çalışmaz; hedef derece söylenmelidir.
- **Ünsüz yumuşaması:** Yalnızca Mutfak tanımlı ("mutfağın"). Diğerleri için [rehber](docs/REHBER.md).
- **Adında büyük I olan cihaz:** "Tavan Işığı" yazılmış ad, "tavan ışığını aç" ile eşleşmez. Küçük harfli takma ad gerekir, [rehberde](docs/REHBER.md) anlatıldı.
- **Alışveriş listesi eki ayıklamaz:** "sütü listeme ekle" listeye "sütü" yazar.
- **Dahil edilmedi:** Müzik arama ve çalma, yapılacaklar listeleri, duyuru (broadcast), çim biçme, klimadaki hedef sıcaklığı sorma, hava tahmini.
- **Dolgu sözcükleri yok sayılır:** şu, hadi, haydi, bi, bir, biraz, tamamen, acaba, hemen, bana, şimdi, şu an. Bu liste tüm Türkçe Assist cümleleri için geçerlidir, yerleşikler dahil.

## Lisans ve atıf

Bu paket [MIT](LICENSE) lisanslıdır.

Cümle biçimi ve niyet adları Home Assistant'ın [home-assistant/intents](https://github.com/home-assistant/intents) projesindeki yapıya uyar; o proje [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) lisanslıdır. Bu depoda o projenin dosyası kopyalanmadı, cümleler ve kurallar yeniden yazıldı. Hava durumu ve zamanlayıcı yanıtlarının içerdiği alan adları ve mantık, o projenin İngilizce yanıtları incelenerek hazırlandı. Testte resmi cümleler ayrı bir klondan okunur, depoya alınmaz. Bu proje Home Assistant veya Nabu Casa ile bağlantılı değildir.

## English summary

An add-on sentence pack for Home Assistant Assist in everyday Turkish. It is added on top of the built-in Turkish sentences, not a replacement. Built-in Turkish covers 8 intents; this pack adds sentences for 26 more (light brightness and colour, state queries, floors, scenes, cover position, fan speed, media, volume, time, date, weather, shopping list, timer controls) and widens 6 existing ones with singular forms, polite verbs and possessive suffixes.

**Install:** copy `custom_sentences/tr/*.yaml` to `/config/custom_sentences/tr/`, run `conversation.reload`.

**Honest results** (Home Assistant 2026.10.4, fake devices, real API, text only): 48/60 on sentences written without seeing the pack (9/60 without the pack), 170/170 on the project's own tuned matrix, 144/144 of upstream's Turkish tests still match. Not tested with real speech, real satellites or real devices.

**Safety:** this pack adds no phrases that unlock doors, disarm alarms or open garage doors. Built-in Turkish sentences can still unlock an exposed lock or open an exposed garage door, so do not expose those to Assist.

**Better long term:** most of this belongs upstream in `home-assistant/intents`. See [docs/UST_PROJE.md](docs/UST_PROJE.md).

## ⭐ Support this project

If this project helped you, please give it a ⭐ and [follow me on GitHub](https://github.com/berkantshn) for more.

İşine yaradıysa projeye ⭐ verip [beni GitHub'da takip edebilirsin](https://github.com/berkantshn).

---

Made By FALCREB
