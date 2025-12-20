from django.db import models
import user.models as user
import group.models as grp

class message(models.Model):
    id = models.CharField(max_length=60, primary_key=True, unique=True)
    pengirim = models.ForeignKey(user.user, on_delete=models.CASCADE, related_name="pengirim")
    penerima = models.ForeignKey(user.user, on_delete=models.CASCADE, related_name="penerima")
    grup = models.ForeignKey(grp.group, on_delete=models.CASCADE )
    isi_pesan = models.TextField()
    waktu_kirim = models.DateTimeField(auto_now_add=True)
    status_dibaca = models.BooleanField(default=False)
