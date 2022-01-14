import json
import re

from django.views import View
from django.http import JsonResponse

from users.models import User

class SignUpView(View):
    def post(self,request):
        try:
            data                    = json.loads(request.body)
            email                   = data['email']
            password                = data['password']
            phone_number            = data['phone_number']
            email_validation        = r'\w+[@]+\w+[.]+\w+'
            password_validation     = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*\W).{8,}'
            phone_number_validation = r'^(010)\d{8}$'
            
            if not email or not password:
                raise KeyError
            
            elif User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "DUPLICATED_EMAIL"}, status = 409)
            
            elif not re.match(email_validation, email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status = 400)
                    
            elif not re.match(password_validation, password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
        
            elif not re.match(phone_number_validation, phone_number):
                return JsonResponse({"message" : "INVALID_PHONE_NUMBER"}, status = 400)
            
            User.objects.create(
                name         = data["name"],
                email        = email,
                password     = password,
                phone_number = phone_number
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)   
        
        except KeyError as e:
            return JsonResponse({"message" : f"KEY_ERROR : ENTER_YOUR_{e.args[0].upper()}"}, status = 400)
        

        
        
        