# view들을 구현
# view : 하나의 user 요청을 처리하는 func

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse     # urls.py에 path이름으로 설정된 url을 조회하는 메소드
from datetime import datetime
from .models import Question, Choice # 모델 클래스들 import

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
        {"now" : now, "name" : "우망구"}           # view가 template에 전달할 값들을 directory에 name : value로 묶어서 전달
                                # => context value라고 함.
    )
    # response : HttpResponse(polls/welcome.html 처리 내용)
    print("="*30, type(response))
    return response



##########################################
# 설문 질문 목록을 출력하는 View
#
# url: polls/list
# view함수: list
# template: polls/templates/polls/list.html

def list(request):
    # DB에서 question들을 조회
    q_list = Question.objects.all().order_by("-pub_date")

    # render() : template 실행해서 그결과로 HttpResponse를 반환하는 func
    return render(
        request,    # HttpRequest객체
        "polls/list.html",  # template 파일 경로
        {"question_list" : q_list}   # template에게 전달할 값, context value
    )


##########################################
# 개별 설문 page로 이동하는 view
## 설문 질문 id를 받아서 그 질문에 대해 보기를 선택할 수 있는 page를 응답.
# url : polls/vote_form/질문_id
#   ex) polls/vote_form/2
# view func : vote_form
# template : polls/vote_form.html

def vote_form(request, question_id):
    # question_id : path parameter로 넘어온 값을 받을 변수
    question = Question.objects.get(pk=question_id)

    return render(request, "polls/vote_form.html", {"question":question})


##########################################
# 투표 처리
## choice_id 받아서 votes를 1 증가
# - 응답 : 정상처리 - 투표결과를 응답, 질문 - 보기 (choice_text, votes)
#         요청 parameter 검증 실패(아무것도 선택안하고 요청) - vote_form.html 이동 (다시 투표)
# url : polls/vote
# view func : vote
# 응답 : 정상 - vote_result.html,
#        오류 - vote_form.html

# view func에서 요청 parameter 값 조회
## GET : request.GET - 요청 parameter가 dict에 담겨서 제공
## POST : request.POST - 요청 parameter가 dict에 담겨서 제공

def vote(request):
    # 1. 요청 parameter 조회
    # question_id = request.POST("question_id") # 없으면 Exception
    question_id = request.POST.get("question_id")    # 없으면 None
    choice_id = request.POST.get("choice")
    # 2. 요청 parameter 검증 -> choice가 선택 되었는지 여부
    if choice_id:   # 선택이 된 경우 (정상)
        # votes를 1증가
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save()
        # # 응답 page 이동 -> Question 객체
        # question = Question.objects.get(pk = question_id)
        # return render(request, "polls/vote_result.html", {"question" : question})
    
        # vote_result를 요청하도록 응답 - http응답 상태코드 : 302, 이동할 url 선언 ==> redirect()
        # response = redirect(f"/polls/vote_result/{question_id}")
        url = reverse("polls:vote_result", args=[question_id])  # app_name이 polls인 urls.py에서 name
        print("reverse()가 생성한 url :", type(url), url)
        response = redirect(url)
        print(type(response))
        return response

    else:   # 선택 안된 경우 (예외)
        question = Question.objects.get(pk=question_id)
        return render(
            request, 
            "polls/vote_form.html", 
            {"question" : question, "error_message" : "선택을하셔야죵,,?"}
        )
    

##########################################
# question_id를 받아서 그 질문의 투표 결과를 응답하는 view
# url : polls/vote_reuslt/질문_id
# view func : vote_result
# 응답 template : polls/vote_result.html

def vote_result(request, question_id):
    question = Question.objects.get(pk = question_id)
    return render(request, "polls/vote_result.html", {"question":question})


##########################################
# 설문 질문 등록 (admin에서 안하고도)
# url : polls/vote_create
# view func : vote_create
## Get 방식 요청 : 등록 폼을 제공
## POST 방식 요청 : 등록 처리
# 응답 template
## Get 방식 요청 : polls/vote_create.html
## Post 방식 요청 : list로 이동 -> redirect 방식

# HTTP 요청 방식 조회 - HttpRequest.method => "GET", "POST"

def vote_create(request):
    http_method = request.method
    if http_method == "GET":
        return render(request, "polls/vote_create.html")
    elif http_method == "POST":
        # 요청 parameter 읽기 - 질문, 보기들
        question_text = request.POST.get("question_text")
        # 같은 이름으로 여러 개의 값이 전달된 경우 .getlist("요청 parameter") -> list
        choice_list = request.POST.getlist("choice_text")
        
        # DB에 저장
        q = Question(question_text=question_text)
        q.save()
        for choice_text in choice_list:
            c = Choice(choice_text=choice_text, question = q)
            c.save()

        # 응답 - list로 redirect 방식으로 이동
        # return redirect("/polls/list")
        return redirect(reverse("polls:list"))