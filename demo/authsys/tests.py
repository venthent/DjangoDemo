from django.test import TestCase
import jwt,os
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "ThisIsASecretKEY"
import datetime

if __name__=="__main__":
    a=jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'data': 'eagwage'
        },JWT_SECRET_KEY)
    # print(a)
    # a='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODE1NzI4NTEsImlhdCI6MTU4MTU2OTI1MSwiZGF0YSI6eyJ1c2VybmFtZSI6ImFkbWluIn19.su4HW6G6r51lfm8l_sgLKdQ7fejw11ZQvSVAIMS'
    a='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODE1NzMyNDEsImlhdCI6MTU4MTU2OTY0MSwiZGF0YSI6eyJ1c2VybmFtZSI6ImFkbWluIn19.KXjJJs1OJRJGdjH5uiOxq_7g904BjHxTU-l'
    print(jwt.decode(a,JWT_SECRET_KEY,algorithms=['HS256']))

# Create your tests here.
