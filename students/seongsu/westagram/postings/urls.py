from django.urls import path

from .views      import PostingView, CommentView, LikeView, FollowView

urlpatterns = [
    path("/posting", PostingView.as_view()),
    path("/comment", CommentView.as_view()),
    path("/like", LikeView.as_view()),
    path("/follow", FollowView.as_view())
]
