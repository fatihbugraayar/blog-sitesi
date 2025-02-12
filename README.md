👉 Blogium - KİŞİSEL BLOG PROJESİ



📝 Proje Açıklaması

Blogium, hobi amaçlı geliştirilmiş modern ve şık bir blog platformudur. Projede Python Django, HTML, CSS, JS ve Bootstrap kullanılmıştır. Kullanıcılar giriş yapabilir, yeni yazılar oluşturabilir, düzenleyebilir, silebilir ve yorum yapabilirler.

🌟 Öne Çıkan Özellikler:

📉 Django Admin Paneli ile yönetim

✍️ Post oluşturma, düzenleme, silme

💬 Yorum yapma ve sosyal medya paylaşımı

🔍 Gelişmiş arama sistemi

📂 Kategori bazlı yazılar

🔑 Kullanıcı giriş ve kayıt sistemi

🎨 Sportif ve modern tasarım

🚀 Kurulum

1️⃣ Gerekli Bağımlılıkları Yükleyin

Bağımlılıkları yüklemek için:

pip install -r requirements.txt

2️⃣ .env Dosyasını Oluşturun

Projenin kök dizinine bir .env dosyası ekleyin ve aşağıdaki değişkenleri girin:

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

3️⃣ Veritabanı Migrasyon Yapın

python manage.py makemigrations
python manage.py migrate

4️⃣ Admin Kullanıcısı Oluşturun

python manage.py createsuperuser

5️⃣ Sunucuyu Çalıştırın

python manage.py runserver

🎨 Ekran Görüntülerı

Ana Sayfa

Post Detay





🐝 Katkıda Bulunma

Katkı sağlamak için lütfen bir pull request oluşturun!

🐛 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakabilirsiniz.

💡 Proje hakkında geliştirme fikirlerin varsa benimle iletişime geçebilirsin! 🚀

