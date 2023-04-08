import math
import numpy


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


aval=ReadCascadeFile("a_to_e_Example_net_Input_Files/a_Test_Circuit_1.net")

ablock=locateBlocks(aval.get("cascadeFile"),"CIRCUIT")
bblock=locateBlocks(aval.get("cascadeFile"),"TERMS")
cblock=locateBlocks(aval.get("cascadeFile"),"OUTPUT")
theTerms=getTerms(bblock)


Fstart = theTerms.get("Fstart")
Fend = theTerms.get("Fend")
Nfreqs = theTerms.get("Nfreqs")
step = int(theTerms.get("Fend")-theTerms.get("Fstart"))/(theTerms.get("Nfreqs")-1)

ablock.sort()



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


def ABCDmatrix (start):
    abcd = []
    abcdCounter=0

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

    nabcd = []

    for y in range(start+1,len(ablock)+start): 
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

    return (abcd)

cascadeCalc = ABCDmatrix(90)
abcd = cascadeCalc[9]
a = abcd[0][0]
b = abcd[0][1]
c = abcd[1][0]
d = abcd[1][1]

RL = theTerms.get("RL")
RS = theTerms.get("RS")
VT = theTerms.get("VT")





#Pin = 
Zout = ((d*RS)+b)/((c*RS)+a)
#Pout = 
Zin = ((a*RL)+b)/((c*RL)+d)
Vin = (Zin/(Zin+RS))*VT
Av = RL/((a*RL)+b)
Ai = 1/((c*RL)+d)
Vout = Av*Vin
Iout = Vout/RL
Iin = Iout/Ai

print (Vin)
print(Vout)
print(Iin)
print(Iout)





        








#print(impedences)