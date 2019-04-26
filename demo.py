a = 'asdfASDdf'

import re

b = re.match(r'[a-z,A-Z]{5}', a)
print(b)
