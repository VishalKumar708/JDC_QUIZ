from django.db import models


class BaseModel(models.Model):
    isActive = models.BooleanField(default=False)
    groupId = models.CharField(max_length=40, default=1)
    createdBy = models.ForeignKey('User.User', on_delete=models.SET_NULL, related_name="%(class)s_createdBy",
                                  null=True, blank=True)
    updatedBy = models.ForeignKey('User.User', on_delete=models.SET_NULL, related_name="%(class)s_updatedBy",
                                  null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True)
    updatedDate = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


