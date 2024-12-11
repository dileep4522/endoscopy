from asyncio import current_task
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

from .models import *
from .serializers import *

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import random
from dev.database_router import DatabaseRouter
from .serializers import LoginSerializer, ReportSerializers,PatientDetailSerializers,RegistrationSerializer,UserDetailsSerializer,EmailVerificationSerializer,PasswordUpdateSerializer





@api_view(['POST'])
def add_patient(request):
    # current_user = request.user
    # if request.user.is_authenticated:
        patient_email=Patientsdetails.objects.filter(patient_email=request.data.get('patient_email'))
        if request.method == 'POST':
            if patient_email.exists():
                return JsonResponse({"status": "patient_already_exists"})
            serializer = PatientsdetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "patient_added_successfully"})

            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def delete_patients(request):
    if request.user.is_authenticated:
        ids_to_delete = request.data.get('ids', [])  # Expects a list of ids to delete
        if not ids_to_delete:
            return JsonResponse({"status": "No_IDs_provided"}, status=status.HTTP_400_BAD_REQUEST)
        patients = Patientsdetails.objects.filter(id__in=ids_to_delete)

        if patients.exists():
            patients.delete()
            return JsonResponse({"status": "Patients_deleted_successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({"status": "No_patients_found_with_the_provided_IDs"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def patient_report_file(request):
    if request.user.is_authenticated:
        reports = Patientreports.objects.filter(patient_details_id=request.query_params.get("patient_id"))
        if reports.exists():
            serializer = PatientreportsSerializer(reports, many=True)
            return JsonResponse(
                {"status": "Patient_report_file_retrieved_successfully", "patient_reports": serializer.data},
                status=status.HTTP_200_OK  # Correct usage of status code
            )
        else:
            return JsonResponse(
                {"status": "No_reports_found_for_this_patient."},
                status=status.HTTP_404_NOT_FOUND  # Correct usage of status code
            )
    else:
        return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def patient_save_report(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            serializer = Patient_save_report(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status':'successfully_added_Patient_report'})
            else:
                return JsonResponse({'status':'please_add_valid_id_or_valid_Report'})
    else:
        return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            print("Username:",username)
            print("Password:",password)

            user = authenticate(username=username,password=password)

            if user is not None:
                login(request, user)
                # user_id = User.objects.get(username=request.user)
                return Response({"status": "user_validated"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)


        return Response({'status': 'Invalid_Credentials'}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
# @csrf_exempt
def register_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "User_created_successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def email_verification(request):
    # if request.user.is_authenticated:
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = random.randint(100000, 999999)

            try:
                user = User.objects.get(email=email)
                user_details, created = UserDetails.objects.get_or_create(user_id=user)
                user_details.otp = otp
                user_details.save()

                send_mail(
                    subject="Your OTP for Email Verification",
                    message=f"Your OTP is: {otp}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                return Response({"message": "OTP_sent_successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User_with_this_email_does_not_exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def validate_otp(request):
    # if request.user.is_authenticated:
        otp = request.data.get('otp')

        if not otp:
            return Response({"error": "OTP_is_required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_details = UserDetails.objects.get(otp=otp)

            if user_details:
                return Response({"message": "OTP_verified_successfully."}, status=status.HTTP_200_OK)

        except UserDetails.DoesNotExist:
            return Response({"error": "Invalid_OTP."}, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def update_password(request):
    # if request.user.is_authenticated:
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not email or not password or not confirm_password:
            return Response({"error": "Email, password, and confirm_password are_required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            serializer = PasswordUpdateSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(password)
                user.save()
                return Response({"message": "Password_updated_successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User_with_this_email_does_not_exist."}, status=status.HTTP_404_NOT_FOUND)
    # else:
    #     return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def patient_list(request):
    if request.user.is_authenticated:
        patients = Patientsdetails.objects.all()
        serializer = PatientDetailSerializers(patients,many=True)
        return Response(serializer.data)
    else:
        return JsonResponse({"status": "unauthorized_user"}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def logout_view(request):
        logout(request)
        return Response({"message": "Successfully_logged_out."}, status=status.HTTP_200_OK)




class WorkersListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        print("getttt WorkersListAPIView")
        # try:
        db = DatabaseRouter.db_for_read(Patientsdetails)  # Pass the model
        data = Patientsdetails.objects.using(db).all()
        serializer = patient_detailsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     print("eeeee",e)

