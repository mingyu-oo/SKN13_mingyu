#  account/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# adumin에서 User를 어떻게 관리할지 화면을 재구성.
# UserAdmin 정의
## list_display : List - admin의 Users(사용자들)의 메인 화면 목록에 나올 항목을 등록.
## add_fieldsets : Tuple - User 등록 화면에 나올 항목들 지정
## fieldsets : Tuple - User 수정 화면에 나올 항목들 지정

class CustomUserAdmin(UserAdmin):
    list_display = ["username", "name", "email"]
    add_fieldsets = (
        ("인증 정보", {"fields":("username", "password1", "password2")}),
        ("개인 정보", {"fields":("name", "email", "birthday")})
    )
    fieldsets = (
        ("인증 정보", {"fields":("username", "password")}),
        ("개인 정보", {"fields":("name", "email", "birthday")})
    )
admin.site.register(User, CustomUserAdmin)
