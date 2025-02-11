from rest_framework import permissions
import logging
from apps.product.models import Product


class IsAdminOrVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        """Admin can view and modify all vendors"""
        if request.user.role == 'admin':
            return True

        if request.user.role == 'vendor':
            if view.action in ['retrieve', 'update', 'destroy']:
                print('working')
                # Vendor can view and modify only their own vendor
                # if request.user.vendor.id == int(view.kwargs.get('pk')):
                #     print("Access Granted!")
                #     return True
                # else:
                #     print("Access Denied!")
                return request.user.vendor.id == int(view.kwargs.get('pk'))
            return False
        return False


from rest_framework import permissions


class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        """Ensure only vendors can view and modify their products"""
        if request.user.role == 'admin':
            return True

        if request.user.role == 'customer':
            if view.action == 'list':
                return True
            return False
        if request.user.role == 'vendor':
            if view.action == 'create':
                return True
            if view.action == 'list':
                return True
            if view.action in ['retrieve', 'update', 'destroy']:
                # return request.user.vendor.id == int(view.kwargs.get('pk'))
                product_pk = view.kwargs.get('pk')
                if product_pk:
                    product = Product.objects.filter(id=product_pk).first()
                    if product and product.vendor.id == request.user.vendor.id:
                        return True
            return False

        return False
