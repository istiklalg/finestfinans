
from io import BytesIO

# Mizan Kalemleri skontlar ile eşleştirilmiş sözlük formatlı data yapısı (başlıklar dahil)
M = {
    "100": "100 Kasa",
    "101": "101 Alınan Çekler",
    "102": "102 Bankalar",
    "103": "103 Verilen Çekler ve Ödeme Emirleri (-)",
    "108": "108 Diğer Hazır Değerler",
    "10": "10 HAZIR DEĞERLER",
    "110": "110 Hisse Senetleri",
    "111": "111 Özel Kesim Tahvil, Senet ve Bonoları",
    "112": "112 Kamu Kesim Tahvil, Senet ve Bonoları",
    "118": "118 Diğer Menkul Kıymetler",
    "119": "119 Menkul Kıymetler Değ. Düş. Karş.(-)",
    "11": "11 MENKUL KIYMETLER",
    "1201": "120-01 Yurtiçi Alacaklar",
    "1202": "120-02 Yurtdışı Alacaklar",
    "1203": "120-03 Alacak Reeskontu(-)",
    "120": "120 ALACAKLAR",
    "121": "121 Alacak Senetleri",
    "122": "122 Alacak Senetleri Reeskontu",
    "126": "126 Verilen Depozito ve teminatlar",
    "127": "127 Diğer Ticari Alacaklar",
    "128": "128 Şüpheli Ticari Alacaklar",
    "129": "129 Şüpheli Ticari Alacak Karşılığı (-)",
    "12": "12 TİCARİ ALACAKLAR (KV)",
    "131": "131 Ortaklardan Alacaklar",
    "132": "132 İştiraklarden Alacaklar",
    "133": "133 Bağlı Ortaklıklardan Alacaklar",
    "135": "135 Personelden Alacaklar",
    "136": "136 Diğer Çeşitli Alacaklar",
    "137": "137 Diğer Alacak Senetleri Reeskontu (-)",
    "138": "138 Şüpheli Diğer Alacaklar",
    "139": "139 Şüpheli Diğer Alacaklar Karşılığı (-)",
    "13": "13 DİĞER ALACAKLAR",
    "150": "150 İlk Madde ve Malzeme",
    "151": "151 Yarı Mamuller Üretim",
    "152": "152 Mamullar",
    "153": "153 Ticari Mallar",
    "157": "157 Diğer Stoklar",
    "158": "158 Stok Değer Düşük Karşılığı",
    "159": "159 Verilen Sipariş Avansları",
    "15": "15 STOKLAR",
    "170": "170 Yıllara Yaygın İnş. ve Onarım Maliyetleri",
    "171": "171 Taşeronlara Verilen Avanslar",
    "178": "178 Yıllara Yaygın İnş. Enf. Düzeltmeleri",
    "17": "17 YILLARA YAYGIN İNŞ.ve ONARIM MALİYETLERİ",
    "180": "180 Gelecek Aylara Ait Giderler",
    "181": "181 Gelir Tahakkukları",
    "18": "18 GELECEK AYLARA AİT GİDER VE GELİR TAAH.",
    "190": "190 Devreden KDV",
    "191": "191 İndirilecek KDV",
    "192": "192 Diğer KDV",
    "193": "193 Peşin Ödenen Vergiler",
    "194": "194 Ertelenen Vergi Varlıkları",
    "195": "195 İş Avansları",
    "196": "196 Personel Avansları",
    "197": "197 Sayım ve Tesellüm Noksanları",
    "198": "198 Diğer Çeşitli Dönen Varlıklar",
    "199": "199 Diğer Dönen Varlıklar Karşılığı",
    "19": "19 DİĞER DÖNEN VARLIKLAR",
    "1": "1 DÖNEN VARLIKLAR",
    "200": "200 Yıllara Yaygın İnş. ve Onarım Maliyetleri",
    "201": "201 Taşeronlara Verilen Avanslar",
    "20": "20 YILLARA YAYGIN İNŞ. VE ONAR. MALİYETLERİ",
    "210": "210 Leasing İle Alınan Sabit Kıymetler",
    "211": "211 Birikmiş Amortismanlar (-)",
    "21": "21 LEASING İLE ALINAN SABİT KIYMETLER",
    "2201": "220-1 UV Ticari Alacaklar",
    "2202": "220-2 Alacak Reeskontu(-)",
    "220": "UZUN VADELİ TİCARİ ALACAKLAR",
    "221": "221 Alacak Senetleri",
    "222": "222 Alacak Senetleri Reeskontu(-)",
    "226": "226 Verilen Depozito ve Teminatlar",
    "228": "228 Şüpheli Alacaklar",
    "229": "229 Şüpheli Alacaklar Karşılığı(-)",
    "22": "22 TİCARİ ALACAKLAR (UV)",
    "231": "231 Ortaklardan Alacaklar",
    "232": "232 İstiraklerden Alacaklar",
    "233": "233 Bağlı Ortaklıklardan Alacaklar",
    "235": "235 Personelden Alacaklar",
    "236": "236 Diğer Çeşitli Alacaklar",
    "237": "237 Diğer Alacak Senetleri Reeskontu(-)",
    "239": "239 Şüpheli Diğer Alacaklar Karşılığı(-)",
    "23": "23 DİĞER ALACAKLAR",
    "240": "240 Bağlı Menkul Kıymetler",
    "241": "241 Bağlı Menkul Kıymet Değ. Düş. Karş.(-)",
    "242": "242 İştirakler",
    "243": "243 İştirak Sermaye Taahhütleri(-)",
    "244": "244 İştirakler Ser. Pay. Değ. Düş. Karş.(-)",
    "245": "245 Bağlı Ortaklıklar",
    "246": "246 Bağlı Ortaklıklara Sermaye Taah.(-)",
    "247": "247 Bağlı Ort. Ser. Pay. Değ. Düş. Karş.(-)",
    "248": "248 Diğer Mali Duran VArlıklar",
    "249": "249 Diğer Mali Duran Varlıklar Karşılığı",
    "24": "24 MALİ DURAN VARLILAR",
    "250": "250 Arazi ve Arsalar",
    "251": "251 Yer Altı ve Yer Üstü Düzenleri",
    "252": "252 Binalar",
    "253": "253 Tesis, Makina ve Cihazlar",
    "254": "254 Taşıtlar",
    "255": "255 Demirbaşlar",
    "256": "256 Diğer Maddi Duran Varlıklar",
    "257": "257 Birikmiş Amortismanlar(-)",
    "258": "258 Yapılmakta Olan Yatırımlar",
    "259": "259 Verilen Avanslar",
    "25": "25 MADDİ DURAN VARLIKLAR",
    "260": "260 Haklar",
    "261": "261 Şerefiye",
    "262": "262 Kuruluş ve Örgütlenme Giderleri",
    "263": "263 Araştırma ve Geliştirme giderleri",
    "264": "264 Özel Maliyetler",
    "267": "267 Diğer Maddi Olmayan Duran Varlıklar",
    "268": "268 Birikmiş Amortismanlar(-)",
    "269": "269 Verilen Avanslar",
    "26": "26 MADDİ OLMAYAN DURAN VARLIKLARI",
    "271": "271 Arama Giderleri",
    "272": "272 Hazırlık ve Geliştirme Giderleri",
    "277": "277 Diğer Özel Tüketime Tabi Varlıklar",
    "278": "278 Birikmiş Tükenme Payları(-)",
    "279": "279 Verilen Avanslar",
    "27": "27 ÖZEL TÜKENMEYE TABİ VARLIKLAR",
    "280": "280 Gelecek Yıllara Ait Giderler",
    "281": "281 Gelir Tahakkukları",
    "28": "GELECEK YILLARA AİT GİDER VE GELİR TAH.",
    "291": "291 Gelecek Yıllarda İndirilecek KDV",
    "292": "292 Diğer KDV",
    "293": "293 Gelecek Yıllar İhtiyacı Stoklar",
    "294": "294 Elden Çıkarılacak Stok ve Maddi Duran Varlıklar",
    "295": "295 Peşin Ödenen Vergi ve Fonlar / Hakediş Stopajları",
    "296": "296 Ertelenen Vergi Varlıkları",
    "297": "297 Diğer Çeşitli Duran Varlıklar",
    "298": "298 Stok Değer Düşüş Karşılığı (-)",
    "299": "299 Birikmiş Amortismanlar",
    "29": "29 DİĞER DURAN VARLIKLAR",
    "2": "2 DURAN VARLIKLAR",
    "01": "AKTİF TOPLAM",

    "300": "300 Bankalara Borçlar KV",
    "301": "301 Finansal Kiralama Borçları",
    "302": "302 Ertelenmiş Fin. Kir. Borç Maliyetleri(-)",
    "303": "303 UV Kredilerin KV Taksitleri",
    "304": "304 Tahvil Anapara Borç, Taksit ve Faiz",
    "305": "305 Çıkarılmış Bono ve Senetler",
    "306": "306 Çıkarılmış Diğer Menkul Kıymetler",
    "308": "308 Menkul Kıymetler İhraç Farkı",
    "309": "309 Diğer Mali Borçlar",
    "30": "30 MALİ BORÇLAR",
    "3201": "320-1 Yurtiçine Boçlar",
    "3202": "320-2 Yurtdışına Borçlar",
    "320": "320 SATICILAR",
    "321": "321 Borç Senetleri",
    "322": "322 Borç Senetleri Reeskontu(-)",
    "326": "326 Alınan Depozito ve Teminatlar",
    "329": "329 Diğer Ticari Borçlar",
    "32": "32 TİCARİ BORÇLAR",
    "331": "331 Ortaklara Borçlar",
    "332": "332 İştiraklere Borçlar",
    "333": "333 Bağlı Ortaklıklara Borçlar",
    "335": "335 Personele Borçlar",
    "336": "336 Diğer Çeşitli Borçlar",
    "337": "337 Diğer Borç Senetleri Reeskontu(-)",
    "338": "338 Dağıtılacak Kar Payları",
    "33": "33 DİĞER BORÇLAR",
    "340": "340 Alınan Sipariş Avansları",
    "349": "349 Alınan Diğer Avanslar",
    "34": "34 ALINAN AVANLAR",
    "350": "350 Yıllara Yaygın İnş. ve Onarım Hakedişleri",
    "351": "351 Taahhüt Avansı",
    "358": "358 Yıllara Yaygın İnş. Enf. Düz. Hesabı",
    "35": "35 YILLARA YAYGIN İNŞAAT VE ONARIM HAKEDİŞLERİ",
    "360": "360 Ödenecek Vergi ve Fonlar",
    "361": "361 Ödenecek Sosyal Güvenli Kesintileri",
    "368": "368 Vadesi Geçmiş Ert. veya Taks. Vergi ve Diğer",
    "369": "369 Ödenecek Diğer Yükümlülükler",
    "36": "36 ÖDENECEK VERGİ VE DİĞER YASAL YÜKÜMLÜLÜKLER",
    "370": "370 Dönem Karı Vergi ve Diğer Yasal Yük. Karş.",
    "371": "371 Peşin Ödenen Vergi ve Fonlar(-)",
    "372": "372 Kıdem Tazminatı Karşılığı",
    "373": "373 Maliyet Giderleri Karşılığı",
    "379": "379 Diğer Borç ve Gider Karşılıkları",
    "37": "37 BORÇ VE GİDER KARŞILIKLARI",
    "380": "380 Gelecek Aylara Ait Gelirler",
    "381": "381 Gider Tahakkukları",
    "38": "38 GELECEK AYLARA AİT GELİR VE GİDER TAH.",
    "391": "391 Hesaplanan KDV",
    "392": "392 Diğer KDV",
    "393": "393 Merkez ve Şubeler Cari Hesabı",
    "394": "394 Ertelenen Vergi Yükümlülükleri",
    "397": "397 Satım ve Tesellüm Fazlaları",
    "399": "399 Diğer Çeşitli YAbancı Kaynaklar",
    "39": "39 DİĞER KISA VADELİ YABANCI KAYNAKLAR",
    "3": "3 KISA VADELİ YABANCI KAYNAKLAR",
    "400": "400 Banka Kredileri",
    "401": "401 Finansal Kiralama Borçları",
    "402": "402 Ertelenmiş Fin. Kir. Borç. Maliyetleri(-)",
    "405": "405 Çıkarılmış Tahviller",
    "407": "407 Çıkarılmış Diğer Menkul Kıymetler",
    "408": "408 Menkul Kıymetler İhraç Farkı(-)",
    "409": "409 Diğer Mali Borçlar",
    "40": "40 MALİ BORÇLAR",
    "410": "410 Yıllara Yaygın İnşaat ve Onarım Hakedişleri",
    "41": "41 YILLARA YAYGIN İNŞAAT VE ONARIM HAKEDİŞLERİ",
    "420": "420 Satıcılar (UV)",
    "421": "421 Borç Senetleri",
    "422": "422 Borç Senetleri Reeskontu(-)",
    "426": "426 Alınan Depozito ve Teminatlar",
    "429": "429 Diğer Ticari Borçlar",
    "42": "42 TİCARİ BORÇLAR (UZUN VADELİ)",
    "431": "431 Ortaklara Borçlar",
    "432": "432 İştiraklere Borçlar",
    "433": "433 Bağlı Ortaklıklara Borçlar",
    "436": "436 Diğer Çeşitli Borçlar",
    "437": "437 Diğer Borç Senetleri Reeskontu(-)",
    "438": "438 Kamuya Olan Ert. Taks. Borçlar",
    "43": "43 DİĞER BORÇLAR",
    "440": "440 Alınan Sipariş Avansları",
    "449": "449 Alınan Diğer Avanslar",
    "44": "44 ALINAN AVANSLAR",
    "472": "472 Kıdem Tazminatı Karşılığı",
    "479": "479 Diğer Borç ve Gider Karşılıkları",
    "47": "47 BORÇ VE GİDER KARŞILIKLARI",
    "480": "480 Gelecek Yıllara Ait Gelirler",
    "481": "481 Gider Tahakkukları",
    "48": "48 GELECEK YILLARA AİT GELİR VE GİDER TAH.",
    "492": "492 Gelecek Yıllara Ertelenen veya Terkin Edilen KDV",
    "493": "493 Tesise Katılma Payları",
    "496": "496 Ertelenen Vergi Yükümlülükleri",
    "499": "499 Diğer Çeşitli UV Yabancı Kaynaklar",
    "49": "49 DİĞER UZUN VADELİ YABANCI KAYNAKLAR",
    "4": "4 UZUN VADELİ YABANCI KAYNAKLAR",
    "500": "500 Sermaye",
    "501": "501 Ödenmemiş Sermaye(-)",
    "502": "502 Sermaye Düzeltmesi Olumlu Farkları",
    "503": "503 Sermaye Düzeltmesi Olumsuz Farkları(-)",
    "50": "50 ÖDENMİŞ SERMAYE",
    "520": "520 Hisse Senetleri İhraç Pirimleri (Emisyon Pirimi)",
    "521": "521 Hisse Senedi İptal Kararları",
    "522": "522 Maddi Duran Varlık Yeniden Değ. Artışları",
    "523": "523 İstirakler Yeniden Değerleme Artışları",
    "525": "525 Kayda Alınan Emtia Karşılığı",
    "526": "526 Borsada Oluşan Değer Artışları",
    "527": "527 Özkaynak Yöntemi Değer Artışları",
    "529": "529 Diğer Sermaye Yedekleri",
    "52": "52 - SERMAYE YEDEKLERİ",
    "540": "540 Yasal Yedekler",
    "541": "541 Statü Yedekleri",
    "542": "542 Olağanüstü Yedekler",
    "543": "543 Maliyet Artış Fonu",
    "548": "548 Diğer Kar Yedekleri",
    "549": "549 Özel Fonlar",
    "54": "54 KAR YEDEKLERİ",
    "551": "551 İndirimler",
    "55": "55 İNDİRİMLER",
    "560": "560 Ana Ortaklık Dışı Özvarlık (Azınlık Payları)",
    "561": "561 Ana Ortaklık Dışı Özvarlık (Azınlık Payları)(-)",
    "562": "562 Çevrim Farkları",
    "563": "563 Çevrim Farkları(-)",
    "56": "56 ANA ORTAKLIK DIŞI VARLIKLAR",
    "570": "570 Geçmiş Yıllar Karları",
    "57": "57 GEÇMİŞ YILLAR KARLARI",
    "580": "580 Geçmiş Yıllar Zararları(-)",
    "58": "58 GEÇMİŞ YILLAR ZARARLARI (-)",
    "590": "590 Dönem Net Karı",
    "591": "591 Dönem Net Zararı",
    "59": "59 DÖNEM NET KARI/ZARARI",
    "5": "5 ÖZKAYNAKLAR",
    "02": "PASİF TOPLAM",

    "600": "600 Yurtiçi Satışlar",
    "601": "601 Yurtdışı Satışlar",
    "602": "602 Diğer Gelirler",
    "603": "603 Yurtiçi Biten İşler Geliri",
    "604": "604 Yurtdışı Biten İşler Geliri",
    "60": "60 BRÜT SATIŞLAR",
    "610": "610 Satıştan İadeler(-)",
    "611": "611 Satış İskontoları(-)",
    "612": "612 Diğer İndirimler",
    "61": "61 SATIŞ İNDİRİMLERİ (-)",
    "03": "NET SATIŞLAR",
    "620": "620 Satılan Mamuller Maliyeti(-)",
    "621": "621 Satılan Ticari Mallar Maliyeti(-)",
    "622": "622 Satılan Hizmet Maliyeti(-)",
    "623": "623 Diğer Satışların Maliyeti",
    "624": "624 Hammadde ve Malzeme Giderleri",
    "625": "625 Dolaysız İşçilik Giderleri",
    "626": "626 Genel Üretim Giderleri",
    "627": "627 Yarı Mamul Giderleri",
    "628": "628 Amortismanlar",
    "62": "62 SATIŞLARIN MALİYETİ(-)",
    "04": "GAYRISAFİ SATIŞ KARI",
    "630": "630 AR-GE Giderleri(-)",
    "631": "631 Pazarlama, Satış, Dağıtım Giderleri(-)",
    "632": "632 Genele Yönetim Giderleri(-)",
    "633": "633 Diğer",
    "634": "634 Amortismanlar",
    "63": "63 FAALİYET GİDERLERİ(-)",
    "05": "FAALİYET KARI",
    "640": "640 İştiraklerden Temettü Gelirleri",
    "641": "641 Bağlı Ortaklıklardan Temettü Gelirleri",
    "642": "642 Faiz Gelirleri",
    "643": "643 Komisyon Gelirleri",
    "644": "644 Konusu Kalmayan Karşılıklar",
    "645": "645 Menkul Kıymet Satış Karları",
    "646": "646 Kambiyo Karları",
    "647": "647 Reeskont Faiz Giderleri",
    "648": "648 Enflasyon Düzeltmesi Karları",
    "649": "649 Diğer Olağan Gelir ve Karlar",
    "64": "64 DİĞER FAALİYETLERDEN OLAĞAN GELİR VE KARLAR",
    "653": "653 Komisyon Giderleri(-)",
    "654": "654 Karşılık Giderleri",
    "655": "655 Menkul Kıymet Satış Zararları(-)",
    "656": "656 Kambiyo Zararları(-)",
    "657": "657 Reeskont Faiz Giderleri(-)",
    "658": "658 Enflasyon Düzeltmesi Zararları(-)",
    "659": "659 Diğer Gider ve Zararlar(-)",
    "65": "65 DİĞER FAALİYETLERDEN OLAĞAN GİDER VE ZARARLAR (-)",
    "660": "660 Kısa Vadeli Borçlanma Giderleri(-)",
    "661": "661 Uzun Vadeli Borçlanma Giderleri(-)",
    "66": "66 FİNANSMAN GİDERLERİ (-)",
    "671": "671 Önceki Dönem Gelir ve Karları",
    "677": "677 Net Parasal Pozisyon Karı",
    "678": "678 Ana Ortaklık Dışı Kar",
    "679": "679 Diğer Olağandışı Gelir ve Karlar",
    "67": "67 OLAĞANDIŞI GELİR VE KARLAR",
    "680": "680 Çalışmayan Kısım Gider ve Zararları(-)",
    "681": "681 Önceki Dönem Gider ve Zararları(-)",
    "687": "687 Net Parasal Pozisyon Zararı(-)",
    "688": "688 Ana Ortaklık Dışı Zarar(-)",
    "689": "689 Diğer Olağandışı Gider ve Zararlar(-)",
    "68": "68 OLAĞANDIŞI GİDER VE ZARARLAR (-)",
    "06": "DÖNEM KARI VEYA ZARARI",
    "690": "691 Dönem Karı Vergi ve Diğer Yas. Yük. Karş.",
    "6": "DÖNEM NET KARI / ZARARI",
}

