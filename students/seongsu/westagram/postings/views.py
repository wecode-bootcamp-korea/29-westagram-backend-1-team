import json

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError 

from .models                import Posting
from users.models           import User

class PostingView(View):
    def post(self, request):
        
        user_data = json.loads(request.body)

        try:
            post_title   = user_data['post_title']
            post_content = user_data['post_content']
            image        = user_data['image']
            user_id      = user_data['user_id']

            if post_title == '' or post_content == '':
                return JsonResponse({"message" : "Please type title and content"}, status = 400)

            
            posting = Posting.objects.create(
                post_title   = post_title,
                post_content = post_content,
                image        = image,
                user_id      = user_id
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError as e:
            return JsonResponse({"message" : "KEY_ERROR: " + str(e).replace("'", '')}, status = 400)

    def get(self, request):
            postings = Posting.objects.all()

            results = []

            for posting in postings:
                results.append(
                    {
                    "id"               : posting.id,
                    "post_title"       : posting.post_title,
                    "post_content"     : posting.post_content,
                    "image"            : posting.image,
                    "created_at"       : posting.created_at,
                    "updated_at"       : posting.updated_at,
                    "user"             : {
                        "id"           : posting.user.id,
                        "name"         : posting.user.name,
                        "email"        : posting.user.email,
                        "phone_number" : posting.user.phone_number
                        }
                    }
                )

            return JsonResponse({"postings" : results}, status = 200)
