from .repo import RepoDeviceStats
import uuid

class UsecaseDeviceStats:
    @staticmethod
    def post(request):
        reqs = {
            'devicestats': uuid.uuid4(),  # Generate UUID untuk devicestats
            'player': request.data['player'],
            'jenis_perangkat': request.data['jenis_perangkat'],
            'metric': request.data['metric'],
            'value': request.data['value'],
            'unit': request.data['unit']
        }
        dataPost = RepoDeviceStats.post(reqs)
        return dataPost
    
    @staticmethod
    def get(devicestats_id):
        dataStats = RepoDeviceStats.get(devicestats_id)
        return dataStats
    
    @staticmethod
    def get_all():
        dataStats = RepoDeviceStats.get_all()
        return dataStats
    
    @staticmethod
    def put(request):
        reqs = {
            'devicestats': request.data['devicestats'],
            'player': request.data['player'],
            'jenis_perangkat': request.data.get('jenis_perangkat'),
            'metric': request.data.get('metric'),
            'value': request.data.get('value'),
            'unit': request.data.get('unit')
        }
        updated_stats = RepoDeviceStats.put(reqs)
        return updated_stats
    
    @staticmethod
    def delete(request):
        reqs = {
            'devicestats': request.data['devicestats']
        }
        delete_message = RepoDeviceStats.delete(reqs)
        return delete_message