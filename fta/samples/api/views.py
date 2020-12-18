from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Label, LabeledElement, LabeledSample, Sample
from ..utils import convert_fathom_sample_to_labeled_sample
from ..views import sample_from_required
from .serializers import SampleListSerializer, SampleSerializer


class SampleViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SampleSerializer
    queryset = Sample.objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_action_classes = {
            "list": SampleListSerializer,
            "create": SampleSerializer,
            "retrieve": SampleSerializer,
        }

    def get_serializer_class(self, *args, **kwargs):
        """Instantiate the list of serializers per action from class attribute (must be defined)."""
        kwargs["partial"] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class AddSampleViewSet(viewsets.ViewSet):
    basename = "add_sample"

    @action(detail=False, methods=["post"])
    def add_sample(self, request, format=None):
        frozen_page = request.data["frozen_page"]
        freeze_software = request.data["freeze_software"]
        notes = request.data["notes"] if "notes" in request.data else ""
        sample = sample_from_required(frozen_page, freeze_software, notes)
        sample.save()
        return Response({"id": sample.id})


class AddFathomSampleViewSet(viewsets.ViewSet):
    basename = "add_fathom_sample"

    @action(detail=False, methods=["post"])
    def add_fathom_sample(self, request, format=None):
        frozen_page = request.data["frozen_page"]
        freeze_software = request.data["freeze_software"]
        notes = request.data["notes"] if "notes" in request.data else ""
        sample = sample_from_required(frozen_page, freeze_software, notes)
        sample.save()

        fta_sample, labels_to_fta_ids = convert_fathom_sample_to_labeled_sample(
            frozen_page
        )
        labeled_sample, _ = LabeledSample.objects.get_or_create(
            original_sample=sample, modified_sample=fta_sample
        )

        for fathom_label, fta_id in labels_to_fta_ids.items():
            stored_label, created = Label.objects.get_or_create(slug=fathom_label)
            LabeledElement.objects.get_or_create(
                labeled_sample=labeled_sample,
                data_fta_id=fta_id,
                label=stored_label,
            )

        return Response({"id": sample.id})
