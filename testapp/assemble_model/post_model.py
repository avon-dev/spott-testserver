from testapp.assemble_model.hashtag_model import *





class Post(models.Model): #!내용(conents), !작성일, !수정일, !공개여부(public),
                            # !게시물 신고 여부, !신고 날짜, 부적절 게시물 여부(problem), !삭제여부, !삭제 날짜
    posts_image = ImageField(default = 'basic_image')
    back_image = ImageField(default = 'blank')
    latitude = FloatField()
    longitude = FloatField()
    contents = TextField(verbose_name = '내용') #내용
    created = models.DateTimeField(auto_now_add=True) #작성일
    modify_date = models.DateTimeField() #게시글 수정일
    public = models.BooleanField(default = False) #공개여부
    report = models.BooleanField(default = False) #신고여부
    report_date = models.DateTimeField() #신고 날짜
    problem = BooleanField(default = False)
    is_active = BooleanField(default = True)
    delete_date = DateTimeField()
    hashtags = models.ManyToManyField(Hashtag)
    like_users = models.ManyToManyField('User', through = 'PostLike',)
    scrap_users = models.ManyToManyField('User', through = 'Scrap',)
    def __str__(self):
        return self.contents
