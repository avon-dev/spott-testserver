from testapp.assemble_view.__init__ import *
from random import *
import os
from function import security
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import ast
from Crypto.Cipher import PKCS1_v1_5

import ast, json


class Test(APIView):
    permission_classes = []
    def post(self, request, format=None):

        # f = open("/etc/letsencrypt/live/api.phopo.best/privkey.pem", 'r')
        # private_key = RSA.import_key(f.read())
        #
        # # permissions = os.access("/etc/letsencrypt/live/api.phopo.best/privkey.pem",os.R_OK)
        # print(private_key)
        #
        # f.close()
        #
        # f = open("/etc/letsencrypt/live/api.phopo.best/cert.pem", 'r')
        # publickey = RSA.import_key(f.read())
        #
        # # permissions = os.access("/etc/letsencrypt/live/api.phopo.best/privkey.pem",os.R_OK)
        # print(private_key)
        #
        # f.close()
        #
        # #패스워드 바이트 코드
        # password_byte = [115,101,117,110,103,104,121,117,110,49,33]
        #
        # #패스워드 암호화
        # import struct
        #
        # password_encrypt_byte =[-40,-98,52,97,48,109,94,11,-33,-55,-52,124,96,79,-19,-106]
        #
        # # count  = 0
        # # for byte in password_encrypt_byte:
        # #     password_encrypt_byte[count] = byte -(-127) if byte < 0 else byte
        # #     count +=1
        # #대칭키 값
        # secret_key_bytes = [81,-117,-52,-46,-91,-77,93,86,-85,37,-91,63,44,125,122,-41,-49,-118,-96,-104,48,56,-47,-61,109,-105,22,9,-79,121,41,-85]
        #
        # #대칭키를 공개키로 암호화 한 값
        # public_encrypt_byte_string = [32,65,80,-126,90,-113,75,-38,93,-69,-127,-68,30,-80,16,48,-34,-92,93,-32,-49,-51,-124,54,1,-24,48,75,112,-36,12,-74,27,36,107,-48,108,-13,70,97,108,112,14,-16,-87,46,21,93,-77,-49,87,127,-24,61,93,72,8,-50,-2,-31,-21,-17,99,-78,-36,109,-50,107,87,-76,114,120,84,37,76,3,-120,-107,37,-44,-112,-101,-97,29,-87,-5,69,48,84,60,122,-33,25,117,9,124,-5,-120,-15,9,57,-7,50,-56,16,71,-40,-117,-103,21,113,47,74,-80,9,-116,105,-74,81,40,-90,102,95,-3,44,17,-78,-33,65,29,37,-24,-44,-128,-48,25,8,16,-125,-121,19,-53,-30,-68,-95,46,110,-47,-22,-115,-45,21,-128,27,58,16,78,-15,14,105,-94,-105,75,-30,-16,-107,-97,93,-122,105,-64,-27,-68,-49,27,122,-96,121,21,55,-7,26,-101,-11,-58,-44,-67,33,-31,-64,53,97,-66,68,-106,-65,28,-56,7,-9,17,18,54,-50,27,-122,-100,-23,118,-91,76,31,54,19,-55,83,-88,-70,10,-116,-42,62,-66,-67,119,-48,-111,-19,-16,-76,125,-60,-76,101,-100,54,-66,-34,-115,0,-85,-32,94,-49,-22,44,69,4,55,-13,123,-10,-117,-84,67,26]
        #
        # #iv
        # iv_bytes = [87,-7,62,-96,-13,3,7,-78,48,87,-39,-3,-32,-12,124,-110]
        #
        # #iv를 공개키로 암호화 한 값
        # iv_encrypt_bytes = [37,-116,-113,65,-27,-66,-49,-35,39,126,106,81,\
        # 77,92,-120,-1,81,-76,116,-8,-38,-92,77,-37,-28,59,-128,122,118,-86,19,30,\
        # -47,-63,-15,-123,-31,126,80,-52,-116,99,30,123,49,62,116,-33,29,-77,-43,\
        # -128,-24,-98,35,-111,116,71,-18,102,27,-45,-15,-102,38,-118,94,76,-60,-27\
        # ,-118,32,73,-14,-123,-44,-57,-70,-29,-6,106,93,-107,-74,-71,-86,13,99,-25,\
        # -115,38,75,-19,-114,48,-37,35,84,62,-23,-72,114,-96,27,-54,-108,17,118,49,\
        # -8,40,102,-127,28,-69,33,-127,54,-111,-20,-25,-76,112,48,68,-90,-34,-39,0,-27,5,6]
        #
        #
        # # secret_key_bytes = bytes(secret_key_bytes)
        # elements =[-40,-98,52,97,48,109,94,11,-33,-55,-52,124,96,79,-19,-106]
        # # b_array = bytearray(elements)
        #
        # #1번 공개키
        # test1 = [-59, -128, 29, -13, 125, -109, -60, 85, -91, -58, 92, -90, -90, -71, -96, -57, -118, -77, -97, 32, -21, -38, 24, -79, 7, -62, -8, -79, 94, 87, 90, -53, 120, 38, -21, -23, 13, -100, 74, 115, 116, -77, -61, 8, 115, 29, -33, 12, -83, 66, 116, -38, 79, 32, 57, 61, -89, 49, 62, -61, -27, -40, -79, 79, -5, -7, -20, 12, 8, -25, -114, -33, 103, 125, -79, 61, -45, 43, -121, -77, 28, -17, 63, -70, -9, -23, -81, -64, -12, -4, -13, 43, 90, -108, 102, -94, 94, 47, 78, 56, -1, 102, -117, 16, 68, -76, 32, -109, -33, 58, 36, -17, -21, -121, -72, 37, -26, -23, 48, -102, -41, 65, -60, 61, 24, 71, -121, -76, -54, -88, 55, -99, 103, -7, 94, 81, 37, 59, -71, -128, 20, -23, 17, -23, 15, -111, 80, -18, 92, -125, -9, -110, 68, -114, 103, -51, 113, 69, -92, -70, 27, 123, 119, 8, -19, 42, -112, 42, 112, 24, 93, 38, -31, -48, -9, -48, 14, 74, -78, -119, -59, 35, 23, 114, 66, 37, 119, -31, 53, -101, 77, 105, 26, -111, 103, 26, -44, 46, 123, 120, 9, 115, 65, -7, 1, -73, -22, 63, -24, -63, 46, 120, 26, 125, 16, 8, 117, 34, 15, 111, 102, 89, -118, -75, -66, -15, 50, 104, 67, 89, -22, 52, -54, 67, 34, 12, 31, 22, 13, 65, 110, 89, 43, -82, 40, 28, -15, -52, 93, 8, -30, 106, -101, -127, -60, -126]
        #
        # #2번 공개키
        # test2 = [42, -124, -4, 119, 78, -96, 18, 101, 55, -1, -37, -88, -81, 71, 25, 116, 37, -26, 67, -125, -4, 42, -39, -53, 13, 43, -11, -41, -119, 94, -93, -98, -65, -91, -21, -42, -121, -7, 121, 52, 113, -37, 35, -96, -17, 39, 70, 101, -57, -122, -73, -125, -113, 4, 98, 87, -3, -65, -13, 61, 55, 63, -52, -54, 47, 108, -58, 123, 47, -9, 93, -58, -2, 90, 12, -42, -52, -72, 100, 24, -23, 118, 84, -59, -47, 30, -86, 58, -67, 18, 93, 46, 3, -109, -11, 15, -35, 102, -87, -94, -122, 102, 45, -117, -15, 90, -128, 48, 56, -87, -77, -118, -54, 16, 84, -28, 15, -117, -43, -65, -50, 119, -39, -16, 85, 49, 31, 27, 45, 107, 62, 92, 98, -12, 10, -59, 43, -3, -53, 42, -69, -85, -103, 118, -11, -88, 35, -117, 9, 86, 4, -101, -91, -106, 16, 8, -77, 24, 15, 25, -88, -69, 16, 91, 4, 43, 5, -67, -104, 65, -2, 78, 47, 43, 124, 20, -2, -59, -110, 23, 29, 21, -113, -6, 112, -110, -104, 53, 25, -27, -65, -128, -126, -19, -121, 50, 126, 59, -20, 70, 48, -86, -86, 24, -21, -30, 111, -90, 61, -89, 95, -50, 30, -77, 20, 17, -123, 5, -112, 69, -123, 61, -23, 118, 114, 9, -113, 79, -17, 27, -122, -99, 121, 125, 86, 92, -6, -54, -46, 93, -47, -98, -26, -35, -2, 41, -87, -109, 39, -35, -82, -7, -68, 51, 93, -26]
        #
        #
        # #RSA -> RSA/NONE/PKCS1PADDING cipher1Result:
        # test3 =  [32, -21, 71, 96, -31, 116, 33, -59, -44, -52, -20, 39, -5, -126, -104, 39, 48, -15, 38, 85, 76, -33, 92, -127, -91, 126, -85, -20, 105, -54, -106, 58, 4, -17, -128, -91, -12, -36, -119, -6, 45, -89, 62, 28, -79, -63, -86, 42, 11, -37, -95, 105, 102, 104, -40, 44, 16, -109, 85, 118, 113, 20, 89, 27, 77, -1, -100, 73, 68, 4, -112, 104, -71, 11, -35, -74, 109, 73, -5, -96, 71, -82, -59, -23, 113, -121, 77, 1, 94, -82, 62, -126, 63, -5, 98, 29, 65, -117, -41, 93, 2, 126, -94, -7, 27, -85, 25, 54, 61, 25, -85, -59, -35, 125, 36, -2, 20, -50, 71, -93, -39, 68, -61, 117, 110, 127, -13, -88, 40, 55, 106, -27, 47, 96, 85, -51, -86, 120, 81, 15, 33, 54, 83, -107, 69, 109, -21, -95, -112, -80, -60, -86, -103, 113, -125, -55, -95, -108, 122, 111, -94, 83, 58, 123, -119, -92, 105, 94, -45, -109, 40, 34, -36, -63, -77, -119, 63, 19, 26, 2, 104, -72, 75, -47, 112, 78, 44, 69, -121, 103, -18, -106, 115, -68, -75, 114, 62, 105, 97, -83, 58, -105, 6, -5, -55, 108, -59, -8, -8, -33, 74, -6, -79, 36, -118, 8, -105, -106, -4, -99, -126, 112, -55, 52, -45, 108, 89, 43, -89, 26, 125, -84, 77, -114, 1, 24, -72, -83, -80, 24, -29, -120, -87, -84, 77, 120, 117, 54, -9, 93, 77, -69, -26, -38, 124, 29]
        # #RSA -> RSA/NONE/PKCS1PADDING cipher2Result:
        # test4 =  [29, -76, 102, -100, 107, 55, 20, -73, -78, 89, -89, -118, 114, 97, -103, 89, 56, 69, -45, 11, -23, -105, -8, -121, 41, -36, -10, 77, 33, -19, 29, 47, -3, 1, -6, 22, -21, -8, -99, -90, 110, -121, -101, -112, -114, -9, -125, -126, -31, -117, 51, -6, -118, 94, 56, -90, 8, 80, 67, -78, 47, 107, 114, -72, -88, 127, 41, -124, -61, -84, 63, 95, -81, 80, 71, -72, 117, -123, 27, 110, 127, -15, 25, -72, -45, -78, -61, -53, -28, -71, 110, -116, -82, -68, -70, -50, -80, -5, -124, 81, 58, 5, -18, -20, 9, 41, 107, -91, 80, 92, -101, -5, -30, 27, -81, -83, -77, -101, 119, 15, 83, -104, 33, 57, -2, 64, 35, -113, -93, 87, 68, 30, 60, -36, -42, -61, -95, -77, 90, -1, -80, -22, -5, -59, -28, -38, -55, 65, -22, 105, 39, -95, 105, 100, -18, -59, -106, 115, 118, 43, -29, 45, -3, -31, 18, 38, -82, -38, -14, -24, 50, 79, -81, -89, -60, -86, -37, -128, 3, 126, -126, -111, -73, -5, 68, 126, 51, -36, -125, 92, -33, -120, -116, 44, 20, -73, -82, -54, 51, -39, 99, -90, 73, 127, 110, 12, -44, -98, -50, -108, -76, 78, 103, 81, 100, 93, -7, -75, -89, 91, 85, -2, 92, -71, -18, -113, 93, 29, 123, 27, 115, -8, -12, -18, -70, -2, -100, 41, -65, 114, -68, -116, 80, 58, 106, -77, 93, 35, -26, 113, 109, -11, 118, 50, 43, 72]
        #
        # #RSA/NONE/PKCS1PADDING cipher1Result: 대칭키 암호화
        # test5 = [-77, -30, 2, -90, 43, 52, 41, 63, 49, 19, 87, -49, 1, -29, 20, 77, -60, 36, 119, 15, 107, 40, 20, -71, 117, -23, -82, -7, 60, 68, 116, 14]
        #
        # password_byte = bytes(password_byte)
        #
        # # dd = "tmdgus1!"
        # # publickey = private_key.publickey()
        # #
        # # encryptor = PKCS1_OAEP.new(publickey)
        # # encrypted = encryptor.encrypt(hangle)
        # rsa = security.RSAPublicKey()
        # encrypted = rsa.signed_to_unsigned(test3)
        # decrypted = rsa.decrypt(encrypted)
        # password = security.RSAPublicKey().out_password(test3)
        # dddd = security.AESCipher.decrypt(decrypted)
        print(f'request_data : {request.data}')
        print(f'request_data : {request.GET}')
        password = request.GET['sending']
        # security.RSAPublicKey.literal_eval(password)
        re = security.RSAPublicKey()
        asd = re.literal_eval(password)
        print(f'password : {re.literal_eval(password)}')
        aaa = re.signed_to_unsigned(asd)
        print(aaa.decode())
        return Response(request.data)
