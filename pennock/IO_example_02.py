# -*- coding: utf-8 -*-
"""
Created on Fri Dec 06 09:12 2019 - ish
@author: eessrp
"""
import sys
import os

def find_int(string_to_search,name,noisy):
    """
    Function that looks for an occurence of name in string_to_search. 
    If found the equals sign following name is sought and the string to the
    right of the equals sign is interpretted as an integer. Looks for a string
    like 'Npt=3" in string_to_search, looking for 'Npt' and to return 3.
    Success or failure is indicated by a boolean that is returned, and this 
    should be acted on in the calling program.
    :param string_to_search - the text string to be searched
    :type string
    :param name - text string of the item to be sought in string_to_search
    :type string
    :param noisy - boolean, if true produces more output to the screen
    :type boolean
    :return rtn - integer value found, or particular negative values when not found
    :rtype integer
    :return ok - boolean, true if name and integer found otherwise false
    :rtype bool
    """
    pp=string_to_search.find(name)    # looks for name in string_to_search
    if noisy:
        print("Found <%s> in <%s> at %d"%(name,string_to_search,pp))
    if (pp>-1):     # name has been found, pp is the index where name is
        lname=len(name)
        idx=pp+lname   # points at character after name
        new_str=string_to_search[idx:]  # copy from idx to end
        qqe=new_str.find('=')  # search for equals sign
        if (qqe>-1):   # equals found
            idx=qqe+1  # point at character after equals sign
            valstring=new_str[idx:]
            substring=valstring.split(';') #variables need to be separated by semicolon
            teststring=substring[0].strip() # strip gets rid of spare spaces
            try:
                rtn=int(teststring)  #convert string to integer
                if noisy:
                    print("Found %s = %d from <%s>"%(name,rtn,teststring))
                ok=True
            except ValueError:
                n3, n3_found=find_float(line,"Node1",True) # look for Node1 in line with extra output
                n4, n4_found=find_float(line,"Node2",False)
                rtn=-123
                ok = True
                if noisy:
                    print('ERROR:\nTried to find int <%s> in string <%s>, valstring is <%s>, teststring is <%s>'%(name,string_to_search,valstring,teststring))
                rtn=-987654321
                ok=False
        else:  # equals not found
            rtn=-113355
            ok=False
            if noisy:
                print('ERROR:\nTried to find int <%s> in string <%s>. Found <%s> but no equals symbol'%(name,new_str,qqe))
    else:  # name not found in string_to_search
        rtn=-123456789
        if noisy:
            print("Failed to find <%s> in <%s>"%(name, str))
        ok = False
    return(rtn, ok)
#

def find_float(string_to_search,name,noisy):
 
    pp=string_to_search.find(name)    # looks for name in string_to_search
    if noisy:
        print("Found <%s> in <%s> at %d"%(name,string_to_search,pp))
    if (pp>-1):     # name has been found, pp is the index where name is
        lname=len(name)
        idx=pp+lname   # points at character after name
        new_str=string_to_search[idx:]  # copy from idx to end
        qqe=new_str.find('=')  # search for equals sign
        if (qqe>-1):   # equals found
            idx=qqe+1  # point at character after equals sign
            valstring=new_str[idx:]
            substring=valstring.split(';') #variables need to be separated by semicolon
            teststring=substring[0].strip() # strip gets rid of spare spaces
            try:
                rtn=float(teststring)  #convert string to integer
                if noisy:
                    print("Found %s = %d from <%s>"%(name,rtn,teststring))
                ok=True
            except ValueError:
                n3, n3_found=find_string(line,"Node1",True) # look for Node1 in line with extra output
                n4, n4_found=find_string(line,"Node2",False
                if noisy:
                    print('ERROR:\nTried to find float <%s> in string <%s>, valstring is <%s>, teststring is <%s>'%(name,string_to_search,valstring,teststring))
                rtn=-987654321
                ok=False
        else:  # equals not found
            rtn=-113355
            ok=False
            if noisy:
                print('ERROR:\nTried to find float <%s> in string <%s>. Found <%s> but no equals symbol'%(name,new_str,qqe))
    else:  # name not found in string_to_search
        rtn=-123456789
        if noisy:
            print("Failed to find <%s> in <%s>"%(name, str))
        ok = False
    return(rtn, ok)
#

def find_string(string_to_search,name,noisy):
    

    pp=string_to_search.find(name)    # looks for name in string_to_search
    if noisy:
        print("Found <%s> in <%s> at %d"%(name,string_to_search,pp))
    if (pp>-1):     # name has been found, pp is the index where name is
        lname=len(name)
        idx=pp+lname   # points at character after name
        new_str=string_to_search[idx:]  # copy from idx to end
        qqe=new_str.find('=')  # search for equals sign
        if (qqe>-1):   # equals found
            idx=qqe+1  # point at character after equals sign
            valstring=new_str[idx:]
            substring=valstring.split(';') #variables need to be separated by semicolon
            teststring=substring[0].strip() # strip gets rid of spare spaces
            try:
                rtn=str(teststring)  #convert string to integer
                if noisy:
                    print("Found %s = %s from <%s>"%(name,rtn,teststring))
                ok=True
            except ValueError:
                if noisy:
                    print('ERROR:\nTried to find str <%s> in string <%s>, valstring is <%s>, teststring is <%s>'%(name,string_to_search,valstring,teststring))
                rtn=-987654321
                ok=False
        else:  # equals not found
            rtn=-113355
            ok=False
            if noisy:
                print('ERROR:\nTried to find str <%s> in string <%s>. Found <%s> but no equals symbol'%(name,new_str,qqe))
    else:  # name not found in string_to_search
        rtn=-123456789
        if noisy:
            print("Failed to find <%s> in <%s>"%(name, str))
        ok = False
    return(rtn, ok)
#
# main program
    
print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: " , str(sys.argv))
if (len(sys.argv)<2):
    print("\n\tError, program needs two arguments to run\n" )
    sys.exit(1)
# now open file
input_filename=sys.argv[1]
try:
    fin=open( input_filename,'rt')
except FileNotFoundError:
    print('File <%s> not found'%(input_filename))
    current_location=os.getcwd() 
    # gets the directory where the program is executing from the operating 
    # system as this is where the file is expected to be
    print("executing program in directory: "+current_location) 
    sys.exit(1)  # exits the program, returning a value of 1 to the operating system 
#now interpret file
file_lines=fin.readlines()
for index,line in enumerate(file_lines):
    print("Line[%d] =<%s>"%(index,line))
    n1, n1_found=find_int(line,"Node1",True) # look for Node1 in line with extra output
    n2, n2_found=find_int(line,"Node2",False) # look for Node2 in line with less output
    n3, n3_found=find_float(line,"Node1",True) # look for Node1 in line with extra output
    n4, n4_found=find_float(line,"Node2",False) # look for Node2 in line with less output
    happy=n1_found and n2_found and n3_found and n4_found
    if (not happy):
        print("Failed to find input in line <%s>\nn1=%d, n1_found=%r, n2=%d, n2_found=%r"%(line,n1,n1_found,n2,n2_found))
    else:
        print("Found nodes: n1=%d, n2=%d, n3=%d,n4=%d "%(n1,n2,n3,n4))

#test=input("Enter a value: ")
fin.close()



