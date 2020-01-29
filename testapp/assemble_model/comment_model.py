from . import init_models


class Comment(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    contents = TextField(verbose_name = '내용') #내용
    created = models.DateTimeField(auto_now_add=True) #작성일
    modify_date = models.DateTimeField(null = True, blank = True) #댓글 수정일
    is_active = BooleanField(default = True)
    delete_date = DateTimeField(null = True, blank = True)


    def __str__(self):
        return self.contents
