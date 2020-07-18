import os
import sys


def generateMapping(filename):
    filepath = logFilePath + "\\" + str(filename)
    file = open(filepath, "r+")
    linecontent = file.readlines()
    linecontent_linecount = len(linecontent)
    file.close();

    filenames = dictionary_all.get("filename")
    filenames.append(filename)
    dictionary_all["filename"] = filenames

    starttimes = dictionary_all.get("StartTimeStamp")
    starttimes.append(linecontent[1].split(sep=", ")[0])
    dictionary_all["StartTimestamp"] = starttimes

    endtimes = dictionary_all.get("LastTimeStamp")
    endtimes.append(linecontent[linecontent_linecount - 1].split(sep=", ")[0])
    dictionary_all["LastTimestamp"] = endtimes


def binary_search_starttime(starttime):
    arr = dictionary_all["StartTimeStamp"]
    low = 0
    high = len(arr) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if arr[mid] < starttime:
            low = mid + 1
        elif arr[mid] > starttime:
            high = mid - 1
        else:
            return mid
    return mid - 1


def binary_search_endtime(endtime):
    arr = dictionary_all["LastTimeStamp"]
    low = 0
    high = len(arr) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if arr[mid] < endtime:
            low = mid + 1
        elif arr[mid] > endtime:
            high = mid - 1
        else:
            return mid
    return mid


def searchline_start(content):
    low = 0
    high = len(content) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if content[mid].split(sep=", ")[0] < requested_starttime:
            low = mid + 1
        elif content[mid].split(sep=", ")[0] > requested_starttime:
            high = mid - 1
        else:
            return mid


def searchline_end(content):
    low = 0
    high = len(content) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if content[mid].split(sep=", ")[0] < requested_endtime:
            low = mid + 1
        elif content[mid].split(sep=", ")[0] > requested_endtime:
            high = mid - 1
        else:
            return mid


def getstartfileline(startfile):
    filepath = logFilePath + "\\" + str(startfile)
    file = open(filepath, "r+")
    content = file.readlines()
    lineindex = searchline_start(content)
    return lineindex


def getlastfileline(endfile):
    filepath = logFilePath + "\\" + str(endfile)
    file = open(filepath, "r+")
    content = file.readlines()
    lineindex = searchline_end(content)
    return lineindex


def print_logs():
    for logfilenumber in range(start_index, end_index + 1):
        filepath = (logFilePath + "\\" + str(dictionary_all["filename"][logfilenumber]))
        file = open(filepath, "r+")
        lineslist = file.readlines()
        if (logfilenumber == start_index):
            for index in range(startfilelinenumber, len(lineslist)):
                print(lineslist[index])
        if (logfilenumber != start_index) and (logfilenumber != end_index):
            for index in range(0, len(lineslist)):
                print(lineslist[index])
        if (logfilenumber == end_index):
            for index in range(0, lastfilelinenumber):
                print(lineslist[index])
        file.close();


# MAIN

args = sys.argv
requested_starttime = 0
requested_endtime = 0
requested_path = ""
for token_index in range(len(args)):
    if args[token_index] == "-f":
        requested_starttime = args[token_index + 1]
    if args[token_index] == "-t":
        requested_endtime = args[token_index + 1]
    if args[token_index] == "-i":
        requested_path = args[token_index + 1]

if(requested_endtime<requested_starttime):
    print("Invalid Requested Time")
    exit(0)

logFilePath = requested_path

dictionary_all = {
    "filename": [],
    "StartTimeStamp": [],
    "LastTimeStamp": []
}

files = os.listdir(logFilePath)
for file_name in range(len(files)):
    generateMapping(files[file_name])

start_index = binary_search_starttime(requested_starttime)
start_index_file = dictionary_all["filename"][start_index]
startfilelinenumber = getstartfileline(start_index_file)
# print("Startfile name is "+str(start_index_file)+" and LineStartNumber is "+str(startfilelinenumber))

if (requested_endtime <= dictionary_all["LastTimeStamp"][start_index]):
    end_index = start_index
if (requested_endtime > dictionary_all["LastTimeStamp"][start_index]):
    end_index = binary_search_endtime(requested_endtime)

end_index_file = dictionary_all["filename"][end_index]
lastfilelinenumber = getlastfileline(end_index_file)
# print("Endfile name is "+str(end_index_file)+ " and EndLineNumber is "+str(lastfilelinenumber))

# nooflogfiles=end_index-start_index+1
# print("Number of LogFiles are "+str(nooflogfiles))

print_logs()
