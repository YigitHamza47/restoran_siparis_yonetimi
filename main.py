from peewee import *

# Veritabanı bağlantısı
db = SqliteDatabase('restoran_siparis_yonetimi.db')


# Modeller (Tablolar)
class BaseModel(Model):
    class Meta:
        database = db


class Urun(BaseModel):
    isim = CharField(unique=True)
    fiyat = FloatField()


class Siparis(BaseModel):
    toplam_tutar = FloatField()
    tarih = DateField(constraints=[SQL('DEFAULT CURRENT_DATE')])


class SiparisDetay(BaseModel):
    siparis = ForeignKeyField(Siparis, backref='detaylar')
    urun = ForeignKeyField(Urun, backref='siparisler')
    miktar = IntegerField()


# Veritabanını oluştur
db.connect()
db.create_tables([Urun, Siparis, SiparisDetay])


# Ürün ekleme fonksiyonu
def urun_ekle(isim, fiyat):
    urun = Urun.create(isim=isim, fiyat=fiyat)
    print(f"Ürün eklendi: {isim}, {fiyat} TL")


# Sipariş oluşturma fonksiyonu
def siparis_olustur():
    toplam_tutar = 0
    siparis_urunler = []

    while True:
        urun_id = int(input("Eklemek istediğiniz ürün ID'si (bitirmek için 0): "))
        if urun_id == 0:
            break
        miktar = int(input("Miktar: "))

        try:
            urun = Urun.get(Urun.id == urun_id)
            fiyat = urun.fiyat
            isim = urun.isim
            toplam_tutar += fiyat * miktar
            siparis_urunler.append((urun_id, miktar, fiyat, isim))
        except Urun.DoesNotExist:
            print("Geçersiz ürün ID'si.")

    if toplam_tutar > 0:
        siparis = Siparis.create(toplam_tutar=toplam_tutar)
        for urun_id, miktar, fiyat, isim in siparis_urunler:
            urun = Urun.get(Urun.id == urun_id)
            SiparisDetay.create(siparis=siparis, urun=urun, miktar=miktar)

        print(f"Sipariş oluşturuldu. Toplam tutar: {toplam_tutar} TL")
    else:
        print("Sipariş oluşturulamadı. Lütfen geçerli ürünler ekleyin.")


# Sipariş detaylarını listeleme fonksiyonu
def siparis_detaylari_goster():
    for siparis in Siparis.select():
        print(f"Sipariş ID: {siparis.id}, Tarih: {siparis.tarih}, Toplam Tutar: {siparis.toplam_tutar} TL")
        for detay in siparis.detaylar:
            print(f"  Ürün: {detay.urun.isim}, Miktar: {detay.miktar}, Fiyat: {detay.urun.fiyat} TL")


# Ürün listeleme fonksiyonu
def urunleri_listele():
    for urun in Urun.select():
        print(f"ID: {urun.id}, İsim: {urun.isim}, Fiyat: {urun.fiyat} TL")


# Ana program
if __name__ == "__main__":
    while True:
        print("\n1. Ürün Ekle")
        print("2. Ürünleri Listele")
        print("3. Sipariş Oluştur")
        print("4. Sipariş Detaylarını Göster")
        print("5. Çıkış")

        secim = input("Seçiminizi yapın: ")

        if secim == '1':
            isim = input("Ürün ismi: ")
            fiyat = float(input("Ürün fiyatı: "))
            urun_ekle(isim, fiyat)
        elif secim == '2':
            urunleri_listele()
        elif secim == '3':
            siparis_olustur()
        elif secim == '4':
            siparis_detaylari_goster()
        elif secim == '5':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

    # Bağlantıyı kapat
    db.close()
