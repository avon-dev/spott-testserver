# Phopo Server

*인생샷 서포트 어플리케이션 포포 서버*

#### Download

<a href="https://play.google.com/store/apps/details?id=com.avon.spott"><img src="https://lh3.googleusercontent.com/cjsqrWQKJQp9RFO7-hJ9AfpKzbUb_Y84vXfjlP0iRHBvladwAfXih984olktDhPnFqyZ0nu9A5jvFwOEQPXzv7hr3ce3QVsLN8kQ2Ao=s0"></a>

<br>


## 프로젝트 기간
2019.11 ~ 2020.03

## Requirements

#### 서버 환경 설정
+ Ubuntu 18.04
+ Python 3.6
+ PostgreSQL 10.12
+ NGINX 1.14
+ pip 20.0.2
+ libpq-dev 12.2-2
+ postgresql-contrib

#### 데이터베이스 세팅
+ client_encoding = utf8
+ default_transaction_isolation = read committed
+ timezone = UTC

#### Django
+ asgiref==3.2.3
+ boto3==1.11.9
+ botocore==1.14.9
+ config==0.4.2
+ Django==3.0.1
+ django-debug-toolbar==2.1
+ django-request-logging==0.7.0
+ django-sslserver==0.22
+ django-storages==1.8
+ djangorestframework==3.11.0
+ docutils==0.15.2
+ drf-tracking==1.5.0
+ gunicorn==20.0.4
+ Pillow==7.0.0
+ psycopg2-binary==2.8.4
+ PyJWT==1.7.1
+ python-dateutil==2.8.1
+ pytz==2019.3
+ s3transfer==0.3.2
+ six==1.14.0
+ sqlparse==0.3.0
+ urllib3==1.25.8

## API Document
+ https://lwbvv.gitbook.io/lee/

<br>

기능
-------
### 1. 지도
<p>
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77423869-7aafd880-6e13-11ea-9484-9b1645cef511.gif">  
</p>

- 지도에서 인생샷 장소를 찾아볼 수 있습니다.

### 2. 카메라
<p>
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77516642-19910f00-6ebe-11ea-96d4-ba8968683629.gif">  
</p>

- 윤곽선과 가이드 사진을 이용하여 원하는 사진을 따라찍을 수 있습니다.


### 3. 검색
<p>
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77425020-6b318f00-6e15-11ea-9e47-22f09a59ebd7.jpg">  
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77425043-7684ba80-6e15-11ea-894a-d5d1a43d9071.jpg">
</p>

- 해시태그나 유저를 검색 할 수 있습니다.
- 최근 검색에는 최근에 검색한 해시태그, 유저가 표시됩니다.

### 4. 사진 업로드
<p>
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77424930-4210fe80-6e15-11ea-87f2-4102ae53c860.jpg">
</p>

- 업로드할 사진의 위치 정보를 가져옵니다. 위치 정보가 없다면 위치 검색, 내 위치를 활용하여 직접 위치 정보를 등록해야 합니다.

### 5. 로그인
<p>
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77424976-56ed9200-6e15-11ea-9d3e-e5ffe9625be5.jpg">
</p>

- 이메일 로그인과 구글 로그인, 페북 로그인을 사용할 수 있습니다.



### 6. 기타
<p>
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77425167-a3d16880-6e15-11ea-8f26-3dbfa9ffdff9.jpg">  
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77425193-af249400-6e15-11ea-884f-6bcbbe5c5bc7.jpg">
  <img width="240" src="https://user-images.githubusercontent.com/51042849/77425207-b5b30b80-6e15-11ea-90b4-12511a6186dc.jpg">
</p>

- 다른 사람의 사진을 좋아요, 스크랩할 수 있고 사진에 댓글을 남길 수 있습니다.
- 부적절한 사진과 댓글을 신고할 수 있습니다.

<br/>

