import json, re

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import User

class UserView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        if user_data['email'] == '' or user_data['password'] == '':
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
            
        elif not re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', user_data['email']):
            return JsonResponse({"message" : "Please type valid email address"}, status = 400)

        elif not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', user_data['password']):
            return JsonResponse({"message" : "must have 1 alphabet, 1 numbers, 1 special character and minimum 8 letter"}, status = 400)

        elif User.objects.filter(email = user_data['email']).exists():
            return JsonResponse({"message" : "email already exist"}, status = 400)

        else:
            user = User.objects.create(
                name         = user_data["name"],
                email        = user_data["email"],
                password     = user_data["password"],
                phone_number = user_data["phone_number"]
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)

    def get(self, request):
        users = User.objects.all()

        results = []

        for user in users:
            results.append({
                "id"            : user.id,
                "name"          : user.name,
                "email"         : user.email,
                "password"      : user.password,
                "phone_number"  : user.phone_number,
                "created_at"    : user.created_at,
                "updated_at"    : user.updated_at,
            })

        return JsonResponse({"owners" : results}, status = 200)
