from django.db import models
import group.models as grp
import user.models as user

class notif(models.Model):
    id = models.CharField(max_length=60, primary_key=True, unique=True)
    penerima = models.ForeignKey(user.user, on_delete=models.CASCADE )
    grup = models.ForeignKey(grp.group, on_delete=models.CASCADE)
    status_dibaca = models.BooleanField(default=False)