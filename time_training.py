import time
from datetime import datetime



now = datetime.now()
dt_string = now.strftime("%H")
print(9 == int(dt_string))
