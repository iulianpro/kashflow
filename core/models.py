from django.db import models


class AuthVarsControl(models.Model):
    state = models.CharField(null=True, blank=True, max_length=32)

    def __str__(self):
        return self.state
