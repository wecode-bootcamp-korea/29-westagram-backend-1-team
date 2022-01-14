import json
import re

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
        data = json.loads(request.body)
        
        try:
            if re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data["email"]) == None:
                    return JsonResponse({"message" : "Bad Request_Invalid Email Format"}, status=400)

            if re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", data["password"]) == None:
                    return JsonResponse({"message" : "Bad Request_Invalid Password Format"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                    return JsonResponse({"message" : "Bad Request_Email Already Exist"}, status=400)

            user = User(
                username     = data["username"],
                email        = data["email"],
                password     = data["password"],
                phone_number = data["phone_number"],
            )
            user.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message" : "KeyError"}, status=400)

