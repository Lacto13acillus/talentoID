# repository/notif_repository.py
from django.shortcuts import get_object_or_404
from .models import notif
from user.models import user
from group.models import group

class RepoNotif:
    @staticmethod
    def post(req):
        Penerima = get_object_or_404(user, id_user=req['penerima'])
        Grup = get_object_or_404(group, id=req['grup'])

        new_notif = notif.objects.create(
            id=req['id'],
            penerima=Penerima,
            grup=Grup,
            status_dibaca=req.get('status_dibaca', False)
        )
        return {
            'id': new_notif.id,
            'penerima': {
                'id': Penerima.id_user,
                'nama': Penerima.nama,
                'email': Penerima.email
            },
            'grup': {
                'id': Grup.id,
                'nama_group': Grup.nama_group
            },
            'status_dibaca': new_notif.status_dibaca
        }
    
    @staticmethod
    def get(notif_id):
        notif_data = get_object_or_404(notif, id=notif_id)
        return {
            'id': notif_data.id,
            'penerima': {
                'id': notif_data.penerima.id_user,
                'nama': notif_data.penerima.nama,
                'email': notif_data.penerima.email
            },
            'grup': {
                'id': notif_data.grup.id,
                'nama_group': notif_data.grup.nama_group
            },
            'status_dibaca': notif_data.status_dibaca
        }
    
    @staticmethod
    def get_all():
        notifications = notif.objects.all()
        return [{
            'id': notif_data.id,
            'penerima': {
                'id': notif_data.penerima.id_user,
                'nama': notif_data.penerima.nama,
                'email': notif_data.penerima.email
            },
            'grup': {
                'id': notif_data.grup.id,
                'nama_group': notif_data.grup.nama_group
            },
            'status_dibaca': notif_data.status_dibaca
        } for notif_data in notifications]

    @staticmethod
    def put(req):
        Notif = get_object_or_404(notif, id=req['id'])
        Penerima = get_object_or_404(user, id_user=req['penerima'])
        Grup = get_object_or_404(group, id=req['grup'])

        Notif.penerima = Penerima
        Notif.grup = Grup
        Notif.status_dibaca = req.get('status_dibaca', Notif.status_dibaca)
        Notif.save()

        return {
            'id': Notif.id,
            'penerima': {
                'id': Penerima.id_user,
                'nama': Penerima.nama,
                'email': Penerima.email
            },
            'grup': {
                'id': Grup.id,
                'nama_group': Grup.nama_group
            },
            'status_dibaca': Notif.status_dibaca
        }
    
    @staticmethod
    def delete(req):
        Notif = get_object_or_404(notif, id=req['id'])
        Notif.delete()
        return {'message': f"Notif with id {req['id']} has been deleted."}