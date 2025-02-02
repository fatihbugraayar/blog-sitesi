from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Açıklama")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Etiket Adı")
    slug = models.SlugField(unique=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Yazar")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    content = RichTextField(verbose_name="İçerik")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Oluşturulma Tarihi")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Yayınlanma Tarihi")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Görsel")
    views = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")
    slug = models.SlugField(unique=True, max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name="Kategori")
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="Etiketler")

    class Meta:
        verbose_name = "Yazı"
        verbose_name_plural = "Yazılar"
        ordering = ['-published_date']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# blog/models.py
from django.contrib.auth.models import User

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.text[:20]}"


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png'
    )
    followers = models.ManyToManyField(User, blank=True, related_name='following', through='Follow')

    def __str__(self):
        return f"{self.user.username} Profili"

    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.user.following.count()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follow_follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='follow_following', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Takip"
        verbose_name_plural = "Takipler"
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} -> {self.following.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)    