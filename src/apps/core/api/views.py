from rest_framework.response import Response
from rest_framework.views import APIView


class DeleteView(APIView):
    """АПИ Вьюшка удаления сущности"""
    model = None

    def post(self, request):
        object_id = request.data.get('id')
        try:
            self.model.objects.get(pk=object_id).safe_delete()
        except Exception as e:
            print('something gone wrong')
            print(repr(e))
        return Response({'result': {'status': True}})