# Detay görünümde girilen tüm hesapların etiketleri
aktifhesaplar = [
    '100 Kasa',
    '101 Alınan Çekler',
    '102 Bankalar',
    '103 Verilen Çekler ve Ödeme Emirleri (-)',
    '108 Diğer Hazır Değerler',
    '10 HAZIR DEĞERLER',
    '110 Hisse Senetleri',
    '111 Özel Kesim Tahvil, Senet ve Bonoları',
    '112 Kamu Kesim Tahvil, Senet ve Bonoları',
    '118 Diğer Menkul Kıymetler',
    '119 Menkul Kıymetler Değ. Düş. Karş.(-)',
    '11 MENKUL KIYMETLER',
    '120-01 Yurtiçi Alacaklar',
    '120-02 Yurtdışı Alacaklar',
    '120-03 Alacak Reeskontu(-)',
    '120 ALACAKLAR',
    '121 Alacak Senetleri',
    '122 Alacak Senetleri Reeskontu',
    '126 Verilen Depozito ve teminatlar',
    '127 Diğer Ticari Alacaklar',
    '128 Şüpheli Ticari Alacaklar',
    '129 Şüpheli Ticari Alacak Karşılığı (-)',
    '12 TİCARİ ALACAKLAR (KV)',
    '131 Ortaklardan Alacaklar',
    '132 İştiraklarden Alacaklar',
    '133 Bağlı Ortaklıklardan Alacaklar',
    '135 Personelden Alacaklar',
    '136 Diğer Çeşitli Alacaklar',
    '137 Diğer Alacak Senetleri Reeskontu (-)',
    '138 Şüpheli Diğer Alacaklar',
    '139 Şüpheli Diğer Alacaklar Karşılığı (-)',
    '13 DİĞER ALACAKLAR',
    '150 İlk Madde ve Malzeme',
    '151 Yarı Mamuller Üretim',
    '152 Mamullar',
    '153 Ticari Mallar',
    '157 Diğer Stoklar',
    '158 Stok Değer Düşük Karşılığı',
    '159 Verilen Sipariş Avansları',
    '15 STOKLAR',
    '170 Yıllara Yaygın İnş. ve Onarım Maliyetleri',
    '171 Taşeronlara Verilen Avanslar',
    '178 Yıllara Yaygın İnş. Enf. Düzeltmeleri',
    '17 YILLARA YAYGIN İNŞ.ve ONARIM MALİYETLERİ',
    '180 Gelecek Aylara Ait Giderler',
    '181 Gelir Tahakkukları',
    '18 GELECEK AYLARA AİT GİDER VE GELİR TAAH.',
    '190 Devreden KDV',
    '191 İndirilecek KDV',
    '192 Diğer KDV',
    '193 Peşin Ödenen Vergiler',
    '194 Ertelenen Vergi Varlıkları',
    '195 İş Avansları',
    '196 Personel Avansları',
    '197 Sayım ve Tesellüm Noksanları',
    '198 Diğer Çeşitli Dönen Varlıklar',
    '199 Diğer Dönen Varlıklar Karşılığı',
    '19 DİĞER DÖNEN VARLIKLAR',
    '1 DÖNEN VARLIKLAR',
    '200 Yıllara Yaygın İnş. ve Onarım Maliyetleri',
    '201 Taşeronlara Verilen Avanslar',
    '20 YILLARA YAYGIN İNŞ. VE ONAR. MALİYETLERİ',
    '210 Leasing İle Alınan Sabit Kıymetler',
    '211 Birikmiş Amortismanlar (-)',
    '21 LEASING İLE ALINAN SABİT KIYMETLER',
    '220-1 UV Ticari Alacaklar',
    '220-2 Alacak Reeskontu(-)',
    'UZUN VADELİ TİCARİ ALACAKLAR',
    '221 Alacak Senetleri',
    '222 Alacak Senetleri Reeskontu(-)',
    '226 Verilen Depozito ve Teminatlar',
    '228 Şüpheli Alacaklar',
    '229 Şüpheli Alacaklar Karşılığı(-)',
    '22 TİCARİ ALACAKLAR (UV)',
    '231 Ortaklardan Alacaklar',
    '232 İstiraklerden Alacaklar',
    '233 Bağlı Ortaklıklardan Alacaklar',
    '235 Personelden Alacaklar',
    '236 Diğer Çeşitli Alacaklar',
    '237 Diğer Alacak Senetleri Reeskontu(-)',
    '239 Şüpheli Diğer Alacaklar Karşılığı(-)',
    '23 DİĞER ALACAKLAR',
    '240 Bağlı Menkul Kıymetler',
    '241 Bağlı Menkul Kıymet Değ. Düş. Karş.(-)',
    '242 İştirakler',
    '243 İştirak Sermaye Taahhütleri(-)',
    '244 İştirakler Ser. Pay. Değ. Düş. Karş.(-)',
    '245 Bağlı Ortaklıklar',
    '246 Bağlı Ortaklıklara Sermaye Taah.(-)',
    '247 Bağlı Ort. Ser. Pay. Değ. Düş. Karş.(-)',
    '248 Diğer Mali Duran VArlıklar',
    '249 Diğer Mali Duran Varlıklar Karşılığı',
    '24 MALİ DURAN VARLILAR',
    '250 Arazi ve Arsalar',
    '251 Yer Altı ve Yer Üstü Düzenleri',
    '252 Binalar',
    '253 Tesis, Makina ve Cihazlar',
    '254 Taşıtlar',
    '255 Demirbaşlar',
    '256 Diğer Maddi Duran Varlıklar',
    '257 Birikmiş Amortismanlar(-)',
    '258 Yapılmakta Olan Yatırımlar',
    '259 Verilen Avanslar',
    '25 MADDİ DURAN VARLIKLAR',
    '260 Haklar',
    '261 Şerefiye',
    '262 Kuruluş ve Örgütlenme Giderleri',
    '263 Araştırma ve Geliştirme giderleri',
    '264 Özel Maliyetler',
    '267 Diğer Maddi Olmayan Duran Varlıklar',
    '268 Birikmiş Amortismanlar(-)',
    '269 Verilen Avanslar',
    '26 MADDİ OLMAYAN DURAN VARLIKLARI',
    '271 Arama Giderleri',
    '272 Hazırlık ve Geliştirme Giderleri',
    '277 Diğer Özel Tüketime Tabi Varlıklar',
    '278 Birikmiş Tükenme Payları(-)',
    '279 Verilen Avanslar',
    '27 ÖZEL TÜKENMEYE TABİ VARLIKLAR',
    '280 Gelecek Yıllara Ait Giderler',
    '281 Gelir Tahakkukları',
    'GELECEK YILLARA AİT GİDER VE GELİR TAH.',
    '291 Gelecek Yıllarda İndirilecek KDV',
    '292 Diğer KDV',
    '293 Gelecek Yıllar İhtiyacı Stoklar',
    '294 Elden Çıkarılacak Stok ve Maddi Duran Varlıklar',
    '295 Peşin Ödenen Vergi ve Fonlar / Hakediş Stopajları',
    '296 Ertelenen Vergi Varlıkları',
    '297 Diğer Çeşitli Duran Varlıklar',
    '298 Stok Değer Düşüş Karşılığı (-)',
    '299 Birikmiş Amortismanlar',
    '29 DİĞER DURAN VARLIKLAR',
    '2 DURAN VARLIKLAR'
]

pasifhesaplar = [
    '300 Bankalara Borçlar KV',
    '301 Finansal Kiralama Borçları',
    '302 Ertelenmiş Fin. Kir. Borç Maliyetleri(-)',
    '303 UV Kredilerin KV Taksitleri',
    '304 Tahvil Anapara Borç, Taksit ve Faiz',
    '305 Çıkarılmış Bono ve Senetler',
    '306 Çıkarılmış Diğer Menkul Kıymetler',
    '308 Menkul Kıymetler İhraç Farkı',
    '309 Diğer Mali Borçlar',
    '30 MALİ BORÇLAR',
    '320-1 Yurtiçine Boçlar',
    '320-2 Yurtdışına Borçlar',
    '320 SATICILAR',
    '321 Borç Senetleri',
    '322 Borç Senetleri Reeskontu(-)',
    '326 Alınan Depozito ve Teminatlar',
    '329 Diğer Ticari Borçlar',
    '32 TİCARİ BORÇLAR',
    '331 Ortaklara Borçlar',
    '332 İştiraklere Borçlar',
    '333 Bağlı Ortaklıklara Borçlar',
    '335 Personele Borçlar',
    '336 Diğer Çeşitli Borçlar',
    '337 Diğer Borç Senetleri Reeskontu(-)',
    '338 Dağıtılacak Kar Payları',
    '33 DİĞER BORÇLAR',
    '340 Alınan Sipariş Avansları',
    '349 Alınan Diğer Avanslar',
    '34 ALINAN AVANLAR',
    '350 Yıllara Yaygın İnş. ve Onarım Hakedişleri',
    '351 Taahhüt Avansı',
    '358 Yıllara Yaygın İnş. Enf. Düz. Hesabı',
    '35 YILLARA YAYGIN İNŞAAT VE ONARIM HAKEDİŞLERİ',
    '360 Ödenecek Vergi ve Fonlar',
    '361 Ödenecek Sosyal Güvenli Kesintileri',
    '368 Vadesi Geçmiş Ert. veya Taks. Vergi ve Diğer',
    '369 Ödenecek Diğer Yükümlülükler',
    '36 ÖDENECEK VERGİ VE DİĞER YASAL YÜKÜMLÜLÜKLER',
    '370 Dönem Karı Vergi ve Diğer Yasal Yük. Karş.',
    '371 Peşin Ödenen Vergi ve Fonlar(-)',
    '372 Kıdem Tazminatı Karşılığı',
    '373 Maliyet Giderleri Karşılığı',
    '379 Diğer Borç ve Gider Karşılıkları',
    '37 BORÇ VE GİDER KARŞILIKLARI',
    '380 Gelecek Aylara Ait Gelirler',
    '381 Gider Tahakkukları',
    '38 GELECEK AYLARA AİT GELİR VE GİDER TAH.',
    '391 Hesaplanan KDV',
    '392 Diğer KDV',
    '393 Merkez ve Şubeler Cari Hesabı',
    '394 Ertelenen Vergi Yükümlülükleri',
    '397 Satım ve Tesellüm Fazlaları',
    '399 Diğer Çeşitli YAbancı Kaynaklar',
    '39 DİĞER KISA VADELİ YABANCI KAYNAKLAR',
    ' ',
    ' ',
    ' ',
    ' ',
    '3 KISA VADELİ YABANCI KAYNAKLAR',
    '400 Banka Kredileri',
    '401 Finansal Kiralama Borçları',
    '402 Ertelenmiş Fin. Kir. Borç. Maliyetleri(-)',
    '405 Çıkarılmış Tahviller',
    '407 Çıkarılmış Diğer Menkul Kıymetler',
    '408 Menkul Kıymetler İhraç Farkı(-)',
    '409 Diğer Mali Borçlar',
    '40 MALİ BORÇLAR',
    '410 Yıllara Yaygın İnşaat ve Onarım Hakedişleri',
    '41 YILLARA YAYGIN İNŞAAT VE ONARIM HAKEDİŞLERİ',
    '420 Satıcılar (UV)',
    '421 Borç Senetleri',
    '422 Borç Senetleri Reeskontu(-)',
    '426 Alınan Depozito ve Teminatlar',
    '429 Diğer Ticari Borçlar',
    '42 TİCARİ BORÇLAR (UZUN VADELİ)',
    '431 Ortaklara Borçlar',
    '432 İştiraklere Borçlar',
    '433 Bağlı Ortaklıklara Borçlar',
    '436 Diğer Çeşitli Borçlar',
    '437 Diğer Borç Senetleri Reeskontu(-)',
    '438 Kamuya Olan Ert. Taks. Borçlar',
    '43 DİĞER BORÇLAR',
    '440 Alınan Sipariş Avansları',
    '449 Alınan Diğer Avanslar',
    '44 ALINAN AVANSLAR',
    '472 Kıdem Tazminatı Karşılığı',
    '479 Diğer Borç ve Gider Karşılıkları',
    '47 BORÇ VE GİDER KARŞILIKLARI',
    '480 Gelecek Yıllara Ait Gelirler',
    '481 Gider Tahakkukları',
    '48 GELECEK YILLARA AİT GELİR VE GİDER TAH.',
    '492 Gelecek Yıllara Ertelenen veya Terkin Edilen KDV',
    '493 Tesise Katılma Payları',
    '496 Ertelenen Vergi Yükümlülükleri',
    '499 Diğer Çeşitli UV Yabancı Kaynaklar',
    '49 DİĞER UZUN VADELİ YABANCI KAYNAKLAR',
    '4 UZUN VADELİ YABANCI KAYNAKLAR',
    '500 Sermaye',
    '501 Ödenmemiş Sermaye(-)',
    '502 Sermaye Düzeltmesi Olumlu Farkları',
    '503 Sermaye Düzeltmesi Olumsuz Farkları(-)',
    '50 ÖDENMİŞ SERMAYE',
    '520 Hisse Senetleri İhraç Pirimleri (Emisyon Pirimi)',
    '521 Hisse Senedi İptal Kararları',
    '522 Maddi Duran Varlık Yeniden Değ. Artışları',
    '523 İstirakler Yeniden Değerleme Artışları',
    '525 Kayda Alınan Emtia Karşılığı',
    '526 Borsada Oluşan Değer Artışları',
    '527 Özkaynak Yöntemi Değer Artışları',
    '529 Diğer Sermaye Yedekleri',
    '52 - SERMAYE YEDEKLERİ',
    '540 Yasal Yedekler',
    '541 Statü Yedekleri',
    '542 Olağanüstü Yedekler',
    '543 Maliyet Artış Fonu',
    '548 Diğer Kar Yedekleri',
    '549 Özel Fonlar',
    '54 KAR YEDEKLERİ',
    '551 İndirimler',
    '55 İNDİRİMLER',
    '560 Ana Ortaklık Dışı Özvarlık (Azınlık Payları)',
    '561 Ana Ortaklık Dışı Özvarlık (Azınlık Payları)(-)',
    '562 Çevrim Farkları',
    '563 Çevrim Farkları(-)',
    '56 ANA ORTAKLIK DIŞI VARLIKLAR',
    '570 Geçmiş Yıllar Karları',
    '57 GEÇMİŞ YILLAR KARLARI',
    '580 Geçmiş Yıllar Zararları(-)',
    '58 GEÇMİŞ YILLAR ZARARLARI (-)',
    '590 Dönem Net Karı',
    '591 Dönem Net Zararı',
    '59 DÖNEM NET KARI/ZARARI',
    '5 ÖZKAYNAKLAR'
]

