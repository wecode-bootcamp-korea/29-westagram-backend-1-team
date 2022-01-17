import email
import json, re, bcrypt, jwt

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
            hashed_password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
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
                password     = hashed_password.decode("utf-8"),
                phone_number = phone_number
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)   
        
        except KeyError as e:
            return JsonResponse({"message" : f"KEY_ERROR : ENTER_YOUR_{e.args[0].upper()}"}, status = 400)

class SignInView(View):
    def post(self,request):
        try:
            data       = json.loads(request.body)
            email      = data['email']       
            password   = data['password']
            user       = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 401)
            
            access_token = jwt.encode({'user_id' : user.id}, user.password, algorithm = 'HS256')
            
            return JsonResponse({"message" : f"LOGIN SUCCESS , JWT :{access_token}"}, status = 201)

        except KeyError as e:
            return JsonResponse({"message" : f"KEY_ERROR : {e.args[0].upper()}"}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)