# start of lexical analyzer by michael pierce titled: lexer.py
import os
import sys
import string
from typing import final

Letter  = [ "a" , "b" , "c" , "d" , "e" , "f" , "g" , 
            "h" , "i" , "j" , "k", "l" , "m" , "n" , 
            "o" , "p" , "q" , "u" , "r" , "s" , "t" , 
            "u", "v" , "w" , "x" , "y" , "z" , "A" , 
            "B" , "C" , "D" , "E" , "F" , "G" , "H" , 
            "I" , "J" , "K" , "L" , "M" , "N" , "O" , 
            "P" , "Q" , "U" , "R" , "S" , "T" , "U" , 
            "V" , "W" , "X" , "Y" , "Z" ]
Digit  =  [ "0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" ]
eot = "end"
eol = "end-of-line"
Keywords = [ "program", "end", "while", "do", "od", "if", "then", "else", "fi", "bool", "int", "and", "or", "not", "true", "false", "print" ]
Symbols = [ "_", "-", "+", "<","=<","=","!=",">=",">", "*", "/", ";", ":=", "(", ")", "[", "]", "{", "}", ":"]
Specials = [ " ", "\n", "\t" ]
ERROR = ('error')

RelationalOperator  =  ["<" , "=<" , "=" , "!=" , ">=" , ">"]
AdditiveOperator  =  ["+" , "-" , "or"]
MultiplicativeOperator  =  ["*" , "/" , "and"]
UnaryOperator  =  ["-" , "not"]
BooleanLiteral  =  ["false"  ,  "true"]

#IntegerLiteral  =  Digit { Digit } .
#Identifier  =  Letter { Letter | Digit | "_" }.

#starts program by testing file input
def start():
    if(len(sys.argv) < 2):      #if no file given, end program
        print("Error: Lack of arguments.\nTerminating Program ... \nGoodbye\n")
        return False

    if(os.path.isfile(sys.argv[1]) == False):   #if file isn't able to opened, end program
        print("Invalid File ... \nTerminating Program ... \nGoodbye\n")
        return False
    else:           #if given file is valid, open, read lines into list, then close file
        file = open(sys.argv[1], 'r')
        str_list = file.readlines()
        file.close()

        return str_list

#checks whether the character read is in the language's alphabet, ex: $ will return False
def in_alphabet(char):
    if(char not in Letter and char not in Digit and 
        char not in Keywords and char not in Symbols
            and char not in Specials):
        return False

    else: return True

#checks whether an updated position is outside of valid list range, and returns the next valid position
def check_pos(str_list, position):
    if(position[1] >= len(str_list[position[0]])):
        position = [position[0]+1, 0]
    return position

# reads the next lexeme in the input file.
def next(str_list, position):
    lexeme = ""
    char = ""
    next_char = ""    

    #start of current lexeme
    start = position
    i = 0

    while(i != -1):
        char = str_list[position[0]][position[1]]

        if (i == 0): #if it is the first character of the lexeme, check for symbols
            if(char == ";" and i == 0):
                position = [position[0]+1, 0]
                return [char, start, position]

            elif(char == "/" and str_list[position[0]][position[1]+1] == "/" and i == 0):
                position = [position[0]+1, 0]
                return [None, None, position]

            elif((char == ":" or char == "!" or char == ">") and str_list[position[0]][position[1]+1] == "=" and i == 0):
                next_char = str_list[position[0]][position[1]+1]
                position = [position[0], position[1]+2]
                position = check_pos(str_list, position)
                return [char + next_char, start, position]

            elif(char == "=" and str_list[position[0]][position[1]+1] == "<" and i == 0):
                next_char = str_list[position[0]][position[1]+1]
                position = [position[0], position[1]+2]
                position = check_pos(str_list, position)
                return [char + next_char, start, position]

            elif(char in Symbols and i == 0):
                position = [position[0], position[1]+1]
                position = check_pos(str_list, position)
                return [char, start, position]

            elif(in_alphabet(char) == False):
                msg = "error Occurred: Invalid Character:"
                return [msg, start, position, char]
            i = 1

        if(char.isspace() or in_alphabet(char) == False): #if the read char is space, pass the current lexeme, although this if statement may be redundant
            if(in_alphabet(char) == False):
                return [lexeme, start, position]

            position = [position[0], position[1]+1]
            position = check_pos(str_list, position)
            return [lexeme, start, position]

        else: #if read char is not symbol, add it to the lexeme
            i = i + 1
            #adds character to current lexeme
            lexeme = lexeme + char

            #update position for next char to be read
            position = [position[0], position[1]+1]
            position = check_pos(str_list, position)
            next_char = str_list[position[0]][position[1]] #lookahead char
            
            #check whether lexeme should be returned based off lookahead char
            if((lexeme in Keywords and next_char.isspace()) or (next_char in Symbols and next_char != "_")): 
                return [lexeme, start, position]
            elif(lexeme[0] in Digit and next_char not in Digit): #if the current lexeme is int, return when next char is not a digit
                return [lexeme, start, position]
    return 0