gelirtablosu = [
    '600 Yurtiçi Satışlar',
    '601 Yurtdışı Satışlar',
    '602 Diğer Gelirler',
    '603 Yurtiçi Biten İşler Geliri',
    '604 Yurtdışı Biten İşler Geliri',
    '60 BRÜT SATIŞLAR',
    ' ',
    '610 Satıştan İadeler(-)',
    '611 Satış İskontoları(-)',
    '612 Diğer İndirimler',
    '61 SATIŞ İNDİRİMLERİ (-)',
    'NET SATIŞLAR',
    ' ',
    '620 Satılan Mamuller Maliyeti(-)',
    '621 Satılan Ticari Mallar Maliyeti(-)',
    '622 Satılan Hizmet Maliyeti(-)',
    '623 Diğer Satışların Maliyeti',
    '624 Hammadde ve Malzeme Giderleri',
    '625 Dolaysız İşçilik Giderleri',
    '626 Genel Üretim Giderleri',
    '627 Yarı Mamul Giderleri',
    '628 Amortismanlar',
    '62 SATIŞLARIN MALİYETİ(-)',
    'GAYRISAFİ SATIŞ KARI',
    ' ',
    '630 AR-GE Giderleri(-)',
    '631 Pazarlama, Satış, Dağıtım Giderleri(-)',
    '632 Genele Yönetim Giderleri(-)',
    '633 Diğer',
    '634 Amortismanlar',
    '63 FAALİYET GİDERLERİ(-)',
    'FAALİYET KARI',
    ' ',
    '640 İştiraklerden Temettü Gelirleri',
    '641 Bağlı Ortaklıklardan Temettü Gelirleri',
    '642 Faiz Gelirleri',
    '643 Komisyon Gelirleri',
    '644 Konusu Kalmayan Karşılıklar',
    '645 Menkul Kıymet Satış Karları',
    '646 Kambiyo Karları',
    '647 Reeskont Faiz Giderleri',
    '648 Enflasyon Düzeltmesi Karları',
    '649 Diğer Olağan Gelir ve Karlar',
    '64 DİĞER FAALİYETLERDEN OLAĞAN GELİR VE KARLAR',
    ' ',
    '653 Komisyon Giderleri(-)',
    '654 Karşılık Giderleri',
    '655 Menkul Kıymet Satış Zararları(-)',
    '656 Kambiyo Zararları(-)',
    '657 Reeskont Faiz Giderleri(-)',
    '658 Enflasyon Düzeltmesi Zararları(-)',
    '659 Diğer Gider ve Zararlar(-)',
    '65 DİĞER FAALİYETLERDEN OLAĞAN GİDER VE ZARARLAR (-)',
    ' ',
    '660 Kısa Vadeli Borçlanma Giderleri(-)',
    '661 Uzun Vadeli Borçlanma Giderleri(-)',
    '66 FİNANSMAN GİDERLERİ (-)',
    ' ',
    '671 Önceki Dönem Gelir ve Karları',
    '677 Net Parasal Pozisyon Karı',
    '678 Ana Ortaklık Dışı Kar',
    '679 Diğer Olağandışı Gelir ve Karlar',
    '67 OLAĞANDIŞI GELİR VE KARLAR',
    '680 Çalışmayan Kısım Gider ve Zararları(-)',
    '681 Önceki Dönem Gider ve Zararları(-)',
    '687 Net Parasal Pozisyon Zararı(-)',
    '688 Ana Ortaklık Dışı Zarar(-)',
    '689 Diğer Olağandışı Gider ve Zararlar(-)',
    '68 OLAĞANDIŞI GİDER VE ZARARLAR (-)',
    'DÖNEM KARI VEYA ZARARI',
    ' ',
    '691 Dönem Karı Vergi ve Diğer Yas. Yük. Karş.',
    ' ',
    ' ',
    'DÖNEM NET KARI / ZARARI',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    'TEMEL VERİMLİLİK GÖSTERGELERİ',
    ' ',
    'KASA / HAZIR DEĞERLER',
    'KASA/DÖNEN VARLIKLAR',
    'STOKLAR/DÖNEN VARLIKLAR',
    ' ',
    ' ',
    'ORTAKLARDAN ALACAKLAR(kv) / DÖNEN VARLIKLAR',
    'ORTAKLARDAN ALACAKLAR(uv)/DURAN VARLIKLAR',
    'ORTAKLARDAN ALACAKLAR/AKTİF TOPLAM',
    'ORTAKLARDAN ALACAKLAR/ÖDENMİŞ SERMAYE',
    'ORTAKLARDAN ALACAKLAR/ÖZKAYNAKLAR',
    ' ',
    ' ',
    'ORTAKLARA BORÇLAR(kv)/KISA VADELİ YABANCI KAYNAKLAR',
    'ORTAKLARA BORÇLAR(uv)/UZUN VADELİ YABANCI KAYNAKLAR',
    'ORTAKLARA BORÇLAR/PASİF TOPLAM',
    ' ',
    ' ',
    'ŞÜPHELİ TİCARİ ALACAKLAR/TİCARİ ALACAKLAR',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    'DÖNEM NET KARI / ZARARI',
    ' '
]

# Oran analizlerine ilişkin sözlük formatlı data yapısı (başlıklar dahil)
Oran = {
    'tg': 'TEMEL VERİMLİLİK GÖSTERGELERİ (%)',
    'tg1': 'KASA / HAZIR DEĞERLER',
    'tg2': 'KASA/DÖNEN VARLIKLAR',
    'tg3': 'STOKLAR/DÖNEN VARLIKLAR',
    'tg4': 'ORTAKLARDAN ALACAKLAR(kv) / DÖNEN VARLIKLAR',
    'tg5': 'ORTAKLARDAN ALACAKLAR(uv)/DURAN VARLIKLAR',
    'tg6': 'ORTAKLARDAN ALACAKLAR/AKTİF TOPLAM',
    'tg7': 'ORTAKLARDAN ALACAKLAR/ÖDENMİŞ SERMAYE',
    'tg8': 'ORTAKLARDAN ALACAKLAR/ÖZKAYNAKLAR',
    'tg9': 'ORTAKLARA BORÇLAR(kv)/KISA VADELİ YABANCI KAYNAKLAR',
    'tg10': 'ORTAKLARA BORÇLAR(uv)/UZUN VADELİ YABANCI KAYNAKLAR',
    'tg11': 'ORTAKLARA BORÇLAR/PASİF TOPLAM',
    'tg12': 'ŞÜPHELİ TİCARİ ALACAKLAR/TİCARİ ALACAKLAR',
    # ----
    'fg': 'FİNANSAL GÖSTERGELER',
    'fg1': 'CARİ ORAN',  # 2 nin üzerinde olması istenen seviyedir.
    'fg2': 'LİKİDİTE ORANI',  # 1 den büyük olması beklenir.
    'fg3': 'NAKİT (DİSPONİBİLİTE )ORANI',  # 1 den büyük olması beklenir.
    'fg4': 'BORÇLAR TOPLAMI/MADDİ ÖZVARLIK (%)',
    'fg5': 'KALDIRAÇ ORANI (%)',  # %50 den küçük olması istenir, üzeri riskli durumları işaret edebilir.
    'fg6': 'BORÇLAR TOPLAMI / CİRO (%)',
    'fg7': 'ÖZKAYNAK ORANI (%)',
    'fg8': 'OTO FİNANSMAN ORANI (%)',
    # ----
    'ag': 'AKTİVİTE GÖSTERGELERİ',
    'ag1': 'ALACAK DEVİR HIZI (Kez)',
    'ag2': 'ALACAKLARIN TAHSİL SÜRESİ (Gün)',
    'ag3': 'STOK DEVİR HIZI (Kez)',
    'ag4': 'STOKTA KALMA SÜRESİ (Gün)',
    'ag5': 'AKTİF DEVİR HIZI (Kez)',
    # ----
    'kg': 'KARLILIK GÖSTERGELERİ',
    'kg1': 'BİLANÇO KARI/NET SATIŞLAR (%)',
    'kg2': 'NET KAR/MADDİ ÖZVARLIK (%)',
    'kg3': 'FİNANSMAN GİDERLERİ/G.SAFİ SATIŞ KARI (%)',
    'kg4': 'EBITDA',
    'kg5': 'TOPLAM VARLIKLARIN KARLILIĞI (du-pont analizi) (%)',
    'kg6': 'ÖZ SERMAYE KARLILIĞI (du-pont analizi) (%)',
    'kg7': 'NET KAR MARJI (%)',
    'kg8': 'MALİ RANTABİLİTE ORANI (%)',
    'kg9': 'EKONOMİK RANTABİLİTE (%)',
    # ----
    'mg': 'MALİYET GÖSTERGELERİ',
    'mg1': 'MALİYET/GELİR ORANI(COST/INCOME)(%)',
    # ----
    'nis': 'NET İŞLETME SERMAYESİ',
}

# Spread tablosu için kalemler ve değişkenler ile uyumlu sözlük yapısı;
Spread = {
    '110': 'Kasa ve Bankalar',
    '111': 'Paraya Ç. Menkul Kıymet',
    '112': 'Yurt İçi Alacaklar',
    '113': 'Yurt Dışı Alacaklar',
    '114': 'Senetli Alacaklar',
    '115': 'Ortaklardan Alacaklar',
    '116': 'İşt.ve Bağlı ortaklık.Al.',
    '117': 'Diğer Alacaklar',
    '11': 'LİKİT VARLIK TOPLAMI',
    '150': 'İlk Madde ve Malzeme',
    '151': 'Yarı Mamul, Mamul',
    '152': 'Emtia / Diğer',
    '159': 'Akreditif/Sipariş Avansları',
    '15': 'STOK ve AVANSLAR TOPLAMI',
    '1': 'DÖNEN VARLIK TOPLAMI',
    '210': 'İştirakler ve Bağlı Ortaklıklar(Net)',
    '211': 'Alacak Senetleri',
    '212': 'Uzun Vadeli Alacaklar',
    '213': 'Depozito ve Teminatlar',
    '214': 'Ortaklardan Alacaklar',
    '215': 'İşt. ve Bağlı Ort. Alacak',
    '216': 'Taahhüt Harcamaları',
    '217': 'Diğer Bağlı Varlıklar',
    '218': 'Yapılmakta Olan Yatırımlar',
    '219': 'Sipariş Avansları',
    '220': 'BAĞLI VARLIK TOPLAMI',
    '221': 'Arsa ve Binalar',
    '222': 'Makine ve Tesisler',
    '223': 'Demirbaş/Taşıt/Diğer Sabit Kıymetler',
    '224': 'Leasingle Alınan Sabit Kıymetler',
    '20': 'MADDİ DURAN VAR. TOP.',
    '225': 'Birikmiş Amortismanlar (-)',
    '21': 'NET MADDİ DURAN VAR.',
    '226': 'Net Maddi olmayan Duran Varlıklar',
    '2': 'SABİT VARLIK TOPLAMI',
    '01': 'AKTİF TOPLAMI',  # Aktif hesaplar bitti

    '300': 'Bankalara Borçlar',
    '301': 'U.V.B. A.para Taksit ve Faiz',
    '302': 'İthalat Borçları',
    '303': 'Senetsiz Borçlar',
    '304': 'Senetli Borçlar',
    '312': 'Sipariş Avansları',
    '305': 'Ortaklara Borçlar',
    '306': 'Dağıtılacak Kar Payları',
    '307': 'İşt.ve Bağlı ortaklık.Borçlar',
    '308': 'K.V. Leasing Borçları',
    '309': 'Borç ve Gider Karşılıkları',
    '310': 'Ödenecek Vergiler',
    '311': 'Diğer Borçlar',
    '3': 'KISA VADELİ BORÇLAR',
    '400': 'Uzun Vadeli Banka Borçları',
    '401': 'Tahvil/Menkul Kıymet/Finans. Bonoları',
    '402': 'Borç Senetleri',
    '403': 'Ortaklara Borçlar',
    '404': 'İştirak ve Bağlı Ort. Borçlar',
    '405': 'Diğer Uzun Vadeli Borçlar',
    '406': 'Alınan Hakedişler',
    '407': 'Uzun Vadeli Leasing Borçları',
    '408': 'Kıdem Tazminatı Karşılığı',
    '4': 'UZUN VADELİ BORÇLAR',
    '34': 'BORÇLAR TOPLAMI',
    '500': 'Sermaye',
    '501': 'Ödenmiş Sermaye',
    '502': 'Sermaye Düzeltme Farkları',
    '503': 'Kar Yedekleri',
    '504': 'Yeniden Değerleme Fonu',
    '505': 'Diğer Sermaye Yed. ve Emisyon Primi',
    '506': 'Geçmiş Yıl Karları',
    '507': 'Dönem Net Karı / Zararı',
    '508': 'İndirimler (-)',
    '5': 'ÖZVARLIK TOPLAMI',
    '02': 'PASİF TOPLAMI',  # Pasif Hesaplar bitti

    '600': 'Yurtiçi Satışlar',
    '601': 'Yurtdışı Satışlar',
    '602': 'Diğer(Kur,Vade Farkları,İhracat Pr.)',
    '60': 'BRÜT SATIŞLAR',
    '610': 'Satıştan İadeler (-)',
    '611': 'Satış İskontoları (-)',
    '612': 'Diğer İndirimler(-)',
    '61': 'SATIŞTAN İNDİRİMLER (-)',
    '03': 'NET SATIŞLAR',
    '620': 'Satılan Mamuller Maliyeti (-)',
    '621': 'Satılan Emtia Maliyeti (-)',
    '622': 'Satılan Hizmet Maliyeti (-)',
    '623': 'Diğer Satışların Maliyeti (-)',
    '628': 'Amortismanlar (-)',
    '62': 'SATIŞLARIN MALİYETİ (-)',
    '04': 'BRÜT SATIŞ KARI/ZARARI',
    '630': 'Ar-Ge Giderleri',
    '631': 'Paz-Satış, Dağıtım Giderleri',
    '632': 'Genel Yönetim Giderleri',
    '634': 'Amortismanlar',
    '63': 'FAALİYET GİDERLERİ (-)',
    '66': 'FİNANSMAN GİDERLERİ (-)',
    '05': 'FAALİYET KARI / ZARARI',
    '64': 'DİĞER GELİRLER (+)',
    '65': 'DİĞER GİDERLER (-)',
    '06': 'BİLANÇO KARI/ZARARI',
    '690': 'Ödenecek Vergi ve Fonlar (-)',
    '6': 'NET DÖNEM KARI / ZARARI',  # Gelir Tablosu bitti

}

