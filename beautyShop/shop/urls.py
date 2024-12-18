from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .import views

app_name = 'shop'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('catalog/', views.catalog, name='catalog'),
    path('about_shop/', views.about_shop, name='about_shop'),
    path('description/<int:products_id>/', views.description_product, name='description_product'),
    path('catalog/category/<int:category_id>/', views.category_view, name='category_view'),
    path('order_registration/', views.checkout, name='checkout'),
    path('order_registration/order_confirmation/', views.order_confirmation, name='order_confirmation'),

    path('admins/', views.home_page_admin, name='home_page_admin'),
    path('admins/roles/', views.RolesListView.as_view(), name='RolesListView'),
    path('admins/roles/create/', views.RolesCreateView.as_view(), name='RolesCreateView'),
    path('admins/roles/detail/<int:pk>/', views.RolesDetailView.as_view(), name='RolesDetailView'),
    path('admins/roles/<int:pk>/update/', views.RolesUpdateView.as_view(), name='RolesUpdateView'),
    path('admins/roles/<int:pk>/delete/', views.RolesDeleteView.as_view(), name='Roles_Delete'),

    path('admins/products/', views.ProductsListView.as_view(), name='ProductsListView'),
    path('admins/products/create/', views.ProductsCreateView.as_view(), name='ProductsCreateView'),
    path('admins/products/detail/<int:pk>/', views.ProductsDetailView.as_view(), name='ProductsDetailView'),
    path('admins/products/<int:pk>/update/', views.ProductsUpdateView.as_view(), name='ProductsUpdateView'),
    path('admins/products/<int:pk>/delete/', views.ProductsDeleteView.as_view(), name='Products_Delete'),

    path('admins/country/', views.CountryListView.as_view(), name='CountryListView'),
    path('admins/country/create/', views.CountryCreateView.as_view(), name='CountryCreateView'),
    path('admins/country/detail/<int:pk>/', views.CountryDetailView.as_view(), name='CountryDetailView'),
    path('admins/country/<int:pk>/update/', views.CountryUpdateView.as_view(), name='CountryUpdateView'),
    path('admins/country/<int:pk>/delete/', views.CountryDeleteView.as_view(), name='County_Delete'),

    path('admins/brends/', views.BrendsListView.as_view(), name='BrendsListView'),
    path('admins/brends/create/', views.BrendsCreateView.as_view(), name='BrendsCreateView'),
    path('admins/brends/detail/<int:pk>/', views.BrendsDetailView.as_view(), name='BrendsDetailView'),
    path('admins/brends/<int:pk>/update/', views.BrendsUpdateView.as_view(), name='BrendsUpdateView'),
    path('admins/brends/<int:pk>/delete/', views.BrendsDeleteView.as_view(), name='Brend_Delete'),

    path('admins/category/', views.CategoryListView.as_view(), name='CategoryListView'),
    path('admins/category/create/', views.CategoryCreateView.as_view(), name='CategoryCreateView'),
    path('admins/category/detail/<int:pk>/', views.CategoryDetailView.as_view(), name='CategoryDetailView'),
    path('admins/category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='CategoryUpdateView'),
    path('admins/category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='Category_Delete'),

    path('admins/address/', views.AddressListView.as_view(), name='AddressListView'),
    path('admins/address/create/', views.AddressCreateView.as_view(), name='AddressCreateView'),
    path('admins/address/detail/<int:pk>/', views.AddressDetailView.as_view(), name='AddressDetailView'),
    path('admins/address/<int:pk>/update/', views.AddressUpdateView.as_view(), name='AddressUpdateView'),
    path('admins/address/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='Address_Delete'),

    path('admins/user_roles/', views.RolesUserListView.as_view(), name='RolesUserListView'),
    path('admins/user_roles/create/', views.RolesUserCreateView.as_view(), name='RolesUserCreateView'),
    path('admins/user_roles/detail/<int:pk>/', views.RolesUserDetailView.as_view(), name='RolesUserDetailView'),
    path('admins/user_roles/<int:pk>/update/', views.RolesUserUpdateView.as_view(), name='RolesUserUpdateView'),
    path('admins/user_roles/<int:pk>/delete/', views.RolesUserDeleteView.as_view(), name='RolesUser_Delete'),

    path('admins/user/', views.UserListView.as_view(), name='UserListView'),
    path('admins/user/create/', views.UserCreateView.as_view(), name='UserCreateView'),
    path('admins/user/detail/<int:pk>/', views.UserDetailView.as_view(), name='UserDetailView'),
    path('admins/user/<int:pk>/update/', views.UserUpdateView.as_view(), name='UserUpdateView'),
    path('admins/user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='User_Delete'),

    path('admins/order/', views.OrderListView.as_view(), name='OrderListView'),
    path('admins/order/detail/<int:pk>/', views.OrderDetailView.as_view(), name='OrderDetailView'),
    path('admins/order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='OrderUpdateView'),
    path('admins/order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='Order_Delete'),

    path('admins/order_detail/', views.OrderDetailsListView.as_view(), name='OrderDetailsListView'),
    path('admins/order_detail/detail/<int:pk>/', views.OrderDetails_DetailView.as_view(), name='OrderDetails_DetailView'),
    path('admins/order_detail/<int:pk>/update/', views.OrderDetailsUpdateView.as_view(), name='OrderDetailsUpdateView'),
    path('admins/order_detail/<int:pk>/delete/', views.OrderDetailsDeleteView.as_view(), name='Order_detail_Delete'),

    path('admins/payment/', views.PaymentListView.as_view(), name='PaymentListView'),
    path('admins/payment/detail/<int:pk>/', views.PaymentDetailView.as_view(), name='PaymentDetailView'),
    path('admins/payment/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='PaymentUpdateView'),
    path('admins/payment/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='Payment_Delete'),


    path('manager/', views.home_page_manager, name='home_page_manager'),
    path('manager/brends/', views.BrendsListView.as_view(), name='BrendsListView'),
    path('manager/brends/create/', views.BrendsCreateView.as_view(), name='BrendsCreateView'),
    path('manager/brends/detail/<int:pk>/', views.BrendsDetailView.as_view(), name='BrendsDetailView'),
    path('manager/brends/<int:pk>/update/', views.BrendsUpdateView.as_view(), name='BrendsUpdateView'),
    path('manager/brends/<int:pk>/delete/', views.BrendsDeleteView.as_view(), name='Brend_Delete'),

    path('manager/category/', views.CategoryListView.as_view(), name='CategoryListView'),
    path('manager/category/create/', views.CategoryCreateView.as_view(), name='CategoryCreateView'),
    path('manager/category/detail/<int:pk>/', views.CategoryDetailView.as_view(), name='CategoryDetailView'),
    path('manager/category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='CategoryUpdateView'),
    path('manager/category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='Category_Delete'),

    path('manager/products/', views.ProductsListView.as_view(), name='ProductsListView'),
    path('manager/products/create/', views.ProductsCreateView.as_view(), name='ProductsCreateView'),
    path('manager/products/detail/<int:pk>/', views.ProductsDetailView.as_view(), name='ProductsDetailView'),
    path('manager/products/<int:pk>/update/', views.ProductsUpdateView.as_view(), name='ProductsUpdateView'),
    path('manager/products/<int:pk>/delete/', views.ProductsDeleteView.as_view(), name='Products_Delete'),

    path('manager/order_detail/', views.OrderDetailsListView.as_view(), name='OrderDetailsListView'),
    path('manager/order_detail/detail/<int:pk>/', views.OrderDetails_DetailView.as_view(), name='OrderDetails_DetailView'),
    path('manager/order_detail/<int:pk>/update/', views.OrderDetailsUpdateView.as_view(), name='OrderDetailsUpdateView'),
    path('payments/export/', views.export_payments_to_excel, name='export_payments_to_excel'),

    path('manager/status/', views.StatusListView.as_view(), name='StatusListView'),
    path('manager/status/create/', views.StatusCreateView.as_view(), name='StatusCreateView'),
    path('manager/status/detail/<int:pk>/', views.StatusDetailView.as_view(), name='StatusDetailView'),
    path('manager/status/<int:pk>/update/', views.StatusUpdateView.as_view(), name='StatusUpdateView'),
    path('manager/status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='Status_Delete'),
    
    path('manager/order/', views.OrderListView.as_view(), name='OrderListView'),
    path('manager/order/detail/<int:pk>/', views.OrderDetailView.as_view(), name='OrderDetailView'),

    path('manager/payment_method/', views.PaymentMethodListView.as_view(), name='PaymentMethodListView'),
    path('manager/payment_method/create/', views.PaymentMethodCreateView.as_view(), name='PaymentMethodCreateView'),
    path('manager/payment_method/detail/<int:pk>/', views.PaymentMethodDetailView.as_view(), name='PaymentMethodDetailView'),
    path('manager/payment_method/<int:pk>/update/', views.PaymentMethodUpdateView.as_view(), name='PaymentMethodUpdateView'),
    path('manager/payment_method/<int:pk>/delete/', views.PaymentMethodDeleteView.as_view(), name='PaymentMethod_Delete'),

    path('manager/address/', views.AddressListView.as_view(), name='AddressListView'),
    path('manager/address/create/', views.AddressCreateView.as_view(), name='AddressCreateView'),
    path('manager/address/detail/<int:pk>/', views.AddressDetailView.as_view(), name='AddressDetailView'),
    path('manager/address/<int:pk>/update/', views.AddressUpdateView.as_view(), name='AddressUpdateView'),

    path('manager/payment/', views.PaymentListView.as_view(), name='PaymentListView'),
    path('manager/payment/detail/<int:pk>/', views.PaymentDetailView.as_view(), name='PaymentDetailView'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)