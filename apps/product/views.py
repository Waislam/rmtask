from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from apps.vendor.permissions import IsVendor


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsVendor]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'vendor']
    search_fields = ['name', 'vendor__name']

    def perform_create(self, serializer):
        print('working view')
        """Ensure the vendor is associated with the product during creation"""
        serializer.save(vendor=self.request.user.vendor)

    def get_queryset(self):
        """For 'list' action, return products associated with the vendor"""
        user = self.request.user
        if user.role == 'vendor':
            return Product.objects.filter(vendor=user.vendor)
        elif user.role == 'admin':
            return Product.objects.all()
        elif user.role == 'customer':
            return Product.objects.all()
        return Product.objects.none()