# Temel tablo görünümü için Gelir Tablosu etiket listesi;
gelirtabbase = [
    "600 Yurtiçi Satışlar",
    "601 Yurtdışı Satışlar",
    "602 Diğer Gelirler",
    "603 Yurtiçi Biten İşler Geliri",
    "604 Yurtdışı Biten İşler Geliri",
    "60 BRÜT SATIŞLAR",
    "610 Satıştan İadeler(-)",
    "611 Satış İskontoları(-)",
    "612 Diğer İndirimler",
    "61 SATIŞ İNDİRİMLERİ (-)",
    "NET SATIŞLAR",
    "620 Satılan Mamuller Maliyeti(-)",
    "621 Satılan Ticari Mallar Maliyeti(-)",
    "622 Satılan Hizmet Maliyeti(-)",
    "623 Diğer Satışların Maliyeti",
    "624 Hammadde ve Malzeme Giderleri",
    "625 Dolaysız İşçilik Giderleri",
    "626 Genel Üretim Giderleri",
    "627 Yarı Mamul Giderleri",
    "628 Amortismanlar",
    "62 SATIŞLARIN MALİYETİ(-)",
    "GAYRISAFİ SATIŞ KARI",
    "630 AR-GE Giderleri(-)",
    "631 Pazarlama, Satış, Dağıtım Giderleri(-)",
    "632 Genele Yönetim Giderleri(-)",
    "633 Diğer",
    "634 Amortismanlar",
    "63 FAALİYET GİDERLERİ(-)",
    "FAALİYET KARI",
    "640 İştiraklerden Temettü Gelirleri",
    "641 Bağlı Ortaklıklardan Temettü Gelirleri",
    "642 Faiz Gelirleri",
    "643 Komisyon Gelirleri",
    "644 Konusu Kalmayan Karşılıklar",
    "645 Menkul Kıymet Satış Karları",
    "646 Kambiyo Karları",
    "647 Reeskont Faiz Giderleri",
    "648 Enflasyon Düzeltmesi Karları",
    "649 Diğer Olağan Gelir ve Karlar",
    "64 DİĞER FAALİYETLERDEN OLAĞAN GELİR VE KARLAR",
    "653 Komisyon Giderleri(-)",
    "654 Karşılık Giderleri",
    "655 Menkul Kıymet Satış Zararları(-)",
    "656 Kambiyo Zararları(-)",
    "657 Reeskont Faiz Giderleri(-)",
    "658 Enflasyon Düzeltmesi Zararları(-)",
    "659 Diğer Gider ve Zararlar(-)",
    "65 DİĞER FAALİYETLERDEN OLAĞAN GİDER VE ZARARLAR (-)",
    "660 Kısa Vadeli Borçlanma Giderleri(-)",
    "661 Uzun Vadeli Borçlanma Giderleri(-)",
    "66 FİNANSMAN GİDERLERİ (-)",
    "671 Önceki Dönem Gelir ve Karları",
    "677 Net Parasal Pozisyon Karı",
    "678 Ana Ortaklık Dışı Kar",
    "679 Diğer Olağandışı Gelir ve Karlar",
    "67 OLAĞANDIŞI GELİR VE KARLAR",
    "680 Çalışmayan Kısım Gider ve Zararları(-)",
    "681 Önceki Dönem Gider ve Zararları(-)",
    "687 Net Parasal Pozisyon Zararı(-)",
    "688 Ana Ortaklık Dışı Zarar(-)",
    "689 Diğer Olağandışı Gider ve Zararlar(-)",
    "68 OLAĞANDIŞI GİDER VE ZARARLAR (-)",
    "06 DÖNEM KARI VEYA ZARARI",
    "691 Dönem Karı Vergi ve Diğer Yas. Yük. Karş."
]

# Spread için gelir tablosu etiket listesi
gelir = [
    'Yurtiçi Satışlar',
    'Yurtdışı Satışlar',
    'Diğer(Kur,Vade Farkları,İhracat Pr.)',
    'BRÜT SATIŞLAR',
    'Satıştan İadeler (-)',
    'Satış İskontoları (-)',
    'Diğer İndirimler(-)',
    'SATIŞTAN İNDİRİMLER (-)',
    'NET SATIŞLAR',
    'Satılan Mamuller Maliyeti (-)',
    'Satılan Emtia Maliyeti (-)',
    'Satılan Hizmet Maliyeti (-)',
    'Diğer Satışların Maliyeti (-)',
    'Amortismanlar (-)',
    'SATIŞLARIN MALİYETİ (-)',
    'BRÜT SATIŞ KARI/ZARARI',
    'Ar-Ge Giderleri',
    'Paz-Satış, Dağıtım Giderleri',
    'Genel Yönetim Giderleri',
    'Amortismanlar',
    'FAALİYET GİDERLERİ (-)',
    'FİNANSMAN GİDERLERİ (-)',
    'FAALİYET KARI / ZARARI',
    'DİĞER GELİRLER (+)',
    'DİĞER GİDERLER (-)',
    'BİLANÇO KARI/ZARARI',
    'Ödenecek Vergi ve Fonlar (-)',
    'NET DÖNEM KARI / ZARARI',
]

# aktifler etiket listesi
aktifler = [
    'Kasa ve Bankalar',
    'Paraya Ç. Menkul Kıymet',
    'Yurt İçi Alacaklar',
    'Yurt Dışı Alacaklar',
    'Senetli Alacaklar',
    'Ortaklardan Alacaklar',
    'İşt.ve Bağlı ortaklık.Al.',
    'Diğer Alacaklar',
    'LİKİT VARLIK TOPLAMI',
    'İlk Madde ve Malzeme',
    'Yarı Mamul, Mamul',
    'Emtia / Diğer',
    'Akreditif/Sipariş Avansları',
    'STOK ve AVANSLAR TOPLAMI',
    'DÖNEN VARLIK TOPLAMI',
    'İştirakler ve Bağlı Ortaklıklar(Net)',
    'Alacak Senetleri',
    'Uzun Vadeli Alacaklar',
    'Depozito ve Teminatlar',
    'Ortaklardan Alacaklar',
    'İşt. ve Bağlı Ort. Alacak',
    'Taahhüt Harcamaları',
    'Diğer Bağlı Varlıklar',
    'Yapılmakta Olan Yatırımlar',
    'Sipariş Avansları',
    'BAĞLI VARLIK TOPLAMI',
    'Arsa ve Binalar',
    'Makine ve Tesisler',
    'Demirbaş/Taşıt/Diğer Sabit Kıymetler',
    'Leasingle Alınan Sabit Kıymetler',
    'MADDİ DURAN VAR. TOP.',
    'Birikmiş Amortismanlar (-)',
    'NET MADDİ DURAN VAR.',
    'Net Maddi olmayan Duran Varlıklar',
    'SABİT VARLIK TOPLAMI',
    'AKTİF TOPLAMI',
]

# pasifler etiket listesi
pasifler = [
    'Bankalara Borçlar',
    'U.V.B. A.para Taksit ve Faiz',
    'İthalat Borçları',
    'Senetsiz Borçlar',
    'Senetli Borçlar',
    'Sipariş Avansları',
    'Ortaklara Borçlar',
    'Dağıtılacak Kar Payları',
    'İşt.ve Bağlı ortaklık.Borçlar',
    'K.V. Leasing Borçları',
    'Borç ve Gider Karşılıkları',
    'Ödenecek Vergiler',
    'Diğer Borçlar',
    'KISA VADELİ BORÇLAR',
    'Uzun Vadeli Banka Borçları',
    'Tahvil/Menkul Kıymet/Finans. Bonoları',
    'Borç Senetleri',
    'Ortaklara Borçlar',
    'İştirak ve Bağlı Ort. Borçlar',
    'Diğer Uzun Vadeli Borçlar',
    'Alınan Hakedişler',
    'Uzun Vadeli Leasing Borçları',
    'Kıdem Tazminatı Karşılığı',
    'UZUN VADELİ BORÇLAR',
    'BORÇLAR TOPLAMI',
    'Sermaye',
    'Ödenmiş Sermaye',
    'Sermaye Düzeltme Farkları',
    'Kar Yedekleri',
    'Yeniden Değerleme Fonu',
    'Diğer Sermaye Yed. ve Emisyon Primi',
    'Geçmiş Yıl Karları',
    'Dönem Net Karı / Zararı',
    'İndirimler (-)',
    'ÖZVARLIK TOPLAMI',
    'PASİF TOPLAMI',
]

# temel göstergeler etiket listesi;
temel = [
    'TEMEL VERİMLİLİK GÖSTERGELERİ',
    'KASA / HAZIR DEĞERLER',
    'KASA/DÖNEN VARLIKLAR',
    'STOKLAR/DÖNEN VARLIKLAR',
    'ORTAKLARDAN ALACAKLAR(kv) / DÖNEN VARLIKLAR',
    'ORTAKLARDAN ALACAKLAR(uv)/DURAN VARLIKLAR',
    'ORTAKLARDAN ALACAKLAR/AKTİF TOPLAM',
    'ORTAKLARDAN ALACAKLAR/ÖDENMİŞ SERMAYE',
    'ORTAKLARDAN ALACAKLAR/ÖZKAYNAKLAR',
    'ORTAKLARA BORÇLAR(kv)/KISA VADELİ YABANCI KAYNAKLAR',
    'ORTAKLARA BORÇLAR(uv)/UZUN VADELİ YABANCI KAYNAKLAR',
    'ORTAKLARA BORÇLAR/PASİF TOPLAM',
    'ŞÜPHELİ TİCARİ ALACAKLAR/TİCARİ ALACAKLAR',
]

# finansal göstergeler etiket listesi;
finansal = [
    'CARİ ORAN',  # 2 nin üzerinde olması istenen seviyedir.
    'LİKİDİTE ORANI',  # 1 den büyük olması beklenir.
    'NAKİT (DİSPONİBİLİTE )ORANI',  # 1 den büyük olması beklenir.
    'BORÇLAR TOPLAMI/MADDİ ÖZVARLIK (%)',
    'KALDIRAÇ ORANI (%)',  # %50 den küçük olması istenir, üzeri riskli durumları işaret edebilir.
    'BORÇLAR TOPLAMI / CİRO (%)',
    'ÖZKAYNAK ORANI (%)',
    'OTO FİNANSMAN ORANI (%)',
]

# Aktivite göstergeleri için etiket listesi;
aktivite = [
    'ALACAK DEVİR HIZI (Kez)',
    'ALACAKLARIN TAHSİL SÜRESİ (Gün)',
    'STOK DEVİR HIZI (Kez)',
    'STOKTA KALMA SÜRESİ (Gün)',
    'AKTİF DEVİR HIZI (Kez)',
]

# Karlılık göstergeleri için etiket listesi;
karlilik = [
    'BİLANÇO KARI/NET SATIŞLAR (%)',
    'NET KAR/MADDİ ÖZVARLIK (%)',
    'FİNANSMAN GİDERLERİ/G.SAFİ SATIŞ KARI (%)',
    'EBITDA',
    'TOPLAM VARLIKLARIN KARLILIĞI (du-pont analizi) (%)',
    'ÖZ SERMAYE KARLILIĞI (du-pont analizi) (%)',
    'NET KAR MARJI (%)',
    'MALİ RANTABİLİTE ORANI (%)',
    'EKONOMİK RANTABİLİTE (%)',
]


