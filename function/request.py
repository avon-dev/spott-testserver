import jwt


request_bundle = "sending"
sign_up_email_auth = 1001 #email-auth이메일 인증 액션
forgot_user_password = 1002 #
show_posts_home = 1003
show_posts_map = 1004



notice_to_comment = 2000 #알림에서 코멘트 불러오는 액션
basic_comment = 1000 #기본 댓글 api 호출

#리퀘스트 데이터 키

#email-auth 리퀘스트 key

action = 'action' #분기처리
email = 'email'
password = 'password'
nickname = 'nickname'
user_type = 'user_type'
email_auth_req_key = [action, email]




##### 회원가입
sign_req_keys = [email, password, nickname]


###소셜 회원 아이디 체크
social_check_req_keys = [email, user_type]

##소셜 로그인 회원가입
social_sign_req_keys = [email, nickname, user_type]


#############패스워드 찾기
find_password_req_keys = [email, password]



############자동로그인 token_verify and refresh
access = 'access'
refresh = 'refresh'
token_verify_and_refresh = [access,refresh]




####################################댓글 수정
contents = 'contents'
comment_update_keys = [contents]


#############댓글 리스트 보기
created_time = "created_time"
page = 'page'
comment_show_list_keys = [created_time, page, action]

pattern_error = "Not an %s pattern"


##########댓글 추가
caption = 'caption'
comment_create_keys = [caption]


def my_user_uid(self, request):
    string = request.headers["Authorization"]
    decodedPayload = jwt.decode(string[4:],None,None)

    return decodedPayload['user_uid']
