from rmtask.urls import router
from .views import VendorViewSet

router.register('vendors', VendorViewSet)

urlpatterns = router.urls
