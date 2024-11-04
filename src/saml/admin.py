from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.SAMLAuthNRequestConfiguration)
admin.site.register(models.SAMLIdPConfiguration)
