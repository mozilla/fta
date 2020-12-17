from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from fta.samples.api.views import AddSampleViewSet, SampleViewSet, AddFathomSampleViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Example how to register
router.register("samples", SampleViewSet)
router.register("add_sample", AddSampleViewSet, basename="add_sample")
router.register("add_fathom_sample", AddFathomSampleViewSet, basename="add_fathom_sample")


app_name = "api"
urlpatterns = router.urls
