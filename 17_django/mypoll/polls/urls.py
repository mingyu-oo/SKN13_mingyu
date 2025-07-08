# polls/urls.py : polls app의 url-mapping을 선정
## url - view

from django.urls import path
from . import views

urlpatterns = [
    path("welcome", views.welcome_poll, name="welcome"),
    path("list", views.list, name="list"),
    # http://127.0.0.1:8000/polls/list -> views.list() -> list.html -> User
    path("vote_form/<int:question_id>", views.vote_form, name="vote_form"),
    # http://127.0.0.1:8000/polls/vote_form/질문ID -> path parameter 설정
    ## <type:받을 view parameter 이름>
    path("vote", views.vote, name="vote"),
    # http://127.0.0.1:8000/polls/vote -> 투표처리
    path("vote_result/<int:question_id>", views.vote_result, name="view_result")
    # http://127.0.0.1:8000/polls/vote_result/1
]