import math
import numpy
from   pathlib import Path
import csv
import sys
import time


class Circuit:
    bValue=0
    cValue=0

    def __init__(self,node1,node2,resistorValue,capacitanceValue,inductanceValue,conductorValue,frequency):
        self.node1=node1
        self.node2=node2
        
        self.resistorValue=resistorValue
        
        self.capacitanceValue=capacitanceValue
        
        self.inductanceValue=inductanceValue
        
        self.conductorValue=conductorValue

        self.bValue=0
        self.cValue=0
        self.frequency=frequency

        if self.node2==0:
            self.cValue=self.calculate_Value()
        else:
            self.bValue=self.calculate_Value()

    def calculate_Value(self):
        
        if self.resistorValue!=None:
            calcValue=self.resistorValue
        elif self.conductorValue!=None:
            calcValue=1 / self.conductorValue
        elif self.inductanceValue!=None:
            calcValue=1j*2*math.pi*self.frequency*self.inductanceValue
        elif self.capacitanceValue!=None:
            calcValue=(-1j)/(2*math.pi*self.frequency*self.capacitanceValue)
        else:
            calcValue=0
        return calcValue

def ReadCascadeFile(inputFile):
    
    circuitCheck = 0
    termsCheck = 0
    outputCheck = 0
    cascadeFile = []
    returnStatus="OK"
    errorCodes=[]

    returnDict={}
    returnDict.update({"cascadeFile":cascadeFile,"returnState":returnStatus,"errorCodes":errorCodes})
    
    for line in inputFile.readlines():
        if "#" in line:
            continue
        else:
            if "<CIRCUIT>" in line:
                circuitCheck = 1
            if "</CIRCUIT>" in line:
                circuitCheck += 1
            if "<TERMS>" in line:
                termsCheck = 1
            if "</TERMS>" in line:
                termsCheck += 1
            if "<OUTPUT>" in line:
                outputCheck = 1
            if "</OUTPUT>" in line:
                outputCheck += 1
            line=line.rstrip("\n")
            cascadeFile.append(line)

    if circuitCheck !=2:
        errorCodes.append("F001")
        returnStatus="NOTOK"
    if termsCheck !=2:
        errorCodes.append("F002")
        returnStatus="NOTOK"
    if outputCheck !=2:
        errorCodes.append("F003")
        returnStatus="NOTOK"

    return returnDict

def locateBlocks(cascadeList,blockName):

    block=[]
    startLine=-1
    endLine=-1
    i=0
    for line in cascadeList:
        if (blockName in line ):
            if startLine==-1:
                startLine=i
                continue
            if endLine==-1:
                endLine=i
                continue
            continue
        i+=1

    block=cascadeList[startLine+1:endLine+1]

    return block

def getValueFromString(name,type,string):
    nameFind = string.find(name)
    if nameFind >-1:
        lname = len(name)
        idx = nameFind+lname
        new_str=string[idx:]
        eq = new_str.find('=')
        if (eq >-1):
            idx=eq+1
            valstring=new_str[idx:]
            substring=valstring.split(' ')
            teststring=substring[0].strip() 
            if type == 'float':
                try:
                    rtn = float(teststring)
                    error = None 
                except ValueError:
                    rtn = None
                    error = "V001"
            elif type == 'int':
                try:
                    rtn = int(teststring)
                    error = None
                except ValueError:
                    rtn = None
                    error = "V002"
        else:
            error = "V003"
            rtn = None
    else:
        error = "V004"
        rtn = None
    return(rtn,error) 
            
