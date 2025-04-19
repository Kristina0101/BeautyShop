from prometheus_client import Gauge
from shop.models import Products, AuthUser, Payment, Orders
from django.db.models import Avg


active_users_gauge = Gauge('active_users', 'Количество активных пользователей на сайте')
products_count_gauge = Gauge( 'products_count', 'Количество продуктов')
orders_count_gauge = Gauge( 'orders_count', 'Количество заказов')
payment_review_rating = Gauge( 'average_payment', 'Средняя сумма оплаты')
request_processing_time = Gauge( 'django_request_processing_time', 'Среднее время обработки запросов')
def update_metrics():
    active_users_gauge.set(AuthUser.objects.filter(is_active=True).count())
    products_count_gauge.set(Products.objects.count())
    orders_count_gauge.set(Orders.objects.count())
    avg_payment = Payment.objects.aggregate(avg=Avg('sum_payment'))['avg'] or 0
    payment_review_rating.set(avg_payment)