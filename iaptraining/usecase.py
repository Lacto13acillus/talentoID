from .repo import RepoIAPTraining
import uuid

class UsecaseIAPTraining:
    @staticmethod
    def post(request):
        technical = []
        physical = []
        goalkeeper = []
        social = []
        
        # Process technical data
        tech_data = request.data.get('technical', [])
        for i in range(0, len(tech_data), 3):
            technical.append({
                'type': tech_data[i],
                'current_achieve': tech_data[i + 1],
                'target': tech_data[i + 2]
            })

        # Process physical data
        phys_data = request.data.get('physical', [])
        for i in range(0, len(phys_data), 3):
            physical.append({
                'type': phys_data[i],
                'current_achieve': phys_data[i + 1],
                'target': phys_data[i + 2]
            })

        # Process goalkeeper data
        gk_data = request.data.get('goalkeeper', [])
        for i in range(0, len(gk_data), 3):
            goalkeeper.append({
                'type': gk_data[i],
                'current_achieve': gk_data[i + 1],
                'target': gk_data[i + 2]
            })

        # Process social data
        soc_data = request.data.get('social', [])
        for i in range(0, len(soc_data), 3):
            social.append({
                'type': soc_data[i],
                'current_achieve': soc_data[i + 1],
                'target': soc_data[i + 2]
            })

        reqs = {
            'player': request.data['player'],
            'training': request.data['training'],
            'technical': technical,
            'physical': physical,
            'goalkeeper': goalkeeper,
            'social': social
        }
        return RepoIAPTraining.post(reqs)

    @staticmethod
    def get(iaptraining_id):
        return RepoIAPTraining.get(iaptraining_id)

    @staticmethod
    def get_all():
        return RepoIAPTraining.get_all()
    
    @staticmethod
    def get_by_player_and_training(player_id, training_id):
        return RepoIAPTraining.get_by_player_and_training(player_id, training_id)

    @staticmethod
    def put(request):
        reqs = {
            'iaptraining': request.data['iaptraining'],
            'player': request.data['player'],
            'training': request.data.get('training'),
            'category': request.data.get('category'),
            'type': request.data.get('type'),
            'current_achieve': request.data.get('current_achieve'),
            'target': request.data.get('target')
        }
        return RepoIAPTraining.put(reqs)

    @staticmethod
    def delete(request):
        reqs = {
            'iaptraining': request.data['iaptraining']
        }
        return RepoIAPTraining.delete(reqs)