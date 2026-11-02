# Rehber: paketi kendi evine uydurmak

<!-- Made By FALCREB -->

## Cümle nasıl eşleşir?

Home Assistant, Assist'e gelen metni bir sözlük gibi tarayıp kalıplarla karşılaştırır. Yapay zeka kullanmaz, kalıpta olmayan cümleyi tanımaz. Kalıp dili şöyle okunur:

| Yazım | Anlamı | Örnek |
|---|---|---|
| `(a\|b)` | a veya b | `(aç\|yak)` |
| `[a]` | a olabilir de olmayabilir de | `[bütün] ışıkları` |
| `{name}` | Assist'e açık bir cihazın adı | `{name}` -> Avize |
| `{area}` | Bir oda adı | `{area}` -> Salon |
| `<kural>` | Başka yerde tanımlı parça | `<ac_fiil>` |

## Türkçe ekler nasıl çözülüyor?

Bu paket adı ve ekini ayrı parça olarak eşleştirir. `_ortak.yaml` içindeki üç kural bunu yapar:

- `<ek>`: hâl ekleri. Salon-**un**, salon-**da**, salon-**daki**, lamba-**yı**, oda-**nın**, hoparlör-**den**, lamba-**ları**.
- `<iyelik>`: lamba-**sını**, abajur-**unu**, fan-**ını**. Üst projede eksik olan parça budur.
- `<sayi_eki>`: 50**'ye**, 30**'a**, yetmiş**e**.

Sonuçta `{area}[<ek>] {name}[(<ek>|<iyelik>)] <ac_fiil>` kalıbı "salonun avizesini açar mısın" cümlesini tanır.

## Ekle çözülemeyen iki durum

### Ünsüz yumuşaması

"Mutfak" kelimesi "mutfağa, mutfağın" olur. Ek eklemek bu dönüşümü üretemez. Paket bunu `_ortak.yaml` içindeki `tr_yumusak_alan` listesiyle çözer, ama yalnızca "Mutfak" tanımlıdır. Evinizde "Mutfak" adında oda yoksa ya da başka yumuşayan bir odanız varsa listeyi değiştirin. `out` değeri Home Assistant'taki oda adıyla aynı olmalıdır:

```yaml
tr_yumusak_alan:
  values:
    - in: "mutfağ(ı|a|ın)"
      out: "Mutfak"
    - in: "kitaplığ(ı|a|ın)"
      out: "Kitaplık"
```

İkinci satır örnektir, testlerde yalnızca Mutfak denendi.

Cihaz adlarında bu liste yoktur. Adı "Köşe Işık" gibi yumuşayan bir sözcükle biten cihaza takma ad verin ya da adını "Köşe Lambası" gibi yumuşamayan bir biçimde yazın.

### Adında büyük I olan cihazlar

Eşleştirici küçük harfe çevirirken büyük I harfini "i" yapar. Bu yüzden adı **Tavan Işığı** yazılmış bir lamba, "tavan ışığını aç" cümlesini tanımaz. Bu, testte görülmüş gerçek bir sınırdır.

Çözüm: Cihaz ayarlarından küçük harfli bir takma ad (alias) ekleyin: `tavan ışığı`. Testte bu takma adla cümle çalıştı.

Büyük İ ile başlayan adlarda ("İkinci Lamba") testte böyle bir sorun görülmedi. Kendi yazdığınız kalıpta ise `İ` ile başlayan sözcüğü ayrıca yazmanız gerekir, örneğin `(iyi|İyi) geceler`.

## Kendi cümleni eklemek

`custom_sentences/tr/` altına yeni bir dosya açın, paket dosyalarını değiştirmek zorunda kalmazsınız, sonraki sürümde üzerine yazılmaz:
nBu bölümdeki örnek bir şablondur ve test edilmemiştir; kendi sisteminizde deneyin.

```yaml
language: "tr"
intents:
  HassTurnOn:
    data:
      - sentences:
          - "{name}[<ek>] devreye al"
        requires_context:
          domain:
            - light
            - switch
        response: "cihaz"
```

Sonra **Geliştirici Araçları > Eylemler** bölümünden `conversation.reload` çalıştırın. Testte yeniden başlatmadan cümleler yüklendi.

Denemek için **Geliştirici Araçları > Assist** ekranı cümlenin hangi kalıba takıldığını gösterir.

## Birden çok işi tek cümleye bağlamak

Bunun için cümleyle tetiklenen otomasyon kullanılır, örnekler `examples/otomasyonlar.yaml` içinde. `entity_id` değerlerini kendi cihazlarınıza göre değiştirin.

## Güvenlik kuralı

`{name}` içeren bir kalıba her zaman `requires_context.domain` yazın. Yazmazsanız kalıp evdeki her cihaza uygulanır. Kilitlerde `HassTurnOff` kilidi **açar**, yani `{name} kapat` gibi sınırsız bir kalıp kapıyı açabilir.

## Testleri çalıştırmak

Docker ve Python 3 yeterlidir:

```bash
python tests/run_tests.py
```

Betik sahte bir ev kurar, kapsayıcıyı yalnızca `127.0.0.1:18123` üzerinde açar, keşif entegrasyonlarını yüklemez, işi bitince yalnızca kendi kapsayıcısını ve ağını siler. Depoda şifre veya jeton yoktur, test kullanıcısının şifresi her kurulumda rastgele üretilir. Yeni bir cümle eklediğinizde `tests/matrix.yaml` dosyasına da bir satır ekleyin.
