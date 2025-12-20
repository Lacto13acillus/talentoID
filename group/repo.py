from django.shortcuts import get_object_or_404
from .models import group
from team.models import team
from user.models import user

class RepoGroup:
    @staticmethod
    def post(req):
        Team = get_object_or_404(team, team=req['team'])
        User = get_object_or_404(user, id_user=req['anggota'])

        new_group = group.objects.create(
            id=req['id'],
            nama_group=req['nama_group'],
            tim=Team,
            anggota=User
        )
        return {
            'id': new_group.id,
            'nama_group': new_group.nama_group,
            'team': {
                'team': Team.team,
                'nama_team': Team.nama_team,
                'kategori_team': Team.kategori_team,
                'logo_team': Team.logo_team.url if Team.logo_team else None
            },
            'anggota': {
                'id': User.id_user,
                'nama': User.nama,
                'email': User.email,
                'nomor_telepon': User.nomor_telepon,
                'foto_profil': User.foto_profil.url if User.foto_profil else None,
                'role': User.role
            }
        }
    
    @staticmethod
    def get(group_id):
        group_data = get_object_or_404(group, id=group_id)
        Team = group_data.tim
        User = group_data.anggota

        return {
            'id': group_data.id,
            'nama_group': group_data.nama_group,
            'team': {
                'team': Team.team,
                'nama_team': Team.nama_team,
                'kategori_team': Team.kategori_team,
                'logo_team': Team.logo_team.url if Team.logo_team else None
            },
            'anggota': {
                'id': User.id_user,
                'nama': User.nama,
                'email': User.email,
                'nomor_telepon': User.nomor_telepon,
                'foto_profil': User.foto_profil.url if User.foto_profil else None,
                'role': User.role
            }
        }
    
    @staticmethod
    def get_all():
        groups = group.objects.all()
        return [{
            'id': group_data.id,
            'nama_group': group_data.nama_group,
            'team': {
                'team': group_data.tim.team,
                'nama_team': group_data.tim.nama_team,
                'kategori_team': group_data.tim.kategori_team,
                'logo_team': group_data.tim.logo_team.url if group_data.tim.logo_team else None
            },
            'anggota': {
                'id': group_data.anggota.id_user,
                'nama': group_data.anggota.nama,
                'email': group_data.anggota.email,
                'nomor_telepon': group_data.anggota.nomor_telepon,
                'foto_profil': group_data.anggota.foto_profil.url if group_data.anggota.foto_profil else None,
                'role': group_data.anggota.role
            }
        } for group_data in groups]

    @staticmethod
    def put(req):
        Group = get_object_or_404(group, id=req['id'])
        Team = get_object_or_404(team, team=req['team'])
        User = get_object_or_404(user, id=req['anggota'])

        Group.nama_group = req.get('nama_group', Group.nama_group)
        Group.tim = Team
        Group.anggota = User
        Group.save()

        return {
            'id': Group.id,
            'nama_group': Group.nama_group,
            'team': {
                'team': Team.team,
                'nama_team': Team.nama_team,
                'kategori_team': Team.kategori_team,
                'logo_team': Team.logo_team.url if Team.logo_team else None
            },
            'anggota': {
                'id': User.id_user,
                'nama': User.nama,
                'email': User.email,
                'nomor_telepon': User.nomor_telepon,
                'foto_profil': User.foto_profil.url if User.foto_profil else None,
                'role': User.role
            }
        }
    
    @staticmethod
    def delete(req):
        Group = get_object_or_404(group, id=req['id'])
        Group.delete()
        return {'message': f"Group with id {req['id']} has been deleted."}