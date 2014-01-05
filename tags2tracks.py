#!/usr/bin/python
# -*- coding: UTF-8 -*-


'''
Created on 04.01.2014

@author: volodja
'''





import sys
import os
import mutagen


def printList(name, list_): 
    print(name + ":")
    for row in list_:
        print(str(row).replace("\n", ""))


def executeShellCommand(command):
    command = command.replace("$", "\\$")
    print("exec: " + command)
    result_pipe = os.popen(command)
    result_     = result_pipe.readlines()
    result      = []
    for line in result_:
        result.append(line.replace('\n', ''))
    return result


def capitalizeWords(s):
    s = s.split(" ")
    r = ""
    for l in s:
        r = r + l.capitalize() + " "
    r = str(r).strip()
    r = str(r).replace('/', ',')
    r = str(r).replace('\\', ',')
    return r


def copyImages(file_name_source, directory):
    if os.path.exists(directory + "/scans"):
        return
    
    
    file_name_image_list          = executeShellCommand("find \"" + os.path.split(file_name_source)[0] + "\" \\( -iname \"*.jpg\" -o -iname \"*.png\" \\)")
#     print("file_name_image_list = " + str(file_name_image_list))
    
    if len(file_name_image_list) > 0:
        os.mkdir(directory + "/scans")
#     else:
#         print("no scans")
    
    
    for file_name_image in file_name_image_list:
        file_name_image_dst = directory + "/scans/" + os.path.split(file_name_image)[1]
        for i in range(0, 9):
            if os.path.exists(file_name_image_dst):
                file_name_image_dst = os.path.splitext(file_name_image_dst)[0] + str(i) + os.path.splitext(file_name_image_dst)[1]
        if os.path.exists(file_name_image_dst):
            print("error copy images: '" + file_name_image_dst + "' already exists")
            exit(1) 
        executeShellCommand("cp -v \"" + file_name_image + "\" \"" + file_name_image_dst + "\" > /dev/tty") 


def setUTF8Terminal():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    

setUTF8Terminal()


# print("args = '" + str(sys.argv) + "'")
if len(sys.argv) < 3  or  len(sys.argv) > 4:
    print(sys.argv[0] + " track_file destination_dir [encoding]")
    exit(1)


file_name_source    = sys.argv[1]
ext                 = os.path.splitext(file_name_source)[-1]
destination         = sys.argv[2]

tag                 = mutagen.File(file_name_source)


if not(tag.has_key("artist")  and  tag.has_key("album")  and  tag.has_key("date")  and  tag.has_key("title")  and  tag.has_key("tracknumber")): 
    print
#     print("artist  = '" + str(tag["artist"]) + "'")
#     print("album   = '" + str(tag["album"])  + "'")
#     print("date    = '" + str(tag["date"])   + "'")
#     print("genre   = '" + str(tag["genre"])  + "'")
#     print("title   = '" + str(tag["title"])  + "'")
#     print("number  = '" + str(tag["number"]) + "'")
    print ("tag = '" + str(tag) + "'")
    exit(1)


artist  = capitalizeWords(tag["artist"][0])
album   = capitalizeWords(tag["album"][0])
date    = tag["date"][0]
# genre   = capitalizeWords(tag["genre"][0])
title   = capitalizeWords(tag["title"][0])


# tracknumber = tag["tracknumber"][0]
# tracknumber = tracknumber.split("/")[0]
# number  = int(tracknumber)


number  = int(tag["tracknumber"][0])
if number < 10:
    number = "0" + str(number)
else:
    number = str(number)


directory = destination + "/" + artist + '/' + date + ' ' + album
if not os.path.exists(directory):
    print('mkdir "' + directory + '"')
    os.makedirs(directory)


copyImages(file_name_source, directory)


file_name_destination = directory + '/' + number + ' ' + title + ext
if not os.path.exists(file_name_destination):
    executeShellCommand('cp "' + file_name_source + '" "' + file_name_destination + '"')