def detayhesaplama(budget):
    # Yapılması gereken temel toplamlar
    # Aktif Hesaplamaları
    L10 = (budget.L100 + budget.L101 + budget.L102 - budget.L103 + budget.L108)
    L11 = (budget.L110 + budget.L111 + budget.L112 + budget.L118 - budget.L119)
    L12 = (budget.L1201 + budget.L1202 + budget.L121 - budget.L122 + budget.L126 + budget.L127 + budget.L128
           - budget.L129)
    L120 = (budget.L1201 + budget.L1202)
    L13 = (budget.L131 + budget.L132 + budget.L133 + budget.L135 + budget.L136 - budget.L137 + budget.L138
           - budget.L139)
    L15 = (budget.L150 + budget.L151 + budget.L152 + budget.L153 + budget.L157 - budget.L158 + budget.L159)
    L17 = (budget.L170 + budget.L171 + budget.L178)
    L18 = (budget.L180 + budget.L181)
    L19 = (budget.L190 + budget.L191 + budget.L192 + budget.L193 + budget.L194 + budget.L195 + budget.L196
           + budget.L197 + budget.L198 - budget.L199)
    L1 = (L10 + L11 + L12 + L13 + L15 + L17 + L18 + L19)  # Dönen Varlıklar
    L20 = (budget.L200 + budget.L201)
    L21 = (budget.L210 - budget.L211)
    L22 = (budget.L2201 - budget.L2202 + budget.L221 - budget.L222 + budget.L226 + budget.L228 - budget.L229)
    L220 = (budget.L2201 - budget.L2202)
    L23 = (budget.L231 + budget.L232 + budget.L233 + budget.L235 + budget.L236
           - budget.L237 - budget.L239)
    L24 = (budget.L240 - budget.L241 + budget.L242 - budget.L243 - budget.L244
           + budget.L245 - budget.L246 - budget.L247 + budget.L248 - budget.L249)
    L25 = (budget.L250 + budget.L251 + budget.L252 + budget.L253 + budget.L254
           + budget.L255 + budget.L256 - budget.L257 + budget.L258 + budget.L259)
    L26 = (budget.L260 + budget.L261 + budget.L262 + budget.L263 + budget.L264
           + budget.L267 - budget.L268 + budget.L269)
    L27 = (budget.L271 + budget.L272 + budget.L277 - budget.L278 + budget.L279)
    L28 = (budget.L280 + budget.L281)
    L29 = (budget.L291 + budget.L292 + budget.L293 + budget.L294 + budget.L295 + budget.L296
           + budget.L297 - budget.L298 - budget.L299)
    L2 = (L20 + L21 + L22 + L23 + L24 + L25 + L26 + L27 + L28 + L29)  # Duran Varlıklar
    L01 = (L1 + L2)  # Aktif Toplam
    # print(type(L01))

    # Pasif Hesaplamaları
    L30 = (budget.L300 + budget.L301 - budget.L302 + budget.L303 + budget.L304 + budget.L305
           + budget.L306 - budget.L308 + budget.L309)
    L320 = (budget.L3201 + budget.L3202)
    L32 = (budget.L3201 + budget.L3202 + budget.L321 - budget.L322 + budget.L326 + budget.L329)
    L33 = (budget.L331 + budget.L332 + budget.L333 + budget.L335 + budget.L336 - budget.L337 + budget.L338)
    L34 = (budget.L340 + budget.L349)
    L35 = (budget.L350 + budget.L351 + budget.L358)
    L36 = (budget.L360 + budget.L361 + budget.L368 + budget.L369)
    L37 = (budget.L370 - budget.L371 + budget.L372 + budget.L373 + budget.L379)
    L38 = (budget.L380 + budget.L381)
    L39 = (budget.L391 + budget.L392 + budget.L393 + budget.L394 + budget.L397 + budget.L399)
    L3 = (L30 + L32 + L33 + L34 + L35 + L36 + L37 + L38 + L39)  # Kısa Vadeli Yabancı Kaynaklar
    L40 = (budget.L400 + budget.L401 - budget.L402 + budget.L405 + budget.L407 - budget.L408 + budget.L409)
    L41 = budget.L410
    L42 = (budget.L420 + budget.L421 - budget.L422 + budget.L426 + budget.L429)
    L43 = (budget.L431 + budget.L432 + budget.L433 + budget.L436 - budget.L437 + budget.L438)
    L44 = (budget.L440 + budget.L449)
    L47 = (budget.L472 + budget.L479)
    L48 = (budget.L480 + budget.L481)
    L49 = (budget.L492 + budget.L493 + budget.L496 + budget.L499)
    L4 = (L40 + L41 + L42 + L43 + L44 + L47 + L48 + L49)  # Uzun Vadeli Yabancı Kaynaklar
    L50 = (budget.L500 - budget.L501 + budget.L502 - budget.L503)
    L52 = (budget.L520 + budget.L521 + budget.L522 + budget.L523 + budget.L525 + budget.L526
           + budget.L527 + budget.L529)
    L54 = (budget.L540 + budget.L541 + budget.L542 + budget.L543 + budget.L548 + budget.L549)
    L55 = budget.L551
    L56 = (budget.L560 - budget.L561 + budget.L562 - budget.L563)
    L57 = budget.L570
    L58 = budget.L580
    L59 = (budget.L590 - budget.L591)
    L5 = (L50 + L52 + L54 - L55 + L56 + L57 - L58 + L59)  # Özkaynaklar Toplamı
    L02 = (L3 + L4 + L5)  # Pasif Toplam
    # print(type(L02))

    # Gelir Tablosu Hesaplamaları
    L60 = (budget.L600 + budget.L601 + budget.L602 + budget.L603 + budget.L604)
    L61 = (budget.L610 + budget.L611 + budget.L612)
    L03 = (L60 - L61)  # Net Satışlar
    L62 = (budget.L620 + budget.L621 + budget.L622 + budget.L623 + budget.L624 + budget.L625 + budget.L626
           + budget.L627 + budget.L628)
    L04 = (L03 - L62)  # Gayrisafi Satış Karı
    L63 = (budget.L630 + budget.L631 + budget.L632 + budget.L633 + budget.L634)
    L05 = (L04 - L63)  # Faaliyet Karı
    L64 = (budget.L640 + budget.L641 + budget.L642 + budget.L643 + budget.L644 + budget.L645 + budget.L646
           + budget.L647 + budget.L648 + budget.L649)
    L65 = (budget.L653 + budget.L654 + budget.L655 + budget.L656 + budget.L657 + budget.L658 + budget.L659)
    L66 = (budget.L660 + budget.L661)
    L67 = (budget.L671 + budget.L677 + budget.L678 + budget.L679)
    L68 = (budget.L680 + budget.L681 + budget.L687 + budget.L688 + budget.L689)
    L06 = (L05 + L64 - L65 - L66 + L67 - L68)  # Dönem Karı veya zararı
    L6 = (L06 - budget.L690)  # Dönem Net Karı/Zararı
    # print(type(L6))

    # Oran analizlerine ilişkin hesaplamalar;
    if L10 != 0:
        tg1 = float(format((budget.L100 * 100 / L10), '.2f'))
    else:
        tg1 = 0
    if L1 != 0:
        tg2 = float(format((L10 * 100 / L1), '.2f'))
        tg3 = float(format((L15 * 100 / L1), '.2f'))
        tg4 = float(format((budget.L131 * 100 / L1), '.2f'))
    else:
        tg2, tg3, tg4 = 0, 0, 0
    if L2 != 0:
        tg5 = float(format((budget.L231 * 100 / L2), '.2f'))
    else:
        tg5 = 0
    if L01 != 0:
        tg6 = float(format(((budget.L131 + budget.L231) * 100 / L01), '.2f'))
    else:
        tg6 = 0
    if L50 != 0:
        tg7 = float(format(((budget.L131 + budget.L231) * 100 / L50), '.2f'))
    else:
        tg7 = 0
    if L5 != 0:
        tg8 = float(format(((budget.L131 + budget.L231) * 100 / L5), '.2f'))
    else:
        tg8 = 0
    if L3 != 0:
        tg9 = float(format((budget.L331 * 100 / L3), '.2f'))
    else:
        tg9 = 0
    if L4 != 0:
        tg10 = float(format((budget.L431 * 100 / L4), '.2f'))
    else:
        tg10 = 0
    if L02 != 0:
        tg11 = float(format(((budget.L331 + budget.L431) * 100 / L02), '.2f'))
    else:
        tg11 = 0
    if L12 != 0:
        tg12 = float(format(((budget.L128 - budget.L129) * 100 / L12), '.2f'))
    else:
        tg12 = 0

    temel_g = [tg1, tg2, tg3, tg4, tg5, tg6, tg7, tg8, tg9, tg10, tg11, tg12]
    temel_gostergeler = [(temel[i + 1], temel_g[i]) for i in range(0, len(temel_g)) if temel_g[i] != 0]

    nis = (L1 - L3)
    if (L05 + L64) != 0:
        mg1 = float(format(((L63 + L65 + L66) * 100 / (L05 + L64)), '.2f'))
    else:
        mg1 = 0

    diger = [(Oran['nis'], nis), (Oran['mg1'], mg1)]

    if L3 != 0:
        fg1 = float(format((L1 / L3), '.2f'))
    else:
        fg1 = 0
    if L3 != 0:
        fg2 = float(format(((L1 - L15) / L3), '.2f'))
    else:
        fg2 = 0
    if L3 != 0:
        fg3 = float(format((L11 / L3), '.2f'))
    else:
        fg3 = 0
    if L5 != 0:
        fg4 = float(format(((L3 + L4) * 100 / L5), '.2f'))
    else:
        fg4 = 0
    if L02 != 0:
        fg5 = float(format(((L3 + L4) * 100 / L02), '.2f'))
    else:
        fg5 = 0
    if L60 != 0:
        fg6 = float(format(((L3 + L4) * 100 / L60), '.2f'))
    else:
        fg6 = 0
    if L01 != 0:
        fg7 = float(format((L5 * 100 / L01), '.2f'))
    else:
        fg7 = 0
    if L50 != 0:
        fg8 = float(format(((L54 - L58) * 100 / L50), '.2f'))
    else:
        fg8 = 0

    finansal_g = [fg1, fg2, fg3, fg4, fg5, fg6, fg7, fg8]
    finansal_gostergeler = [(finansal[i], finansal_g[i]) for i in range(0, len(finansal_g)) if finansal_g[i] != 0]

    if L12 != 0:
        ag1 = float(format((L03 / L12), '.2f'))
    else:
        ag1 = 0
    if ag1 != 0:
        ag2 = float(format((365 / (L03 / L12)), '.2f'))
    else:
        ag2 = 0
    if L15 != 0:
        ag3 = float(format((L62 / L15), '.2f'))
    else:
        ag3 = 0
    if ag3 != 0:
        ag4 = float(format((365 / (L62 / L15)), '.2f'))
    else:
        ag4 = 0
    if L01 != 0:
        ag5 = float(format((L03 / L01), '.2f'))
    else:
        ag5 = 0

    aktivite_g = [ag1, ag2, ag3, ag4, ag5]
    aktivite_gostergeleri = [(aktivite[i], aktivite_g[i]) for i in range(0, len(aktivite_g)) if aktivite_g[i] != 0]

    if L03 != 0:
        kg1 = float(format((L06 * 100 / L03), '.2f'))
    else:
        kg1 = 0
    if L5 != 0:
        kg2 = float(format((L6 * 100 / L5), '.2f'))
    else:
        kg2 = 0
    if L04 != 0:
        kg3 = float(format((L66 * 100 / L04), '.2f'))
    else:
        kg3 = 0

    kg4 = (L05 - budget.L257)

    if (L1 + L2) != 0:
        kg5 = float(format((L6 * 100 / (L1 + L2)), '.2f'))
    else:
        kg5 = 0
    if L5 != 0:
        kg6 = float(format((L6 * 100 / L5), '.2f'))
    else:
        kg6 = 0
    if L03 != 0:
        kg7 = float(format((L6 * 100 / L03), '.2f'))
    else:
        kg7 = 0
    if L5 != 0:
        kg8 = float(format((L6 / L5), '.2f'))
    else:
        kg8 = 0
    if L02 != 0:
        kg9 = float(format(((L06 - L66) * 100 / L02), '.2f'))
    else:
        kg9 = 0

    karlilik_g = [kg1, kg2, kg3, kg4, kg5, kg6, kg7, kg8, kg9]
    karlilik_gostergeleri = [(karlilik[i], karlilik_g[i]) for i in range(0, len(karlilik_g)) if karlilik_g[i] != 0]

    akt = [budget.L100, budget.L101, budget.L102, budget.L103, budget.L108, L10, budget.L110, budget.L111,
           budget.L112, budget.L118, budget.L119, L11, budget.L1201, budget.L1202, budget.L1203, L120, budget.L121,
           budget.L122, budget.L126, budget.L127, budget.L128, budget.L129, L12, budget.L131, budget.L132, budget.L133,
           budget.L135, budget.L136, budget.L137, budget.L138, budget.L139, L13, budget.L150, budget.L151, budget.L152,
           budget.L153, budget.L157, budget.L158, budget.L159, L15, budget.L170, budget.L171, budget.L178, L17,
           budget.L180, budget.L181, L18, budget.L190, budget.L191, budget.L192, budget.L193, budget.L194, budget.L195,
           budget.L196, budget.L197, budget.L198, budget.L199, L19, L1, budget.L200, budget.L201, L20, budget.L210,
           budget.L211, L21, budget.L2201, budget.L2202, L220, budget.L221, budget.L222, budget.L226, budget.L228,
           budget.L229, L22, budget.L231, budget.L232, budget.L233, budget.L235, budget.L236, budget.L237, budget.L239,
           L23, budget.L240, budget.L241, budget.L242, budget.L243, budget.L244, budget.L245, budget.L246, budget.L247,
           budget.L248, budget.L249, L24, budget.L250, budget.L251, budget.L252, budget.L253, budget.L254, budget.L255,
           budget.L256, budget.L257, budget.L258, budget.L259, L25, budget.L260, budget.L261, budget.L262, budget.L263,
           budget.L264, budget.L267, budget.L268, budget.L269, L26, budget.L271, budget.L272, budget.L277, budget.L278,
           budget.L279, L27, budget.L280, budget.L281, L28, budget.L291, budget.L292, budget.L293, budget.L294,
           budget.L295, budget.L296, budget.L297, budget.L298, budget.L299, L26, L2]  # AKTİF TOP (133 DEĞİŞKEN)

    pas = [budget.L300, budget.L301, budget.L302, budget.L303, budget.L304, budget.L305, budget.L306, budget.L308,
           budget.L309, L30, budget.L3201, budget.L3202, L320, budget.L321, budget.L322, budget.L326, budget.L329, L32,
           budget.L331, budget.L332, budget.L333, budget.L335, budget.L336, budget.L337, budget.L338, L33, budget.L340,
           budget.L349, L34, budget.L350, budget.L351, budget.L358, L35, budget.L360, budget.L361, budget.L368,
           budget.L369, L36, budget.L370, budget.L371, budget.L372, budget.L373, budget.L379, L37, budget.L380,
           budget.L381, L38, budget.L391, budget.L392, budget.L393, budget.L394, budget.L397, budget.L399, L39, ' ',
           ' ', ' ', ' ', L3, budget.L400, budget.L401, budget.L402, budget.L405, budget.L407, budget.L408, budget.L409,
           L40, budget.L410, L41, budget.L420, budget.L421, budget.L422, budget.L426, budget.L429, L42, budget.L431,
           budget.L432, budget.L433, budget.L436, budget.L437, budget.L438, L43, budget.L440, budget.L449, L44,
           budget.L472, budget.L479, L47, budget.L480, budget.L481, L48, budget.L492, budget.L493, budget.L496,
           budget.L499, L49, L4, budget.L500, budget.L501, budget.L502, budget.L503, L50, budget.L520,
           budget.L521, budget.L522, budget.L523, budget.L525, budget.L526, budget.L527, budget.L529, L52, budget.L540,
           budget.L541, budget.L542, budget.L543, budget.L548, budget.L549, L54, budget.L551, L55, budget.L560,
           budget.L561, budget.L562, budget.L563, L56, budget.L570, L57, budget.L580, L58, budget.L590, budget.L591,
           L59, L5]  # PASİF TOP (129 DEĞİŞKEN + 4 tane ' ', Toplam 133)

    gel = [budget.L600, budget.L601, budget.L602, budget.L603, budget.L604, L60, ' ', budget.L610, budget.L611,
           budget.L612, L61, L03, ' ', budget.L620, budget.L621, budget.L622, budget.L623, budget.L624, budget.L625,
           budget.L626, budget.L627, budget.L628, L62, L04, ' ', budget.L630, budget.L631, budget.L632, budget.L633,
           budget.L634, L63, L05, ' ', budget.L640, budget.L641, budget.L642, budget.L643, budget.L644, budget.L645,
           budget.L646, budget.L647, budget.L648, budget.L649, L64, ' ', budget.L653, budget.L654, budget.L655,
           budget.L656, budget.L657, budget.L658, budget.L659, L65, ' ', budget.L660, budget.L661, L66, ' ',
           budget.L671, budget.L677, budget.L678, budget.L679, L67, budget.L680, budget.L681, budget.L687,
           budget.L688, budget.L689, L68, L06, ' ', budget.L690, ' ', ' ', L6, ' ', ' ', ' ', ' ', ' ', ' ', ' ',
           ' ', ' ', ' ', ' ', '(%)', ' ', tg1, tg2, tg3, ' ', ' ', tg4, tg5, tg6, tg7, tg8, ' ', ' ', tg9, tg10, tg11,
           ' ', ' ', tg12, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
           ' ', ' ', ' ', ' ', ' ', ' ', ' ', L6, ' ']  # (133)
    gelir_kalemleri = [budget.L600, budget.L601, budget.L602, budget.L603, budget.L604, L60, budget.L610, budget.L611,
           budget.L612, L61, L03, budget.L620, budget.L621, budget.L622, budget.L623, budget.L624, budget.L625,
           budget.L626, budget.L627, budget.L628, L62, L04, budget.L630, budget.L631, budget.L632, budget.L633,
           budget.L634, L63, L05, budget.L640, budget.L641, budget.L642, budget.L643, budget.L644, budget.L645,
           budget.L646, budget.L647, budget.L648, budget.L649, L64, budget.L653, budget.L654, budget.L655,
           budget.L656, budget.L657, budget.L658, budget.L659, L65, budget.L660, budget.L661, L66,
           budget.L671, budget.L677, budget.L678, budget.L679, L67, budget.L680, budget.L681, budget.L687,
           budget.L688, budget.L689, L68, L06, budget.L690]
    # print(f'metod içi gelir_kalemleri uzunluğu: {len(gelir_kalemleri)}')

    detaytablolar = [(aktifhesaplar[i], akt[i], pasifhesaplar[i], pas[i], gelirtablosu[i], gel[i])
                     for i in range(0, len(akt))]

    aktif_tablosu = [(aktifhesaplar[i], akt[i]) for i in range(0, len(akt)) if aktifhesaplar[i] != ' ' and akt[i] != 0]
    # print(aktif_tablosu)

    pasif_tablosu = [(pasifhesaplar[i], pas[i]) for i in range(0, len(akt)) if pasifhesaplar[i] != ' ' and pas[i] != 0]
    # print(pasif_tablosu)

    gelir_tablosu = [(gelirtabbase[i], gelir_kalemleri[i])
                     for i in range(0, len(gelirtabbase)) if gelir_kalemleri[i] != 0]
    # print(f'metod hesaplıyor : {gelir_tablosu}')

    # oranlar = [(Oran['tg'], ' ')] + temel_gostergeler + [(Oran['fg'], ' ')] + finansal_gostergeler \
    #           + [('AKTİVİTE GÖSTERGELERİ', ' ')] + aktivite_gostergeleri \
    #           + [('KARLILIK GÖSTERGELERİ', ' ')] + karlilik_gostergeleri + [(' ', ' ')] + diger
    # # print(f'metod içinde oranlar tablosu: {oranlar}')
    # temel_oran = [(Oran['tg'], '%')] + temel_gostergeler
    finansal_oran = finansal_gostergeler + [(' ', ' '), ('DİĞER TEMEL GÖSTERGELER', ' ')] + diger
    aktivite_oran = aktivite_gostergeleri
    # karlilik_oran = [('KARLILIK GÖSTERGELERİ', ' ')] + karlilik_gostergeleri

    context = {
        'DT': detaytablolar,
        'L6': L6, 'L10': L10, 'L11': L11, 'L12': L12, 'L120': L120, 'L13': L13, 'L15': L15, 'L17': L17, 'L19': L19,
        'L1': L1, 'L20': L20, 'L21': L21, 'L22': L22, 'L220': L220, 'L23': L23, 'L24': L24, 'L25': L25, 'L26': L26,
        'L27': L27, 'L28': L28, 'L29': L29, 'L2': L2, 'L01': L01, 'L30': L30, 'L320': L320, 'L32': L32, 'L33': L33,
        'L34': L34, 'L35': L35, 'L36': L36, 'L37': L37, 'L38': L38, 'L39': L39, 'L3': L3, 'L40': L40, 'L41': L41,
        'L42': L42, 'L43': L43, 'L44': L44, 'L47': L47, 'L48': L48, 'L49': L49, 'L4': L4, 'L50': L50, 'L52': L52,
        'L54': L54, 'L55': L55, 'L56': L56, 'L57': L57, 'L58': L58, 'L59': L59, 'L5': L5, 'L02': L02, 'L60': L60,
        'L61': L61, 'L03': L03, 'L62': L62, 'L04': L04, 'L63': L63, 'L05': L05, 'L64': L64, 'L65': L65, 'L66': L66,
        'L67': L67, 'L68': L68, 'L06': L06,
        'nis': nis,
        'tg1': tg1, 'tg2': tg2, 'tg3': tg3, 'tg4': tg4, 'tg5': tg5, 'tg6': tg6, 'tg7': tg7, 'tg8': tg8, 'tg9': tg9,
        'tg10': tg10, 'tg11': tg11, 'tg12': tg12,
        'mg1': mg1, 'fg1': fg1, 'fg2': fg2, 'fg3': fg3, 'fg4': fg4, 'fg5': fg5, 'fg6': fg6, 'fg7': fg7,
        'fg8': fg8,
        'ag1': ag1, 'ag2': ag2, 'ag3': ag3, 'ag4': ag4, 'ag5': ag5,
        'kg1': kg1, 'kg2': kg2, 'kg3': kg3, 'kg4': kg4, 'kg5': kg5, 'kg6': kg6, 'kg7': kg7, 'kg8': kg8, 'kg9': kg9,
        'aktif_tablosu': aktif_tablosu, 'pasif_tablosu': pasif_tablosu, 'gelir_tablosu': gelir_tablosu,
        'aktiftoplam': L01, 'pasiftoplam': L02, 'kar_zarar': L6,
        'temel_oran': temel_gostergeler, 'finansal_oran': finansal_oran, 'aktivite_oran': aktivite_gostergeleri,
        'karlilik_oran': karlilik_gostergeleri
    }
    return context


