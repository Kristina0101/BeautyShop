import openpyxl
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from beautyShop.metrics import update_metrics
from shop.serializers import *
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
from cart.cart import Cart
from users.views import *

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import genericsX



# Create your views here.
def main_page(request):
    products = Products.objects.all()
    update_metrics()
    return render(request, 'shop/main_page.html', {'products': products})

def about_shop(request):
    return render(request, 'shop/about_shop.html')

def description_product(request, products_id):
    products = get_object_or_404(Products, products_id=products_id)
    cart_product_form = CartAddProductForm(max_quantity=products.quantity)
    return render(request, 'shop/buyer/description_product.html', {'products': products, 'cart_product_form':cart_product_form})

from django.shortcuts import get_object_or_404

@login_required
def checkout(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Orders.objects.create(
                user=request.user,
                dates_order=timezone.now(),
                total_amount=cart.get_total_price()
            )
            DeliveryAddress.objects.create(
                order=order,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postcode=form.cleaned_data['postcode']
            )

            status_instance, created = Status.objects.get_or_create(name_status="В обработке")

            ordered_items = []
            for item in cart:
                OrderDetails.objects.create(
                    order=order,
                    products=item['product'],
                    quantity_products=item['quantity'],
                    unit_price=item['price'],
                    status=status_instance 
                )
                ordered_items.append({
                    'product': item['product'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                })

            payment_method_instance, created = PaymentMethod.objects.get_or_create(
                payment_method=form.cleaned_data['payment_method']
            )

            Payment.objects.create(
                order=order,
                date_payment=timezone.now(),
                sum_payment=cart.get_total_price(),
                payment_method=payment_method_instance
            )

            email_subject = "Ваш заказ успешно оформлен!"
            email_context = {
                'user': request.user,
                'ordered_items': ordered_items,
                'address': form.cleaned_data['address'],
                'city': form.cleaned_data['city'],
                'postcode': form.cleaned_data['postcode'],
                'total_amount': cart.get_total_price()
            }
            email_html_content = render_to_string('shop/buyer/order_confirmation_email.html', email_context)
            
            email = EmailMultiAlternatives(
                email_subject,
                email_html_content,
                'kristik.85p@mail.ru',
                [request.user.email]    
            )
            email.attach_alternative(email_html_content, "text/html")
            email.send(fail_silently=False)

            cart.clear()
            return redirect('shop:order_confirmation')
    else:
        form = OrderForm()

    return render(request, 'shop/buyer/checkout.html', {'cart': cart, 'form': form})


def order_confirmation(request):
    return render(request, 'shop/buyer/order_confirmation.html')

def catalog(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    update_metrics()
    return render(request, 'shop/buyer/Catalog.html', {'products': products, 'categories': categories})
    

def category_view(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, category_id=category_id)
    products = Products.objects.filter(category=category)
    return render(request, 'shop/buyer/Catalog.html', {
        'categories': categories,
        'products': products,
        'selected_category': category
    })

def home_page_admin(request):
    return render(request, 'shop/admin/home_page_admin.html')

class RolesListView(ListView):
    model = Roles
    template_name = 'shop/admin/Roles/ListView.html'
    context_object_name = 'RolesListView'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        RolesListView = paginator.get_page(page)
        context['RolesListView'] = RolesListView
        return context


class RolesCreateView(CreateView):
    model = Roles
    form_class = RolesForm
    template_name = 'shop/admin/Roles/CreateView.html'
    context_object_name = 'RolesCreateView'
    success_url = reverse_lazy('shop:RolesListView')

class RolesDetailView(DetailView):
    model = Roles
    pk_url_kwarg = 'pk'
    template_name = 'shop/admin/Roles/DetailView.html'
    context_object_name = 'RolesListView'

class RolesUpdateView(UpdateView):
    model = Roles
    form_class = RolesForm
    pk_url_kwarg = 'pk'
    context_object_name = 'RolesUpdateView'
    template_name = 'shop/admin/Roles/UpdateView.html'
    success_url = reverse_lazy('shop:RolesListView')

class RolesDeleteView(DeleteView):
    model = Roles
    context_object_name = 'RolesDeleteView'
    template_name = 'shop/admin/Roles/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:RolesListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['role'] = get_object_or_404(Roles, pk=self.kwargs['pk'])
        return context


class ProductsListView(ListView):
    model = Products
    context_object_name = 'ProductsListView'
    paginate_by = 5
    
    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/Products/ListView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/Products/ListView.html']
        else:
            return ['shop/main_page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        ProductsListView = paginator.get_page(page)
        context['ProductsListView'] = ProductsListView
        return context
    

class ProductsCreateView(CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'shop/admin/Products/CreateView.html'
    context_object_name = 'ProductsListView'
    success_url = reverse_lazy('shop:ProductsListView')

class ProductsDetailView(DetailView):
    model = Products
    pk_url_kwarg = 'pk'
    template_name = 'shop/admin/Products/DetailView.html'
    context_object_name = 'ProductsListView'

class ProductsUpdateView(UpdateView):
    model = Products
    form_class = ProductsForm
    pk_url_kwarg = 'pk'
    context_object_name = 'ProductsUpdateView'
    template_name = 'shop/admin/Products/UpdateView.html'
    success_url = reverse_lazy('shop:ProductsListView')

class ProductsDeleteView(DeleteView):
    model = Products
    context_object_name = 'ProductsDeleteView'
    template_name = 'shop/admin/Products/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:ProductsListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']  # Передаем pk в контекст
        context['product'] = get_object_or_404(Products, pk=self.kwargs['pk'])
        return context


class CountryListView(ListView):
    model = Country
    template_name = 'shop/admin/Countries/ListView.html'
    context_object_name = 'CountryListView'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        CountryListView = paginator.get_page(page)
        context['CountryListView'] = CountryListView
        return context
    

class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm
    template_name = 'shop/admin/Countries/CreateView.html'
    context_object_name = 'CountryListView'
    success_url = reverse_lazy('shop:CountryListView')

class CountryDetailView(DetailView):
    model = Country
    pk_url_kwarg = 'pk'
    template_name = 'shop/admin/Countries/DetailView.html'
    context_object_name = 'CountryListView'

class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm
    pk_url_kwarg = 'pk'
    context_object_name = 'CountryUpdateView'
    template_name = 'shop/admin/Countries/UpdateView.html'
    success_url = reverse_lazy('shop:CountryListView')

class CountryDeleteView(DeleteView):
    model = Country
    context_object_name = 'CountryDeleteView'
    template_name = 'shop/admin/Countries/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:CountryListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['country'] = get_object_or_404(Country, pk=self.kwargs['pk'])
        return context
    

class BrendsListView(ListView):
    model = Brends
    context_object_name = 'BrendsListView'
    paginate_by = 10

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/Brends/ListView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/Brends/ListView.html']
        else:
            return ['shop/main_page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        context['BrendsListView'] = paginator.get_page(page)
        return context
    

class BrendsCreateView(CreateView):
    model = Brends
    form_class = BrendsForm
    template_name = 'shop/admin/Brends/CreateView.html'
    context_object_name = 'BrendsListView'
    success_url = reverse_lazy('shop:BrendsListView')

class BrendsDetailView(DetailView):
    model = Brends
    pk_url_kwarg = 'pk'
    template_name = 'shop/admin/Brends/DetailView.html'
    context_object_name = 'BrendsListView'

class BrendsUpdateView(UpdateView):
    model = Brends
    form_class = BrendsForm
    pk_url_kwarg = 'pk'
    context_object_name = 'BrendsUpdateView'
    template_name = 'shop/admin/Brends/UpdateView.html'
    success_url = reverse_lazy('shop:BrendsListView')

class BrendsDeleteView(DeleteView):
    model = Brends
    context_object_name = 'BrendsDeleteView'
    template_name = 'shop/admin/Brends/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:BrendsListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['brand'] = get_object_or_404(Brends, pk=self.kwargs['pk'])
        return context
    

class CategoryListView(ListView):
    model = Category
    context_object_name = 'CategoryListView'
    paginate_by = 10

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/Category/ListView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/Category/ListView.html']
        else:
            return ['shop/main_page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        CategoryListView = paginator.get_page(page)
        context['CategoryListView'] = CategoryListView
        return context
    

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/admin/Category/CreateView.html'
    context_object_name = 'CategoryListView'
    success_url = reverse_lazy('shop:CategoryListView')

class CategoryDetailView(DetailView):
    model = Category
    pk_url_kwarg = 'pk'
    template_name = 'shop/admin/Category/DetailView.html'
    context_object_name = 'CategoryListView'

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    pk_url_kwarg = 'pk'
    context_object_name = 'CategoryUpdateView'
    template_name = 'shop/admin/Category/UpdateView.html'
    success_url = reverse_lazy('shop:CategoryListView')

class CategoryDeleteView(DeleteView):
    model = Category
    context_object_name = 'CategoryDeleteView'
    template_name = 'shop/admin/Category/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:CategoryListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context
    

class AddressListView(ListView):
    model = DeliveryAddress
    context_object_name = 'AddressListView'
    paginate_by = 10

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/delivery_address/ListView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/delivery_address/ListView.html']
        else:
            return ['shop/main_page.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        AddressListView = paginator.get_page(page)
        context['AddressListView'] = AddressListView
        return context
    

class AddressCreateView(CreateView):
    model = DeliveryAddress
    form_class = DeliveryAddressForm
    template_name = 'shop/admin/delivery_address/CreateView.html'
    context_object_name = 'AddressListView'
    success_url = reverse_lazy('shop:AddressListView')

class AddressDetailView(DetailView):
    model = DeliveryAddress
    pk_url_kwarg = 'pk'
    context_object_name = 'AddressListView'

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/delivery_address/DetailView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/delivery_address/DetailView.html']
        else:
            return ['shop/main_page.html']

class AddressUpdateView(UpdateView):
    model = DeliveryAddress
    form_class = DeliveryAddressForm
    pk_url_kwarg = 'pk'
    context_object_name = 'AddressUpdateView'
    success_url = reverse_lazy('shop:AddressListView')

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/delivery_address/UpdateView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/delivery_address/UpdateView.html']
        else:
            return ['shop/main_page.html']

class AddressDeleteView(DeleteView):
    model = DeliveryAddress
    context_object_name = 'AddressDeleteView'
    template_name = 'shop/admin/delivery_address/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:AddressListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['address'] = get_object_or_404(DeliveryAddress, pk=self.kwargs['pk'])
        return context
    
class RolesUserListView(ListView):
    model = UserRoles
    template_name = 'shop/admin/Roles_user/ListView.html'
    context_object_name = 'RolesUserListView'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        RolesUserListView = paginator.get_page(page)
        context['RolesUserListView'] = RolesUserListView
        return context
    

class RolesUserCreateView(CreateView):
    model = UserRoles
    form_class = UserRolesForm
    template_name = 'shop/admin/Roles_user/CreateView.html'
    context_object_name = 'RolesUserListView'
    success_url = reverse_lazy('shop:RolesUserListView')

class RolesUserDetailView(DetailView):
    model = UserRoles
    pk_url_kwarg = 'pk'
    template_name = 'shop/admin/Roles_user/DetailView.html'
    context_object_name = 'RolesUserListView'

class RolesUserUpdateView(UpdateView):
    model = UserRoles
    form_class = UserRolesForm
    pk_url_kwarg = 'pk'
    context_object_name = 'RolesUserUpdateView'
    template_name = 'shop/admin/Roles_user/UpdateView.html'
    success_url = reverse_lazy('shop:RolesUserListView')

class RolesUserDeleteView(DeleteView):
    model = UserRoles
    context_object_name = 'RolesUserDeleteView'
    template_name = 'shop/admin/Roles_user/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:RolesUserListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['RolesUser'] = get_object_or_404(UserRoles, pk=self.kwargs['pk'])
        return context
    

class UserListView(ListView):
    model = User
    template_name = 'shop/admin/users/ListView.html'
    context_object_name = 'UserListView'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        UserListView = paginator.get_page(page)
        context['UserListView'] = UserListView
        return context
    

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'shop/admin/users/CreateView.html'
    context_object_name = 'UserListView'
    success_url = reverse_lazy('shop:UserListView')

class UserDetailView(DetailView):
    model = User
    pk_url_kwarg = 'pk'
    template_name = 'shop/admin/users/DetailView.html'
    context_object_name = 'UserListView'

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    pk_url_kwarg = 'pk'
    context_object_name = 'UserUpdateView'
    template_name = 'shop/admin/users/UpdateView.html'
    success_url = reverse_lazy('shop:UserListView')

class UserDeleteView(DeleteView):
    model = User
    context_object_name = 'UserDeleteView'
    template_name = 'shop/admin/users/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:UserListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['User'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context
    

class OrderListView(ListView):
    model = Orders
    context_object_name = 'OrderListView'
    paginate_by = 5

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/orders/ListView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/orders/ListView.html']
        else:
            return ['shop/main_page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        OrderListView = paginator.get_page(page)
        context['OrderListView'] = OrderListView
        return context

class OrderDetailView(DetailView):
    model = Orders
    pk_url_kwarg = 'pk'
    context_object_name = 'OrderListView'

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/orders/DetailView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/orders/DetailView.html']
        else:
            return ['shop/main_page.html']
    

class OrderUpdateView(UpdateView):
    model = Orders
    form_class = OrdersForm
    pk_url_kwarg = 'pk'
    context_object_name = 'OrderUpdateView'
    template_name = 'shop/admin/orders/UpdateView.html'
    success_url = reverse_lazy('shop:OrderListView')

class OrderDeleteView(DeleteView):
    model = Orders
    context_object_name = 'OrderDeleteView'
    template_name = 'shop/admin/orders/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:OrderListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['Order'] = get_object_or_404(Orders, pk=self.kwargs['pk'])
        return context
    

class OrderDetailsListView(ListView):
    model = OrderDetails
    context_object_name = 'OrderDetailsListView'
    paginate_by = 5

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/order_details/ListView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/order_details/ListView.html']
        else:
            return ['shop/main_page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        OrderDetailsListView = paginator.get_page(page)
        context['OrderDetailsListView'] = OrderDetailsListView
        return context

class OrderDetails_DetailView(DetailView):
    model = OrderDetails
    pk_url_kwarg = 'pk'
    context_object_name = 'OrderDetailsListView'

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/order_details/DetailView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/order_details/DetailView.html']
        else:
            return ['shop/main_page.html']

class OrderDetailsUpdateView(UpdateView):
    model = OrderDetails
    form_class = OrderDetailsForm
    pk_url_kwarg = 'pk'
    context_object_name = 'OrderDetailsUpdateView'
    success_url = reverse_lazy('shop:OrderDetailsListView')

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/order_details/UpdateView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/order_details/UpdateView.html']
        else:
            return ['shop/main_page.html']

class OrderDetailsDeleteView(DeleteView):
    model = OrderDetails
    context_object_name = 'OrderDetailsDeleteView'
    template_name = 'shop/admin/order_details/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:OrderDetailsListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['OrderDetail'] = get_object_or_404(OrderDetails, pk=self.kwargs['pk'])
        return context
    
def export_payments_to_excel(request):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Платежи"

    headers = ['ID платежа', 'ID заказа', 'Пользователь', 'Имя', 'Фамилия', 'Дата оплаты', 'Сумма', 'Метод оплаты']
    sheet.append(headers)

    payments = Payment.objects.select_related('order', 'payment_method').all()
    total_sum = 0

    for payment in payments:
        sum_payment = float(payment.sum_payment)
        total_sum += sum_payment
        sheet.append([
            payment.payment_id,
            payment.order.order_id if payment.order else None,
            payment.order.user.username if payment.order else None,
            payment.order.user.first_name if payment.order else None,
            payment.order.user.last_name if payment.order else None,
            payment.date_payment.strftime('%Y-%m-%d %H:%M:%S'),
            sum_payment,
            payment.payment_method.payment_method if payment.payment_method else None,
        ])

    sheet.append([])
    sheet.append(['', '', '', '', '', 'Общая сумма:', total_sum, 'руб.'])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=payments.xlsx'
    workbook.save(response)
    return response


class PaymentListView(ListView):
    model = Payment
    context_object_name = 'PaymentListView'
    paginate_by = 5

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/payment/ListView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/payment/ListView.html']
        else:
            return ['shop/main_page.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        PaymentListView = paginator.get_page(page)
        context['PaymentListView'] = PaymentListView
        return context
    
class PaymentDetailView(DetailView):
    model = Payment
    pk_url_kwarg = 'pk'
    context_object_name = 'PaymentListView'

    def get_template_names(self):
        user = self.request.user
        try:
            user_role = UserRoles.objects.get(user=user).roles
        except UserRoles.DoesNotExist:
            return ['shop/main_page.html']
        if user_role.name_role == 'admin':
            return ['shop/admin/payment/DetailView.html']
        elif user_role.name_role == 'seller':
            return ['shop/manager/payment/DetailView.html']
        else:
            return ['shop/main_page.html']

class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    pk_url_kwarg = 'pk'
    context_object_name = 'PaymentUpdateView'
    template_name = 'shop/admin/payment/UpdateView.html'
    success_url = reverse_lazy('shop:PaymentListView')

class PaymentDeleteView(DeleteView):
    model = Payment
    context_object_name = 'PaymentDeleteView'
    template_name = 'shop/admin/payment/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:PaymentListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['payment'] = get_object_or_404(Payment, pk=self.kwargs['pk'])
        return context
    

def home_page_manager(request):
    return render(request, 'shop/manager/home_page_employee.html')


class StatusListView(ListView):
    model = Status
    template_name = 'shop/manager/status/ListView.html'
    context_object_name = 'StatusListView'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        StatusListView = paginator.get_page(page)
        context['StatusListView'] = StatusListView
        return context
    

class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'shop/manager/status/CreateView.html'
    context_object_name = 'StatusListView'
    success_url = reverse_lazy('shop:StatusListView')

class StatusDetailView(DetailView):
    model = Status
    pk_url_kwarg = 'pk'
    template_name = 'shop/manager/status/DetailView.html'
    context_object_name = 'StatusListView'

class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    pk_url_kwarg = 'pk'
    context_object_name = 'StatusUpdateView'
    template_name = 'shop/manager/status/UpdateView.html'
    success_url = reverse_lazy('shop:StatusListView')

class StatusDeleteView(DeleteView):
    model = Status
    context_object_name = 'StatusDeleteView'
    template_name = 'shop/manager/status/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:StatusListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['Status'] = get_object_or_404(Status, pk=self.kwargs['pk'])
        return context
    
class PaymentMethodListView(ListView):
    model = PaymentMethod
    template_name = 'shop/manager/payment_method/ListView.html'
    context_object_name = 'PaymentMethodListView'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        PaymentMethodListView = paginator.get_page(page)
        context['PaymentMethodListView'] = PaymentMethodListView
        return context
    

class PaymentMethodCreateView(CreateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = 'shop/manager/payment_method/CreateView.html'
    context_object_name = 'PaymentMethodListView'
    success_url = reverse_lazy('shop:PaymentMethodListView')

class PaymentMethodDetailView(DetailView):
    model = PaymentMethod
    pk_url_kwarg = 'pk'
    template_name = 'shop/manager/payment_method/DetailView.html'
    context_object_name = 'PaymentMethodListView'

class PaymentMethodUpdateView(UpdateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    pk_url_kwarg = 'pk'
    context_object_name = 'PaymentMethodUpdateView'
    template_name = 'shop/manager/payment_method/UpdateView.html'
    success_url = reverse_lazy('shop:PaymentMethodListView')

class PaymentMethodDeleteView(DeleteView):
    model = PaymentMethod
    context_object_name = 'PaymentMethodDeleteView'
    template_name = 'shop/manager/payment_method/DeleteView.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('shop:PaymentMethodListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['PaymentMethod'] = get_object_or_404(PaymentMethod, pk=self.kwargs['pk'])
        return context
    
@api_view(['GET', 'POST'])
def products_api(request):
    if request.method == 'GET':
        list_data = Products.objects.filter()
        serializer = serializer_Products(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_Products(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def products_api_detail(request, pk=None):
    one_data = get_object_or_404(Products, pk=pk)
    if request.method == 'GET':
        serializer = serializer_Products(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_Products(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductList(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = serializer_Products

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = serializer_Products

@api_view(['GET', 'POST'])
def category_api(request):
    if request.method == 'GET':
        list_data = Category.objects.filter()
        serializer = serializer_Category(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_Category(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def category_api_detail(request, pk=None):
    one_data = get_object_or_404(Category, pk=pk)
    if request.method == 'GET':
        serializer = serializer_Category(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_Category(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializer_Category

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializer_Category

@api_view(['GET', 'POST'])
def brend_api(request):
    if request.method == 'GET':
        list_data = Brends.objects.filter()
        serializer = serializer_Brends(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_Brends(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def brend_api_detail(request, pk=None):
    one_data = get_object_or_404(Brends, pk=pk)
    if request.method == 'GET':
        serializer = serializer_Brends(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_Brends(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BrendsList(generics.ListCreateAPIView):
    queryset = Brends.objects.all()
    serializer_class = serializer_Brends

class BrendsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brends.objects.all()
    serializer_class = serializer_Brends


@api_view(['GET', 'POST'])
def deliveryAddress_api(request):
    if request.method == 'GET':
        list_data = DeliveryAddress.objects.filter()
        serializer = serializer_DeliveryAddress(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_DeliveryAddress(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def deliveryAddress_api_detail(request, pk=None):
    one_data = get_object_or_404(DeliveryAddress, pk=pk)
    if request.method == 'GET':
        serializer = serializer_DeliveryAddress(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_DeliveryAddress(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DeliveryAddressList(generics.ListCreateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = serializer_DeliveryAddress

class DeliveryAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = serializer_DeliveryAddress

@api_view(['GET', 'POST'])
def payment_api(request):
    if request.method == 'GET':
        list_data = Payment.objects.filter()
        serializer = serializer_Payment(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_Payment(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def payment_api_detail(request, pk=None):
    one_data = get_object_or_404(Payment, pk=pk)
    if request.method == 'GET':
        serializer = serializer_Payment(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_Payment(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = serializer_Payment

class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = serializer_Payment


@api_view(['GET', 'POST'])
def country_api(request):
    if request.method == 'GET':
        list_data = Country.objects.filter()
        serializer = serializer_Country(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_Country(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def country_api_detail(request, pk=None):
    one_data = get_object_or_404(Country, pk=pk)
    if request.method == 'GET':
        serializer = serializer_Country(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_Country(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = serializer_Country

class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = serializer_Country


@api_view(['GET', 'POST'])
def status_api(request):
    if request.method == 'GET':
        list_data = Status.objects.filter()
        serializer = serializer_Status(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_Status(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def status_api_detail(request, pk=None):
    one_data = get_object_or_404(Status, pk=pk)
    if request.method == 'GET':
        serializer = serializer_Status(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_Status(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StatusList(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = serializer_Status

class StatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = serializer_Status
    

@api_view(['GET', 'POST'])
def PaymentMethod_api(request):
    if request.method == 'GET':
        list_data = PaymentMethod.objects.filter()
        serializer = serializer_PaymentMethod(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_PaymentMethod(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def PaymentMethod_api_detail(request, pk=None):
    one_data = get_object_or_404(PaymentMethod, pk=pk)
    if request.method == 'GET':
        serializer = serializer_PaymentMethod(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_PaymentMethod(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PaymentMethodList(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = serializer_PaymentMethod

class PaymentMethodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = serializer_PaymentMethod



@api_view(['GET', 'POST'])
def orderDetails_api(request):
    if request.method == 'GET':
        list_data = OrderDetails.objects.filter()
        serializer = serializer_orderDetails(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_orderDetails(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def orderDetails_api_detail(request, pk=None):
    one_data = get_object_or_404(OrderDetails, pk=pk)
    if request.method == 'GET':
        serializer = serializer_orderDetails(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_orderDetails(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderDetailsList(generics.ListCreateAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = serializer_orderDetails

class OrderDetailsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = serializer_orderDetails

@api_view(['GET', 'POST'])
def orders_api(request):
    if request.method == 'GET':
        list_data = Orders.objects.filter()
        serializer = serializer_orders(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_orders(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def orders_api_detail(request, pk=None):
    one_data = get_object_or_404(Orders, pk=pk)
    if request.method == 'GET':
        serializer = serializer_orders(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_orders(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrdersList(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = serializer_orders

class OrdersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = serializer_orders


@api_view(['GET', 'POST'])
def authUser_api(request):
    if request.method == 'GET':
        list_data = AuthUser.objects.filter()
        serializer = serializer_authUser(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_authUser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def authUser_api_detail(request, pk=None):
    one_data = get_object_or_404(AuthUser, pk=pk)
    if request.method == 'GET':
        serializer = serializer_authUser(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_authUser(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AuthUserList(generics.ListCreateAPIView):
    queryset = AuthUser.objects.all()
    serializer_class = serializer_authUser

class AuthUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuthUser.objects.all()
    serializer_class = serializer_authUser


@api_view(['GET', 'POST'])
def roles_api(request):
    if request.method == 'GET':
        list_data = Roles.objects.filter()
        serializer = serializer_roles(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_roles(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def roles_api_detail(request, pk=None):
    one_data = get_object_or_404(Roles, pk=pk)
    if request.method == 'GET':
        serializer = serializer_roles(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_roles(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RolesList(generics.ListCreateAPIView):
    queryset = Roles.objects.all()
    serializer_class = serializer_roles

class RolesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Roles.objects.all()
    serializer_class = serializer_roles


@api_view(['GET', 'POST'])
def userRoles_api(request):
    if request.method == 'GET':
        list_data = UserRoles.objects.filter()
        serializer = serializer_userRoles(list_data, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializer_userRoles(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def userRoles_api_detail(request, pk=None):
    one_data = get_object_or_404(UserRoles, pk=pk)
    if request.method == 'GET':
        serializer = serializer_userRoles(one_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializer_userRoles(one_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        one_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserRolesList(generics.ListCreateAPIView):
    queryset = UserRoles.objects.all()
    serializer_class = serializer_userRoles

class UserRolesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRoles.objects.all()
    serializer_class = serializer_userRoles

def api_page(request):
    return render(request, 'shop/manager/API.html')