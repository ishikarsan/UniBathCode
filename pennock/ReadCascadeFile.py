import math
import matplotlib.pyplot as plt
import numpy
from   pathlib import Path
import csv
import sys
import time
import argparse
import cmath


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

    return returnDict,errorCodes

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

            if name in "R,L,C,G":
                valstring=valstring.replace(' ','')
                valstring=valstring.replace('p','e-12')
                valstring=valstring.replace('n','e-9')
                valstring=valstring.replace('u','e-6')
                valstring=valstring.replace('m','e-3')
                valstring=valstring.replace('k','e3')
                valstring=valstring.replace('M','e6')
                valstring=valstring.replace('G','e9')
                valstring=valstring.replace('T','e12')

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
    CascadeValue={"VT":None,"RS":None,"RL":None,"IN":None,"GS":None,"Fstart":None,"Fend":None,"Nfreqs":None,"LFstart":None,"LFend":None}
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
            "name":"LFstart",
            "type":"FLOAT"
        },
        {
            "name":"LFend",
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

def getOutputBlock(cBlock):
    
    #cBlock=["Vin mV","Vin dBmV","Vout V","Vout dBV","Iin uA","Iin dBuA","Iout A","Iout mA","Iout dBmA","Pin W","Pin dBW","Zout Ohms","Zout mOhms","Pout W","Pout mW","Pout dBmW","Zin Ohms","Zin kOhms","Av  dB","Av dB","Ai dB"]
    pos=0
    scale=""
    units=""
    dbCalc=False

    outputList=[]

    for a in cBlock:
        outputTerms=a.split(" ")

        if len(outputTerms)==1:
            outputTerms.append("")

        if outputTerms[1].startswith("dB"):
            dbCalc=True
            units=outputTerms[1].removeprefix("dB")
        else:
            dbCalc=False
            units=outputTerms[1]

        if units[:1] in "p,n,u,m,k,M,G,T":
            scale=units[:1]
        else:
            scale=""

        if dbCalc:
            label1=f"|{outputTerms[0]}|"
            label2=f"/_{outputTerms[0]}"
        else:
            label1=f"Re({outputTerms[0]})"
            label2=f"Im({outputTerms[0]})"

        for item in getOutputDetails(pos,scale,units,dbCalc,outputTerms[0],label1,None):
        #for item in getOutputDetails(pos,scale,units,dbCalc,outputTerms[0],label1,label2):
            outputList.append(item)

    i=1
    for outputItem in outputList:
        outputItem.update({"position":i})
        i+=1


    return outputList

def getOutputDetails(pos,scale,units,dbCalc,name,label1,label2):
    outputDict={}
    extended=[]
    outputDict.update({"position":pos,"name":name,"units":units,"scale":scale,"dbCalc":dbCalc,"label":label1})
    extended.append(outputDict.copy())

    if label2!=None:
        outputDict.update({"position":pos+1,"name":name,"units":units,"scale":scale,"dbCalc":dbCalc,"label":label2})
        extended.append(outputDict.copy())

    return extended


def getLogicalCascadeBlocks(cascadeInputFile):

    aval,error=ReadCascadeFile(inputFile=cascadeInputFile.open(mode='r'))

    if len(error) == 0:

        ablock=locateBlocks(aval.get("cascadeFile"),"CIRCUIT")
        bblock=locateBlocks(aval.get("cascadeFile"),"TERMS")
        cblock=locateBlocks(aval.get("cascadeFile"),"OUTPUT")
    
        theOutput=getOutputBlock(cblock)
    
        theTerms=getTerms(bblock)
    
        ablock.sort()

        return ablock,theOutput,theTerms

    else:
        return None,None,None

def getImpendenceByLogFrequency(ablock,theTerms):
    Fstart = theTerms.get("LFstart")
    Fend = theTerms.get("LFend")
    Nfreqs = theTerms.get("Nfreqs")
    y=Fend/Fstart
    x=Nfreqs-1
    b=y**(1/x)
    a=Fend/(b**Nfreqs)
    frequencies=[]

    for i in range (1,int(Nfreqs)):
        frequencies.append(a*(b**i)) 
      

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
                else:
                    reportError(nerror,node)
            else:
                reportError(error,node)

    return impedences
"""
Create a function to get the impedence by frequency with Log base 10 
"""
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
                else:
                    reportError(nerror,node)
            else:
                reportError(error,node)
    
    return impedences

def reportError(error,node):
    print("ERROR: "+error+" in node "+node)
    sys.exit()

def getCascadeCalc(freq,theTerms,abcd):
    allCalcs={
        "Frequency":0,
        "Vin":[0,0],
        "Vout":[0,0],
        "Iin":[0,0],
        "Iout":[0,0],
        "Pin":[0,0],
        "Pout":[0,0],
        "Zin":[0,0],
        "Zout":[0,0],
        "Av":[0,0],
        "Ai":[0,0],
        "Ap":[0,0],
        "dBVin":[0,0],
        "dBVout":[0,0],
        "dBIin":[0,0],
        "dBIout":[0,0],
        "dBPin":[0,0],
        "dBPout":[0,0],
        "dBZin":[0,0],
        "dBZout":[0,0],
        "dBAv":[0,0],
        "dBAi":[0,0],
        "dBAp":[0,0]
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
    Ap=Av*Ai

    Vout = Av*Vin
    Iout = Vout/RL
    Iin = Iout/Ai
    Pin = Vin*Iin
    Pout = Vout*Iout

    dBVin=20*math.log(abs(Vin),10)
    dBVout=20*math.log(abs(Vout),10)   
    dBIin=20*math.log(abs(Iin),10) 
    dBIout=20*math.log(abs(Iout),10) 
    dBPin=10*math.log(abs(Pin),10) 
    dBPout=10*math.log(abs(Pout),10)
    dBZin=20*math.log(abs(Zin),10) 
    dBZout=20*math.log(abs(Zout),10) 
    dBAv=20*math.log(abs(Av),10) 
    dBAi=20*math.log(abs(Ai),10) 
    dBAp=10*math.log(abs(Ap),10) 

    r,dBVinPhase=cmath.polar(Vin)
    r,dBVoutPhase=cmath.polar(Vout) 
    r,dBIinPhase=cmath.polar(Iin) 
    r,dBIoutPhase=cmath.polar(Iout)
    r,dBPinPhase=cmath.polar(Pin)
    r,dBPoutPhase=cmath.polar(Pout)
    r,dBZinPhase=cmath.polar(Zin)
    r,dBZoutPhase=cmath.polar(Zout)
    r,dBAvPhase=cmath.polar(Av)
    r,dBAiPhase=cmath.polar(Ai)
    r,dBApPhase=cmath.polar(Ap)


    #add imaginary values with real 
    #make all values the same length

    allCalcs.update({
            "Vin":[Vin.real,Vin.imag],
            "Vout":[Vout.real,Vout.imag],
            "Iin":[Iin.real,Iin.imag],
            "Iout":[Iout.real,Iout.imag],
            "Pin":[Pin.real,Pin.imag],
            "Pout":[Pout.real,Pout.imag],
            "Zin":[Zin.real,Zin.imag],
            "Zout":[Zout.real,Zout.imag],
            "Av":[Av.real,Av.imag],
            "Ai":[Ai.real,Ai.imag], 
            "Ap":[Ap.real,Ap.imag],
            "dBVin":[dBVin,dBVinPhase],
            "dBVout":[dBVout,dBVoutPhase],
            "dBIin":[dBIin,dBIinPhase],
            "dBIout":[dBIout,dBIoutPhase],
            "dBPin":[dBPin,dBPinPhase],
            "dBPout":[dBPout,dBPoutPhase],
            "dBZin":[dBZin,dBZinPhase],
            "dBZout":[dBZout,dBZoutPhase],
            "dBAv":[dBAv,dBAvPhase],
            "dBAi":[dBAi,dBAiPhase],
            "dBAp":[dBAp,dBApPhase]
        })    

    return allCalcs

def getUnitBasedValue(unit ,value): 
    if unit==None or unit=="":
        return value
    if unit.startswith("k"):
        return value/1000
    if unit.startswith("p"):
        return value/10^-12
    if unit.startswith("n"):
        return value/10^-9
    if unit.startswith("u"):
        return value*1000000
    if unit.startswith("m"):
        return value*1000
    if unit.startswith("M"):
        return value/10^6
    if unit.startswith("G"):
        return value/10^9

def writeCSV(cascadeOutput):

    hdr=list(cascadeOutput[0].keys())
    hdr_line_1=[]
    hdr_line_2=[]
    for item in hdr:
        hdr_parts=item.strip().split(' ')
        if cascadeOutput[0][item]!=None:
            hdr_line_1.append(hdr_parts[0])
            if len(hdr_parts)>1:
                hdr_line_2.append(hdr_parts[1])
            else:
                hdr_line_2.append("")
        
    with open(output_name, 'a') as output_to_file:
        for hl1 in hdr_line_1:
            h1=f"{hl1}, ".rjust(12," ")
            output_to_file.write(h1)

        output_to_file.write("\n")

        for hl2 in hdr_line_2:
            h2=f"{hl2}, ".rjust(12," ")
            output_to_file.write(h2)

        output_to_file.write("\n")

        for vals in cascadeOutput:
            for valItem in hdr:
                if vals[valItem]!=None:
                    v=f"{vals[valItem]:1.3E}, ".rjust(12," ")
                    output_to_file.write(v)

            output_to_file.write("\n")

def writeGraphData(graphData):
    
    for graph in graphsToCreate:
        xList=[d["x"] for d in graphData if str(d['graph']) in graph["Column"]]
        yList=[d["y"] for d in graphData if str(d['graph']) in graph["Column"]]
        ylabel=[[d["y-label"],d['graphName']] for d in graphData if str(d['graph']) in graph["Column"]][0]

        x=numpy.array(xList)
        y=numpy.array(yList)
        plt.ioff()
    
# Create a new figure, plot into it, then close it so it never gets displayed
        plt.plot(x,y)
        plt.title(ylabel[1])
        plt.xlabel("Hz")
        plt.ylabel(ylabel[0])

        plt.savefig(graph["File"])
        plt.close()




def processCascadeFile(cascadeFile):
    ablock,cblock,theTerms=getLogicalCascadeBlocks(cascadeFile)
    if ablock==None:
        reportError("Error reading file",None)
        return

    graphData=[]
    if theTerms.get("LFstart")==None:
        impendenceList=getImpendenceByFrequency(ablock,theTerms)
    else:
        impendenceList=getImpendenceByLogFrequency(ablock,theTerms)

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

        colPos=0
        for cblockItem in cblock:

            calcOutputItem=cblockItem["name"]
            calcUnit=cblockItem["units"]
            calcScale=cblockItem["scale"]

            cascadeCalcItem = cascadeCalculated[-1]
            if cblockItem["dbCalc"]:
                calcOutputItem=f"dB{calcOutputItem}"
                label2=f"/_{calcOutputItem} Rads"
                calcUnit=f"dB{calcUnit}"
            else:
                label2=f"Im({calcOutputItem}) {calcUnit}"

            label1=f"{cblockItem['label']} {calcUnit}"

            calcValue=cascadeCalcItem.get(calcOutputItem)            
            
            outputDict.update({label1:getUnitBasedValue(calcScale,calcValue[0]),label2:getUnitBasedValue(calcScale,calcValue[1])})
            if str(colPos) in graphParams:
                graphData.append({
                    "graph":colPos,
                    "graphName":label1,
                    "y-label":calcUnit,
                    "x":freq,
                    "y":getUnitBasedValue(calcScale,calcValue[0])})

            colPos+=1

        outputArray.append(outputDict)

    writeCSV(outputArray)
    writeGraphData(graphData)

if __name__ == '__main__':

    """
    Check input arguments
    check file availability for reading
    report errors
    output file validity
    https://builtin.com/software-engineering-perspectives/python-pathlib
    """    
    parser = argparse.ArgumentParser(
                    prog=sys.argv[0],
                    description='Analyses cascade circuits, where series and shunt impedances of any value can be connected in any order between a source and a load. The output file is named the same as the input file but with extension .csv',
                    epilog='Boohoo')
    
    parser.add_argument('input_file',nargs='?',default=None)
    parser.add_argument('output_file',nargs='?',default=None)
    parser.add_argument('-i',required=False,default=None,metavar='a_Test_Circuit_1',help='Input file name should be without the .net extension')      
    parser.add_argument('-p',required=False,default=None,metavar='[1,2,3]',help='Optional list of output columns e.g. [2,4,6]')

    args = parser.parse_args()
    graphParams=None

    noPositionalParameters=False

    if args.input_file==None or args.output_file==None:
        noPositionalParameters=True
    
    if noPositionalParameters:
        if args.i==None:
            print("No input file name")
            sys.exit(1)
        if args.p==None:
            print("No graph parameters")
            sys.exit(1)
        
        fname=args.i.strip()
        graphParams=args.p.strip().replace('[','').replace(']','').split(',')

    else:
        fname=args.input_file
        output_name=args.output_file 
    
    if not Path(fname).suffix==".net":
        output_name=f"{fname}.csv"
        fname=f"{fname}.net"
    else:
        output_name=Path(fname).with_suffix(".csv")
        output_name=str(output_name)
        

    base_file_name=Path(fname).stem 

    input_file_arg=fname
# now open file

    input_file=Path(input_file_arg)
    output_file=Path(output_name)

    if output_file.exists() and output_file.is_file():
        print("Output file exists")

    graphsToCreate=[]
    for graphCol in graphParams:
        graphFile=Path(f"{base_file_name}_{graphCol}.png")
        graphsToCreate.append({"Column":graphCol,"File":graphFile})
        if graphFile.exists() and graphFile.is_file():
            print(f"Graph file {str(graphFile)} exists")

    if input_file.exists() and input_file.is_file(): 
       processCascadeFile(input_file)
    else:
        print("Unable to find file")
