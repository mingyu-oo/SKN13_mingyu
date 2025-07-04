# view들을 구현
# view : 하나의 user 요청을 처리하는 func

from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

def welcome_poll_old(request):
    # view func은 1개 이상의 parameter를 선언해야함. (HttpRequest 객체를 받음)
    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    res_html = f"""<!doctype html>
<html>
    <head>
        <title>Welcome Poll</title>
    </head>
    <body>
        <h1>설문조사 App</h1>
        현재시간 {now}
    </body>
</html>
"""
    return HttpResponse(res_html)

def welcome_poll(request):
    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    # template를 이용해서 응답 page 생성
    response = render(
        request,                # HttpRequest
        "polls/welcome.html",   # template의 경로 (app_directory/templates 이후 경로)
        {"now" : now}           # view가 template에 전달할 값들을 directory에 name : value로 묶어서 전달
                                # => context value라고 함.
    )
    # response : HttpResponse(polls/welcome.html 처리 내용)
    print("="*30, type(response))
    return response