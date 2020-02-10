from testapp.assemble_model.user_model import *

# 스크랩을 취소 한다는건 해당 스크랩 테이블에서 레코드가 지워진다는 것을 뜻함
# 게시물이 지워졌을 때 연결 돼 있는 해당 스크랩까지 지워지도록 구현
# 스크랩 날짜를 구해야 될까??? 딱히??? 안 구해도 될거 같다.
class Hashtag(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    name = CharField(max_length = 255)


    def __str__(self):
        return self.name
