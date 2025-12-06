import tkinter as tk
from tkinter import messagebox
import random
import time # Animasyon için

# --- OYUN AYARLARI ---

KISILER = [
    "Sana",
    "Karşındakine",
    "İkiniz de"
]

# (Bu kısma 100+ görev listesi, önceki koddan kopyalanarak buraya entegre edilmelidir.)
# Kodun okunabilirliği için temsili görev listesi:
GOREVLER_ORIJINAL = [
    ("30 saniye boyunca karşındakine bir 'superstar' gibi imza dağıt.", 1),
    ("Karşındakinin en sevdiği yemeği 5 saniye boyunca taklit et.", 1),
    ("Karşındakine içten bir iltifat et (aynı iltifat daha önce yapılmamış olmalı).", 2),
    ("Eğer bir film çekseydiniz, başlık, ana karakter ve konusu ne olurdu?", 3),
    ("Hayatında yaptığın ve şu an gülerek hatırladığın bir hatayı anlat.", 3),
    ("1 dakika boyunca karşıdakinin sana verdiği bir kelimeyi kullanmadan, bir konu hakkında konuş.", 2),
] * 20 # 120 görev simülasyonu
random.shuffle(GOREVLER_ORIJINAL)
GOREVLER = GOREVLER_ORIJINAL 


# --- Tkinter Uygulaması ---