def hesaplamalar(self):
    # Spread özet tablosu için yapılması gereken ara toplamlar
    # Aktif Hesaplar
    L10 = self.L100 + self.L101 + self.L102 - self.L103 + self.L108
    L11 = self.L110 + self.L111 + self.L112 + self.L118 - self.L119
    L12 = (self.L1201 + self.L1202 + self.L121 - self.L122 + self.L126
           + self.L127 + self.L128 - self.L129)
    L120 = (self.L1201 + self.L1202)
    L13 = (self.L131 + self.L132 + self.L133 + self.L135
           + self.L136 - self.L137 + self.L138 - self.L139)
    L15 = (self.L150 + self.L151 + self.L152 + self.L153 + self.L157 - self.L158 + self.L159)
    L17 = (self.L170 + self.L171 + self.L178)
    L18 = (self.L180 + self.L181)
    L19 = (self.L190 + self.L191 + self.L192 + self.L193 + self.L194 + self.L195
           + self.L196 + self.L197 + self.L198 - self.L199)
    L1 = (L10 + L11 + L12 + L13 + L15 + L17 + L18 + L19)  # Dönen Varlıklar
    L20 = (self.L200 + self.L201)
    L21 = (self.L210 - self.L211)
    L22 = (self.L2201 - self.L2202 + self.L221 - self.L222 + self.L226 + self.L228 - self.L229)
    L220 = (self.L2201 - self.L2202)
    L23 = (self.L231 + self.L232 + self.L233 + self.L235
           + self.L236 - self.L237 - self.L239)
    L24 = (self.L240 - self.L241 + self.L242 - self.L243 - self.L244
           + self.L245 - self.L246 - self.L247 + self.L248 - self.L249)
    L25 = (self.L250 + self.L251 + self.L252 + self.L253 + self.L254
           + self.L255 + self.L256 - self.L257 + self.L258 + self.L259)
    L26 = (self.L260 + self.L261 + self.L262 + self.L263 + self.L264
           + self.L267 - self.L268 + self.L269)
    L27 = (self.L271 + self.L272 + self.L277 - self.L278 + self.L279)
    L28 = (self.L280 + self.L281)
    L29 = (self.L291 + self.L292 + self.L293 + self.L294 + self.L295 + self.L296
           + self.L297 - self.L298 - self.L299)
    L2 = (L20 + L21 + L22 + L23 + L24 + L25 + L26 + L27 + L28 + L29)  # Duran Varlıklar
    L01 = (L1 + L2)  # Aktif Toplam

    # Pasif Hesaplar
    L30 = (self.L300 + self.L301 - self.L302 + self.L303 + self.L304
           + self.L305 + self.L306 - self.L308 + self.L309)
    L320 = (self.L3201 + self.L3202)
    L32 = (self.L3201 + self.L3202 + self.L321 - self.L322 + self.L326 + self.L329)
    L33 = (self.L331 + self.L332 + self.L333 + self.L335 + self.L336 - self.L337 + self.L338)
    L34 = (self.L340 + self.L349)
    L35 = (self.L350 + self.L351 + self.L358)
    L36 = (self.L360 + self.L361 + self.L368 + self.L369)
    L37 = (self.L370 - self.L371 + self.L372 + self.L373 + self.L379)
    L38 = (self.L380 + self.L381)
    L39 = (self.L391 + self.L392 + self.L393 + self.L394 + self.L397 + self.L399)
    L3 = (L30 + L32 + L33 + L34 + L35 + L36 + L37 + L38 + L39)  # Kısa Vadeli Yabancı Kaynaklar
    L40 = (self.L400 + self.L401 - self.L402 + self.L405 + self.L407 - self.L408 + self.L409)
    L41 = self.L410
    L42 = (self.L420 + self.L421 - self.L422 + self.L426 + self.L429)
    L43 = (self.L431 + self.L432 + self.L433 + self.L436 - self.L437 + self.L438)
    L44 = (self.L440 + self.L449)
    L47 = (self.L472 + self.L479)
    L48 = (self.L480 + self.L481)
    L49 = (self.L492 + self.L493 + self.L496 + self.L499)
    L4 = (L40 + L41 + L42 + L43 + L44 + L47 + L48 + L49)  # Uzun Vadeli Yabancı Kaynaklar
    L50 = (self.L500 - self.L501 + self.L502 - self.L503)
    L52 = (self.L520 + self.L521 + self.L522 + self.L523
           + self.L525 + self.L526 + self.L527 + self.L529)
    L54 = (self.L540 + self.L541 + self.L542 + self.L543 + self.L548 + self.L549)
    L55 = self.L551
    L56 = (self.L560 - self.L561 + self.L562 - self.L563)
    L57 = self.L570
    L58 = self.L580
    L59 = (self.L590 - self.L591)
    L5 = (L50 + L52 + L54 - L55 + L56 + L57 - L58 + L59)  # Özkaynaklar Toplamı
    L02 = (L3 + L4 + L5)  # Pasif Toplam

    # Gelir Tablosu
    L60 = (self.L600 + self.L601 + self.L602 + self.L603 + self.L604)
    L61 = (self.L610 + self.L611 + self.L612)
    L03 = (L60 - L61)  # Net Satışlar
    L62 = (self.L620 + self.L621 + self.L622 + self.L623 + self.L624
           + self.L625 + self.L626 + self.L627 + self.L628)
    L04 = (L03 - L62)  # Gayrisafi Satış Karı
    L63 = (self.L630 + self.L631 + self.L632 + self.L633 + self.L634)
    L05 = (L04 - L63)  # Faaliyet Karı
    L64 = (self.L640 + self.L641 + self.L642 + self.L643 + self.L644
           + self.L645 + self.L646 + self.L647 + self.L648 + self.L649)
    L65 = (self.L653 + self.L654 + self.L655 + self.L656 + self.L657 + self.L658 + self.L659)
    L66 = (self.L660 + self.L661)
    L67 = (self.L671 + self.L677 + self.L678 + self.L679)
    L68 = (self.L680 + self.L681 + self.L687 + self.L688 + self.L689)
    L06 = (L05 + L64 - L65 - L66 + L67 - L68)  # Dönem Karı veya zararı
    L6 = (L06 - self.L690)  # Dönem Net Karı/Zararı
    # Spread ekranında görünecek hesaplamalar;

    # Oran analizlerine ilişkin hesaplamalar;
    nis = (L1 - L3)
    if (L05 + L64) != 0:
        mg1 = float(format(((L63 + L65 + L66) * 100 / (L05 + L64)), '.2f'))
    else:
        mg1 = 0
    # finansal göstergeler;
    if L3 != 0:
        fg1 = float(format((L1 / L3), '.2f'))
    else:
        fg1 = 0
    if L3 != 0:
        fg2 = float(format(((L1 - L15) / L3), '.2f'))
    else:
        fg2 = 0
    if L3 != 0:
        fg3 = float(format((L11 / L3), '.2f'))
    else:
        fg3 = 0
    if L5 != 0:
        fg4 = float(format(((L3 + L4) * 100 / L5), '.2f'))
    else:
        fg4 = 0
    if L02 != 0:
        fg5 = float(format(((L3 + L4) * 100 / L02), '.2f'))
    else:
        fg5 = 0
    if L60 != 0:
        fg6 = float(format(((L3 + L4) * 100 / L60), '.2f'))
    else:
        fg6 = 0
    if L01 != 0:
        fg7 = float(format((L5 * 100 / L01), '.2f'))
    else:
        fg7 = 0
    if L50 != 0:
        fg8 = float(format(((L54 - L58) * 100 / L50), '.2f'))
    else:
        fg8 = 0
    finansal_g = [fg1, fg2, fg3, fg4, fg5, fg6, fg7, fg8]
    # print('finansal göstergeler', len(fin_g), len(finansal))
    finansal_gostergeler = [(finansal[i], finansal_g[i]) for i in range(0, len(finansal_g))]

    if L12 != 0:
        ag1 = float(format((L03 / L12), '.2f'))
    else:
        ag1 = 0
    if ag1 != 0:
        ag2 = float(format((365 / (L03 / L12)), '.2f'))
    else:
        ag2 = 0
    if L15 != 0:
        ag3 = float(format((L62 / L15), '.2f'))
    else:
        ag3 = 0
    if ag3 != 0:
        ag4 = float(format((365 / (L62 / L15)), '.2f'))
    else:
        ag4 = 0
    if L01 != 0:
        ag5 = float(format((L03 / L01), '.2f'))
    else:
        ag5 = 0
    aktivite_g = [ag1, ag2, ag3, ag4, ag5]
    # print('Aktivite göstergeleri', len(aktivite_g), len(aktivite))
    aktivite_gostergeleri = [(aktivite[i], aktivite_g[i]) for i in range(0, len(aktivite_g))]

    if L03 != 0:
        kg1 = float(format((L06 * 100 / L03), '.2f'))
    else:
        kg1 = 0
    if L5 != 0:
        kg2 = float(format((L6 * 100 / L5), '.2f'))
    else:
        kg2 = 0
    if L04 != 0:
        kg3 = float(format((L66 * 100 / L04), '.2f'))
    else:
        kg3 = 0

    kg4 = (L05 - self.L257)

    if (L1 + L2) != 0:
        kg5 = float(format((L6 * 100 / (L1 + L2)), '.2f'))
    else:
        kg5 = 0
    if L5 != 0:
        kg6 = float(format((L6 * 100 / L5), '.2f'))
    else:
        kg6 = 0
    if L03 != 0:
        kg7 = float(format((L6 * 100 / L03), '.2f'))
    else:
        kg7 = 0
    if L5 != 0:
        kg8 = float(format((L6 / L5), '.2f'))
    else:
        kg8 = 0
    if L02 != 0:
        kg9 = float(format(((L06 - L66) * 100 / L02), '.2f'))
    else:
        kg9 = 0
    karlilik_g = [kg1, kg2, kg3, kg4, kg5, kg6, kg7, kg8, kg9]
    # print('Karlılık göstergeleri', len(karlilik_g), len(karlilik))
    karlilik_gostergeleri = [(karlilik[i], karlilik_g[i]) for i in range(0, len(karlilik_g))]

    # Spread tablosu için yapılacak hesaplamalar;
    # Aktif
    s110 = (self.L100 + self.L102)
    s111 = L11
    s112 = self.L1201
    s113 = self.L1202
    s114 = (self.L101 + self.L121)
    s115 = self.L131
    s116 = (self.L132 + self.L133)
    s117 = (self.L126 + self.L127 + self.L135 + self.L136 + self.L138 + L18 + L19)
    s11 = (s112 + s113 + s115 + s110 + s111 + s114 + s116 + s117)
    s150 = self.L150
    s151 = (self.L151 + self.L152)
    s152 = (self.L153 + self.L157 - self.L158)
    s159 = self.L159
    s15 = (s150 + s159 + s151 + s152)
    s1 = L1
    s210 = ((self.L240 + self.L242 + self.L245 + self.L248)
            - (self.L241 + self.L243 + self.L244 + self.L246 + self.L247 + self.L249))
    s211 = (self.L221 + self.L222)
    s212 = (self.L2201 + self.L2202)
    s213 = self.L226
    s214 = self.L231
    s215 = (self.L232 + self.L233)
    s216 = (L17 + L20)
    s217 = (self.L235 + self.L236 + L26 + L27 + L28 + L29 - self.L237)
    s218 = self.L258
    s219 = self.L259
    s220 = (s210 + s211 + s212 + s213 + s214 + s215 + s216 + s217 + s218 + s219)
    s221 = (self.L250 + self.L251 + self.L252)
    s222 = self.L253
    s223 = (self.L254 + self.L255 + self.L256)
    s224 = L21
    s20 = (s221 + s222 + s223 + s224)
    s225 = self.L257
    s21 = (s20 - s225)
    s226 = (L26 + L27)
    s2 = (s220 + s21)
    s01 = L01
    a = [s110, s111, s112, s113, s114, s115, s116, s117, s11, s150, s151, s152, s159, s15, s1, s210, s211, s212, s213,
         s214, s215, s216, s217, s218, s219, s220, s221, s222, s223, s224, s20, s225, s21, s226, s2, s01]
    # print('aktif tablosu', len(a), len(aktifler))
    aktif_tablosu = [(aktifler[i], a[i]) for i in range(0, len(a))]
    donen_varlik = [(aktif_tablosu[i]) for i in range(0, 15)]
    duran_varlik = [(aktif_tablosu[i]) for i in range(15, 36)]

    # Pasif
    s300 = self.L300
    s301 = self.L303
    s302 = self.L3202
    s303 = self.L3201
    s304 = (self.L103 + self.L321 - self.L322)
    s312 = L34
    s305 = self.L331
    s306 = self.L338
    s307 = (self.L332 + self.L333)
    s308 = (self.L301 - self.L302)
    s309 = L37
    s310 = L36
    s311 = (self.L309 + self.L329 + self.L335 + self.L336 + self.L381 + L39)
    s3 = L3
    s400 = self.L400
    s401 = (self.L304 + self.L305 + self.L306 + self.L405 + self.L407 - (self.L308 + self.L408))
    s402 = (self.L420 + self.L421 - self.L422)
    s403 = self.L431
    s404 = (self.L432 + self.L433)
    s405 = (self.L409 + self.L426 + self.L429 + self.L436 - self.L437 + self.L438 + L44 + L47 + L48 + L49)
    s406 = (L35 + L41)
    s407 = (self.L401 + self.L402)
    s408 = self.L472
    s4 = L4
    s34 = (L3 + L4)
    s500 = self.L500
    s501 = L50
    s502 = (self.L502 - self.L503)
    s503 = L54
    s504 = (self.L522 + self.L523)
    s505 = (L52 - s504)
    s506 = (L57 - L58)
    s507 = L59
    s508 = (self.L128 + self.L228 - (self.L129 + self.L229 + self.L239))
    s5 = (L5 - s508)
    s02 = L02
    p = [s300, s301, s302, s303, s304, s312, s305, s306, s307, s308, s309, s310, s311, s3, s400, s401, s402, s403, s404,
         s405, s406, s407, s408, s4, s34, s500, s501, s502, s503, s504, s505, s506, s507, s508, s5, s02]
    # print('pasif tablosu', len(p), len(pasifler))
    pasif_tablosu = [(pasifler[i], p[i]) for i in range(0, len(p))]
    kv_borc = [pasif_tablosu[i] for i in range(0, 14)]
    uv_borc = [pasif_tablosu[i] for i in range(14, 24)]
    ozkaynak = [pasif_tablosu[i] for i in range(25, 35)]

    # Gelir Tablosu
    s600 = self.L600
    s601 = self.L601
    s602 = self.L602
    s60 = L60
    s610 = self.L610
    s611 = self.L611
    s612 = self.L612
    s61 = L61
    s03 = L03
    s620 = self.L620
    s621 = self.L621
    s622 = self.L622
    s623 = self.L623
    s628 = self.L628
    s62 = L62
    s04 = L04
    s630 = self.L630
    s631 = self.L631
    s632 = self.L632
    s634 = self.L634
    s63 = L63
    s66 = L66
    s05 = L05
    s64 = L64
    s65 = L65
    s06 = L06
    s690 = self.L690
    s6 = L6
    g = [s600, s601, s602, s60, s610, s611, s612, s61, s03, s620, s621, s622, s623, s628, s62, s04, s630,
         s631, s632, s634, s63, s66, s05, s64, s65, s06, s690, s6]
    # print('gelir tablosu', len(g), len(gelir))
    gelir_tablosu = [(gelir[i], g[i]) for i in range(0, len(g))]

    context = {
        'a': a, 'p': p, 'g': g,
        'finansal_g': finansal_g, 'aktivite_g': aktivite_g, 'karlilik_g': karlilik_g,
        'nis': nis, 'mg1': mg1,
        'aktif_tablosu': aktif_tablosu, 'pasif_tablosu': pasif_tablosu, 'gelir_tablosu': gelir_tablosu,
        'donen_varlik': donen_varlik, 'duran_varlik': duran_varlik, 'kv_borc': kv_borc, 'uv_borc': uv_borc,
        'ozkaynak': ozkaynak, 'finansal_gostergeler': finansal_gostergeler,
        'aktivite_gostergeleri': aktivite_gostergeleri, 'karlilik_gostergeleri': karlilik_gostergeleri
    }
    return context


