from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from shop.models import UserRoles, Roles
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Profile
from shop.models import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            try:
                buyer_role = Roles.objects.get(name_role='buyer')
            except Roles.DoesNotExist:
                messages.error(request, 'Роль "покупатель" не найдена.')
                return redirect('register')  # перенаправляем назад на страницу регистрации
            UserRoles.objects.create(roles=buyer_role, user=user)

            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username} с ролью покупателя!')
            return redirect('shop:main_page')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Получаем заказы пользователя
    user_orders = Orders.objects.filter(user=request.user).order_by('-dates_order')

    # Объединяем все данные в один контекст
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_orders': user_orders
    }

    return render(request, 'users/profile.html', context)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return reverse('shop:main_page')

        if user_role.name_role == 'admin': 
            return reverse('shop:home_page_admin')
        elif user_role.name_role == 'seller': 
            return reverse('shop:home_page_manager')
        elif user_role.name_role == 'buyer': 
            return reverse('shop:main_page')
        else:
            return reverse('shop:main_page')