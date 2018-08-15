from django.db import models

from django.utils.translation import pgettext_lazy

from saleor.core.permissions import MODELS_PERMISSIONS


# Add in the permissions specific to our models.
MODELS_PERMISSIONS += [
    'category_extensions.view',
    'category_extensions.edit'
]


class CategoryExtension(models.Model):
    category = models.OneToOneField(
        'product.Category', on_delete=models.CASCADE, related_name='extension')
    alternative_name = models.CharField(max_length=255, blank=True)
    content = models.TextField(help_text=pgettext_lazy(
        'Category extension', 'CMS-able content.'), blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'category_extensions'

        permissions = (
            ('view', pgettext_lazy('Permission description',
                                   'Can view category extensions')
             ),
            ('edit', pgettext_lazy('Permission description',
                                   'Can edit category extensions')))

    def __str__(self):
        return self.category.name
