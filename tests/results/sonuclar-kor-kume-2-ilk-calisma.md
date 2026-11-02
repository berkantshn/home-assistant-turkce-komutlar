# Test sonucu: kor-kume-2

Geçen: **48/60** · süre: 4.0 sn

| # | Grup | Cümle | Beklenen niyet | Eşleşen niyet | Kaynak | Sonuç | Yanıt / sorun |
|---|------|-------|----------------|---------------|--------|-------|---------------|
| 1 | heldout2 | Avizeyi yakar mısın | HassTurnOn | HassTurnOn | custom | GEÇTİ | Avize açıldı. |
| 2 | heldout2 | Mutfak lambasını söndür lütfen | HassTurnOff | HassTurnOff | custom | GEÇTİ | Mutfak lambası kapatıldı. |
| 3 | heldout2 | Işığı açsana | HassTurnOn | HassTurnOn | custom | GEÇTİ | Işıklar açıldı. |
| 4 | heldout2 | Lambayı kapatır mısın | HassTurnOff | HassTurnOff | custom | GEÇTİ | Işıklar kapatıldı. |
| 5 | heldout2 | Yatak odasındaki abajuru yak | HassTurnOn | HassTurnOn | custom | GEÇTİ | abajur açıldı. |
| 6 | heldout2 | Salondaki ışıkları kapat | HassTurnOff | HassTurnOff | custom | GEÇTİ | Salon ışıkları kapatıldı. |
| 7 | heldout2 | Abajurun ışığını söndürür müsün | HassTurnOff | - | - | KALDI | niyet=None beklenen=HassTurnOff; hata yanıtı: no_intent_match / Üzgünüm, bunu anlayamadım. |
| 8 | heldout2 | Mutfağın ışığını açsana biraz | HassTurnOn | HassTurnOn | custom | GEÇTİ | Mutfağın ışıkları açıldı. |
| 9 | heldout2 | Salon lambası kapansın | HassTurnOff | HassTurnOff | custom | GEÇTİ | Salon lambası kapatıldı. |
| 10 | heldout2 | Kahve makinesini çalıştır | HassTurnOn | HassTurnOn | custom | GEÇTİ | Kahve makinesi açıldı. |
| 11 | heldout2 | Kahve makinesini kapatabilir misin | HassTurnOff | HassTurnOff | custom | GEÇTİ | Kahve makinesi kapatıldı. |
| 12 | heldout2 | Prizi açar mısın | HassTurnOn | HassTurnOn | custom | GEÇTİ | Priz açıldı. |
| 13 | heldout2 | Şu prizi kapat | HassTurnOff | HassTurnOff | custom | GEÇTİ | priz kapatıldı. |
| 14 | heldout2 | Tavan fanını çalıştır | HassTurnOn | HassTurnOn | custom | GEÇTİ | Tavan fanı açıldı. |
| 15 | heldout2 | Yatak odasındaki fanı durdur | HassTurnOff | - | custom | KALDI | niyet=None beklenen=HassTurnOff; hata yanıtı: no_valid_targets / Yatak odasındaki fanı  adında alan yok. |
| 16 | heldout2 | Klimayı çalıştırsana | HassTurnOn | HassTurnOn | custom | GEÇTİ | Klima açıldı. |
| 17 | heldout2 | Salon klimasını kapat | HassTurnOff | HassTurnOff | custom | GEÇTİ | Salon kliması kapatıldı. |
| 18 | heldout2 | Perdeyi aç | HassTurnOn | HassTurnOn | custom | GEÇTİ | Açıldı. |
| 19 | heldout2 | Salon perdesini kapatır mısın | HassTurnOff | HassTurnOff | custom | GEÇTİ | Salon perdesi kapatıldı. |
| 20 | heldout2 | Mutfaktaki panjuru indir | HassTurnOff | HassTurnOff | custom | GEÇTİ | panjur kapatıldı. |
| 21 | heldout2 | Panjuru açsana | HassTurnOn | HassTurnOn | custom | GEÇTİ | Panjur açıldı. |
| 22 | heldout2 | Televizyonu aç | HassTurnOn | HassTurnOn | custom | GEÇTİ | Televizyon açıldı. |
| 23 | heldout2 | Televizyonu kapatır mısın | HassTurnOff | HassTurnOff | custom | GEÇTİ | Televizyon kapatıldı. |
| 24 | heldout2 | Film Gecesi sahnesini başlat | HassTurnOn | HassTurnOn | custom | GEÇTİ | Film Gecesi etkinleştirildi. |
| 25 | heldout2 | Avizenin parlaklığını yüzde 40 yap | HassLightSet | HassLightSet | custom | GEÇTİ | Parlaklık yüzde 40 yapıldı. |
| 26 | heldout2 | Abajuru kırmızı yapar mısın | HassLightSet | HassLightSet | custom | GEÇTİ | Renk ayarlandı. |
| 27 | heldout2 | Işıkları yüzde 70 parlaklığa getir | HassLightSet | - | custom | KALDI | niyet=None beklenen=HassLightSet; hata yanıtı: no_valid_targets / Üzgünüm, bunu anlayamadım. |
| 28 | heldout2 | Mutfak lambasını mavi renge çevir | HassLightSet | HassLightSet | custom | GEÇTİ | Renk ayarlandı. |
| 29 | heldout2 | Salon klimasını 23 dereceye ayarla | HassClimateSetTemperature | HassClimateSetTemperature | custom | GEÇTİ | Sıcaklık 23 derece yapıldı. |
| 30 | heldout2 | Klimayı 26 derece yap | HassClimateSetTemperature | HassClimateSetTemperature | custom | GEÇTİ | Sıcaklık 26 derece yapıldı. |
| 31 | heldout2 | Salonda hava kaç derece | HassClimateGetTemperature | - | custom | KALDI | niyet=None beklenen=HassClimateGetTemperature; hata yanıtı: no_valid_targets / Salonda hava adında bir cihaz yok. |
| 32 | heldout2 | Burası kaç derece şu an | HassClimateGetTemperature | - | custom | KALDI | niyet=None beklenen=HassClimateGetTemperature; hata yanıtı: no_valid_targets / Burası adında bir cihaz yok. |
| 33 | heldout2 | Salon penceresi açık mı | HassGetState | HassGetState | custom | GEÇTİ | Hayır, kapalı. |
| 34 | heldout2 | Mutfaktaki nem oranı nedir | HassGetState | HassGetState | custom | GEÇTİ | 60 % |
| 35 | heldout2 | Mutfakta hareket var mı | HassGetState | HassGetState | custom | GEÇTİ | Hayır. |
| 36 | heldout2 | Avize açık mı şu an | HassGetState | HassGetState | custom | GEÇTİ | Evet. |
| 37 | heldout2 | Tavan fanının hızını yüzde 50 yap | HassFanSetSpeed | HassFanSetSpeed | custom | GEÇTİ | Fan hızı ayarlandı. |
| 38 | heldout2 | Fanı yüzde 80 hıza ayarlar mısın | HassFanSetSpeed | - | custom | KALDI | niyet=None beklenen=HassFanSetSpeed; hata yanıtı: no_valid_targets / Üzgünüm, bunu anlayamadım. |
| 39 | heldout2 | Panjuru yüzde 30 aç | HassSetPosition | HassSetPosition | custom | GEÇTİ | Konum ayarlandı. |
| 40 | heldout2 | Perdeyi yüzde 50 kapat | HassSetPosition | - | custom | KALDI | niyet=None beklenen=HassSetPosition; hata yanıtı: no_valid_targets / Perdeyi yüzde 50 adında bir cihaz yok. |
| 41 | heldout2 | Salon perdesini yüzde 75 konumuna getir | HassSetPosition | - | custom | KALDI | niyet=None beklenen=HassSetPosition; hata yanıtı: no_valid_targets / Üzgünüm, bunu anlayamadım. |
| 42 | heldout2 | Televizyonu duraklat | HassMediaPause | HassMediaPause | custom | GEÇTİ | Duraklatıldı. |
| 43 | heldout2 | Müziği durdur biraz | HassMediaPause | HassMediaPause | custom | GEÇTİ | Duraklatıldı. |
| 44 | heldout2 | Hoparlörden devam et | HassMediaUnpause | - | custom | KALDI | niyet=None beklenen=HassMediaUnpause; hata yanıtı: no_valid_targets / Hoparlörden  adında alan yok. |
| 45 | heldout2 | Oynatmaya devam et | HassMediaUnpause | - | custom | KALDI | niyet=None beklenen=HassMediaUnpause; hata yanıtı: no_valid_targets / Oynatmaya adında bir cihaz yok. |
| 46 | heldout2 | Sonraki şarkıya geç | HassMediaNext | HassMediaNext | custom | GEÇTİ | Sonrakine geçildi. |
| 47 | heldout2 | Hoparlörde bir sonraki parçayı çal | HassMediaNext | HassMediaNext | custom | GEÇTİ | Sonrakine geçildi. |
| 48 | heldout2 | Önceki şarkıya dön | HassMediaPrevious | HassMediaPrevious | custom | GEÇTİ | Öncekine dönüldü. |
| 49 | heldout2 | Televizyonun sesini 25 yap | HassSetVolume | HassSetVolume | custom | GEÇTİ | Ses ayarlandı. |
| 50 | heldout2 | Sesi yüzde 40 yapar mısın | HassSetVolume | HassSetVolume | custom | GEÇTİ | Ses ayarlandı. |
| 51 | heldout2 | Hoparlörün sesini kıs | HassSetVolumeRelative | HassSetVolumeRelative | custom | GEÇTİ | Ses ayarlandı. |
| 52 | heldout2 | Sesi biraz aç | HassSetVolumeRelative | HassSetVolumeRelative | custom | GEÇTİ | Ses ayarlandı. |
| 53 | heldout2 | Televizyonu sessize al | HassMediaPlayerMute | HassMediaPlayerMute | custom | GEÇTİ | Ses kapatıldı. |
| 54 | heldout2 | Robot süpürgeyi çalıştır | HassVacuumStart | HassVacuumStart | custom | GEÇTİ | Süpürge başlatıldı. |
| 55 | heldout2 | Süpürgeyi eve gönder | HassVacuumReturnToBase | - | - | KALDI | niyet=None beklenen=HassVacuumReturnToBase; hata yanıtı: no_intent_match / Üzgünüm, bunu anlayamadım. |
| 56 | heldout2 | Saat kaç | HassGetCurrentTime | HassGetCurrentTime | custom | GEÇTİ | Saat 11:38. |
| 57 | heldout2 | Bugün ayın kaçı | HassGetCurrentDate | HassGetCurrentDate | custom | GEÇTİ | 2 Kasım 2026, Pazartesi. |
| 58 | heldout2 | Hava durumu nasıl | HassGetWeather | HassGetWeather | custom | GEÇTİ | 18.0 °C, parçalı bulutlu. |
| 59 | heldout2 | Alışveriş listesine süt ekle | HassShoppingListAddItem | HassShoppingListAddItem | custom | GEÇTİ | süt listeye eklendi. |
| 60 | heldout2 | 10 dakikalık sayaç kur | HassStartTimer | HassStartTimer | builtin | KALDI | hata yanıtı: failed_to_handle / Bu cihazda zamanlayıcılar desteklenmiyor. |