def groupspread(list):
    # Grup spread özet tablosu için değişkenler
    # Aktifler için;
    s110 = s111 = s112 = s113 = s114 = s115 = s116 = s117 = s150 = s151 = s152 = s159 = s210 = s211 = 0
    s212 = s213 = s214 = s215 = s216 = s217 = s218 = s219 = s221 = s222 = s223 = s224 = s225 = 0
    s226 = s1 = s01 = 0
    # Pasifler için;
    s300 = s301 = s302 = s303 = s304 = s312 = s305 = s306 = s307 = s308 = s309 = s310 = s311 = s3 = s400 = s401 = 0
    s402 = s403 = s404 = s405 = s406 = s407 = s408 = s4 = s500 = s501 = s502 = s503 = s504 = s505 = s506 = 0
    s507 = s508 = s5 = s02 = 0
    # Gelir Tablosu için;
    s600 = s601 = s602 = s60 = s610 = s611 = s612 = s61 = s620 = s621 = s622 = s623 = s628 = s62 = s630 = 0
    s631 = s632 = s634 = s63 = s66 = s64 = s65 = s690 = 0
    s67 = s68 = 0
    L15 = L12 = L257 = 0
    for a in list:
        # print('hesaplama yapılan fonksiyon içinde, şu an hesaplamaları yapılan : ', a,
        #       'için hesaplanan dönem : ', a.period)
        # aktif için;
        L12 = L12 + (a.L1201 + a.L1202 + a.L121 - a.L122 + a.L126 + a.L127 + a.L128 - a.L129)
        L15 = L15 + (a.L150 + a.L151 + a.L152 + a.L153 + a.L157 - a.L158 + a.L159)
        L257 = L257 + a.L257  # toplam birikmiş amortismanları hesaplıyoruz ebitda için

        s110 = s110 + (a.L100 + a.L102)
        s111 = s111 + (a.L110 + a.L111 + a.L112 + a.L118 - a.L119)
        s112 = s112 + a.L1201
        s113 = s113 + a.L1202
        s114 = s114 + (a.L101 + a.L121)
        s115 = s115 + a.L131
        s116 = s116 + (a.L132 + a.L133)
        s117 = s117 + (a.L126 + a.L127 + a.L135 + a.L136 + a.L138 + (a.L180 + a.L181) +
                       (a.L190 + a.L191 + a.L192 + a.L193 + a.L194 + a.L195 + a.L196 + a.L197 + a.L198 - a.L199))
        s150 = s150 + a.L150
        s151 = s151 + (a.L151 + a.L152)
        s152 = s152 + (a.L153 + a.L157 - a.L158)
        s159 = s159 + a.L159
        # hesaplama s1 = L1 için yapılan hesaplamadır Dönen varlıklar;
        s1 = s1 + ((a.L100 + a.L101 + a.L102 - a.L103 + a.L108) + (a.L110 + a.L111 + a.L112 + a.L118 - a.L119) +
                   (a.L1201 + a.L1202 + a.L121 - a.L122 + a.L126 + a.L127 + a.L128 - a.L129) +
                   (a.L131 + a.L132 + a.L133 + a.L135 + a.L136 - a.L137 + a.L138 - a.L139) + (a.L180 + a.L181) +
                   (a.L150 + a.L151 + a.L152 + a.L153 + a.L157 - a.L158 + a.L159) + (a.L170 + a.L171 + a.L178) +
                   (a.L190 + a.L191 + a.L192 + a.L193 + a.L194 + a.L195 + a.L196 + a.L197 + a.L198 - a.L199))
        s210 = s210 + ((a.L240 + a.L242 + a.L245 + a.L248) - (a.L241 + a.L243 + a.L244 + a.L246 + a.L247 + a.L249))
        s211 = s211 + (a.L221 + a.L222)
        s212 = s212 + (a.L2201 + a.L2202)
        s213 = s213 + a.L226
        s214 = s214 + a.L231
        s215 = s215 + (a.L232 + a.L233)
        s216 = s216 + ((a.L170 + a.L171 + a.L178) + (a.L200 + a.L201))
        s217 = s217 + (a.L235 + a.L236 + (a.L260 + a.L261 + a.L262 + a.L263 + a.L264 + a.L267 - a.L268 + a.L269) +
                       (a.L271 + a.L272 + a.L277 - a.L278 + a.L279) + (a.L280 + a.L281) + (a.L291 + a.L292 + a.L293 +
                                                                                           a.L294 + a.L295 + a.L296 +
                                                                                           a.L297 - a.L298 - a.L299) -
                       a.L237)
        s218 = s218 + a.L258
        s219 = s219 + a.L259
        s221 = s211 + (a.L250 + a.L251 + a.L252)
        s222 = s222 + a.L253
        s223 = s223 + (a.L254 + a.L255 + a.L256)
        s224 = s224 + (a.L210 - a.L211)
        s225 = s225 + a.L257
        s226 = s226 + ((a.L260 + a.L261 + a.L262 + a.L263 + a.L264 + a.L267 - a.L268 + a.L269) +
                       (a.L271 + a.L272 + a.L277 - a.L278 + a.L279))
        s01 = s01 + (((a.L100 + a.L101 + a.L102 - a.L103 + a.L108) +
                      (a.L110 + a.L111 + a.L112 + a.L118 - a.L119) +
                      (a.L1201 + a.L1202 + a.L121 - a.L122 + a.L126 + a.L127 + a.L128 - a.L129) +
                      (a.L131 + a.L132 + a.L133 + a.L135 + a.L136 - a.L137 + a.L138 - a.L139) +
                      (a.L150 + a.L151 + a.L152 + a.L153 + a.L157 - a.L158 + a.L159) +
                      (a.L170 + a.L171 + a.L178) + (a.L180 + a.L181) +
                      (a.L190 + a.L191 + a.L192 + a.L193 + a.L194 + a.L195 + a.L196 + a.L197 + a.L198 - a.L199)) +
                     ((a.L200 + a.L201) + (a.L210 - a.L211) +
                      (a.L2201 - a.L2202 + a.L221 - a.L222 + a.L226 + a.L228 - a.L229) +
                      (a.L231 + a.L232 + a.L233 + a.L235 + a.L236 - a.L237 - a.L239) +
                      (a.L240 - a.L241 + a.L242 - a.L243 - a.L244 + a.L245 - a.L246 - a.L247 + a.L248 - a.L249) +
                      (a.L250 + a.L251 + a.L252 + a.L253 + a.L254 + a.L255 + a.L256 - a.L257 + a.L258 + a.L259) +
                      (a.L260 + a.L261 + a.L262 + a.L263 + a.L264 + a.L267 - a.L268 + a.L269) +
                      (a.L271 + a.L272 + a.L277 - a.L278 + a.L279) + (a.L280 + a.L281) +
                      (a.L291 + a.L292 + a.L293 + a.L294 + a.L295 + a.L296 + a.L297 - a.L298 - a.L299)))

        # pasif için;
        s300 = s300 + a.L300
        s301 = s301 + a.L303
        s302 = s302 + a.L3202
        s303 = s303 + a.L3201
        s304 = s304 + (a.L103 + a.L321 - a.L322)
        s312 = s312 + (a.L340 + a.L349)
        s305 = s305 + a.L331
        s306 = s306 + a.L338
        s307 = s307 + (a.L332 + a.L333)
        s308 = s308 + (a.L301 - a.L302)
        s309 = s309 + (a.L370 - a.L371 + a.L372 + a.L373 + a.L379)
        s310 = s310 + (a.L360 + a.L361 + a.L368 + a.L369)
        s311 = s311 + (a.L309 + a.L329 + a.L335 + a.L336 + a.L381 + a.L391 + a.L392 + a.L393 + a.L394 + a.L397 + a.L399)
        # s3 = L3 yani (L30 + L32 + L33 + L34 + L35 + L36 + L37 + L38 + L39) hesaplaması KV Yabancı Kaynaklar;
        s3 = s3 + ((a.L300 + a.L301 - a.L302 + a.L303 + a.L304 + a.L305 + a.L306 - a.L308 + a.L309) +
                   (a.L3201 + a.L3202 + a.L321 - a.L322 + a.L326 + a.L329) +
                   (a.L331 + a.L332 + a.L333 + a.L335 + a.L336 - a.L337 + a.L338) + (a.L340 + a.L349) +
                   (a.L350 + a.L351 + a.L358) + (a.L360 + a.L361 + a.L368 + a.L369) +
                   (a.L370 - a.L371 + a.L372 + a.L373 + a.L379) + (a.L380 + a.L381) +
                   (a.L391 + a.L392 + a.L393 + a.L394 + a.L397 + a.L399))
        s400 = s400 + a.L400
        s401 = s401 + (a.L304 + a.L305 + a.L306 + a.L405 + a.L407 - (a.L308 + a.L408))
        s402 = s402 + (a.L420 + a.L421 - a.L422)
        s403 = s403 + a.L431
        s404 = s404 + (a.L432 + a.L433)
        s405 = s405 + (a.L409 + a.L426 + a.L429 + a.L436 - a.L437 + a.L438 + (a.L440 + a.L449) + (a.L472 + a.L479) +
                       (a.L480 + a.L481) + (a.L492 + a.L493 + a.L496 + a.L499))
        s406 = s406 + ((a.L350 + a.L351 + a.L358) + a.L410)
        s407 = s407 + (a.L401 + a.L402)
        s408 = s408 + a.L472
        #  s4 = L4 yani (L40 + L41 + L42 + L43 + L44 + L47 + L48 + L49) hesaplaması UV Yabancı Kaynaklar;
        s4 = s4 + ((a.L400 + a.L401 - a.L402 + a.L405 + a.L407 - a.L408 + a.L409) + a.L410 +
                   (a.L420 + a.L421 - a.L422 + a.L426 + a.L429) +
                   (a.L431 + a.L432 + a.L433 + a.L436 - a.L437 + a.L438) +
                   (a.L440 + a.L449) + (a.L472 + a.L479) + (a.L480 + a.L481) + (a.L492 + a.L493 + a.L496 + a.L499))
        s500 = s500 + a.L500
        s501 = s501 + (a.L500 - a.L501 + a.L502 - a.L503)
        s502 = s502 + (a.L502 - a.L503)
        s503 = s503 + (a.L540 + a.L541 + a.L542 + a.L543 + a.L548 + a.L549)
        s504 = s504 + (a.L522 + a.L523)
        s505 = s505 + ((a.L520 + a.L521 + a.L522 + a.L523 + a.L525 + a.L526 + a.L527 + a.L529) - (a.L522 + a.L523))
        s506 = s506 + (a.L570 - a.L580)
        s507 = s507 + (a.L590 - a.L591)
        s508 = s508 + (a.L128 + a.L228 - (a.L129 + a.L229 + a.L239))
        #  s5 = L5 - s508 hesaplaması L5 = (L50 + L52 + L54 - L55 + L56 + L57 - L58 + L59) Özkaynak toplamı;
        s5 = s5 + (((a.L500 - a.L501 + a.L502 - a.L503) +
                    (a.L520 + a.L521 + a.L522 + a.L523 + a.L525 + a.L526 + a.L527 + a.L529) +
                    (a.L540 + a.L541 + a.L542 + a.L543 + a.L548 + a.L549) - a.L551 +
                    (a.L560 - a.L561 + a.L562 - a.L563) + a.L570 - a.L580 + (a.L590 - a.L591)) -
                    (a.L128 + a.L228 - (a.L129 + a.L229 + a.L239)))
        s02 = s02 + (((a.L300 + a.L301 - a.L302 + a.L303 + a.L304 + a.L305 + a.L306 - a.L308 + a.L309) +
                      (a.L3201 + a.L3202 + a.L321 - a.L322 + a.L326 + a.L329) +
                      (a.L331 + a.L332 + a.L333 + a.L335 + a.L336 - a.L337 + a.L338) + (a.L340 + a.L349) +
                      (a.L350 + a.L351 + a.L358) + (a.L360 + a.L361 + a.L368 + a.L369) +
                      (a.L370 - a.L371 + a.L372 + a.L373 + a.L379) + (a.L380 + a.L381) +
                      (a.L391 + a.L392 + a.L393 + a.L394 + a.L397 + a.L399)) +
                     ((a.L400 + a.L401 - a.L402 + a.L405 + a.L407 - a.L408 + a.L409) + a.L410 +
                      (a.L420 + a.L421 - a.L422 + a.L426 + a.L429) +
                      (a.L431 + a.L432 + a.L433 + a.L436 - a.L437 + a.L438) + (a.L440 + a.L449) +
                      (a.L472 + a.L479) + (a.L480 + a.L481) + (a.L492 + a.L493 + a.L496 + a.L499)) +
                     ((a.L500 - a.L501 + a.L502 - a.L503) +
                      (a.L520 + a.L521 + a.L522 + a.L523 + a.L525 + a.L526 + a.L527 + a.L529) +
                      (a.L540 + a.L541 + a.L542 + a.L543 + a.L548 + a.L549) - a.L551 +
                      (a.L560 - a.L561 + a.L562 - a.L563) + a.L570 - a.L580 + (a.L590 - a.L591)))
        # Gelir Tablosu için;
        s600 = s600 + a.L600
        s601 = s601 + a.L601
        s602 = s602 + a.L602
        s60 = s60 + (a.L600 + a.L601 + a.L602 + a.L603 + a.L604)
        s610 = s610 + a.L610
        s611 = s611 + a.L611
        s612 = s612 + a.L612
        s61 = s61 + (a.L610 + a.L611 + a.L612)
        s620 = s620 + a.L620
        s621 = s621 + a.L621
        s622 = s622 + a.L622
        s623 = s623 + a.L623
        s628 = s628 + a.L628
        s62 = s62 + (a.L620 + a.L621 + a.L622 + a.L623 + a.L624 + a.L625 + a.L626 + a.L627 + a.L628)
        s630 = s630 + a.L630
        s631 = s631 + a.L631
        s632 = s632 + a.L632
        s634 = s634 + a.L634
        s63 = s63 + (a.L630 + a.L631 + a.L632 + a.L633 + a.L634)
        s66 = s66 + (a.L660 + a.L661)
        s64 = s64 + (a.L640 + a.L641 + a.L642 + a.L643 + a.L644 + a.L645 + a.L646 + a.L647 + a.L648 + a.L649)
        s65 = s65 + (a.L653 + a.L654 + a.L655 + a.L656 + a.L657 + a.L658 + a.L659)
        s67 = s67 + (a.L671 + a.L677 + a.L678 + a.L679)
        s68 = s68 + (a.L680 + a.L681 + a.L687 + a.L688 + a.L689)
        s690 = s690 + a.L690
    # for döngüsü bitti

    s11 = (s112 + s113 + s115 + s110 + s111 + s114 + s116 + s117)
    s15 = (s150 + s159 + s151 + s152)
    s220 = (s210 + s211 + s212 + s213 + s214 + s215 + s216 + s217 + s218 + s219)
    s20 = (s221 + s222 + s223 + s224)
    s21 = (s20 - s225)
    s2 = (s220 + s21)  # Duran Varlıklar
    s34 = (s3 + s4)  # Borçlar toplamı (Toplam Yabancı Kaynaklar)
    s03 = (s60 - s61)  # Net Satışlar
    s04 = (s03 - s62)  # Gayrisafi satış karı
    s05 = (s04 - s63)  # Faaliyet Karı
    s06 = (s05 + s64 - s65 - s66 + s67 - s68)  # vergi öncesi kar
    s6 = (s06 - s690)  # Net kar

    akt = [s110, s111, s112, s113, s114, s115, s116, s117, s11, s150, s151, s152, s159, s15, s1, s210, s211, s212, s213,
           s214, s215, s216, s217, s218, s219, s220, s221, s222, s223, s224, s20, s225, s21, s226, s2, s01]
    aktif_tablosu = [(aktifler[i], akt[i]) for i in range(0, len(akt))]

    psf = [s300, s301, s302, s303, s304, s312, s305, s306, s307, s308, s309, s310, s311, s3, s400, s401, s402, s403,
           s404,
           s405, s406, s407, s408, s4, s34, s500, s501, s502, s503, s504, s505, s506, s507, s508, s5, s02]
    pasif_tablosu = [(pasifler[i], psf[i]) for i in range(0, len(psf))]

    glr = [s600, s601, s602, s60, s610, s611, s612, s61, s03, s620, s621, s622, s623, s628, s62, s04, s630,
           s631, s632, s634, s63, s66, s05, s64, s65, s06, s690, s6]
    gelir_tablosu = [(gelir[i], glr[i]) for i in range(0, len(glr))]

    # Oran analizlerine ilişkin hesaplamalar;
    nis = (s1 - s3)
    if (s05 + s64) != 0:
        mg1 = float(format(((s63 + s65 + s66) * 100 / (s05 + s64)), '.2f'))
    else:
        mg1 = 0
    # finansal göstergeler;
    if s3 != 0:
        fg1 = float(format((s1 / s3), '.2f'))
    else:
        fg1 = 0
    if s3 != 0:
        fg2 = float(format(((s1 - L15) / s3), '.2f'))
    else:
        fg2 = 0
    if s3 != 0:
        fg3 = float(format((s111 / s3), '.2f'))
    else:
        fg3 = 0
    if s5 != 0:
        fg4 = float(format(((s3 + s4) * 100 / s5), '.2f'))
    else:
        fg4 = 0
    if s02 != 0:
        fg5 = float(format(((s3 + s4) * 100 / s02), '.2f'))
    else:
        fg5 = 0
    if s60 != 0:
        fg6 = float(format(((s3 + s4) * 100 / s60), '.2f'))
    else:
        fg6 = 0
    if s01 != 0:
        fg7 = float(format((s5 * 100 / s01), '.2f'))
    else:
        fg7 = 0
    if s501 != 0:
        fg8 = float(format(((s503 + s506) * 100 / s501), '.2f'))
    else:
        fg8 = 0
    finansal_g = [fg1, fg2, fg3, fg4, fg5, fg6, fg7, fg8]
    finansal_gostergeler = [(finansal[i], finansal_g[i]) for i in range(0, len(finansal_g))]

    if L12 != 0:
        ag1 = float(format((s03 / L12), '.2f'))
    else:
        ag1 = 0
    if ag1 != 0:
        ag2 = float(format((365 / (s03 / L12)), '.2f'))
    else:
        ag2 = 0
    if L15 != 0:
        ag3 = float(format((s62 / L15), '.2f'))
    else:
        ag3 = 0
    if ag3 != 0:
        ag4 = float(format((365 / (s62 / L15)), '.2f'))
    else:
        ag4 = 0
    if s01 != 0:
        ag5 = float(format((s03 / s01), '.2f'))
    else:
        ag5 = 0
    aktivite_g = [ag1, ag2, ag3, ag4, ag5]
    aktivite_gostergeleri = [(aktivite[i], aktivite_g[i]) for i in range(0, len(aktivite_g))]

    if s03 != 0:
        kg1 = float(format((s06 * 100 / s03), '.2f'))
    else:
        kg1 = 0
    if s5 != 0:
        kg2 = float(format((s6 * 100 / s5), '.2f'))
    else:
        kg2 = 0
    if s04 != 0:
        kg3 = float(format((s66 * 100 / s04), '.2f'))
    else:
        kg3 = 0

    kg4 = (s05 - L257)

    if (s1 + s2) != 0:
        kg5 = float(format((s6 * 100 / (s1 + s2)), '.2f'))
    else:
        kg5 = 0
    if s5 != 0:
        kg6 = float(format((s6 * 100 / s5), '.2f'))
    else:
        kg6 = 0
    if s03 != 0:
        kg7 = float(format((s6 * 100 / s03), '.2f'))
    else:
        kg7 = 0
    if s5 != 0:
        kg8 = float(format((s6 / s5), '.2f'))
    else:
        kg8 = 0
    if s02 != 0:
        kg9 = float(format(((s06 - s66) * 100 / s02), '.2f'))
    else:
        kg9 = 0
    karlilik_g = [kg1, kg2, kg3, kg4, kg5, kg6, kg7, kg8, kg9]
    karlilik_gostergeleri = [(karlilik[i], karlilik_g[i]) for i in range(0, len(karlilik_g))]

    context = {
        'a': akt, 'p': psf, 'g': glr,
        'AT': aktif_tablosu, 'PT': pasif_tablosu, 'GT': gelir_tablosu,
        'FG': finansal_gostergeler, 'KG': karlilik_gostergeleri, 'AG': aktivite_gostergeleri,
        'finansal_g': finansal_g, 'aktivite_g': aktivite_g, 'karlilik_g': karlilik_g,
        'nis': nis, 'mg1': mg1
    }
    return context


