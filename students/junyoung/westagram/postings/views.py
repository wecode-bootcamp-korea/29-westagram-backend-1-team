import json

from django.views import View
from django.http  import JsonResponse
from json.decoder import JSONDecodeError

from users.models    import User
from users.utils     import login_decorator
from postings.models import Posting, Image
from my_settings     import SECRET_KEY

class PostingView(View):
    @login_decorator
    def post(self,request):
        try:
            data           = json.loads(request.body)
            user           = request.user
            
            content        = data.get('content')
            image_url_list = data.get('image_url').split(',')

            post = Posting.objects.create(
                content = content,
                user = user,
            )
            for image_url in image_url_list:
                Image.objects.create(
                    image_url = image_url,
                    posting   = post
                )

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except AttributeError:
            return JsonResponse({'message':'NO_IMAGE_URL'}, status=400)
            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        try:
            posts = Posting.objects.all()
            result= [{
                'Name'      : User.objects.get(id=post.user.id).name,
                'Content'   : post.content,
                'Images'    : [image.image_url for image in post.images.all()],
                'Created_at': post.created_at
            } for post in posts
                ]
            
            return JsonResponse({'message': result}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
