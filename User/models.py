from django.db import models
from utils.base_model import BaseModel


class User(BaseModel):
    username = models.CharField(max_length=100)


# Create your models here.
