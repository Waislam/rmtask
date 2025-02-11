from rest_framework import permissions


# class IsCustomer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'customer'


class IsAdminVendorOrCustomer(permissions.BasePermission):
    """
    Admin: Full access
    Vendor: Can only view orders containing their products
    Customer: Can only view & create their own orders
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "admin":
            return True

        if user.role == "vendor":
            return obj.items.filter(product__vendor=user.vendor).exists()

        if user.role == "customer":
            return obj.customer == user

        return False
