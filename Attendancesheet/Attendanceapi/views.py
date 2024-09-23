from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer,UserLoginSerializer,ProfileSerializer,UserPasswordChangeSerializer,EmployeeSerializer,EmployeeSearchSerializer,UserPasswordResetSerializer,ForgotPasswordSerializer,EmployeeAttendanceSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Employee
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken  
# Create your views here.

# --------------------------------for token generation-----------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# -------------------------------------User Registration view----------------------------
class UserRegisterView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user= serializer.save()
            return Response({'msg' : "Register Successfull"},status=status.HTTP_201_CREATED) 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#--------------------------------- Admin Or User Login View --------------------------------- 
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer= UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                response_data = {
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin}
                token= get_tokens_for_user(user)
                return Response({'msg' : "Login Successfull",'user':response_data,'Token':token},status=status.HTTP_200_OK)
            else:
                return Response({'Errors' : {'non_fields_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#--------------------- User Data fetching using Access Tokemn ------------------------------
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated] 
    def post(self,request,format=None):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
#---------------------- User password change View-----------------------------------------
class UserPasswordChangeView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserPasswordChangeSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg' : "Password Changed Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# -------------------OTP send for User password Forget View-----------------------------------------
class SendOTPView(APIView):
    def post(self, request, format=None):
        serializer = UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------OTP svalidation for User password Forget View-----------------------------------------
class ResetPasswordView(APIView):
    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------New EmployeeRegistration view----------------------------
class EmployeeRegisterView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user= serializer.save()
            return Response({'msg' : "Employee Register Successfull"},status=status.HTTP_201_CREATED) 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDeleteview(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    # -----------------------------Employee data Delete functions------------------------------
    def delete(self, request, employee_code):
        employee = get_object_or_404(Employee, employee_code=employee_code)
        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    # -----------------------------Employee data Update functions------------------------------
    def put(self, request, employee_code):
        employee = get_object_or_404(Employee, employee_code=employee_code)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeSearchView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = EmployeeSearchSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the validated data
            employee_code = serializer.validated_data.get('employee_code', None)
            zone = serializer.validated_data.get('zone', None)
            supervisor_name = serializer.validated_data.get('supervisor_name', None)
            employee_name = serializer.validated_data.get('employee_name', None)
            date = serializer.validated_data.get('date', None)

            # Construct the query with filters
            query = Q()
            if employee_code:
                query &= Q(employee_code__icontains=employee_code)
            if zone:
                query &= Q(zone__icontains=zone)
            if supervisor_name:
                query &= Q(supervisor_name__icontains=supervisor_name)
            if employee_name:
                query &= Q(employee_name__icontains=employee_name)
            if date:
                query &= Q(date=date)

            # Query the database
            employees = Employee.objects.filter(query)
            
            if employees.exists():
                # Serialize the result
                employee_serializer = EmployeeSerializer(employees, many=True)
                return Response(employee_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "No employees found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeAttendanceAPIView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    
    def post(self,request, *args, **kwargs):
        serializer=EmployeeAttendanceSerializer(data=request.data,many=True)
        if serializer.is_valid(raise_exception=True):
            user= serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes=[UserRenderer]
    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data.get("refresh_token")
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful, token blacklisted"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


