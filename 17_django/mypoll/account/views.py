# account/views.py

from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.forms import (
    AuthenticationForm, # login form
    PasswordChangeForm  # password 변경 form
)
from django.contrib.auth import (
    login,  # login 처리 func, 로그인 한 사용자의 User Model객체를 session에 저장, log 상태를 유지하도록 함.
    logout,  # logout 처리 func, 로그인 상태를 종료
    authenticate,  # 인증 처리 func, username, password를 DB에서 확인.
    update_session_auth_hash,
    # 회원 정보 수정 시 login 상태 유지를 위해 저장된 User모델 객체를 수정된 내용으로 변경하는 func
)
from django.contrib.auth.decorators import login_required

from .forms import CustomUserChangeForm, CustomUserCreationForm

###########################
# 사용자 가입 처리 View
# 요청 url : account/create
#       Get - 가입 폼 양식을 응답
#       POST - 가입 처리
# 응답 : GET - templates/account/create.html
#       POST : home으로 이동 -> redirect

def create(request):
    if request.method == "GET" :
        return render(request, "account/create.html", {"form" : CustomUserCreationForm()})
    else:   # POST
        # 가입 처리
        # 1. 요청 parameter 조회
        form = CustomUserCreationForm(request.POST, request.FILES)
        # 요청 parameter로 넘어온 값을 Form의 instance 변수(attribute)에 저장.

        # 2. 요청 parameter 검증
        ## form.is_valid() : bool -> T : 검증성공, F : 검증 실패
        if form.is_valid():     # 검증 성공 -> 가입 처리
            # form : ModelForm은 save() 기능 제공 -> DB insert 
            # 반환값 : insert 처리한 결과를 가진 Model
            user = form.save()
            print("===== 가입 : user :", type(user), user)
            return redirect(reverse("home"))
        else:   # 검증 실패 -> 실패 처리, 가입 화면으로 이동
            return render(request, "account/create.html", {"form" : form})  # 요청 parameter와 검증결과를 가진


############################
# Login 처리 View
# 요청 url : /account/login
# view : user_login
#   - GET : Login form 제공
#   - POST : Login 처리
# template
#   - GET : templates/account/login.html, POST : home(redirect)

def user_login(request):
    if request.method == "GET":
        # login form 응답
        return render(request, "account/login.html", {"form" : AuthenticationForm()})
    else:
        # login 처리 -> username / password 확인 -> login 상태 유지 처리
        # username / password 조회
        username = request.POST["username"]
        password = request.POST["password"]
        
        # User모델(settings.AUTH_USER_MODEL)을 기반으로 사용자 인증 처리, DB로 부터 username, password 확인
        ## 유효한 username / password면 User모델 객체 반환
        ## 유효하지 않은 경우 None 반환
        user = authenticate(request, username = username, password = password)
        if user is not None:
            # 유효한 user 계정
            login(request, user)    # login 처리 (login 상태 유지)

            next_url = request.GET.get("next")
            if next_url is not None:    # account/login?next=/poll/vote_create
                return redirect(next_url)

            return redirect(reverse("home"))
        else :
            # 유효하지 않은 사용자 계정
            
            return render(request, "account/login.html", 
                          {"form" : AuthenticationForm(), 
                           "error_message" : "아디나 비번이 틀림 😭"})



################################################
# Logout 처리 View
# url : /account/logout
# view : user_logout
# template : redirect 방식 -> home

@login_required
def user_logout(request):
    logout(request)     # logout 처리.
    return redirect(reverse("home"))



################################################
# 사용자 정보를 조회하는 View
#   - 단순 히 template만 실행해서 응답하는 view
#   - Temp;ateView.ax_view(template_name = "template 경로") ==> urls.py
#
# @login_required
# def detail(request):
#     return render(request, "accout/detail.html")



################################################
# password 수정 처리 View
#
# 요청 url : /account/password_change
# view func : password_change
#   - GET : password 변경 form 응답 (template : account/password_change.html)
#   - POST : password 변경 처리 (template : account/detail - redirect)

@login_required
def password_change(request):
    if request.method == "GET":
        # PasswordChangeForm을 비밀번호를 변경할 User 모델을 넣어서 생성, 기존 password 확인용
        # login_user = get_user(request)  # django.contrib.auth.get_user -> login한 User모델 반환
        login_user = request.user
        form = PasswordChangeForm(login_user)
        return render(
            request, "account/password_change.html", {"form" : form}
        )
    else:
        # 요청 parameter 조회 -> 검증(Form)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid(): # 요청 parameter 검증 통과
            # DB에 update
            user = form.save()  # ModelForm.save(): update(0)/insert
            # login 유지를 위해 저장된 User Model 객체를 update된 User Model로 변경
            update_session_auth_hash(request, user)
            return redirect(reverse("account:detail"))
        else :  # 요청 parameter에 문제가 있는 경우
            return render(request, "account/password_change.html", {"form" : form})
        


################################################
# 회원 정보 수정 View
# 요청 url : account/update
# view func : user_update
#   - GET : 수정 양식 page로 이동 (template : account/update.html)
#   - POST : 수정 처리 (template : account/detail - redirect)

@login_required
def user_update(request):
    if request.method == "GET":     # template 반환
        # login한 user의 UserModel 객체를 전달해서 Form 생성
        form = CustomUserChangeForm(instance = request.user)
        return render(request, "account/update.html", {"form" : form})
    else:   # 수정 처리
        # 1. 요청 parameter 조회 + 검증
        form = CustomUserChangeForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            # save
            user = form.save()
            # login 사용자 정보 갱신
            update_session_auth_hash(request, user)
            return redirect(reverse("account:detail"))
        else:
            # 검증 실패 -> 수정폼(update.html)로 이동
            return render(request, "account/update.html", {"form" : form})
        


################################################
# 회원 탈퇴 View
# 요청 url : account/delete
# view func : user_delete
# 응답 : home으로 이동 - redirect

@login_required
def user_delete(request):
    # DB에서 user정보 삭제
    ## data 삭제 - model(pk).delete()
    request.user.delete()
    # logout
    logout(request)
    return redirect(reverse("home"))

# 일반 data를 삭제하는 경우 (제품, 게시판 글 삭제, ...)
# 1. 삭제할 data의 PK값을 요청parameter / Path parameter로 받는다
# 2. Model 이용해서 삭제할 data 조회(1의 PK 이용)
    # q = Question.objects.get(pk=pk)
    # q = Question(pk=pk)
# 3. 2번의 Model.delete()
    # q.delete()