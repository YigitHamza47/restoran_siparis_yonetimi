import sqlite3

conn = sqlite3.connect('restoran_siparis_yonetimi.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS urunler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT NOT NULL,
    fiyat REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS siparisler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    toplam_tutar REAL NOT NULL,
    tarih TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS siparis_detaylari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    siparis_id INTEGER NOT NULL,
    urun_id INTEGER NOT NULL,
    miktar INTEGER NOT NULL,
    FOREIGN KEY(siparis_id) REFERENCES siparisler(id),
    FOREIGN KEY(urun_id) REFERENCES urunler(id)
)
''')

conn.commit()


def urun_ekle(isim, fiyat):
    cursor.execute("INSERT INTO urunler (isim, fiyat) VALUES (?, ?)", (isim, fiyat))
    conn.commit()
    print(f"Ürün eklendi: {isim}, {fiyat} TL")


def siparis_olustur():
    toplam_tutar = 0
    siparis_urunler = []

    while True:
        urun_id = int(input("Eklemek istediğiniz ürün ID'si (bitirmek için 0): "))
        if urun_id == 0:
            break
        miktar = int(input("Miktar: "))

        cursor.execute("SELECT fiyat, isim FROM urunler WHERE id = ?", (urun_id,))
        urun = cursor.fetchone()

        if urun:
            fiyat, isim = urun
            toplam_tutar += fiyat * miktar
            siparis_urunler.append((urun_id, miktar, fiyat, isim))
        else:
            print("Geçersiz ürün ID'si.")

    if toplam_tutar > 0:
        cursor.execute("INSERT INTO siparisler (toplam_tutar, tarih) VALUES (?, date('now'))", (toplam_tutar,))
        siparis_id = cursor.lastrowid
        for urun_id, miktar, fiyat, isim in siparis_urunler:
            cursor.execute("INSERT INTO siparis_detaylari (siparis_id, urun_id, miktar) VALUES (?, ?, ?)",
                           (siparis_id, urun_id, miktar))

        conn.commit()
        print(f"Sipariş oluşturuldu. Toplam tutar: {toplam_tutar} TL")
    else:
        print("Sipariş oluşturulamadı. Lütfen geçerli ürünler ekleyin.")


def siparis_detaylari_goster():
    cursor.execute('''
    SELECT sd.siparis_id, u.isim, sd.miktar, u.fiyat, (sd.miktar * u.fiyat) AS toplam
    FROM siparis_detaylari sd
    JOIN urunler u ON sd.urun_id = u.id
    ''')
    detaylar = cursor.fetchall()
    print("Sipariş Detayları:")
    for detay in detaylar:
        print(
            f"Sipariş ID: {detay[0]}, Ürün: {detay[1]}, Miktar: {detay[2]}, Fiyat: {detay[3]} TL, Toplam: {detay[4]} TL")


def urunleri_listele():
    cursor.execute("SELECT * FROM urunler")
    urunler = cursor.fetchall()
    print("Ürün Listesi:")
    for urun in urunler:
        print(f"ID: {urun[0]}, İsim: {urun[1]}, Fiyat: {urun[2]} TL")


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

conn.close()
