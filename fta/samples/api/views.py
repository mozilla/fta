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
        existing_sample = Sample.objects.filter(url__contains=sample.url).order_by(
            "-id"
        )[:1]

        # If the sample already exists reuse it.
        if existing_sample.exists() is False:
            sample.save()
        else:
            sample = existing_sample.first()

        # check if a LabeledSample already exists for the sample.
        existing_labeled_sample = LabeledSample.objects.filter(
            original_sample_id=sample.id
        )

        id_of_existing_labeled_sample = -1
        if existing_labeled_sample.exists() is True:
            id_of_existing_labeled_sample = existing_labeled_sample.first().id

        fta_sample, fta_ids_to_label = convert_fathom_sample_to_labeled_sample(
            frozen_page
        )
        labeled_sample, _ = LabeledSample.objects.get_or_create(
            original_sample=sample, modified_sample=fta_sample
        )

        # If a LabeledSample already existed need to update the superseded_by field to the newly create LabeledSample.
        if id_of_existing_labeled_sample != -1:
            LabeledSample.objects.filter(id=id_of_existing_labeled_sample).update(
                superseded_by=labeled_sample.id
            )

        # Create a LabeledElement.
        for fta_id, fathom_label in fta_ids_to_label.items():
            stored_label, created = Label.objects.get_or_create(slug=fathom_label)
            LabeledElement.objects.get_or_create(
                labeled_sample=labeled_sample,
                data_fta_id=fta_id,
                label=stored_label,
            )

        return Response({"id": sample.id})
