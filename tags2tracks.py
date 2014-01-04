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
    return r


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
genre   = capitalizeWords(tag["genre"][0])
title   = capitalizeWords(tag["title"][0])
number  = int(tag["tracknumber"][0])
if number < 10:
    number = "0" + str(number)
else:
    number = str(number)


directory = destination + "/" + artist + '/' + date + ' ' + album
if not os.path.exists(directory):
    print('mkdir "' + directory + '"')
    os.mkdir(directory)


file_name_destination = directory + '/' + number + ' ' + title + ext
if not os.path.exists(file_name_destination):
    executeShellCommand('cp "' + file_name_source + '" "' + file_name_destination + '"')


