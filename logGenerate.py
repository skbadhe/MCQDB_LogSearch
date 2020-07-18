import datetime as date
import random
import time as tm

logFilePath="C:\\Users\\Shubham\\Desktop\\MCQdb\\logs\\"
filenameconv="LogFile-"

for j in range(150):
    filename=logFilePath+filenameconv+str(100000+j)+".log"
    logfile=open(filename,'w')
    for i in range (300):
        time = date.datetime.now().isoformat()
        line = time + ", Some Field" + str(random.randint(0, 300)) + ", Other Field" + str(random.randint(0, 300)) + ", And so on, Till new line,...\n"
        logfile.write(line)
    logfile.close()
    tm.sleep(1)