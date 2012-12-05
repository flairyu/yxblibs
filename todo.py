#!/usr/bin/env python

#    'todo' is little tool for create your todo-list.
#
#    Copyright (C) 2012  Yu Xiangbo or YXB for short.  
#                        Email: xiangbo_x@hotmail.com
#	
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import sys, os

# define version
VERSION = "1.0"

# define help msgs
HELPMSG = '''\
todo is a little tool for create your todo-list.
author: yxb
version: %s
usage: todo (a)dd|(d)one|del|(l)ist|(c)lear|(h)elp|? [args]
    add: add a todo item into list. [args] should be the msg what todo.
    done: done a item. [args] is the id.
    del: remove a item. [args] is the id(s)
    clear: clear the todo list.
    list: list undo items. [args] can be 'all' or 'a', for show all item.
    help|?: show this doc.
example:
    todo 'I have write a todo tools.'       #will add a item.
    todo add 'another mission to be done.'  #also add a item.
    todo list                               #list todos.
    todo del 1:10 13 15                     #delete 1 to 10, and 13,15 items
    todo done 1:10 13 15                    #mark 1 to 10, 13 and 15 is done
    todo                                    #list todos.
    todo l a                                #list all
        ''' % VERSION

# define file path
FILEPATH = os.environ['HOME'] + "/.todolist"

# define todo list status
class TodoStatus:
    UNDO = "*"
    DONE = "o"
    DELE = "-"

# the todo list
TODOLIST = []

def loadTodoList():
    global TODOLIST
    try:
        infile = open(FILEPATH)
        for line in infile:
            line = line.strip('\n')
            if len(line)<>0 :
                TODOLIST.append(line)
        infile.close()
    except IOError:
        print "no data file, creat new:", FILEPATH
        saveTodoList()
    #except:
    #    print '\nSome error/exception occurred when open data file:', FILEPATH

# save todo list to file (~/.todolist)
def saveTodoList():
    global TODOLIST
    try:
        outfile = open(FILEPATH, "w")
        for it in TODOLIST:
            outfile.write(it + '\n')
        outfile.close()
    except IOError:
        print "can't write file:", FILEPATH
    except:
        print "\nSome error/exception occured when write data file:", FILEPATH

# add a new todo thing.
def addItem(args):
    global TODOLIST
    loadTodoList()
    if len(args)==2:
        TODOLIST.append(TodoStatus.UNDO + '|' + args[1])
    elif len(args) >2:
        TODOLIST.append(TodoStatus.UNDO + '|' + args[2])
    saveTodoList()
    print "success to add a item"

# set line head to status
def setLineStatu(lines, status):
    global TODOLIST
    linelimit = lines.split(':')
    if len(linelimit) >= 2:
        for i in range(int(linelimit[0]), int(linelimit[1])):
            if i < len(TODOLIST):
                TODOLIST[i] = status + TODOLIST[i][1:]
    else:
        TODOLIST[int(lines)] = status + TODOLIST[int(lines)][1:]

# set one or more todo things to [done] status
def doneItem(args):
    if len(args) <= 2:
        print "miss args for 'done', see help"
        return
    loadTodoList()
    for i in range(2, len(args)):
        lines = args[i]
        setLineStatu(lines, TodoStatus.DONE)
    saveTodoList()
    print "they are mark as done"

# delete one or more todo things
def deleteItem(args):
    global TODOLIST
    if len(args) <= 2:
        print "miss args for 'delete', see help"
        return
    loadTodoList()
    for i in range(2, len(args)):
        lines = args[i]
        setLineStatu(lines, TodoStatus.DELE)
    data = []
    for line in TODOLIST:
        if line[0] <> TodoStatus.DELE:
            data.append(line)
    TODOLIST = data[:]
    saveTodoList()
    print "delete them all"

# list todo things
def listItem(args):
    global TODOLIST
    loadTodoList()
    print "------------------------------------------------------"
    i = 0
    printcount = 0
    for line in TODOLIST:
        if len(args)>2 and ('a' in args[2]):
            print "%3d|%s"%(i,line)
            printcount += 1
        elif line[0] == TodoStatus.UNDO:    
            print "%3d|%s"%(i,line)
            printcount += 1
        i += 1
    if i == 0:
        print "None. \nuse '%s help' for help msg"%args[0]
    if printcount == 0:
        print "All Done.\nuse '%s list all'\nor '%s l a' for full list."%(args[0], args[0])
    print "------------------------------------------------------"

# clear todo list
def clearItem(args):
    TODOLIST = []
    saveTodoList()
    print "clear list success"

# print help msg
def printHelpMsg(args):
    print HELPMSG

# define cmd handlers
handlers = {
        'a':addItem,
        'add':addItem,
        'd':doneItem,
        'done':doneItem,
        'del':deleteItem,
        'delete':deleteItem,
        'l':listItem,
        'list':listItem,
        'c':clearItem,
        'clear':clearItem,
        'help':printHelpMsg,
        'h':printHelpMsg,
        '?':printHelpMsg,
        '-?':printHelpMsg
        }

# parse args from input
def parseArgs(args):
    if len(args)==1:
        listItem(args)
    elif args[1] in handlers:
        handlers[args[1]](args)
    else:
        addItem(args)

# main 
def main():
    parseArgs(sys.argv)

if (__name__ == '__main__'):
    main()
