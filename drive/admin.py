from django.contrib import admin
from drive.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ("type", "size",)
