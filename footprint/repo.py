from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import footprint, FootprintCategory
from training.models import training
import mimetypes


class RepoFootprint:

    # =============================
    # 🔧 HELPER
    # =============================
    @staticmethod
    def _validate_media(media):
        allowed_extensions = ["mp4", "avi", "mov", "mkv"]

        if not media:
            raise ValidationError("media is required.")

        file_extension = media.name.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            raise ValidationError(
                f"Invalid file format. Only {', '.join(allowed_extensions)} are allowed."
            )

    @staticmethod
    def _get_training(training_id):
        return get_object_or_404(training, training=training_id)

    @staticmethod
    def _get_category(category_name):
        if not category_name:
            raise ValidationError("category is required.")

        return get_object_or_404(
            FootprintCategory, category=category_name  # 🔥 PK string
        )

    # =============================
    # ✅ CREATE
    # =============================
    @staticmethod
    def post(req):
        try:
            # =============================
            # ✅ Validasi basic
            # =============================
            if not req.get("training"):
                raise ValueError("training is required")

            if not req.get("category"):
                raise ValueError("category is required")

            # =============================
            # ✅ Ambil relasi
            # =============================
            Training = RepoFootprint._get_training(req.get("training"))
            Category = RepoFootprint._get_category(req.get("category"))

            # =============================
            # ✅ Create data
            # =============================
            new_footprint = footprint.objects.create(
                footprint=req.get("footprint"),
                training=Training,
                category=Category,
                media=req.get("media"),
                hasJerseyNumber=req.get("hasJerseyNumber"),
            )

            # =============================
            # ✅ Response
            # =============================
            return {
                "footprint": new_footprint.footprint,
                "category": new_footprint.category.category,
                "media": new_footprint.media.url if new_footprint.media else None,
                "hasJerseyNumber": new_footprint.hasJerseyNumber,
            }

        except Exception as e:
            print(f"RepoFootprint.post ERROR: {str(e)}")
            raise

    # =============================
    # ✅ GET BY TRAINING
    # =============================
    @staticmethod
    def get(training_id):
        footprint_data = footprint.objects.filter(training=training_id)

        result = []
        for f in footprint_data:
            mime_type, _ = (
                mimetypes.guess_type(f.media.url) if f.media else (None, None)
            )

            result.append(
                {
                    "footprint": f.footprint,
                    "category": f.category.category,
                    "media": f.media.url if f.media else None,
                    "mimeType": mime_type,
                    "hasJerseyNumber": f.hasJerseyNumber,
                }
            )

        return result

    # =============================
    # ✅ GET ALL
    # =============================
    @staticmethod
    def get_all():
        footprint_list = footprint.objects.all()
        result = []

        for f in footprint_list:
            Training = f.training

            result.append(
                {
                    "footprint": f.footprint,
                    "category": f.category.category,  # 🔥 string langsung
                    "training": {
                        "training": Training.training,
                        "nama_latihan": Training.nama_latihan,
                        "team": {
                            "team": Training.tim.team if Training.tim else None,
                            "nama_team": (
                                Training.tim.nama_team if Training.tim else None
                            ),
                            "kategori_team": (
                                Training.tim.kategori_team if Training.tim else None
                            ),
                            "logo_team": (
                                Training.tim.logo_team.url
                                if Training.tim and Training.tim.logo_team
                                else None
                            ),
                        },
                        "schedule": {
                            "schedule": (
                                Training.jadwal.schedule if Training.jadwal else None
                            ),
                            "tanggal": (
                                Training.jadwal.tanggal if Training.jadwal else None
                            ),
                            "start_time": (
                                Training.jadwal.start_time if Training.jadwal else None
                            ),
                            "end_time": (
                                Training.jadwal.end_time if Training.jadwal else None
                            ),
                        },
                        "stadion": {
                            "stadion": (
                                Training.lokasi.stadion if Training.lokasi else None
                            ),
                            "nama_stadion": (
                                Training.lokasi.nama_stadion
                                if Training.lokasi
                                else None
                            ),
                            "lokasi": (
                                Training.lokasi.lokasi if Training.lokasi else None
                            ),
                        },
                        "trainingcategory": (
                            [
                                {
                                    "trainingcategory": c.trainingcategory,
                                    "nama_category": c.nama_category,
                                }
                                for c in Training.kategori.all()
                            ]
                            if Training.kategori.exists()
                            else []
                        ),
                        "frequency": {
                            "frequency": (
                                Training.frequency.frequency
                                if Training.frequency
                                else None
                            ),
                            "frequency_time": (
                                Training.frequency.frequency_time
                                if Training.frequency
                                else None
                            ),
                        },
                        "start_time": Training.start_time,
                        "end_time": Training.end_time,
                        "deskripsi": Training.deskripsi,
                    },
                    "media": f.media.url if f.media else None,
                }
            )

        return result

    # =============================
    # ✅ UPDATE
    # =============================
    @staticmethod
    def put(req):
        FootprintData = get_object_or_404(footprint, footprint=req["footprint"])

        if "training" in req:
            FootprintData.training = RepoFootprint._get_training(req["training"])

        if "category" in req:
            FootprintData.category = RepoFootprint._get_category(req["category"])

        if "media" in req and req["media"]:
            RepoFootprint._validate_media(req["media"])
            FootprintData.media = req["media"]

        FootprintData.save()

        return {
            "footprint": FootprintData.footprint,
            "category": FootprintData.category.category,
            "media": FootprintData.media.url if FootprintData.media else None,
        }

    # =============================
    # ✅ DELETE
    # =============================
    @staticmethod
    def delete(req):
        FootprintData = get_object_or_404(footprint, footprint=req["footprint"])
        footprint_id = FootprintData.footprint
        FootprintData.delete()

        return {"message": f"Footprint with id {footprint_id} has been deleted."}
