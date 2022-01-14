import json
import re

from django.views import View
from django.http import JsonResponse

from users.models import User

class SignUpView(View):
    def post(self,request):
        try:
            data               = json.loads(request.body)
            email              = data['email']
            password           = data['password']
            phone_number       = data['phone_number']
            REGEX_EMAIL        = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD     = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            REGEX_PHONE_NUMBER = r'^(010)\d{8}$'

            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status = 400)
                    
            elif not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
        
            elif not re.match(REGEX_PHONE_NUMBER, phone_number):
                return JsonResponse({"message" : "INVALID_PHONE_NUMBER"}, status = 400)
            
            elif User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "DUPLICATED_EMAIL"}, status = 409)
            
            User.objects.create(
                name         = data["name"],
                email        = email,
                password     = password,
                phone_number = phone_number
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)   
        
        except KeyError as e:
            return JsonResponse({"message" : f"KEY_ERROR : ENTER_YOUR_{e.args[0].upper()}"}, status = 400)

class SignInView(View):
    def post(self,request):
        try:
            data               = json.loads(request.body)
            email              = data['email']
            password           = data['password']
        
            if not User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        
            elif not User.objects.filter(password = password).exists():
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 401)
        
            return JsonResponse({"message" : "LOGIN SUCCESS"}, status = 201)
        
        except KeyError as e:
            return JsonResponse({"message" : f"KEY_ERROR : ENTER_YOUR_{e.args[0].upper()}"}, status = 400)