# returns the kind of the lexeme that was just read.
def getKind(lexeme):
    if (lexeme != None):
        if(len(lexeme) >= 1):
            if (lexeme in Keywords or lexeme in Symbols):
                kind = lexeme
            elif (lexeme[0] in Letter):
                    kind = "ID"
            elif (lexeme[0] in Digit):
                    kind = "NUM"
            else:
                kind = None
        else:
            kind = "WS/None"
    else:
        kind = None
    return kind

# returns the value of the lexeme (if it is an “ID” or a “NUM”).
def getValue(lexeme, kind):
    if (kind == "ID" or kind == "NUM"):
        return lexeme
    else:
        return ""

def Expected(s, l, c):
    print("\n\nexpected " + s + " at line->" + str(l) + ", char->" + str(c) + "\n\n")
    return 

#matches a lexeme with a string
def match(lex, check):
    if(lex == check):
        return True
    else:
        return False

def Literal(str_list, c):
    if((str_list[c][0] in BooleanLiteral) or (match(str_list[c][0], "NUM"))):
        return [True, c+1]
    else:
        return [False]

def Factor(str_list, c):
    if(str_list[c][0] in UnaryOperator):
        c += 1
    res = Literal(str_list, c)
    flag = res[0]
    if(flag == True ):
        c = res[1]
        return [True, c]

    elif(str_list[c][0] == "ID"):
        return [True, c+1]

    elif(str_list[c][0] == "("):
        res = Expression(str_list, c+1)
        flag = res[0]
        if(flag == True):
            c = res[1]
            if(str_list[c][0] == ")"):
                return [True, c+1]
            else:
                Expected(")", str_list[c][1], str_list[c][2])
                return [False]
    else:
        Expected("Literal | ID | '(' Expression ')'", str_list[c][1], str_list[c][2])
        return [False]

def Term(str_list, c):
    res = Factor(str_list, c)
    flag = res[0]
    if(flag == True):
        c = res[1]
        if(str_list[c][0] in MultiplicativeOperator):
            res = Factor(str_list, c+1)
            flag = res[0]
            if(flag == True):
                c = res[1]
            else: 
                return [False]
        return [True, c]
    return [False]    

def SimpleExpression(str_list, c):
    res = Term(str_list, c)
    flag = res[0]
    if(flag == True):
        c = res[1]
        if(str_list[c][0] in AdditiveOperator):
            res = Term(str_list, c+1)
            flag = res[0]
            if(flag == True):
                c = res[1]
            else:
                return [False]
        return [True, c]
    return [False]  
    
def Expression(str_list, c):
    res = SimpleExpression(str_list, c)
    flag = res[0]
    if(flag == True):
        c = res[1]
        if(str_list[c][0] in RelationalOperator):
            res = SimpleExpression(str_list, c+1)
            flag = res[0]
            if(flag == False):
                return [False]
            c = res[1]
        return [True, c]
    return [False]

def PrintStatement(str_list, c):
    res = Expression(str_list, c)
    flag = res[0]
    if(flag == True):
        c = res[1]
        return [True, c]
    return [False]

def IterativeStatement(str_list, c):
    res = Expression(str_list, c)
    flag = res[0]
    if(flag == True):
        c = res[1]
        if(match(str_list[c][0], "do")):
            res = body(str_list, c+1)
            flag = res[0]
            if(flag == True):
                c = res[1]

                if(match(str_list[c][0], "od")):
                    return [True, c]
                else:
                    Expected("od", str_list[c][1], str_list[c][2])
        else:
            Expected("do", str_list[c][1], str_list[c][2])
    return [False]

def ConditionalStatement(str_list, c):
    res = Expression(str_list, c)
    flag = res[0]
    if(flag == True):
        c = res[1]

        if(match(str_list[c][0], "then")):
            res = body(str_list, c+1)
            flag = res[0]
            if(flag == True):
                c = res[1]
                if(match(str_list[c][0], "else")):
                    res = body(str_list, c+1)
                    flag = res[0]
                    if(flag == True):
                        c = res[1]
                    else:
                        return [False]   

                if(match(str_list[c][0], "fi")):
                    return [True, c+1]
                else:
                    Expected("fi",str_list[c][1], str_list[c][2])
        else:
            Expected("then", str_list[c][1], str_list[c][2])    
    return [False]

