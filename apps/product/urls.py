from rmtask.urls import router
from .views import ProductViewSet

router.register('products', ProductViewSet)

urlpatterns = router.urls
