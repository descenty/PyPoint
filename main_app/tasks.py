from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from PyPoint.celery import app
from main_app.models import Customer, Order


@app.task
def send_new_order_info(order_id: int):
    order: Order = Order.objects.get(pk=order_id)
    customer: Customer = order.customer
    email: str = customer.email
    subject: str = f'Заказ {order_id} принят'
    from_email: str = 'd3verty@yandex.ru'
    context = {'order': order, 'customer_name': customer.fio.split()[1]}
    html_message: str = render_to_string('email/new_order_email.html', context)
    plain_message: str = strip_tags(html_message)
    send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[email],
              html_message=html_message, fail_silently=False)
