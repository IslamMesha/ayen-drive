import os
from django.db import models
from django.contrib.auth.models import User

file_types = (
    ("PDF", "Portable Document Format (PDF)"),
    ("PPTX", "PowerPoint Presentation (PPTX)"),
)


class Document(models.Model):
    size = models.FloatField(default=0.0)
    shared = models.BooleanField(default=False)
    description = models.TextField(max_length=500)
    uploaded = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=False, upload_to="uploads/")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    type = models.CharField(choices=file_types, max_length=25, default="PDF")

    def __str__(self):
        return self.file.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.size = self.file.size

        filename, file_type = os.path.splitext(self.file.path)
        if file_type == ".pdf":
            self.type = "PDF"
        elif file_type == ".pptx":
            self.type = "PPTX"
        else:
            return

        # if not self.owner.is_authenticated:
        #     self.owner = "islam_mesha"

        super(Document, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                   update_fields=update_fields)
