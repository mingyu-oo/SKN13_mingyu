from django.db import models
from sqlalchemy import ForeignKey

# Model class ---- DB table
## DB table당 Model class를 정의
## django.db.models.Model 을 상속
## class 변수로 DB table의 column과 연결된 변수(Field)를 선언.
### 변수명(컬럼명) = ModelField(type, 제약 조건 등을 설정)

# Question (설문의 질문을 저장할 Model(table))
class Question(models.Model):
    # Model Field 선언 : 
    ## primary_key 컬럼을 선언하지 않으면 "id"(정수 자동 증가 컬럼)이
    ## primary key 컬럼으로 생성됨.


    # question text(질문) - varcher(문자열 - max length : 200)
    question_text = models.CharField(max_length=200)     # CharField == varchar
    # pub_data (질문 등록 일시) - datetime
    pub_date = models.DateTimeField(auto_now_add=True)  # DateTimeField == datetime
    # auto_now_add : 처음 insert하는 시점의 일시를 자동으로 저장 (등록 일시)
    # auto_now : insert/update하는 시점의 일시를 자동으로 저장 (수정 일시)

    # default : not null, Field에서 nullable 설정, True=null
    
    def __str__(self):
        # 모델 instance 출력/문자열 변환할 때 나올 값을 문자열로 반환
        # self.Field명 -> Field(table column)의 값
        # self.pk -> Primary key Field의 값 반환
        return f"{self.pk}. {self.question_text}"

# Choice(질문의 보기를 저장할 Model)
class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveSmallIntegerField(default=0)
    # FK 설정 : Foreignkey(참조 model class 지정, on_delete 설정)
    question = models.ForeignKey(
        Question,   # 참조 model class
        on_delete=models.CASCADE,   # 부모 table에서 참조하는 값이 삭제되면 같이 삭제. (model.SET_NULL : NULL로 update)
    )
    def __str__(self):

        return f"{self.pk}. {self.choice_text}"