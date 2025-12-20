from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import result
from training.models import training

class RepoResult:
    @staticmethod
    def post(req):
        Training = get_object_or_404(training, training=req['training'])

        new_result = result.objects.create(
            result=req['result'],
            training=Training,
            attendance_summary=req['attendance_summary'],
            footprint_summary=req['footprint_summary'],
            overall_evaluation=req['overall_evaluation']
        )

        return {
            'result': new_result.result,
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
            'attendance_summary': new_result.attendance_summary,
            'footprint_summary': new_result.footprint_summary,
            'overall_evaluation': new_result.overall_evaluation
        }

    @staticmethod
    def get(result_id):
        result_data = get_object_or_404(result, result=result_id)
        Training = result_data.training

        return {
            'result': result_data.result,
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
            'attendance_summary': result_data.attendance_summary,
            'footprint_summary': result_data.footprint_summary,
            'overall_evaluation': result_data.overall_evaluation
        }

    @staticmethod
    def get_all():
        results = result.objects.all()
        return [{
            'result': result_data.result,
            'training': {
                'training': result_data.training.training,
                'nama_latihan': result_data.training.nama_latihan,
                'team': {
                    'team': result_data.training.tim.team if result_data.training.tim else None,
                    'nama_team': result_data.training.tim.nama_team if result_data.training.tim else None,
                    'kategori_team': result_data.training.tim.kategori_team if result_data.training.tim else None,
                    'logo_team': result_data.training.tim.logo_team.url if result_data.training.tim and result_data.training.tim.logo_team else None
                },
                'schedule': {
                    'schedule': result_data.training.jadwal.schedule if result_data.training.jadwal else None,
                    'tanggal': result_data.training.jadwal.tanggal if result_data.training.jadwal else None,
                    'start_time': result_data.training.jadwal.start_time if result_data.training.jadwal else None,
                    'end_time': result_data.training.jadwal.end_time if result_data.training.jadwal else None
                },
                'stadion': {
                    'stadion': result_data.training.lokasi.stadion if result_data.training.lokasi else None,
                    'nama_stadion': result_data.training.lokasi.nama_stadion if result_data.training.lokasi else None,
                    'lokasi': result_data.training.lokasi.lokasi if result_data.training.lokasi else None
                },
                'trainingcategory': [
                    {
                        'trainingcategory': category.trainingcategory,
                        'nama_category': category.nama_category
                    } for category in result_data.training.kategori.all()
                ] if result_data.training.kategori.exists() else [],
                'frequency': {
                    'frequency': result_data.training.frequency.frequency if result_data.training.frequency else None,
                    'frequency_time': result_data.training.frequency.frequency_time if result_data.training.frequency else None
                },
                'start_time': result_data.training.start_time,
                'end_time': result_data.training.end_time,
                'deskripsi': result_data.training.deskripsi
            },
            'attendance_summary': result_data.attendance_summary,
            'footprint_summary': result_data.footprint_summary,
            'overall_evaluation': result_data.overall_evaluation
        } for result_data in results]

    @staticmethod
    def put(req):
        ResultData = get_object_or_404(result, result=req['result'])
        Training = get_object_or_404(training, training=req['training'])

        ResultData.training = Training
        ResultData.attendance_summary = req.get('attendance_summary', ResultData.attendance_summary)
        ResultData.footprint_summary = req.get('footprint_summary', ResultData.footprint_summary)
        ResultData.overall_evaluation = req.get('overall_evaluation', ResultData.overall_evaluation)
        ResultData.save()

        return {
            'result': ResultData.result,
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
            'attendance_summary': ResultData.attendance_summary,
            'footprint_summary': ResultData.footprint_summary,
            'overall_evaluation': ResultData.overall_evaluation
        }

    @staticmethod
    def delete(req):
        ResultData = get_object_or_404(result, result=req['result'])
        result_id = ResultData.result
        ResultData.delete()
        return {'message': f"Result with id {result_id} has been deleted."}