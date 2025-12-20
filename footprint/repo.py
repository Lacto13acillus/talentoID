from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import footprint
from training.models import training

class RepoFootprint:
    @staticmethod
    def post(req):
        allowed_extensions = ["jpg", "jpeg", "png", "gif", "mp4", "avi", "mov", "mkv"]

        # Validate media file
        if "media" not in req or not req["media"]:
            raise ValidationError("media is required.")

        media = req["media"]
        file_extension = media.name.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            raise ValidationError(f"Invalid file format. Only {', '.join(allowed_extensions)} are allowed.")

        Training = get_object_or_404(training, training=req['training'])

        new_footprint = footprint.objects.create(
            footprint=req['footprint'],
            training=Training,
            media=req['media']
        )

        return new_footprint

    @staticmethod
    def get(training_id):
        footprint_data = footprint.objects.filter(training=training_id)
        return [
            {
                'footprint': f.footprint,
                'media': f.media.url if f.media else None
            }
            for f in footprint_data
        ]

    @staticmethod
    def get_all():
        footprint_list = footprint.objects.all()
        result = []

        for footprint_data in footprint_list:
            Training = footprint_data.training
            result.append({
                'footprint': footprint_data.footprint,
                'training': {
                    'training': Training.training,
                    'nama_latihan': Training.nama_latihan,
                    'team': {
                        'team': Training.tim.team if Training.tim else None,
                        'nama_team': Training.tim.nama_team if Training.tim else None,
                        'kategori_team': Training.tim.kategori_team if Training.tim else None,
                        'logo_team': Training.tim.logo_team.url if Training.tim and Training.tim.logo_team else None
                    },
                    'schedule': {
                        'schedule': Training.jadwal.schedule if Training.jadwal else None,
                        'tanggal': Training.jadwal.tanggal if Training.jadwal else None,
                        'start_time': Training.jadwal.start_time if Training.jadwal else None,
                        'end_time': Training.jadwal.end_time if Training.jadwal else None
                    },
                    'stadion': {
                        'stadion': Training.lokasi.stadion if Training.lokasi else None,
                        'nama_stadion': Training.lokasi.nama_stadion if Training.lokasi else None,
                        'lokasi': Training.lokasi.lokasi if Training.lokasi else None
                    },
                    'trainingcategory': [
                        {
                            'trainingcategory': category.trainingcategory,
                            'nama_category': category.nama_category
                        } for category in Training.kategori.all()
                    ] if Training.kategori.exists() else [],
                    'frequency': {
                        'frequency': Training.frequency.frequency if Training.frequency else None,
                        'frequency_time': Training.frequency.frequency_time if Training.frequency else None
                    },
                    'start_time': Training.start_time,
                    'end_time': Training.end_time,
                    'deskripsi': Training.deskripsi
                },
                'media': footprint_data.media.url if footprint_data.media else None
            })

        return result

    @staticmethod
    def put(req):
        allowed_extensions = ["jpg", "jpeg", "png", "gif", "mp4", "avi", "mov", "mkv"]

        FootprintData = get_object_or_404(footprint, footprint=req['footprint'])
        Training = get_object_or_404(training, training=req['training'])

        FootprintData.training = Training

        if 'media' in req and req['media']:
            media = req['media']
            file_extension = media.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(f"Invalid file format. Only {', '.join(allowed_extensions)} are allowed.")
            FootprintData.media = media

        FootprintData.save()

        return {
            'footprint': FootprintData.footprint,
            'training': {
                'training': Training.training,
                'nama_latihan': Training.nama_latihan,
                'team': {
                    'team': Training.tim.team if Training.tim else None,
                    'nama_team': Training.tim.nama_team if Training.tim else None,
                    'kategori_team': Training.tim.kategori_team if Training.tim else None,
                    'logo_team': Training.tim.logo_team.url if Training.tim and Training.tim.logo_team else None
                },
                'schedule': {
                    'schedule': Training.jadwal.schedule if Training.jadwal else None,
                    'tanggal': Training.jadwal.tanggal if Training.jadwal else None,
                    'start_time': Training.jadwal.start_time if Training.jadwal else None,
                    'end_time': Training.jadwal.end_time if Training.jadwal else None
                },
                'stadion': {
                    'stadion': Training.lokasi.stadion if Training.lokasi else None,
                    'nama_stadion': Training.lokasi.nama_stadion if Training.lokasi else None,
                    'lokasi': Training.lokasi.lokasi if Training.lokasi else None
                },
                'trainingcategory': [
                    {
                        'trainingcategory': category.trainingcategory,
                        'nama_category': category.nama_category
                    } for category in Training.kategori.all()
                ] if Training.kategori.exists() else [],
                'frequency': {
                    'frequency': Training.frequency.frequency if Training.frequency else None,
                    'frequency_time': Training.frequency.frequency_time if Training.frequency else None
                },
                'start_time': Training.start_time,
                'end_time': Training.end_time,
                'deskripsi': Training.deskripsi
            },
            'media': FootprintData.media.url if FootprintData.media else None
        }

    @staticmethod
    def delete(req):
        FootprintData = get_object_or_404(footprint, footprint=req['footprint'])
        footprint_id = FootprintData.footprint
        FootprintData.delete()
        return {'message': f"Footprint with id {footprint_id} has been deleted."}
