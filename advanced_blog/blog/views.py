from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm
from django.utils import timezone
from .models import Post, Comment , Profile
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Follow
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages



def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    """
    Yeni blog postu oluşturma görünümü.
    Sadece admin yetkisi olan kullanıcılar post oluşturabilir.
    """
    # Admin kontrolü
    if not request.user.is_staff:
        messages.error(request, 'Yeni post oluşturma yetkiniz yok.')
        return redirect('home')
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Post başarıyla oluşturuldu.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_edit.html', {
        'form': form,
        'title': 'Yeni Post Oluştur'
    })

from django.db.models import F
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views = F('views') + 1  # Atomic update
    post.save()
    comments = post.comments.filter(approved=True)
    comment_form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{user.username} hesabı oluşturuldu! Şimdi giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# blog/views.py


from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def profile(request):
    # Profil yoksa otomatik oluştur
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    # Admin kullanıcılar için postları getir
    context = {
        'u_form': u_form, 
        'p_form': p_form
    }
    
    if request.user.is_staff:
        admin_posts = Post.objects.filter(author=request.user).order_by('-published_date')
        context['admin_posts'] = admin_posts

    return render(request, 'blog/profile.html', context)


from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('post_list')  # Çıkış sonrası yönlenecek sayfanın adı

from .models import Post


def home(request):
    # Slider için son 3 post
    slider_posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')[:3]
    
    # En çok okunan 3 post
    popular_posts = Post.objects.filter(published_date__isnull=False).order_by('-views')[:3]
    
    # Tüm yayınlanmış postlar
    all_posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    
    # Tüm kategoriler
    categories = Category.objects.all().order_by('name')
    
    return render(request, 'blog/home.html', {
        'slider_posts': slider_posts,
        'popular_posts': popular_posts,
        'all_posts': all_posts,
        'categories': categories
    })



# blog/views.py
# blog/views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Post

def search(request):
    query = request.GET.get('q', '')
    popular_posts = Post.objects.filter(published_date__isnull=False).order_by('-views')[:3]

    if query:
        # Post araması
        post_results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query),
            published_date__isnull=False
        ).order_by('-published_date')

        # Profil araması
        profile_results = Profile.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(bio__icontains=query) |
            Q(location__icontains=query)
        ).select_related('user')
    else:
        post_results = []
        profile_results = []
    
    return render(request, 'blog/search.html', {
        'query': query,
        'popular_posts': popular_posts,
        'post_results': post_results,
        'profile_results': profile_results,
        'post_count': len(post_results) if query else 0,
        'profile_count': len(profile_results) if query else 0
    })


# blog/views.py
from django.shortcuts import get_object_or_404

@login_required
def add_comment(request, slug):  # Slug parametresini al
    post = get_object_or_404(Post, slug=slug)  # Slug'a göre postu bul
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)  # Slug ile yönlendir

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Yetki kontrolü
    if not request.user.is_staff or post.author != request.user:
        messages.error(request, 'Bu postu düzenleme yetkiniz yok.')
        return redirect('home')
        
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Post başarıyla güncellendi.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {
        'form': form,
        'title': 'Postu Düzenle'
    })

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Yetki kontrolü
    if not request.user.is_staff or post.author != request.user:
        messages.error(request, 'Bu postu silme yetkiniz yok.')
        return redirect('home')
    
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post başarıyla silindi.')
        return redirect('profile')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        category=category,
        published_date__isnull=False
    ).order_by('-published_date')
    
    return render(request, 'blog/category_detail.html', {
        'category': category,
        'posts': posts
    })

@login_required
def follow_unfollow(request, username):
    try:
        to_follow = User.objects.get(username=username)
        if to_follow == request.user:
            return JsonResponse({'status': 'error', 'message': 'Kendinizi takip edemezsiniz.'})
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=to_follow.profile
        )
        
        if not created:
            follow.delete()
            is_following = False
            message = 'Takipten çıkıldı'
        else:
            is_following = True
            message = 'Takip edildi'
        
        return JsonResponse({
            'status': 'success',
            'is_following': is_following,
            'message': message,
            'follower_count': to_follow.profile.get_followers_count()
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})

@csrf_protect
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user, published_date__isnull=False).order_by('-published_date')
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile).exists()
    
    # Son 5 takipçi
    recent_followers = Follow.objects.filter(
        following=profile
    ).select_related('follower').order_by('-created_date')[:5]
    
    # Son 5 takip edilen
    recent_following = Follow.objects.filter(
        follower=user
    ).select_related('following').order_by('-created_date')[:5]
    
    # Post istatistikleri
    total_views = sum(post.views for post in posts)
    post_count = posts.count()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile.get_followers_count(),
        'following_count': profile.get_following_count(),
        'recent_followers': recent_followers,
        'recent_following': recent_following,
        'total_views': total_views,
        'post_count': post_count
    }
    
    return render(request, 'blog/profile_detail.html', context)

