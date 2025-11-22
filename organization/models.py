from django.db import models
from common.models import Audit

class Organization(Audit):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name