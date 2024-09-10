from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users
from .serializers import UserSerializer
from rest_framework.decorators import api_view

class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Register successful"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Register Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = Users.objects.get(username=username)
        if user.check_password(password):
            serializer = UserSerializer(user)
            return Response({"message": "Login successful", "user": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except Users.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
