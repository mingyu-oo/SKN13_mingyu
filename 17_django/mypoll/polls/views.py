# view들을 구현
# view : 하나의 user 요청을 처리하는 func

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse     # urls.py에 path이름으로 설정된 url을 조회하는 메소드
from datetime import datetime

from .models import Question, Choice # 모델 클래스들 import
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

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

def list_no_paging(request):
    # DB에서 question들을 조회
    q_list = Question.objects.all().order_by("-pub_date")

    # render() : template 실행해서 그결과로 HttpResponse를 반환하는 func
    return render(
        request,    # HttpRequest객체
        "polls/list.html",  # template 파일 경로
        {"question_list" : q_list}   # template에게 전달할 값, context value
    )


##########################################
# list -> paging 처리 목록 view
# - 요청 parameter(querystring)으로 page번호를 받음
# - 응답 context value(data)
#   - 현재 page에 보여줄 data
#   - 현재 page가 속한 group의 시작/끝 apge 번호
#   - 현재 page group의 시작 page가 **이전 page가 있는지 여부/이전페이지 번호**
#   - 현재 page group의 끝 page가 **다음 page가 있는지 여부/다음페이지 번호**

def list(request):
    paginate_by = 10        # 한 page 당 data 개수
    page_group_count = 10   # 한 page group 당 page 개수
    # http://ip:port/polls/list?page=15
    current_page = int(request.GET.get("page", 1))       # 현재 조회하려는 page 번호, 없으면 1

    # Question data 조회 + Paginator객체 생성
    question_list = Question.objects.all().order_by("-pk")
    pn = Paginator(question_list, paginate_by)

    # 현재 page가 속한 page group의 start/end page 번호 조회
    start_idx = int((current_page-1) / page_group_count) * page_group_count
    end_idx = start_idx + page_group_count
    page_range = pn.page_range[start_idx:end_idx]

    # context_value(context_data) -> template에 전달할 값, dict
    context_value = {
        "page_range" : page_range,  # page group의 시작/끝 page range
        "question_list" : pn.page(current_page),    # page의 data들.
    }

    # page group의 시작page가 이전page가 있는지, 이전page 번호는 무엇인지.
    start_page = pn.page(page_range[0])
    has_previous = start_page.has_previous()
    print(start_page)
    if has_previous:
        previous_page = start_page.previous_page_number()
        context_value["has_previous"] = has_previous
        context_value["previous_page"] = previous_page
    # page group의 끝page가 다음page가 있는지, 다음page 번호는 무엇인지.
    end_page = pn.page(page_range[-1])
    has_next = end_page.has_next()
    if has_next:
        next_page = end_page.next_page_number()
        context_value["has_next"] = has_next
        context_value["next_page"] = next_page
    
    return render(request, "polls/list.html", context_value)


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

@login_required
def vote(request):
    # 1. 요청 parameter 조회
    # question_id = request.POST("question_id") # 없으면 Exception
    question_id = request.POST.get("question_id")    # 없으면 None
    choice_id = request.POST.get("choice")

    ###########################################################################
    # Cookie를 이용해서 이미 투표한 적이 있는 질문이면 투표를 못하게 처리.
    #   - cookie 연습용임, 실제론 DB를 통해서 처리해야함
    # 1. cookie에 voted_question에 question_id가 있는지 여부 확인
    #   - 있으면 error_message와 함께 vote_form으로 이동.
    # 2. 투표 처리 후 cookie votee_question에 투표한 question_id를 추가.
    voted_question_ids = request.COOKIES.get("voted_question")  # cookie 값을 조회.
    if voted_question_ids is not None :
        # 투표한 질문ID를 쿠키에 "1, 2, 3, 10, 5", `,`를 구분자로 저장.
        question_ids = voted_question_ids.split(',')     # "1, 2, 3, 10, 5" -> [1, 2, 3, 10, 5]
        if question_id in question_ids: # 이미 투표한 질문
            question = Question.objects.get(pk = question_id)
            return render(request, "polls/vote_form.html",
                          {"question" : question, "error_message" : "이미 투표한 설문인데용 ?!??"})
            

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
        # voted_question cookie에 투표한 질문ID를 setting
        ## 처음 투표일 경우 (voted_question_ids == None) "question_id" 반환
        ## 기존 투표한 값이 있을 경우 "1, 2, 3, question_id" 형태로 기존의 것에 추가해서 반환
        voted_question_ids = str(question_id) if voted_question_ids is None else f"{voted_question_ids},{question_id}"
        response.set_cookie("voted_question", voted_question_ids, max_age=10)     # max_age = 초(sec) : cookie가 client에서 유지할 시간.
                                                                                            # max_age = 0 : 삭제

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

@login_required
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