# data.exportKey()
# {"publickey":str(encryptor)}
class Test2(APIView):
    permission_classes = []
    def get(self, request, format=None):
        # repl = Return_Module.ReturnPattern.string_to_dict(request.data)
        # repl['nickname'] = "asdasd"
        # asd = repl['nickname']
        # result = Return_Module.ReturnPattern.success_text("Create success",**repl)
        # bb = repl.replace("'",'"')
        # json = json.loads(repl)
        # json = json.loads(aa)
        # json = json.loads(aa)
        # asd = json.loads(request.data)
        # load = json.loads(request.data)
        # loads
        # asd = json.dumps(request.data.dict())
        # serializer = TestSerializer(asd)
        # aa = request.data['sending']
        # posts_data = Post.objects.all()
        # asd = posts_data.count()
        # posts_data = posts_data[0:5].values()
        # dateime.datetime.now()
        KST = datetime.timezone(datetime.timedelta(hours=0))
        # today = datetime.datetime.today(datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        return Response(str(now))
            # return Response(random_string)


    @transaction.atomic
    def post(self, request, format=None):

        # request_data = Return_Module.multi_string_to_dict(request.data)
        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        for count in range(1,10):
            lat = uniform(35.204104,37.722390) #전국
            long = uniform(126.706945,128.983172)
            # lat = uniform(37.489324,37.626495) #서울
            # long = uniform(126.903712,127.096659)
            id = randint(2,11)
            stt = ""
            _LENGTH = 8 # 몇자리?
            string_pool = "가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허"
            result = "" # 결과 값
            for i in range(_LENGTH) :
                stt += choice(string_pool)
            user = User.objects.get(id=10)
            posts = Post.objects.create(user=user,\
            latitude = lat,\
            longitude = long,\
            contents = stt,\
            posts_image = request.FILES[f'{count}'],\
            # back_image = request.FILES[f'{count}b'],\
            is_public = True)
        # posts = Post.objects.create(latitude = request.data["latitude"], longitude = request.data["longitude"],text = request.data["text"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts.save()
        # serializers = PostsSerializer(data = request.data)
        # if serializers.is_valid():
        #      serializers.save()
        #      asd = str(request.FILES['posts_image'].name)
        # asd = request_data["text"]
        # file = request.FILES['back_image'].content_type = 'image/jpeg'
        return Response("success", status=status.HTTP_201_CREATED)
