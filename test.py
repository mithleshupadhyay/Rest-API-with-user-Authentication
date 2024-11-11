import hashlib

password = "mith12345"

ans = hashlib.sha256(password.encode("utf-8")).hexdigest()

# print(ans)
# print(len(ans))

import uuid