def getTerms(termBlock):
    CascadeValue={"VT":None,"RS":None,"RL":None,"IN":None,"GS":None,"Fstart":None,"Fend":None,"Nfreqs":None}
    CascadeParameters=[
        {
            "name":"VT",
            "type":"FLOAT"
        },
        {
            "name":"RS",
            "type":"FLOAT"
        },
        {
            "name":"RL",
            "type":"FLOAT"
        },
        {
            "name":"IN",
            "type":"FLOAT"
        },
        {
            "name":"GS",
            "type":"FLOAT"
        },
        {
            "name":"Fstart",
            "type":"FLOAT"
        },
        {
            "name":"Fend",
            "type":"FLOAT"
        },
        {
            "name":"Nfreqs",
            "type":"FLOAT"
        }

        ]
            
    for termLine in termBlock:
        for termParam in CascadeParameters:
            aval,err=getValueFromString(termParam.get("name"),termParam.get("type").lower(),termLine)
            if err==None:
                CascadeValue.update({termParam.get("name"):aval})
            

    return CascadeValue

def ABCDmatrix (circuitNodeCount,impedences):
    abcd = []
    abcdCounter=0
    start=0

    if impedences[start].bValue == 0 and impedences[start].cValue == 0:
            print("ERROR: component value missing between node")
    elif impedences[start].bValue != 0 and impedences[start].cValue == 0:
        A = 1
        B = impedences[start].bValue
        C = 0
        D = 1
    elif impedences[start].bValue == 0 and impedences[start].cValue != 0:
        A = 1
        B = 0
        C = 1/(impedences[start].cValue)
        D = 1
    else:
        print("ERROR: too many component values at nodes")
    
    abcd.append(numpy.array([[A,B],[C,D]]))
    abcdCounter+=1

    for y in range(start+1,circuitNodeCount+start): 
        if impedences[y].bValue == 0 and impedences[y].cValue == 0:
            print("ERROR: component value missing between node")
        elif impedences[y].bValue != 0 and impedences[y].cValue == 0:
            A = 1
            B = impedences[y].bValue
            C = 0
            D = 1
        elif impedences[y].bValue == 0 and impedences[y].cValue != 0:
            A = 1
            B = 0
            C = 1/(impedences[y].cValue)
            D = 1
        else:
            print("ERROR: too many component values at nodes")

    
        abcd.append( numpy.matmul(abcd[abcdCounter-1],numpy.array([[A,B],[C,D]])))
        abcdCounter+=1

    return abcd[-1] #return last element

def getLogicalCascadeBlocks(cascadeInputFile):

    aval=ReadCascadeFile(inputFile=cascadeInputFile.open(mode='r'))

    ablock=locateBlocks(aval.get("cascadeFile"),"CIRCUIT")
    bblock=locateBlocks(aval.get("cascadeFile"),"TERMS")
    cblock=locateBlocks(aval.get("cascadeFile"),"OUTPUT")
    theTerms=getTerms(bblock)

    ablock.sort()

    return ablock,cblock,theTerms

def getImpendenceByFrequency(ablock,theTerms):

    Fstart = theTerms.get("Fstart")
    Fend = theTerms.get("Fend")
    Nfreqs = theTerms.get("Nfreqs")
    step = int(theTerms.get("Fend")-theTerms.get("Fstart"))/(theTerms.get("Nfreqs")-1)

    frequencies = numpy.arange(Fstart,Fend+step,step).tolist()
    impedences = []
    for fq in frequencies:
        for node in ablock:
            res = None
            con = None
            cap = None
            ind = None
            if 'R=' in node:
                res,error = getValueFromString('R','float',node)
            elif 'G=' in node:
                con,error = getValueFromString('G','float',node)
            elif 'L=' in node:
                ind,error=getValueFromString('L','float',node)
            elif 'C='in node:
                cap,error=getValueFromString('C','float',node)
            if error == None:
                n1,nerror = getValueFromString('n1','int',node)
                n2,nerror = getValueFromString('n2','int',node)
                if nerror == None:
                    x = Circuit(n1,n2,res,cap,ind,con,fq)
                    impedences.append(x)
    
    return impedences

