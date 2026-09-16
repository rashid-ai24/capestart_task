from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Assignment
from .serializers import AssignmentSerializer

@api_view(['GET'])
def assignment_list(request):
    assignments = Assignment.objects.all()
    serializer = AssignmentSerializer(assignments,many=True)
    return Response(serializer.data)