class YildizZariOyunu:
    def __init__(self, master):
        self.master = master
        master.title("🌟 Etkileşimli Görev Zarı")
        master.geometry("650x550")
        master.resizable(False, False)
        
        self.arka_plan_rengi = "#34495e"
        self.vurgu_rengi = "#f1c40f"
        self.master.configure(bg=self.arka_plan_rengi)

        self.oyuncu_sirasi = 1 
        self.puanlar = {"Oyuncu 1": 0, "Oyuncu 2": 0}
        self.kullanilmis_gorevler = set()
        self.gorev_puani = 0 
        self.zar_atik_mi = False # Zarın atılıp atılmadığını kontrol eden flag

        self.setup_ui()
        self.guncelle_oyuncu_bilgisi()

    def setup_ui(self):
        # 1. Puan Tablosu
        self.puan_frame = tk.Frame(self.master, bg=self.arka_plan_rengi)
        self.puan_frame.pack(pady=15, padx=10, fill='x')

        self.p1_label = tk.Label(self.puan_frame, text="P1: 0 Puan", font=("Helvetica", 16, "bold"), bg=self.arka_plan_rengi, fg="red")
        self.p1_label.pack(side=tk.LEFT, padx=50)

        self.p2_label = tk.Label(self.puan_frame, text="P2: 0 Puan", font=("Helvetica", 16, "bold"), bg=self.arka_plan_rengi, fg="green")
        self.p2_label.pack(side=tk.RIGHT, padx=50)
        
        # 2. Ana Başlık
        tk.Label(self.master, text="YILDIZ ZARI", font=("Georgia", 30, "bold"), bg=self.arka_plan_rengi, fg=self.vurgu_rengi).pack(pady=10)

        # 3. Oyuncu Sırası Bilgisi
        self.oyuncu_label = tk.Label(self.master, text="", font=("Arial", 18, "bold"), bg=self.arka_plan_rengi, fg="white")
        self.oyuncu_label.pack(pady=10)

        # 4. Etkileşimli Zar Görseli (Yeni)
        self.dice_label = tk.Label(self.master, text="\u2680", # Temsili bir zar emojisi (Unicode)
                                   font=("Arial", 72), bg=self.arka_plan_rengi, fg="white",
                                   cursor="hand2") # Tıklanabilir olduğunu göstermek için imleci değiştir
        self.dice_label.pack(pady=10)
        # Tıklama olayını zar atma fonksiyonuna bağlama
        self.dice_label.bind("<Button-1>", self.zar_at_etkilesimi)

        # 5. Kişi/Görev/Puan Bilgisi Etiketleri
        self.kisi_label = tk.Label(self.master, text="KİŞİ: Tıklama Bekleniyor...", font=("Arial", 14), bg=self.arka_plan_rengi, fg="#bdc3c7", wraplength=550)
        self.kisi_label.pack(pady=5)
        self.gorev_label = tk.Label(self.master, text="GÖREV: Tıklama Bekleniyor...", font=("Arial", 16, "italic"), bg=self.arka_plan_rengi, fg="#bdc3c7", wraplength=550)
        self.gorev_label.pack(pady=10)
        self.puan_bilgi_label = tk.Label(self.master, text="Puan: -", font=("Arial", 14, "bold"), bg=self.arka_plan_rengi, fg=self.vurgu_rengi)
        self.puan_bilgi_label.pack(pady=5)
        
        # 6. Kontrol Butonları
        self.kontrol_frame = tk.Frame(self.master, bg=self.arka_plan_rengi)
        self.kontrol_frame.pack(pady=5)
        
        self.basarili_button = tk.Button(self.kontrol_frame, text="GÖREV BAŞARILI (+Puan)", command=lambda: self.gorev_sonucu(True),
                                        font=("Arial", 14), bg="#2ecc71", fg="white",
                                        activebackground="#27ae60", width=25, state=tk.DISABLED)
        self.basarili_button.pack(side=tk.LEFT, padx=5)
        
        self.basarisiz_button = tk.Button(self.kontrol_frame, text="GÖREV BAŞARISIZ (0 Puan)", command=lambda: self.gorev_sonucu(False),
                                        font=("Arial", 14), bg="#e74c3c", fg="white",
                                        activebackground="#c0392b", width=25, state=tk.DISABLED)
        self.basarisiz_button.pack(side=tk.RIGHT, padx=5)
        
    def guncelle_oyuncu_bilgisi(self):
        """Sıra ve puan bilgilerini günceller."""
        self.p1_label.config(text=f"P1: {self.puanlar['Oyuncu 1']} Puan")
        self.p2_label.config(text=f"P2: {self.puanlar['Oyuncu 2']} Puan")
        
        if self.oyuncu_sirasi == 1:
            self.oyuncu_label.config(text="OYUNCU 1 SIRASI (KIRMIZI) - ZAR AT", fg="red")
            self.dice_label.config(fg="red")
        else:
            self.oyuncu_label.config(text="OYUNCU 2 SIRASI (YEŞİL) - ZAR AT", fg="green")
            self.dice_label.config(fg="green")
            
    def zar_at_etkilesimi(self, event):
        """Zar görseline tıklanınca tetiklenir."""
        if self.zar_atik_mi:
            messagebox.showwarning("Dikkat", "Lütfen önce mevcut görevi tamamlayın!")
            return

        self.dice_label.config(cursor="wait")
        self.zar_atik_mi = True
        self.zar_animasyonu()

    def zar_animasyonu(self):
        """Zar atma efektini simüle eder ve ardından zar_at fonksiyonunu çağırır."""
        
        zar_karakterleri = ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"] # 1'den 6'ya zar emojileri
        
        def animasyon_adimi(sayac):
            if sayac > 0:
                self.dice_label.config(text=random.choice(zar_karakterleri))
                self.master.after(50, animasyon_adimi, sayac - 1) # 50 milisaniye sonra tekrar çağır
            else:
                self._zar_at_aslinda() # Animasyon bitince gerçek görevi göster
        
        animasyon_adimi(10) # 10 kere rastgele karakter değiştir

    def _zar_at_aslinda(self):
        """Gerçek görev seçimi ve etiketi güncelleme işlevi."""
        
        # Kullanılmamış görev bulma mantığı
        secilen_gorev_tuple = None
        for gorev_tuple in GOREVLER:
            if gorev_tuple not in self.kullanilmis_gorevler:
                secilen_gorev_tuple = gorev_tuple
                break
        
        if secilen_gorev_tuple is None:
            messagebox.showinfo("Oyun Bitti!", "Tüm görevler tamamlandı! Tebrikler!")
            self.dice_label.config(text="BİTTİ", font=("Arial", 36))
            return
            
        self.kullanilmis_gorevler.add(secilen_gorev_tuple)
        
        self.secilen_kisi = random.choice(KISILER)
        self.secilen_gorev, self.gorev_puani = secilen_gorev_tuple
        
        # Etiketleri güncelleme
        renk = "red" if self.oyuncu_sirasi == 1 else "green"
        
        self.kisi_label.config(text=f"KİŞİ: {self.secilen_kisi}", fg=renk)
        self.gorev_label.config(text=f"GÖREV: {self.secilen_gorev}", fg=self.vurgu_rengi)
        self.puan_bilgi_label.config(text=f"BU GÖREV: {self.gorev_puani} PUAN", fg=self.vurgu_rengi)
        
        # Kontrol butonlarını aktif et ve imleci sıfırla
        self.basarili_button.config(state=tk.NORMAL)
        self.basarisiz_button.config(state=tk.NORMAL)
        self.dice_label.config(cursor="no") # Görev atanana kadar tıklamayı engelle

        
    def gorev_sonucu(self, basarili):
        """Puanı işler ve sırayı değiştirir."""
        
        puan_ekle = self.gorev_puani if basarili else 0
        
        if self.oyuncu_sirasi == 1:
            self.puanlar["Oyuncu 1"] += puan_ekle
            sonraki_oyuncu = 2
        else:
            self.puanlar["Oyuncu 2"] += puan_ekle
            sonraki_oyuncu = 1

        mesaj = "BAŞARILI! Puan eklendi." if basarili else "BAŞARISIZ! Puan eklenmedi."
        messagebox.showinfo("Görev Sonucu", f"Oyuncu {self.oyuncu_sirasi} görevi tamamladı: {mesaj}")

        # Sırayı değiştir ve UI'ı sıfırla
        self.oyuncu_sirasi = sonraki_oyuncu
        self.zar_atik_mi = False # Yeni zar atışına izin ver

        self.kisi_label.config(text="KİŞİ: Tıklama Bekleniyor...", fg="#bdc3c7")
        self.gorev_label.config(text="GÖREV: Tıklama Bekleniyor...", fg="#bdc3c7")
        self.puan_bilgi_label.config(text="Puan: -", fg=self.vurgu_rengi)
        
        self.guncelle_oyuncu_bilgisi()
        
        # Kontrol butonlarını pasif yap ve zar imlecini aç
        self.basarili_button.config(state=tk.DISABLED)
        self.basarisiz_button.config(state=tk.DISABLED)
        self.dice_label.config(cursor="hand2", text="\u2680") # Zarı tekrar göster

# Ana pencereyi oluştur
root = tk.Tk()
gorev_oyunu = YildizZariOyunu(root)
root.mainloop()