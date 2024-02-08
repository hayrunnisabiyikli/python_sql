import tkinter as tk
from tkinter import messagebox
import pypyodbc
import random

# MSSQL bağlantısı
conn = pypyodbc.connect('Driver={SQL Server};'
                        'Server=PC\SQLEXPRESS;'
                        'Database=master;'
                        'Trusted_Connection=True;')

# Veritabanı üzerinde bir cursor oluştur
cur = conn.cursor()

# Giriş ekranı
class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Login Page")
        self.configure(bg="#c6e2ff")  # Arka plan rengi

        # Kullanıcı adı alanı
        self.label_username = tk.Label(self, text="E-posta:", bg="#c6e2ff", font=("Arial", 12))  # Arka plan rengi ve font ayarı
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        # Şifre alanı
        self.label_password = tk.Label(self, text="Şifre:", bg="#c6e2ff", font=("Arial", 12))  # Arka plan rengi ve font ayarı
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        # Kayıt ol butonu
        self.button_register = tk.Button(self, text="Kayıt Ol", command=self.register_page, bg="#1a8cff", fg="white", font=("Arial", 12))  # Arka plan rengi, yazı rengi ve font ayarı
        self.button_register.pack(pady=5)

        # Giriş yap butonu
        self.button_login = tk.Button(self, text="Giriş Yap", command=self.login, bg="#1a8cff", fg="white", font=("Arial", 12))  # Arka plan rengi, yazı rengi ve font ayarı
        self.button_login.pack(pady=5)

        # Google ile giriş yap (API entegrasyonu gerek çalışması için)
        self.button_google = tk.Button(self, text="Google ile Giriş Yap", command=self.google_login, bg="#db4a39", fg="white", font=("Arial", 12))
        self.button_google.pack(pady=5)

        # LinkedIn ile giriş yap (API entegrasyonu gerek çalışması için)
        self.button_linkedin = tk.Button(self, text="LinkedIn ile Giriş Yap", command=self.linkedin_login, bg="#0e76a8", fg="white", font=("Arial", 12))
        self.button_linkedin.pack(pady=5)

        # Paketleri sıkıca ayarlayın
        self.pack(fill=tk.BOTH, expand=True)

    def login(self):
        email = self.entry_username.get()
        password = self.entry_password.get()

        # Veritabanında kullanıcıyı kontrol et
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()

        if user:
            messagebox.showinfo("Başarılı", "Giriş Başarılı!")
            self.master.switch_frame(WelcomePage, user[1], user[2])  # Hoş geldiniz ekranına geçiş
        else:
            messagebox.showerror("Hata", "Hatalı Kullanıcı Adı veya Şifre!")

    def register_page(self):
        self.master.switch_frame(RegisterPage)  # Kayıt ol ekranına geçiş

    def google_login(self):
        pass  # Google ile giriş yap işlevselliği buraya eklenebilir

    def linkedin_login(self):
        pass  # LinkedIn ile giriş yap işlevselliği buraya eklenebilir


# Kayıt ekranı
class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Kayıt Ol")
        self.configure(bg="#c6e2ff")  # Arka plan rengi

        # Ad alanı
        self.label_name = tk.Label(self, text="Ad:", bg="#c6e2ff", font=("Arial", 12))  # Arka plan rengi ve font ayarı
        self.label_name.pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack(pady=5)

        # Soyad alanı
        self.label_surname = tk.Label(self, text="Soyad:", bg="#c6e2ff", font=("Arial", 12))  # Arka plan rengi ve font ayarı
        self.label_surname.pack()
        self.entry_surname = tk.Entry(self)
        self.entry_surname.pack(pady=5)

        # E-posta alanı
        self.label_email = tk.Label(self, text="E-posta:", bg="#c6e2ff", font=("Arial", 12))  # Arka plan rengi ve font ayarı
        self.label_email.pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack(pady=5)

        # Şifre alanı
        self.label_password = tk.Label(self, text="Şifre:", bg="#c6e2ff", font=("Arial", 12))  # Arka plan rengi ve font ayarı
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        # Şifre tekrarı alanı
        self.label_password_confirm = tk.Label(self, text="Şifre Tekrarı:", bg="#c6e2ff", font=("Arial", 12))  # Arka plan rengi ve font ayarı
        self.label_password_confirm.pack()
        self.entry_password_confirm = tk.Entry(self, show="*")
        self.entry_password_confirm.pack(pady=5)

        # Kayıt ol butonu
        self.button_register = tk.Button(self, text="Kayıt Ol", command=self.register, bg="#1a8cff", fg="white", font=("Arial", 12))  # Arka plan rengi, yazı rengi ve font ayarı
        self.button_register.pack(pady=5)

        # Geri butonu
        self.button_back = tk.Button(self, text="Geri", command=self.back_to_login, bg="#1a8cff", fg="white", font=("Arial", 12))  # Arka plan rengi, yazı rengi ve font ayarı
        self.button_back.pack(pady=5)

        # Paketleri sıkıca ayarlayın
        self.pack(fill=tk.BOTH, expand=True)

    def register(self):
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        password_confirm = self.entry_password_confirm.get()

        if password != password_confirm:
            messagebox.showerror("Hata", "Girilen şifreler eşleşmiyor!")
            return

        # Veritabanına kullanıcıyı ekle
        cur.execute("INSERT INTO users (name, surname, email, password) VALUES (?, ?, ?, ?)",
                    (name, surname, email, password))
        conn.commit()
        messagebox.showinfo("Başarılı", "Kayıt Başarılı!")

    def back_to_login(self):
        self.master.switch_frame(LoginPage)  # Giriş ekranına geçiş


# Hoş geldiniz ekranı
class WelcomePage(tk.Frame):
    def __init__(self, master, name, surname):
        super().__init__(master)
        self.master = master
        self.master.title("Hoş Geldiniz")
        self.configure(bg="#c6e2ff")  # Arka plan rengi

        label_welcome = tk.Label(self, text=f"Hoş Geldiniz!", bg="#c6e2ff", font=("Times New Roman", 16, "bold"))  # Arka plan rengi ve font ayarı
        label_welcome.pack()

        # Arka plana dalgalı bir görünüm eklemek için canvas oluştur
        canvas = tk.Canvas(self, bg="#c6e2ff", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)  # Paketleri sıkıca ayarlayın

        # Dalga efekti için renk listesi
        colors = ["#0066ff", "#0080ff", "#0099ff", "#00b3ff", "#00ccff"]

        # Dalga efekti için çokgenlerin çizilmesi
        for i in range(20):
            x1 = random.randint(0, 400)
            y1 = random.randint(0, 300)
            x2 = x1 + random.randint(50, 150)
            y2 = y1 + random.randint(50, 150)
            color = random.choice(colors)
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

        # Paketleri sıkıca ayarlayın
        self.pack(fill=tk.BOTH, expand=True)


# Ana uygulama sınıfı
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Uygulama")
        self.geometry("400x300")
        self._frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, *args)  # Değişiklik burada
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=tk.BOTH, expand=True)  # Paketleri sıkıca ayarlayın


if __name__ == "__main__":
    app = Application()
    app.mainloop()

# MSSQL bağlantısını kapat
conn.close()