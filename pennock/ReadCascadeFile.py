import math
import numpy


class Circuit:
    bValue=0
    cValue=0

    def __init__(self,node1,node2,resistorValue,capacitanceValue,inductanceValue,conductorValue,frequency):
        self.node1=node1
        self.node2=node2
        if resistorValue==None:
            resistorValue=-1
        self.resistorValue=resistorValue
        if capacitanceValue==None:
            capacitanceValue=-1
        self.capacitanceValue=capacitanceValue
        if inductanceValue==None:
            inductanceValue=-1
        self.inductanceValue=inductanceValue
        if conductorValue==None:
            conductorValue=-1
        self.conductorValue=conductorValue

        self.bValue=0
        self.cValue=0
        self.frequency=frequency

        if self.node2==0:
            self.cValue=self.calculate_Value()
        else:
            self.bValue=self.calculate_Value()

    def calculate_Value(self):
        
        if self.resistorValue!=-1:
            calcValue=self.resistorValue
        elif self.conductorValue!=-1:
            calcValue=1 / self.conductorValue
        elif self.inductanceValue!=-1:
            calcValue=1j*2*math.pi*self.frequency*self.inductanceValue
        elif self.capacitanceValue!=-1:
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
    
    with open(inputFile,'r') as f:
        for line in f.readlines():
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

aval=ReadCascadeFile("a_to_e_Example_net_Input_Files/a_Test_Circuit_1.net")

ablock=locateBlocks(aval.get("cascadeFile"),"CIRCUIT")
bblock=locateBlocks(aval.get("cascadeFile"),"TERMS")
cblock=locateBlocks(aval.get("cascadeFile"),"OUTPUT")