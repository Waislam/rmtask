from rest_framework import serializers
from .models import OrderItem, Order
from apps.product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']

    def to_representation(self, instance):
        ctx = super().to_representation(instance)
        ctx['product'] = {
            'id': instance.product.id,
            'name': instance.product.name
        }
        return ctx


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customer_email = serializers.EmailField(source="customer.email", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "customer_email", "items", "created_at"]

    def get_items(self, instance):
        """Ensure vendors only see their products in an order"""
        request = self.context.get("request")
        user = request.user if request else None

        if user and user.role == "vendor":
            return OrderItemSerializer(instance.items.filter(product__vendor=user.vendor), many=True).data
        return OrderItemSerializer(instance.items.all(), many=True).data


class CreateOrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'items', 'created_at']
        extra_kwargs = {'customer': {'read_only': True}}

    def create(self, validated_data):
        request = self.context.get("request")
        customer = request.user

        items_data = validated_data.pop("items")
        order = Order.objects.create(customer=customer)

        for item in items_data:
            product = Product.objects.get(id=item["product"])
            OrderItem.objects.create(order=order, product=product, quantity=item["quantity"])

        return order
