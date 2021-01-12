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

        if existing_sample.exists() is False:
            print(f"Sample with URL: {sample.url} did not exist, saving")
            sample.save()
        else:
            print(f"Sample with URL: {sample.url} already exists, re-using.")
            sample = existing_sample.first()

        print("Creating LabeledSample")
        fta_sample, fta_ids_to_label = convert_fathom_sample_to_labeled_sample(
            frozen_page
        )
        print("Saving LabeledSample")
        labeled_sample, _ = LabeledSample.objects.get_or_create(
            original_sample=sample, modified_sample=fta_sample
        )

        existing_labeled_sample = LabeledSample.objects.filter(
            original_sample_id=sample.id
        )
        print(f"Existing labeled_sample = {existing_labeled_sample}")

        # Since we will always create a LabelledSample always create a LabelledElement.
        for fta_id, fathom_label in fta_ids_to_label.items():
            stored_label, created = Label.objects.get_or_create(slug=fathom_label)
            LabeledElement.objects.get_or_create(
                labeled_sample=labeled_sample,
                data_fta_id=fta_id,
                label=stored_label,
            )

        return Response({"id": sample.id})
