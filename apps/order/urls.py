from rmtask.urls import router
from .views import OrderViewSet

router.register('orders', OrderViewSet)

urlpatterns = router.urls
