from django.contrib import admin
from .models import Question, Choice

# Model class를 admin app에서 관리할 수 있도록 등록
admin.site.register(Question)
admin.site.register(Choice)