from django import forms
from .models import Post, Comment, Profile, Category, Tag
from django.utils.text import slugify
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorWidget(config_name='default'),
        label='İçerik'
    )
    
    # Etiketler için özel alan
    tags_input = forms.CharField(
        required=False,
        label='Etiketler',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Etiketleri virgülle ayırarak yazın (örn: python, django, web)'
        })
    )
    
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'image')
        labels = {
            'title': 'Başlık',
            'category': 'Kategori',
            'image': 'Görsel'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post başlığını girin'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eğer düzenleme modundaysa, mevcut etiketleri göster
        if self.instance.pk:
            self.initial['tags_input'] = ', '.join(tag.name for tag in self.instance.tags.all())

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Başlık alanı zorunludur.')
        return title

    def save(self, commit=True, author=None):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if author:
            instance.author = author
        
        if commit:
            instance.save()
            
            # Etiketleri kaydet
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                # Önce mevcut etiketleri temizle
                instance.tags.clear()
                # Yeni etiketleri ekle
                tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    instance.tags.add(tag)
        
        return instance

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# blog/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Yorumunuzu buraya yazın...'
            })
        }

from django import forms
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_pic']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Ad')
    last_name = forms.CharField(max_length=30, required=True, label='Soyad')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user