from decimal import Decimal

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import RegistrationForm, AdForm
from django.contrib.auth.decorators import login_required
from .models import Ad, Category, CustomUser
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages




def index(request):
    # Получаем все категории
    categories = Category.objects.all()

    # Получаем все объявления
    ads = Ad.objects.all()

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        ads = ads.filter(category_id=category_id)

    # Фильтрация по минимальной и максимальной цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        ads = ads.filter(price__gte=min_price)
    if max_price:
        ads = ads.filter(price__lte=max_price)

    # Поиск по заголовку и описанию
    search_query = request.GET.get('search')
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'main/index.html', {'ads': ads, 'categories': categories})


def ad_detail(request, id):
    ad = get_object_or_404(Ad, id=id)
    return render(request, 'main/ad_detail.html', {'ad': ad})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)  # Используйте вашу форму регистрации
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            # Если форма не валидна, ошибки будут автоматически добавлены
            return render(request, 'main/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def client_dashboard(request):
    return render(request, 'main/index.html')

@login_required
def moderator_dashboard(request):
    return render(request, 'main/index.html')

@login_required
def create_ad(request):
    categories = Category.objects.all()  # Получаем все категории
    if request.method == 'POST':

        form = AdForm(request.POST, request.FILES)

        if form.is_valid():  # Проверяем, что форма валидна
            ad = form.save(commit=False)  # Не сохраняем сразу в базе данных
            ad.user = request.user  # Устанавливаем текущего пользователя

            ad.save()  # Сохраняем в базе данных
            return redirect('home')  # Перенаправляем после успешной подачи
        else:
            print(form.errors)  # Выводим ошибки, если форма не прошла валидацию
    else:
        form = AdForm()

    return render(request, 'main/createAd.html', {'form': form, 'categories': categories})

def user_profile(request):
    # Получаем все объявления пользователя
    ads = Ad.objects.filter(user=request.user)
    return render(request, 'main/user_profile.html', {'ads': ads})

def delete_ad(request, ad_id):
    # Удаляем объявление
    ad = Ad.objects.get(id=ad_id, user=request.user)
    if ad:
        ad.delete()
    return redirect('user_profile')
def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def moderation(request):

    ads = Ad.objects.all()  # Получаем все объявления
    users = CustomUser.objects.all()  # Получаем всех пользователей

    return render(request, 'main/moderation.html', {'ads': ads, 'users': users})
@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    # Проверяем, кто удаляет: клиент или модератор
    if request.user.is_moderator:  # Если пользователь - модератор (предполагаем, что модератор имеет роль staff)
        ad.delete()  # Удаляем объявление
        return redirect('moderation')  # Перенаправляем на страницу модерации
    else:  # Если это обычный пользователь (клиент)
        if ad.user == request.user:  # Проверяем, что объявление принадлежит текущему пользователю
            ad.delete()  # Удаляем объявление
            return redirect('user_profile')  # Перенаправляем в личный кабинет

    return redirect('home')  # В случае ошибки, например, если пользователь пытается удалить чужое объявление

@login_required
def delete_user(request, user_id):

    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()  # Удаляем пользователя
    return redirect('moderation')  # Перенаправляем обратно на страницу модерации

class CustomLoginView(LoginView):
    template_name = 'main/login.html'

    def form_invalid(self, form):
        # Если форма невалидна (неправильный логин или пароль)
        messages.error(self.request, "Неверное имя пользователя или пароль")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.request.user.is_client:
            return 'home'  # Страница клиента
        elif self.request.user.is_moderator:
            return 'home'  # Страница модератора
        return 'home'