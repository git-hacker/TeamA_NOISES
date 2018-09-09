from rest_framework.routers import SimpleRouter

from api.views import AudioViewset

urlpatterns = []

router = SimpleRouter(trailing_slash=False)
router.register(r'noises', AudioViewset)

urlpatterns += router.urls