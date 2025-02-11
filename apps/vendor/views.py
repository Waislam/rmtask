from django.shortcuts import render

from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrVendor


# Create your views here.
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrVendor]

    # def get_queryset(self):
    #     """
    #     This queryset will return all vendors for an admin, and only the vendor's own vendor instance
    #     if the user is a vendor.
    #     """
    #     user = self.request.user
    #     print(user.role)
    #     if user.role == 'admin':
    #         return Vendor.objects.all()
    #     if user.role == 'vendor':
    #         return Vendor.objects.filter(user=user)
    #     return Vendor.objects.none()
