from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.AllowAny]

class DeleteAllTodo(APIView):

    def delete(self, request):
        # Delete all records
        Todo.objects.all().delete()
        # Returns a status code of 204 indicating that there is not content in our database
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllTodo(APIView):
    
    def get(self, request):
        tasks = Todo.objects.all()

        serializer = TodoSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)