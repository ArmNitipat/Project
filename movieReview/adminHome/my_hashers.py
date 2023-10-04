#seting hasher
from django.contrib.auth.hashers import Argon2PasswordHasher

class MyArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = 4         # default: 2
    memory_cost = 204800  # default: 102400
    parallelism = 4       # default: 2
    digest = 'default'    # default: 'default', or choose another hashlib algorithm

# time_cost: เพิ่มค่านี้จะทำให้การทำ hash ช้าลงและปลอดภัยขึ้น
# memory_cost: เพิ่มค่านี้จะทำให้การทำ hash ใช้ memory มากขึ้นและยากต่อการโจมตีด้วยการใช้ ASICs
# parallelism: เพิ่มค่านี้จะทำให้การทำ hash ใช้ thread มากขึ้น เพิ่มประสิทธิภาพในระบบที่มีหลาย core