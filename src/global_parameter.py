import os
import time

project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), '.'))
current_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
monkey_log_path = project_path + "\\bugreport_out\\monkey_log\\"+current_time+".txt"

print(monkey_log_path)



