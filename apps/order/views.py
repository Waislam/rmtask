# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .serializers import OrderSerializer, CreateOrderSerializer
# from .models import Order
# from .permissions import IsCustomer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer
from .permissions import IsAdminVendorOrCustomer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsAdminVendorOrCustomer]

    def get_serializer_class(self):
        """Switch to CreateOrderSerializer for creating orders"""
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            # Save order instance
            order = serializer.save()

            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Ensure admin sees all orders, vendors see only relevant orders, customers see their own."""
        user = self.request.user

        if user.role == "admin":
            return Order.objects.all()

        if user.role == "vendor":
            print('user: ', user.vendor)
            order_items = Prefetch('items', queryset=OrderItem.objects.select_related('product'))
            return Order.objects.prefetch_related(order_items).filter(items__product__vendor=user.vendor).distinct()

        # return Order.objects.filter(customer=user)
        return Order.objects.select_related('customer').prefetch_related('items').filter(customer=user)
