from django.db import models
from django.contrib.auth import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Action(models.Model):
    """ Action model for activity stream """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions',
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=225)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        """ Metadata """
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-created']
