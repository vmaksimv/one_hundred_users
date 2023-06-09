'''Высчитываю разницу во времени между текущим временем и 23.00, а далее перевожу эту разницу в секунды и делаю задержку выполнения кода'''

import datetime
import time

current_time = datetime.datetime.now().time()
target_time = datetime.time(23, 0)
time_difference = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(datetime.date.today(), current_time)
delay_seconds = time_difference.total_seconds()
# time.sleep(delay_seconds)

print(delay_seconds)

