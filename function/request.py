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
email_auth_req_key = [action, email]




##### 회원가입
sign_req_keys = [email, password, nickname]



pattern_error = "Not an %s pattern"




def my_email(self, request):
    string = request.headers["Authorization"]
    decodedPayload = jwt.decode(string[4:],None,None)

    return decodedPayload['id']
