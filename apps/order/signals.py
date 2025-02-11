# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.mail import send_mail
from .models import Order


@receiver(post_save, sender=Order)
def notify_vendor_on_order_placed(sender, instance, created, **kwargs):
    """Send a notification to the vendor when a new order is placed."""
    if created:
        # Get the vendor related to the order's items
        vendor = instance.items.first().product.vendor

        send_mail(
            subject=f"New Order Placed: Order {instance.id}",
            message=f"A new order has been placed by {instance.customer.email}.",
            from_email="no-reply@yourstore.com",
            recipient_list=[vendor.user.email],
        )

        order_count_cache_key = f"vendor_{vendor.id}_orders"
        if cache.get(order_count_cache_key) is None:
            # Cache miss, fetch and store order count
            cache.set(order_count_cache_key, vendor.orders.count(), timeout=60 * 15)
        # cache.set(f"vendor_{vendor.id}_orders", vendor.orders.count(), timeout=60 * 15)
