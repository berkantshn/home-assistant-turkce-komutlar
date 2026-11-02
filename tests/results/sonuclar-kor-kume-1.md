# Test sonucu: kor-kume-1

Geçen: **49/60** · süre: 4.1 sn

| # | Grup | Cümle | Beklenen niyet | Eşleşen niyet | Kaynak | Sonuç | Yanıt / sorun |
|---|------|-------|----------------|---------------|--------|-------|---------------|
| 1 | heldout | yatak odasında ışık kalmasın | HassTurnOff | HassTurnOff | custom | GEÇTİ | yatak odası ışıkları kapatıldı. |
| 2 | heldout | salon lambasını açar mısın | HassTurnOn | HassTurnOn | custom | GEÇTİ | salon lambası açıldı. |
| 3 | heldout | mutfağın ışığını kapat lütfen | HassTurnOff | HassTurnOff | custom | GEÇTİ | mutfağın ışıkları kapatıldı. |
| 4 | heldout | avizeyi yak | HassTurnOn | HassTurnOn | custom | GEÇTİ | avize açıldı. |
| 5 | heldout | abajuru söndür | HassTurnOff | HassTurnOff | custom | GEÇTİ | abajur kapatıldı. |
| 6 | heldout | ışıkları aç | HassTurnOn | HassTurnOn | custom | GEÇTİ | Işıklar açıldı. |
| 7 | heldout | burada ışık yok, yakar mısın | HassTurnOn | - | custom | KALDI | niyet=None beklenen=HassTurnOn; hata yanıtı: no_valid_targets / burada ışık yok adında bir cihaz yok. |
| 8 | heldout | lambayı kapatsana | HassTurnOff | HassTurnOff | custom | GEÇTİ | Işıklar kapatıldı. |
| 9 | heldout | kahve makinesini çalıştır | HassTurnOn | HassTurnOn | custom | GEÇTİ | kahve makinesi açıldı. |
| 10 | heldout | kahve makinesini kapatır mısın | HassTurnOff | HassTurnOff | custom | GEÇTİ | kahve makinesi kapatıldı. |
| 11 | heldout | prizi aç | HassTurnOn | HassTurnOn | custom | GEÇTİ | priz açıldı. |
| 12 | heldout | priz kapansın | HassTurnOff | HassTurnOff | custom | GEÇTİ | priz kapatıldı. |
| 13 | heldout | tavan fanını çalıştırır mısın | HassTurnOn | HassTurnOn | custom | GEÇTİ | tavan fanı açıldı. |
| 14 | heldout | tavan fanını durdur | HassTurnOff | HassTurnOff | custom | GEÇTİ | tavan fanı kapatıldı. |
| 15 | heldout | televizyonu aç | HassTurnOn | HassTurnOn | custom | GEÇTİ | televizyon açıldı. |
| 16 | heldout | televizyonu kapatabilir misin | HassTurnOff | HassTurnOff | custom | GEÇTİ | televizyon kapatıldı. |
| 17 | heldout | salon klimasını çalıştır | HassTurnOn | HassTurnOn | custom | GEÇTİ | salon kliması açıldı. |
| 18 | heldout | klimayı kapat | HassTurnOff | - | custom | KALDI | niyet=None beklenen=HassTurnOff; hata yanıtı: no_valid_targets / Üzgünüm, bunu anlayamadım. |
| 19 | heldout | film gecesini başlat | HassTurnOn | HassTurnOn | custom | GEÇTİ | film gecesi etkinleştirildi. |
| 20 | heldout | mutfaktaki bütün ışıkları söndür | HassTurnOff | HassTurnOff | custom | GEÇTİ | mutfak ışıkları kapatıldı. |
| 21 | heldout | zemin kattaki ışıkları kapat | HassTurnOff | HassTurnOff | custom | GEÇTİ | zemin kat ışıkları kapatıldı. |
| 22 | heldout | üst kattaki lambaları yak | HassTurnOn | HassTurnOn | custom | GEÇTİ | üst kat ışıkları açıldı. |
| 23 | heldout | salon lambasının parlaklığını yüzde elli yap | HassLightSet | HassLightSet | custom | GEÇTİ | Parlaklık yüzde elli yapıldı. |
| 24 | heldout | avizeyi biraz kıs | HassLightSet | HassLightSet | custom | GEÇTİ | Işık kısıldı. |
| 25 | heldout | abajurun rengini kırmızı yapar mısın | HassLightSet | HassLightSet | custom | GEÇTİ | Renk ayarlandı. |
| 26 | heldout | ışığı yüzde yetmişe ayarla | HassLightSet | HassLightSet | custom | GEÇTİ | Parlaklık yüzde yetmiş yapıldı. |
| 27 | heldout | salon lambası açık mı | HassGetState | HassGetState | custom | GEÇTİ | Evet. |
| 28 | heldout | mutfak penceresi... salon penceresi açık mı | HassGetState | - | - | KALDI | niyet=None beklenen=HassGetState; hata yanıtı: no_intent_match / Üzgünüm, bunu anlayamadım. |
| 29 | heldout | mutfakta hareket var mı | HassGetState | HassGetState | custom | GEÇTİ | Hayır. |
| 30 | heldout | salonun nem oranı kaç | HassGetState | HassGetState | custom | GEÇTİ | 45 % |
| 31 | heldout | salonda sıcaklık kaç derece | HassGetState | HassClimateGetTemperature | custom | KALDI | niyet=HassClimateGetTemperature beklenen=HassGetState |
| 32 | heldout | klimayı 24 dereceye ayarla | HassClimateSetTemperature | - | custom | KALDI | niyet=None beklenen=HassClimateSetTemperature; hata yanıtı: no_valid_targets / Üzgünüm, bunu anlayamadım. |
| 33 | heldout | salon kliması sıcaklığını yirmi iki yap | HassClimateSetTemperature | HassClimateSetTemperature | custom | GEÇTİ | Sıcaklık yirmi iki derece yapıldı. |
| 34 | heldout | klimanın sıcaklığı şu an kaç | HassClimateGetTemperature | - | custom | KALDI | niyet=None beklenen=HassClimateGetTemperature; hata yanıtı: no_valid_targets / Üzgünüm, bunu anlayamadım. |
| 35 | heldout | salon kliması kaç dereceye ayarlı | HassClimateGetTemperature | - | - | KALDI | niyet=None beklenen=HassClimateGetTemperature; hata yanıtı: no_intent_match / Üzgünüm, bunu anlayamadım. |
| 36 | heldout | tavan fanının hızını yüzde altmış yap | HassFanSetSpeed | HassFanSetSpeed | custom | GEÇTİ | Fan hızı ayarlandı. |
| 37 | heldout | tavan fanını biraz hızlandırır mısın | HassFanSetSpeed | HassFanSetSpeed | custom | GEÇTİ | Fan hızı ayarlandı. |
| 38 | heldout | salon perdesini yüzde ellisine kadar aç | HassSetPosition | HassSetPosition | custom | GEÇTİ | Konum ayarlandı. |
| 39 | heldout | perdeyi tamamen aç | HassSetPosition | - | builtin | KALDI | niyet=None beklenen=HassSetPosition; hata yanıtı: no_valid_targets / Üzgünüm, bunu anlayamadım. |
| 40 | heldout | panjuru kapatır mısın | HassSetPosition | HassTurnOff | custom | KALDI | niyet=HassTurnOff beklenen=HassSetPosition |
| 41 | heldout | mutfak panjurunu yüzde otuza getir | HassSetPosition | HassSetPosition | custom | GEÇTİ | Konum ayarlandı. |
| 42 | heldout | televizyonu duraklat | HassMediaPause | HassMediaPause | custom | GEÇTİ | Duraklatıldı. |
| 43 | heldout | hoparlörü bir dur | HassMediaPause | HassMediaPause | custom | GEÇTİ | Duraklatıldı. |
| 44 | heldout | televizyonda devam et | HassMediaUnpause | HassMediaUnpause | custom | GEÇTİ | Devam ediyor. |
| 45 | heldout | hoparlörü tekrar başlat | HassMediaUnpause | HassMediaUnpause | custom | GEÇTİ | Devam ediyor. |
| 46 | heldout | sıradaki şarkıya geç | HassMediaNext | HassMediaNext | custom | GEÇTİ | Sonrakine geçildi. |
| 47 | heldout | hoparlörde bir sonraki parçayı çal | HassMediaNext | HassMediaNext | custom | GEÇTİ | Sonrakine geçildi. |
| 48 | heldout | önceki şarkıya dön | HassMediaPrevious | HassMediaPrevious | custom | GEÇTİ | Öncekine dönüldü. |
| 49 | heldout | televizyonun sesini yüzde yirmi yap | HassSetVolume | HassSetVolume | custom | GEÇTİ | Ses ayarlandı. |
| 50 | heldout | hoparlörün sesini biraz aç | HassSetVolumeRelative | HassSetVolumeRelative | custom | GEÇTİ | Ses ayarlandı. |
| 51 | heldout | televizyonun sesini kıs | HassSetVolumeRelative | HassSetVolumeRelative | custom | GEÇTİ | Ses ayarlandı. |
| 52 | heldout | televizyonu sessize al | HassMediaPlayerMute | HassMediaPlayerMute | custom | GEÇTİ | Ses kapatıldı. |
| 53 | heldout | robot süpürgeyi çalıştır | HassVacuumStart | HassVacuumStart | custom | GEÇTİ | Süpürge başlatıldı. |
| 54 | heldout | süpürgeyi temizliğe başlat | HassVacuumStart | HassVacuumStart | custom | GEÇTİ | Süpürge başlatıldı. |
| 55 | heldout | robot süpürgeyi şarj istasyonuna gönder | HassVacuumReturnToBase | HassVacuumReturnToBase | custom | GEÇTİ | Süpürge istasyona gönderildi. |
| 56 | heldout | saat kaç | HassGetCurrentTime | HassGetCurrentTime | custom | GEÇTİ | Saat 11:45. |
| 57 | heldout | bugün günlerden ne | HassGetCurrentDate | HassGetCurrentDate | custom | GEÇTİ | 2 Kasım 2026, Pazartesi. |
| 58 | heldout | bugün hava nasıl olacak | HassGetWeather | - | - | KALDI | niyet=None beklenen=HassGetWeather; hata yanıtı: no_intent_match / Üzgünüm, bunu anlayamadım. |
| 59 | heldout | alışveriş listeme süt ekle | HassShoppingListAddItem | HassShoppingListAddItem | custom | GEÇTİ | süt listeye eklendi. |
| 60 | heldout | yarım saatlik bir sayaç kur | HassStartTimer | HassStartTimer | builtin | KALDI | hata yanıtı: failed_to_handle / Bu cihazda zamanlayıcılar desteklenmiyor. |
