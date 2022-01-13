import json
import re

from django.views import View
from django.http import JsonResponse

from users.models import User

class SignUpView(View):
    def post(self,request):
        data                    = json.loads(request.body)
        email_validation        = '\w+[@]+\w+[.]+\w+'
        password_validation     = '^(?=.*\D)(?=.*\d)(?=.*\W).{8,}'
        phone_number_validation = '^[010]{1}\d{8}'
                
        if not data["email"] or not data["password"]:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        elif not re.match(email_validation, data["email"]):
            return JsonResponse({"message" : "INVALID_EMAIL"}, status = 400)
        
        elif User.objects.filter(email = data["email"]).exists():
            return JsonResponse({"message" : "DUPLICATED_EMAIL"}, status = 409)
        
        elif not re.match(password_validation, data["password"]):
            return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
        
        elif not re.match(phone_number_validation, data["phone_number"]):
            return JsonResponse({"message" : "INVALID_PHONE_NUMBER"}, status = 400)
                
        else:
            User.objects.create(
                name         = data["name"],
                email        = data["email"],
                password     = data["password"],
                phone_number = data["phone_number"],
            )   
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        
        