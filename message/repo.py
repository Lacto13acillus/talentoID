# repository/message_repository.py
from django.shortcuts import get_object_or_404
from .models import message
from user.models import user
from group.models import group

class RepoMessage:
    @staticmethod
    def post(req):
        Pengirim = get_object_or_404(user, id_user=req['pengirim'])
        Penerima = get_object_or_404(user, id_user=req['penerima'])
        Grup = get_object_or_404(group, id=req['grup'])

        new_message = message.objects.create(
            id=req['id'],
            pengirim=Pengirim,
            penerima=Penerima,
            grup=Grup,
            isi_pesan=req['isi_pesan'],
            status_dibaca=req.get('status_dibaca', False)
        )
        return {
            'id': new_message.id,
            'pengirim': {
                'id': Pengirim.id_user,
                'nama': Pengirim.nama,
                'email': Pengirim.email
            },
            'penerima': {
                'id': Penerima.id_user,
                'nama': Penerima.nama,
                'email': Penerima.email
            },
            'grup': {
                'id': Grup.id,
                'nama_group': Grup.nama_group
            },
            'isi_pesan': new_message.isi_pesan,
            'status_dibaca': new_message.status_dibaca
        }
    
    @staticmethod
    def get(message_id):
        message_data = get_object_or_404(message, id=message_id)
        return {
            'id': message_data.id,
            'pengirim': {
                'id': message_data.pengirim.id_user,
                'nama': message_data.pengirim.nama,
                'email': message_data.pengirim.email
            },
            'penerima': {
                'id': message_data.penerima.id_user,
                'nama': message_data.penerima.nama,
                'email': message_data.penerima.email
            },
            'grup': {
                'id': message_data.grup.id,
                'nama_group': message_data.grup.nama_group
            },
            'isi_pesan': message_data.isi_pesan,
            'status_dibaca': message_data.status_dibaca
        }
    
    @staticmethod
    def get_all():
        messages = message.objects.all()
        return [{
            'id': msg.id,
            'pengirim': {
                'id': msg.pengirim.id_user,
                'nama': msg.pengirim.nama,
                'email': msg.pengirim.email
            },
            'penerima': {
                'id': msg.penerima.id_user,
                'nama': msg.penerima.nama,
                'email': msg.penerima.email
            },
            'grup': {
                'id': msg.grup.id,
                'nama_group': msg.grup.nama_group
            },
            'isi_pesan': msg.isi_pesan,
            'waktu_kirim': msg.waktu_kirim,  # Include timestamp
            'status_dibaca': msg.status_dibaca
        } for msg in messages]

    @staticmethod
    def put(req):
        Message = get_object_or_404(message, id=req['id'])
        Pengirim = get_object_or_404(user, id_user=req['pengirim'])
        Penerima = get_object_or_404(user, id_user=req['penerima'])
        Grup = get_object_or_404(group, id=req['grup'])

        Message.pengirim = Pengirim
        Message.penerima = Penerima
        Message.grup = Grup
        Message.isi_pesan = req.get('isi_pesan', Message.isi_pesan)
        Message.status_dibaca = req.get('status_dibaca', Message.status_dibaca)
        Message.save()

        return {
            'id': Message.id,
            'pengirim': {
                'id': Pengirim.id_user,
                'nama': Pengirim.nama,
                'email': Pengirim.email
            },
            'penerima': {
                'id': Penerima.id_user,
                'nama': Penerima.nama,
                'email': Penerima.email
            },
            'grup': {
                'id': Grup.id,
                'nama_group': Grup.nama_group
            },
            'isi_pesan': Message.isi_pesan,
            'status_dibaca': Message.status_dibaca
        }
    
    @staticmethod
    def delete(req):
        Message = get_object_or_404(message, id=req['id'])
        Message.delete()
        return {'message': f"Message with id {req['id']} has been deleted."}