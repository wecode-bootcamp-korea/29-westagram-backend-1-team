import json, re

from django.views import View
from django.http  import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError 

from .models      import User

class SignUpView(View):
    def post(self, request):
        
        user_data = json.loads(request.body)

        try:
            email          = user_data['email']
            password       = user_data['password']
            regex_email    = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
            regex_password = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if user_data['name'] == '':
                return JsonResponse({"message" : "Please type your name"}, status = 400)
            
            elif not re.fullmatch(regex_email, email):
                return JsonResponse({"message" : "Please type valid email address"}, status = 400)

            elif not re.fullmatch(regex_password, password):
                return JsonResponse({"message" : "must have 1 alphabet, 1 numbers, 1 special character and minimum 8 letter"}, status = 400)

            elif User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "email already exist"}, status = 400)

            else:
                user = User.objects.create(
                    name         = user_data["name"],
                    email        = email,
                    password     = password,
                    phone_number = user_data["phone_number"]
                )
                return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError as e:
            return JsonResponse({"message" : "KEY_ERROR: " + str(e).replace("'", '')}, status = 400)
        