def getCascadeCalc(freq,theTerms,abcd):
    allCalcs={
        "Frequency":0,
        "Vin":0,
        "Vout":0,
        "Iin":0,
        "Iout":0,
        "Pin":0,
        "Pout":0,
        "Zin":0,
        "Zout":0,
        "Av":0,
        "Ai":0
    }

    allCalcs.update({"Frequency":freq})
    a = abcd[0][0]
    b = abcd[0][1]
    c = abcd[1][0]
    d = abcd[1][1]
    
    RL = theTerms.get("RL")
    RS = theTerms.get("RS")
    VT = theTerms.get("VT")


    
    Zout = ((d*RS)+b)/((c*RS)+a)
    Zin = ((a*RL)+b)/((c*RL)+d)
    Vin = (Zin/(Zin+RS))*VT
    Av = RL/((a*RL)+b)
    Ai = 1/((c*RL)+d)
    Vout = Av*Vin
    Iout = Vout/RL
    Iin = Iout/Ai
    Pin = Vin*Iout
    Pout = Vout*Iin

    #add imaginary values with real 
    #make all values the same length

    allCalcs.update({
        "Vin":Vin.real,
        "Vout":Vout.real,
        "Iin":Iin.real,
        "Iout":Iout.real,
        "Pin":Pin.real,
        "Pout":Pout.real,
        "Zin":Zin.real,
        "Zout":Zout.real,
        "Av":Av.real,
        "Ai":Ai.real
    })    

    return allCalcs

def getUnitBasedValue(unit ,value): 
    if unit==None:
        return value
    
    if unit.startswith("k"):
        value=value*1000
    if unit.startswith("p"):
        value = value*10^-12
    if unit.startswith("n"):
        value = value*10^-9
    if unit.startswith("u"):
        value = value/1000000
    if unit.startswith("m"):
        value = value/1000
    if unit.startswith("M"):
        value = value^10^6
    if unit.startswith("G"):
        value = value*10^9

    return value

def writeCSV(cascadeOutput):

    hdr=list(cascadeOutput[0].keys())

    with open('test.csv', 'a') as output_file:
        dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=hdr, delimiter=',')
        dict_writer.writeheader()
        dict_writer.writerows(cascadeOutput)


def processCascadeFile(cascadeFile):
    ablock,cblock,theTerms=getLogicalCascadeBlocks(cascadeFile)
    impendenceList=getImpendenceByFrequency(ablock,theTerms)
    circuitNodeCount=len(ablock)
    
    cascadeCalculated=[]
    outputArray=[]
    
    for x in range(0,len(impendenceList)-1,circuitNodeCount):
        singleFrequency=impendenceList[x:x+circuitNodeCount]
        
        cascadeMatrixCalc=ABCDmatrix(circuitNodeCount,impedences=singleFrequency)
        freq=singleFrequency[0].frequency
        cascadeCalculated.append(getCascadeCalc(freq,theTerms,cascadeMatrixCalc))

        outputDict={}
        outputDict.update({"Frequency Hz":freq})
        for cblockItem in cblock:

            outputItem=cblockItem.split(' ')
            calcOutputItem=outputItem[0]

            if len(outputItem)==1:
                calcUnit=None
            else:
                calcUnit=outputItem[1]

            cascadeCalcItem = cascadeCalculated[-1]
            if calcOutputItem in cascadeCalcItem:
                outputDict.update({cblockItem: getUnitBasedValue(calcUnit,cascadeCalcItem.get(calcOutputItem))})
        outputArray.append(outputDict)

        #print(calcOutputItem)
        #print(calcUnit)
    writeCSV(outputArray)

if __name__ == '__main__':

    """
    Check input arguments
    check file availability for reading
    report errors
    output file validity
    https://builtin.com/software-engineering-perspectives/python-pathlib
    """    



    if (len(sys.argv)<2):
    #   print("\n\tError, program needs two arguments to run\n" )
    #   sys.exit(1)
        input_file_arg="a_to_e_Example_net_Input_Files/a_Test_Circuit_1.net"
    else:
        input_file_arg=sys.argv[1]
# now open file

    input_file=Path(input_file_arg)
    if input_file.exists() and input_file.is_file(): 
       processCascadeFile(input_file)
    else:
        print("Unable to find file")
