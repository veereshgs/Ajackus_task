from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializer import *
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from .models import User
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from rest_framework.generics import ListAPIView


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class FormSignupApi(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            result = {
                "success": True,
                "statusCode": status.HTTP_200_OK,
                "message": "Registered Successfully",
                "token": jwt_token

            }
            return JsonResponse(result, safe=False)
        else:
            result = {
                "success": False,
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "message": "Something Went wrong",

            }
            return JsonResponse(result, safe=False)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("userEmail", None)
        password = request.data.get("password", None)
        if email and password:
            try:
                user = User.objects.get(email=email)
            except:
                final_response = {"message": 'A user with this email is not found.',
                                  "success": False}
                status_code = status.HTTP_200_OK
                return JsonResponse(final_response, status=status_code)

            if user.check_password(password):
                try:
                    payload = JWT_PAYLOAD_HANDLER(user)
                    jwt_token = JWT_ENCODE_HANDLER(payload)
                    update_last_login(None, user)
                except User.DoesNotExist:

                    final_response = {"message": 'User with given email and password does not exists',
                                      "success": False}
                    status_code = status.HTTP_200_OK
                    return Response(final_response, status=status_code)

            else:
                final_response = {"message": 'Given password is wrong',
                                  "success": False}
                status_code = status.HTTP_200_OK
                return Response(final_response, status=status_code)

            final_response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'User logged in  successfully',
                "token": jwt_token,
            }
            status_code = status.HTTP_200_OK
            return Response(final_response, status=status_code)
        else:
            final_response = {"message": 'Please provide password and userEmail',
                              "success": False}
            status_code = status.HTTP_200_OK
            return Response(final_response, status=status_code)


class ContentAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer


    def post(self, request):
        if request.user.is_superuser:
            request.data.update({"is_author": request.user.is_superuser})
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            final_result = {
                "success": True,
                "message": "Content added successfully ",
                "statusCode": status.HTTP_200_OK,
            }
            return JsonResponse(final_result, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Something terrible went wrong',
                                 "success": False, }, safe=False,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        if request.user.is_superuser:
            try:
                if request.data.get('id', None):
                    saved_data = Content.objects.get(pk=request.data.get('id'))
                else:
                    return Response({
                        "id": ["Content id Field is required For Edit"],
                         },
                        status=status.HTTP_400_BAD_REQUEST)
                serializer = self.serializer_class(instance=saved_data, data=request.data)
                serializer.is_valid(raise_exception=True)
                final_result = {
                    "success": True,
                    "statusCode": status.HTTP_200_OK,
                    "message": "Content data of Admin user data Updated successfully "
                }
                return JsonResponse(final_result, safe=False, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e),
                                 "message": "Unable to update Content data",
                                 "success": False, },
                                status=status.HTTP_400_BAD_REQUEST)
        elif request.user:
            try:
                if request.data.get('id', None):
                    saved_data = Content.objects.get(pk=request.data.get('id'), is_author=False)
                else:
                    return Response({
                        "id": ["Content id Field is required For Edit"],
                         },
                        status=status.HTTP_400_BAD_REQUEST)
                serializer = self.serializer_class(instance=saved_data, data=request.data)
                serializer.is_valid(raise_exception=True)
                final_result = {
                    "success": True,
                    "statusCode": status.HTTP_200_OK,
                    "message": "Content data Updated successfully "
                }
                return JsonResponse(final_result, safe=False, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e),
                                 "message": "Unable to update Content data",
                                 "success": False, },
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Author user can Update only Author user data",
                             "message": "Please Login as admin the u can do edit",
                             "success": False, },
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.is_superuser:
            try:
                if request.query_params:
                    obj = Content.objects.get(id=int(request.query_params['id']))
                    obj.delete()

                    final_result = {
                        "success": True,
                        "statusCode": status.HTTP_200_OK,
                        "message": "Content details deleted successfully"
                    }
                    return JsonResponse(final_result, safe=False, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "please provide id in params for to delete",
                                     "success": False, },
                                    status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e),
                                 "message": "Unable to delete Content",
                                 "success": False, },
                                status=status.HTTP_200_OK)
            except BaseException as e:
                return JsonResponse({'error': str(e),
                                     'message': 'Something terrible went wrong',
                                     "success": False,
                                     }, safe=False,
                                    status=status.HTTP_200_OK)

        else:
            try:
                if request.query_params:
                    obj = Content.objects.get(id=int(request.query_params['id']), is_author=False)
                    obj.delete()

                    final_result = {
                        "success": True,
                        "statusCode": status.HTTP_200_OK,
                        "message": "Content details deleted successfully"
                    }
                    return JsonResponse(final_result, safe=False, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "please provide id in params for to delete",
                                     "success": False, },
                                    status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e),
                                 "message": "Unable to delete Content",
                                 "success": False, },
                                status=status.HTTP_200_OK)
            except BaseException as e:
                return JsonResponse({'error': str(e),
                                     'message': 'Something terrible went wrong',
                                     "success": False,
                                     }, safe=False,
                                    status=status.HTTP_200_OK)

class ContentGetAPI(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentGetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "body", "summary"]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            self.queryset = Content.objects.all()
        else:
            self.queryset = Content.objects.filter(is_author=False)
        response = super(ContentGetAPI, self).get(request, *args, **kwargs)
        return response
