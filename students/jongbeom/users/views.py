import json, re, bcrypt

from django.views import View
from django.http  import JsonResponse

from users.models import User

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
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
            email    = data["email"]
            password = data["password"]   

            if User.objects.filter(email = email, password = password).exists():
                return JsonResponse({"message" : "SUCCESS"}, status=200)
            return JsonResponse({"message" : "INVALID_USER"}, status=401)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)