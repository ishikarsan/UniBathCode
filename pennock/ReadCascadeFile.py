def ReadCascadeFile(inputFile):
    
    
    circuitCheck = 0
    termsCheck = 0
    outputCheck = 0
    cascadeFile = []
    
    with open("inputFile",'r') as f:
        [cascadeFile.append(line) for line in f.readlines()]


