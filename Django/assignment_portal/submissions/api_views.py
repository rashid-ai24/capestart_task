from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Submission
from .serializers import SubmissionSerializer

@api_view(['GET'])
def submission_list(request):
    submissions = Submission.objects.all()
    serializer = SubmissionSerializer(submissions,many=True)
    return Response(serializer.data)