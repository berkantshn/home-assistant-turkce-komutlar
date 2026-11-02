# Resmi projeye (home-assistant/intents) katkı

<!-- Made By FALCREB -->

Bu paket boşluğu bugün kapatır, ama cümlelerin en doğru yeri resmi depodur: orada herkese kurulumsuz gelir ve çeviri ekibi bakımını üstlenir. Paket ayrı durduğu sürece kullanıcı onu elle kurmak zorundadır.

## İnceleme özeti

Tarih 2026-11-02, sürüm `b1e9b98`. Türkçe: 8 niyet (`HassTurnOn`, `HassTurnOff`, `HassClimateGetTemperature`, `HassClimateSetTemperature`, `HassStartTimer`, `HassCancelTimer`, `HassCancelAllTimers`, `HassNevermind`). İngilizce: 42 niyet klasörü.

Proje canlı: Türkçe dosyalar Ekim 2026'da değişti (#4253, #4254). Türkçe için kod sahibi `CODEOWNERS` dosyasında yazıyor.

## Resmi depoya önerilebilecek işler (kolaydan zora)

1. **Hata: oda sıcaklığı yanıtı.** `responses/tr/HassClimateGetTemperature.yaml` içindeki `{{ state.state }} derece`, gerçek klima varlığında "off derece" diyor. İngilizce yanıt `current_temperature` özniteliğini okuyor. Bu testte görüldü, küçük ve net bir düzeltme.
2. **Hata: cümle başı büyük I.** "Işıkları kapat" eşleşmiyor, çünkü küçültme "I" harfini "i" yapıyor. Konuşma tanıma cümleye büyük harfle başladığı için Türkçe kullanıcılar bundan etkilenir. Sadece kurallara `(ı|i)şık` yazmak çözüm olur ama asıl düzeltme eşleştiricidedir (hassil), oraya ayrıca bildirilebilir. Aynı neden "Tavan Işığı" adlı cihazın "tavan ışığı" ile eşleşmemesine de yol açıyor.
3. **Yazım:** "boşver" yanında "boş ver" de eklenmeli.
4. **Tekil biçimler:** "salonun ışığını aç", "lambayı yak". Şu an çoğul zorunlu.
5. **İyelik eki:** "salonun avizesini aç". Mevcut ek kalıbı `-sını` biçimini kapsamıyor.
6. **Yeni niyetler:** `HassGetState`, `HassLightSet`, `HassGetCurrentTime`, `HassGetCurrentDate`, medya, ses, perde konumu, fan hızı. Birer birer ayrı PR olmalı.

## Bu paket doğrudan PR olamaz

Biçim farklı. Resmi depo her niyeti `sentences/tr/<Niyet>/<kombinasyon>.yaml` dosyalarına böler, her cümle için `tests/tr/` altında test ister ve `intentfest validate` doğrulamasından geçer. Kuralları da daha sıkıdır: dokümana göre liste bir seçenek grubunun veya isteğe bağlı parçanın içinde olmamalı, bir kural liste veya başka kural içermemeli. Bu paketteki `<alan>` ve `<cihaz>` bu önerilere uymaz. Bu yüzden cümleler o biçime elle aktarılmalı.

`intents.yaml` dosyası korumalıdır; eksik bir kombinasyon için PR'da değiştirmek yerine issue açılır.

## Nasıl başlanır

```bash
git clone https://github.com/home-assistant/intents.git
cd intents
python3 -m script.intentfest validate --language tr
```

Rehber: [How to contribute](https://developers.home-assistant.io/docs/voice/intent-recognition/contributing/). Resmi depoya katkılar o projenin lisansıyla (CC BY 4.0) yayınlanır, bu paketin MIT lisansıyla değil.

## Bu pakete gelecekte ne olur

Resmi depo bir özelliği eklediğinde karşılığı buradan silinmeli. Paket resmi kural adlarına bağlı olmadığı için o güncelleme paketi bozmaz, ama aynı anda iki kaynak aynı cümleyi tanıyabilir. O durumda paket kazanır, çünkü Home Assistant özel cümleleri önce dener.
