from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.module_loading import import_string

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Strategy(models.Model):
    class Meta:
        verbose_name_plural = "Strategies"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    python_class_path = models.TextField()
    parameters_schema = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Confirms that python_class_path resolves to a real strategy class.
        If the path leads to a non existing file/class, will raise error.
        """
        try:
            cls = import_string(self.python_class_path)
        except Exception:
            raise ValidationError(
                {"python_class_path": "Invalid Python class path - import failed."}
            )

    def save(self, *args, **kwargs):
        # Auto-generate slug if missing
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        # Enforces validation from above clean function
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
