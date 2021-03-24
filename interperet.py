#!/usr/bin/env python3

#autor: Jakub Komarek
#login: xkomar33
#ipp- interperet kodu v xml
import sys
import os
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

def main():
    INPUT,SOURCE=parametersParse(sys.argv)
    tree=xmlTreeParsing(SOURCE)
    root=tree.getroot()
    MyProgram=programParsing(root)

    print(MyProgram)
    MyProgram.firstrun()
    exit(0)
class Instrucrion(object):
    Type=""
    args={}
    def __init__(self,Type,args):
        self.Type=Type.upper()
        self.args=args
    def __repr__(self):
        return "<Instruction - type: %s,\t args:%s >\n" % (self.Type, self.args)
    def selfcheck(self):
        op=self.Type
        if(op=="RETURN"or op=="CREATEFRAME"or op=="PUSHFRAME"or op=="POPFRAME"or op=="BREAK"):
            pass
        elif(op=="ADD"or op=="SUB"or op=="MUL"or op=="IDIV"or op=="LT"or op=="GT"or op=="EQ"or op=="AND"or op=="OR"or op=="NOT"or op=="STRI2INT"or op=="CONCAT"or op=="GETCHAR"or op=="SETCHAR"):
			pass
        elif(op=="MOVE"):
			pass
        elif(op=="INT2CHAR"or op=="STRLEN"or op=="TYPE"):
			pass
        elif(op=="DEFVAR"or op=="POPS"):
			pass
        elif(op=="JUMPIFEQ"or op=="JUMPIFNEQ"):
            pass
        elif(op=="LABEL"or op=="CALL"or op=="JUMP"):
            pass
        elif(op=="PUSHS"or op=="WRITE"or op=="EXIT"or op=="DPRINT"):
			pass
        elif(op=="READ"):
			pass
        else:
			error(21,"Unknown op Code")

class operant(object):
    Type=""
    value=""
    def __init__(self,Type,value):
        self.Type=Type.upper()
        self.value=value
    def __repr__(self):
        return "<Operant - type: %s, value: %s>" % (self.Type, self.value)
class program(object):   
    instructructions={}
    def __init__(self,instructructions):
        self.instructructions=instructructions
    def __repr__(self):
        return "<Program: - instructions:\n %s" % (self.instructructions)    
    def firstrun(self):
        for i in range(1, len(self.instructructions)+1):
            self.instructructions[str(i)]
        return

def parametersParse(argv): 
    INPUT=None
    SOURCE=None
    if(len(argv)==2 or len(argv)==3):
        for arg in argv[1:] :
            if(arg=="--help"):
                print("Interperet.py-Interpreting code from xml format \nUsege: interpert.py --[options]=[args...] <[input] >[output] 2>[error_log]")
                print("Options:\n--source=\"file\"       =>  select source file \n--input=\"file\"       =>  select input file\n\nif one option missing the data are reading from STDIN")
                exit(0)
            arg=arg.split('=',1)
            if(arg[0]=="--source" and arg[1]!=None):
                SOURCE=arg[1]
            elif(arg[0]=="--input" and arg[1]!=None):
                INPUT=arg[1]
            else:
                error(10,"wrong parameters, try --help")
    else:
        error(10,"wrong parameters, try --help")
    return INPUT,SOURCE
def xmlTreeParsing(SOURCE):
    try:
        if (SOURCE!=None):
            tree=ET.parse(SOURCE)
        else :
            tree=ET.parse(sys.stdin)
    except OSError: 
        error(11,"file not found")
    except:
        error(31,"bad xml structure")
    return tree
def programParsing(root):
    if(root.tag!="program"):
        error(32,"root tag err")
    childs=list(root)
    childsLen=len(childs)
    instructions={}
    for child in childs:
        if(child.tag!="instruction"):
            error(32,"unknown child in xml")
        if(not("order" in child.attrib)or not("opcode" in child.attrib)):
            error(32,"missing instruction atribut")
        if(int(child.attrib["order"])<1 or int(child.attrib["order"])>childsLen or child.attrib["order"] in instructions):
            error(32,"instruction order not valid")
        args={}
        for arg in child:
            if(arg.tag[0:3]!="arg"):
                error(32,"unknown format of parameter")
            if(not("type" in arg.attrib)):
                error(32,"missing parameter atribut")
            if(int(arg.tag[3:])<0 or int(arg.tag[3:])>3 or arg.tag[3:] in arg):
                error(32,"order of operand is not valid")
            args[arg.tag[3:]]=operant(arg.attrib["type"],arg.text)
        instructions[child.attrib["order"]]=Instrucrion(child.attrib["opcode"],args)
    return program(instructions)
def error(code,massege):
    print(massege, file=sys.stderr) 
    exit(code)

main()




