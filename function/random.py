import string
import random
# class EmailCollection:
#     def email_authentication:
#


class RanStrCraete:
    def number(count):
        _LENGTH = count # 4자릿수 문자 or 숫자
        string_pool = string.digits # 숫자
        random_string = "" # 결과 값
        for i in range(_LENGTH) :
            random_string += random.choice(string_pool) # 랜덤한 문자열 하나 선택

        return random_string

# class asd:
#     aa = "a"