def spreadhesaplama(budget):
    # Aktif Hesaplar
    L10 = budget.L100 + budget.L101 + budget.L102 - budget.L103 + budget.L108
    L11 = budget.L110 + budget.L111 + budget.L112 + budget.L118 - budget.L119
    L12 = (budget.L1201 + budget.L1202 + budget.L121 - budget.L122 + budget.L126
           + budget.L127 + budget.L128 - budget.L129)
    L120 = (budget.L1201 + budget.L1202)
    L13 = (budget.L131 + budget.L132 + budget.L133 + budget.L135
           + budget.L136 - budget.L137 + budget.L138 - budget.L139)
    L15 = (budget.L150 + budget.L151 + budget.L152 + budget.L153 + budget.L157 - budget.L158 + budget.L159)
    L17 = (budget.L170 + budget.L171 + budget.L178)
    L18 = (budget.L180 + budget.L181)
    L19 = (budget.L190 + budget.L191 + budget.L192 + budget.L193 + budget.L194 + budget.L195
           + budget.L196 + budget.L197 + budget.L198 - budget.L199)
    L1 = (L10 + L11 + L12 + L13 + L15 + L17 + L18 + L19)  # Dönen Varlıklar
    L20 = (budget.L200 + budget.L201)
    L21 = (budget.L210 - budget.L211)
    L22 = (budget.L2201 - budget.L2202 + budget.L221 - budget.L222 + budget.L226 + budget.L228 - budget.L229)
    L220 = (budget.L2201 - budget.L2202)
    L23 = (budget.L231 + budget.L232 + budget.L233 + budget.L235
           + budget.L236 - budget.L237 - budget.L239)
    L24 = (budget.L240 - budget.L241 + budget.L242 - budget.L243 - budget.L244
           + budget.L245 - budget.L246 - budget.L247 + budget.L248 - budget.L249)
    L25 = (budget.L250 + budget.L251 + budget.L252 + budget.L253 + budget.L254
           + budget.L255 + budget.L256 - budget.L257 + budget.L258 + budget.L259)
    L26 = (budget.L260 + budget.L261 + budget.L262 + budget.L263 + budget.L264
           + budget.L267 - budget.L268 + budget.L269)
    L27 = (budget.L271 + budget.L272 + budget.L277 - budget.L278 + budget.L279)
    L28 = (budget.L280 + budget.L281)
    L29 = (budget.L291 + budget.L292 + budget.L293 + budget.L294 + budget.L295 + budget.L296
           + budget.L297 - budget.L298 - budget.L299)
    L2 = (L20 + L21 + L22 + L23 + L24 + L25 + L26 + L27 + L28 + L29)  # Duran Varlıklar
    L01 = (L1 + L2)  # Aktif Toplam

    # Pasif Hesaplar
    L30 = (budget.L300 + budget.L301 - budget.L302 + budget.L303 + budget.L304
           + budget.L305 + budget.L306 - budget.L308 + budget.L309)
    L320 = (budget.L3201 + budget.L3202)
    L32 = (budget.L3201 + budget.L3202 + budget.L321 - budget.L322 + budget.L326 + budget.L329)
    L33 = (budget.L331 + budget.L332 + budget.L333 + budget.L335 + budget.L336 - budget.L337 + budget.L338)
    L34 = (budget.L340 + budget.L349)
    L35 = (budget.L350 + budget.L351 + budget.L358)
    L36 = (budget.L360 + budget.L361 + budget.L368 + budget.L369)
    L37 = (budget.L370 - budget.L371 + budget.L372 + budget.L373 + budget.L379)
    L38 = (budget.L380 + budget.L381)
    L39 = (budget.L391 + budget.L392 + budget.L393 + budget.L394 + budget.L397 + budget.L399)
    L3 = (L30 + L32 + L33 + L34 + L35 + L36 + L37 + L38 + L39)  # Kısa Vadeli Yabancı Kaynaklar
    L40 = (budget.L400 + budget.L401 - budget.L402 + budget.L405 + budget.L407 - budget.L408 + budget.L409)
    L41 = budget.L410
    L42 = (budget.L420 + budget.L421 - budget.L422 + budget.L426 + budget.L429)
    L43 = (budget.L431 + budget.L432 + budget.L433 + budget.L436 - budget.L437 + budget.L438)
    L44 = (budget.L440 + budget.L449)
    L47 = (budget.L472 + budget.L479)
    L48 = (budget.L480 + budget.L481)
    L49 = (budget.L492 + budget.L493 + budget.L496 + budget.L499)
    L4 = (L40 + L41 + L42 + L43 + L44 + L47 + L48 + L49)  # Uzun Vadeli Yabancı Kaynaklar
    L50 = (budget.L500 - budget.L501 + budget.L502 - budget.L503)
    L52 = (budget.L520 + budget.L521 + budget.L522 + budget.L523
           + budget.L525 + budget.L526 + budget.L527 + budget.L529)
    L54 = (budget.L540 + budget.L541 + budget.L542 + budget.L543 + budget.L548 + budget.L549)
    L55 = budget.L551
    L56 = (budget.L560 - budget.L561 + budget.L562 - budget.L563)
    L57 = budget.L570
    L58 = budget.L580
    L59 = (budget.L590 - budget.L591)
    L5 = (L50 + L52 + L54 - L55 + L56 + L57 - L58 + L59)  # Özkaynaklar Toplamı
    L02 = (L3 + L4 + L5)  # Pasif Toplam

    # Gelir Tablosu
    L60 = (budget.L600 + budget.L601 + budget.L602 + budget.L603 + budget.L604)
    L61 = (budget.L610 + budget.L611 + budget.L612)
    L03 = (L60 - L61)  # Net Satışlar
    L62 = (budget.L620 + budget.L621 + budget.L622 + budget.L623 + budget.L624
           + budget.L625 + budget.L626 + budget.L627 + budget.L628)
    L04 = (L03 - L62)  # Gayrisafi Satış Karı
    L63 = (budget.L630 + budget.L631 + budget.L632 + budget.L633 + budget.L634)
    L05 = (L04 - L63)  # Faaliyet Karı
    L64 = (budget.L640 + budget.L641 + budget.L642 + budget.L643 + budget.L644
           + budget.L645 + budget.L646 + budget.L647 + budget.L648 + budget.L649)
    L65 = (budget.L653 + budget.L654 + budget.L655 + budget.L656 + budget.L657 + budget.L658 + budget.L659)
    L66 = (budget.L660 + budget.L661)
    L67 = (budget.L671 + budget.L677 + budget.L678 + budget.L679)
    L68 = (budget.L680 + budget.L681 + budget.L687 + budget.L688 + budget.L689)
    L06 = (L05 + L64 - L65 - L66 + L67 - L68)  # Dönem Karı veya zararı
    L6 = (L06 - budget.L690)  # Dönem Net Karı/Zararı
    # Spread ekranında görünecek hesaplamalar;

    # Oran analizlerine ilişkin hesaplamalar;
    nis = (L1 - L3)
    if (L05 + L64) != 0:
        mg1 = float(format(((L63 + L65 + L66) * 100 / (L05 + L64)), '.2f'))
    else:
        mg1 = 0
    # finansal göstergeler;
    if L3 != 0:
        fg1 = float(format((L1 / L3), '.2f'))
    else:
        fg1 = 0
    if L3 != 0:
        fg2 = float(format(((L1 - L15) / L3), '.2f'))
    else:
        fg2 = 0
    if L3 != 0:
        fg3 = float(format((L11 / L3), '.2f'))
    else:
        fg3 = 0
    if L5 != 0:
        fg4 = float(format(((L3 + L4) * 100 / L5), '.2f'))
    else:
        fg4 = 0
    if L02 != 0:
        fg5 = float(format(((L3 + L4) * 100 / L02), '.2f'))
    else:
        fg5 = 0
    if L60 != 0:
        fg6 = float(format(((L3 + L4) * 100 / L60), '.2f'))
    else:
        fg6 = 0
    if L01 != 0:
        fg7 = float(format((L5 * 100 / L01), '.2f'))
    else:
        fg7 = 0
    if L50 != 0:
        fg8 = float(format(((L54 - L58) * 100 / L50), '.2f'))
    else:
        fg8 = 0
    fin_g = [fg1, fg2, fg3, fg4, fg5, fg6, fg7, fg8]
    finansal_gostergeler = [(finansal[i], fin_g[i]) for i in range(0, len(fin_g))]

    if L12 != 0:
        ag1 = float(format((L03 / L12), '.2f'))
    else:
        ag1 = 0
    if ag1 != 0:
        ag2 = float(format((365 / (L03 / L12)), '.2f'))
    else:
        ag2 = 0
    if L15 != 0:
        ag3 = float(format((L62 / L15), '.2f'))
    else:
        ag3 = 0
    if ag3 != 0:
        ag4 = float(format((365 / (L62 / L15)), '.2f'))
    else:
        ag4 = 0
    if L01 != 0:
        ag5 = float(format((L03 / L01), '.2f'))
    else:
        ag5 = 0
    aktivite_g = [ag1, ag2, ag3, ag4, ag5]
    aktivite_gostergeleri = [(aktivite[i], aktivite_g[i]) for i in range(0, len(aktivite_g))]

    if L03 != 0:
        kg1 = float(format((L06 * 100 / L03), '.2f'))
    else:
        kg1 = 0
    if L5 != 0:
        kg2 = float(format((L6 * 100 / L5), '.2f'))
    else:
        kg2 = 0
    if L04 != 0:
        kg3 = float(format((L66 * 100 / L04), '.2f'))
    else:
        kg3 = 0

    kg4 = (L05 - budget.L257)

    if (L1 + L2) != 0:
        kg5 = float(format((L6 * 100 / (L1 + L2)), '.2f'))
    else:
        kg5 = 0
    if L5 != 0:
        kg6 = float(format((L6 * 100 / L5), '.2f'))
    else:
        kg6 = 0
    if L03 != 0:
        kg7 = float(format((L6 * 100 / L03), '.2f'))
    else:
        kg7 = 0
    if L5 != 0:
        kg8 = float(format((L6 / L5), '.2f'))
    else:
        kg8 = 0
    if L02 != 0:
        kg9 = float(format(((L06 - L66) * 100 / L02), '.2f'))
    else:
        kg9 = 0
    karlilik_g = [kg1, kg2, kg3, kg4, kg5, kg6, kg7, kg8, kg9]
    karlilik_gostergeleri = [(karlilik[i], karlilik_g[i]) for i in range(0, len(karlilik_g))]

    # Spread tablosu için yapılacak hesaplamalar;
    # Aktif
    s110 = (budget.L100 + budget.L102)
    s111 = L11
    s112 = budget.L1201
    s113 = budget.L1202
    s114 = (budget.L101 + budget.L121)
    s115 = budget.L131
    s116 = (budget.L132 + budget.L133)
    s117 = (budget.L126 + budget.L127 + budget.L135 + budget.L136 + budget.L138 + L18 + L19)
    s11 = (s112 + s113 + s115 + s110 + s111 + s114 + s116 + s117)
    s150 = budget.L150
    s151 = (budget.L151 + budget.L152)
    s152 = (budget.L153 + budget.L157 - budget.L158)
    s159 = budget.L159
    s15 = (s150 + s159 + s151 + s152)
    s1 = L1
    s210 = ((budget.L240 + budget.L242 + budget.L245 + budget.L248)
            - (budget.L241 + budget.L243 + budget.L244 + budget.L246 + budget.L247 + budget.L249))
    s211 = (budget.L221 + budget.L222)
    s212 = (budget.L2201 + budget.L2202)
    s213 = budget.L226
    s214 = budget.L231
    s215 = (budget.L232 + budget.L233)
    s216 = (L17 + L20)
    s217 = (budget.L235 + budget.L236 + L26 + L27 + L28 + L29 - budget.L237)
    s218 = budget.L258
    s219 = budget.L259
    s220 = (s210 + s211 + s212 + s213 + s214 + s215 + s216 + s217 + s218 + s219)
    s221 = (budget.L250 + budget.L251 + budget.L252)
    s222 = budget.L253
    s223 = (budget.L254 + budget.L255 + budget.L256)
    s224 = L21
    s20 = (s221 + s222 + s223 + s224)
    s225 = budget.L257
    s21 = (s20 - s225)
    s226 = (L26 + L27)
    s2 = (s220 + s21)
    s01 = L01
    a = [s110, s111, s112, s113, s114, s115, s116, s117, s11, s150, s151, s152, s159, s15, s1, s210, s211, s212, s213,
         s214, s215, s216, s217, s218, s219, s220, s221, s222, s223, s224, s20, s225, s21, s226, s2, s01]
    aktif_tablosu = [(aktifler[i], a[i]) for i in range(0, len(a))]

    # Pasif
    s300 = budget.L300
    s301 = budget.L303
    s302 = budget.L3202
    s303 = budget.L3201
    s304 = (budget.L103 + budget.L321 - budget.L322)
    s312 = L34
    s305 = budget.L331
    s306 = budget.L338
    s307 = (budget.L332 + budget.L333)
    s308 = (budget.L301 - budget.L302)
    s309 = L37
    s310 = L36
    s311 = (budget.L309 + budget.L329 + budget.L335 + budget.L336 + budget.L381 + L39)
    s3 = L3
    s400 = budget.L400
    s401 = (budget.L304 + budget.L305 + budget.L306 + budget.L405 + budget.L407 - (budget.L308 + budget.L408))
    s402 = (budget.L420 + budget.L421 - budget.L422)
    s403 = budget.L431
    s404 = (budget.L432 + budget.L433)
    s405 = (budget.L409 + budget.L426 + budget.L429 + budget.L436 - budget.L437 + budget.L438 + L44 + L47 + L48 + L49)
    s406 = (L35 + L41)
    s407 = (budget.L401 + budget.L402)
    s408 = budget.L472
    s4 = L4
    s34 = (L3 + L4)
    s500 = budget.L500
    s501 = L50
    s502 = (budget.L502 - budget.L503)
    s503 = L54
    s504 = (budget.L522 + budget.L523)
    s505 = (L52 - s504)
    s506 = (L57 - L58)
    s507 = L59
    s508 = (budget.L128 + budget.L228 - (budget.L129 + budget.L229 + budget.L239))
    s5 = (L5 - s508)
    s02 = L02
    p = [s300, s301, s302, s303, s304, s312, s305, s306, s307, s308, s309, s310, s311, s3, s400, s401, s402, s403, s404,
         s405, s406, s407, s408, s4, s34, s500, s501, s502, s503, s504, s505, s506, s507, s508, s5, s02]
    pasif_tablosu = [(pasifler[i], p[i]) for i in range(0, len(p))]

    # Gelir Tablosu
    s600 = budget.L600
    s601 = budget.L601
    s602 = budget.L602
    s60 = L60
    s610 = budget.L610
    s611 = budget.L611
    s612 = budget.L612
    s61 = L61
    s03 = L03
    s620 = budget.L620
    s621 = budget.L621
    s622 = budget.L622
    s623 = budget.L623
    s628 = budget.L628
    s62 = L62
    s04 = L04
    s630 = budget.L630
    s631 = budget.L631
    s632 = budget.L632
    s634 = budget.L634
    s63 = L63
    s66 = L66
    s05 = L05
    s64 = L64
    s65 = L65
    s06 = L06
    s690 = budget.L690
    s6 = L6
    g = [s600, s601, s602, s60, s610, s611, s612, s61, s03, s620, s621, s622, s623, s628, s62, s04, s630,
         s631, s632, s634, s63, s66, s05, s64, s65, s06, s690, s6]
    gelir_tablosu = [(gelir[i], g[i]) for i in range(0, len(g))]

    context = {
        'AT': aktif_tablosu, 'PT': pasif_tablosu, 'GT': gelir_tablosu,
        'FG': finansal_gostergeler, 'AG': aktivite_gostergeleri, 'KG': karlilik_gostergeleri, 'nis': nis, 'mg1': mg1
    }

    return context

