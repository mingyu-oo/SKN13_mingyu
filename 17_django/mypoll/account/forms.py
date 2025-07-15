# account/forms.py
## Form이나 ModelForm class를 정의하는 module
## 보통 Form은 등록 / 수정 폼 각각 하나씩 정의함.

### User 등록폼, User 수정폼 ==> ModelForm으로 구성

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

# ModelForm : forms.ModelFrom을 상속, Form : forms.Form을 상속

# UserCreationForm에 정의된 Form field : username, password1, password2
# CustiomUserCreationForm : UserCreationForm의 Form field + name, email, birthday
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User   # User Model의 model field를 이용해서 Form field를 구성.
        # fields = "__all__"  # model의 모든 field를 이용해서 구성.
        fields = ["username", "password1", "password2", "name", "email", "birthday", "profile_img"]    # 특정 model field를 선택해서 구성.
        # exclude = ["name"]     # 지정한 model field를 제외한 나머지로 구성.
        # fields와 exclude는 같이 사용 불가.

        # Form field의 input type을 변경
        ## birthday input type : text -> date
        # key : field 이름, value : widget객체
        widgets = {
            "birthday" : forms.DateInput(attrs={"type" : "date"})
        }


    ##################################################################
    # 검증
    # Form / ModelForm에서 하는 기본 검증
    #   - blank = False : required 검증
    #   - 숫자 입력 : 숫자인지 검증
    #   - Email / 일시 입력 : email / 일시 형식 검증
    #
    # 검증 method를 추가, domain 특화 검증을 할 경우 def
    #   - clean() : 모든 field를 한번에 검증
    #   - clean_field이름() : 개별 field 검증
    #   - 검증 시 문제가 발생하면 forms.ValidationError("에러 이유 메세지") 반환
    #   - 검증 시 문제가 없으면 검증한 값(요청 parameter) 반환.
    
    # name : 두 글자 이상 입력
    def clean_name(self):
        # self.cleaned_data : dict - 기본 검증을 통과한.
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError("사용자 이름은 두 글자 이상 입력하쇼.")
        return name
    

# 회원 정보 수정 폼 - Modelform
class CustomUserChangeForm(UserChangeForm):
    
    password = None # 비밀번호 변경 설정 링크가 나오지 않도록 설정
    
    class Meta:
        model = User
        fields = ["name", "email", "birthday", "profile_img"]
        widget = {
            "birthdaty" : forms.DateInput(attrs = {"type" : "data"})
        }

    # name : 두 글자 이상 입력
    def clean_name(self):
        # self.cleaned_data : dict - 기본 검증을 통과한.
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError("사용자 이름은 두 글자 이상 입력하쇼.")
        return name