from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Label, LabeledElement, LabeledSample, Sample
from .utils import humansize


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pretty_page_size",
        "truncated_url",
        "freeze_time",
        "freeze_software",
    )

    def pretty_page_size(self, obj):
        return humansize(obj.page_size)

    pretty_page_size.short_description = "Page Size"
    pretty_page_size.admin_order_field = "page_size"

    def truncated_url(self, obj):
        return truncatechars(obj.url, 140)

    truncated_url.short_description = "Url"
    truncated_url.admin_order_field = "url"


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("slug", "description")


@admin.register(LabeledElement)
class LabeledElementAdmin(admin.ModelAdmin):
    list_display = ("id", "labeled_sample", "label", "data_fta_id")


admin.site.register(LabeledSample)
