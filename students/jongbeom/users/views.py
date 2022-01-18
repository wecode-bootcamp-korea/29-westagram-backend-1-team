import json, re, bcrypt, jwt

from django.views import View
from django.http  import JsonResponse

from users.models import User
from my_settings import SECRET_KEY, ALGORITHMS

class SignUpView(View):
    def get(self, request):
        users   = User.objects.all()
        results = []

        for user in users:
            results.append({
                "username"     : user.username,
                "email"        : user.email,
                "password"     : user.password,
                "phone_number" : user.phone_number,
                "created_at"   : user.created_at,
                "updated_at"   : user.updated_at,
            })
        return JsonResponse({'users' : results}, status=200)

    def post(self, request):
        data           = json.loads(request.body)
        REGEX_EMAIL    = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

        try:
            username        = data["username"]
            email           = data["email"]
            password        = data["password"]
            phone_number    = data["phone_number"]
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "Bad Request(Invalid Email Format)"}, status=400)
            elif not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "Bad Request(Invalid Password Format)"}, status=400)
            elif User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "Bad Request(Email Already Exist)"}, status=400)

            user = User(
                username     = username,
                email        = email,
                password     = hashed_password,
                phone_number = phone_number,
            )
            user.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError: 
            return JsonResponse({"message" : "KeyError"}, status=400)

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email            = data["email"]
            password         = data["password"]
            user             = User.objects.get(email = email)
            encoded_password = user.password.encode('utf-8')
        
            if bcrypt.checkpw(password.encode("utf-8"), encoded_password):
                access_token = jwt.encode(
                    {"user_id": user.id}, SECRET_KEY, algorithm = ALGORITHMS
                )
                return JsonResponse({
                    "message"      : "SUCCESS",
                    "access_token" : access_token
                    }, status=200)
            return JsonResponse({"message" : "INVALID_USER(PASSWORD)"}, status=401)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER(EMAIL)"}, status=401)