def AssignmentStatement(str_list, c):
    if(match(str_list[c][0], ":=")):
        res = Expression(str_list, c+1)
        flag = res[0]
        if(flag == True):
            c = res[1]
            return [True, c]
    else:
        Expected(":=", str_list[c][1], str_list[c][2])
    return [False, c]

def statement(str_list, c):
    if(match(str_list[c][0], "ID")):
        res = AssignmentStatement(str_list, c+1)
        flag = res[0]
        if(flag == True):
            c = res[1]
            return [True, c]

    elif(match(str_list[c][0], "if")):
        res = ConditionalStatement(str_list, c+1)
        flag = res[0]
        if(flag == True):
            c = res[1]
            return [True, c]

    elif(match(str_list[c][0], "while")):

        res = IterativeStatement(str_list, c+1)
        flag = res[0]
        if(flag == True):
            c = res[1]
            return [True, c]

    elif(match(str_list[c][0], "print")):
        res = PrintStatement(str_list, c+1)
        flag = res[0]
        if(flag == True):
            c = res[1]
            return [True, c]

    return [False]

def statements(str_list, c):
    res = statement(str_list, c)
    flag = res[0]   
    if(flag == False):
        return False
    else:
        c = res[1]
        while(str_list[c][0] == ";"):
            res = statement(str_list, c+1)
            flag = res[0]
            if(flag == False):
                return False
            c = res[1]
        return [True, c]

def declaration(str_list, c):
    if(not(match(str_list[c][0], "bool") or match(str_list[c][0], "int"))):
        Expected("bool | int", str_list[c][1], str_list[c][2])
        return [False]
    else:
        c += 1
        if(match(str_list[c][0], "ID") == False):
            Expected("ID", str_list[c][1], str_list[c][2])
            return [False]
        else:
            c += 1
            if(match(str_list[c][0], ";") == False):
                Expected(";", str_list[c][1], str_list[c][2])
                return [False]
            c += 1
            return [True, c]
    
def declarations(str_list, c):
    res = declaration(str_list, c)
    flag = res[0]
    c = res[1]
    if(flag == False):
        return [False]
    else:
        while(match(str_list[c][0], "bool") or match(str_list[c][0], "int")):
            res = declaration(str_list, c)
            flag = res[0]
            if(flag == False):
                return [False]
            c = res[1]
        return [True, c]
    
def body(str_list, c):
    if(match(str_list[c][0], "bool") or match(str_list[c][0], "int")):
        res = declarations(str_list, c)
        flag = res[0]
        if(flag == False):
            return False
        c = res[1]    
        
    
    return statements(str_list, c)

def program(str_list):
    if(match(str_list[0][0], "program") == False):
        Expected("program", str_list[0][1], str_list[0][2])
        return False
    else:
        if(match(str_list[1][0], "ID") == False):
            Expected("ID", str_list[1][1], str_list[1][2])
            return False
        else:
            if(match(str_list[2][0], ":") == False):
                Expected(":", str_list[2][1], str_list[2][2])
                return False
            else:
                if(body(str_list, 3) != False):
                    if(match(str_list[len(str_list)-1][0], "end") == False):
                        Expected("end", str_list[len(str_list)-1][1], str_list[len(str_list)-1][2])
                        return False
                    else:
                        return True
                else:
                    return False


def main(): 
    
    #get list of lines from given file
    str_list = start()
    if(str_list == False):
        return 0
    else:
        final_str_list = []
        lexeme = " "
        position = [0 , 0]
        next_position = [0, 0]
        current_lexeme_struct = [str_list, lexeme, position, next_position]

    #get list of lexemes for proj 2 implementation
    while( getKind(lexeme) != eot):
        stopFlag = False
        current_lexeme_struct = next(str_list, next_position)
        lexeme = current_lexeme_struct[0]
        position = current_lexeme_struct[1]
        next_position = current_lexeme_struct[2]

        while(lexeme == None):
            current_lexeme_struct = next(str_list, next_position)
            lexeme = current_lexeme_struct[0]
            position = current_lexeme_struct[1]
            next_position = current_lexeme_struct[2]

        while(ERROR in lexeme):
            lexeme = current_lexeme_struct[0]
            position = current_lexeme_struct[1]
            next_position = current_lexeme_struct[2]
            char = current_lexeme_struct[3]
            print(str(position[0]+1) + ":" + str(position[1]+1) + " >>>>> " +
                    lexeme + "\t" + char + "\n\n")
            return 0

        kind = getKind(lexeme)
        value = getValue(lexeme, kind)

        #if the lexeme is valid, add to final list
        if(kind != "WS/None"):
            final_str_list.append([kind, position[0]+1, position[1]+1])
            
    #start proj 2 code implementation
    if(program(final_str_list) == False):
        print("false\n\n")
    else:
        print("\n\ntrue\n\n")
    return 0

main()