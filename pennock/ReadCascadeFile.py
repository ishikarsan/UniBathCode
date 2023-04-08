def ReadCascadeFile(inputFile):
    
    
    circuitCheck = 0
    termsCheck = 0
    outputCheck = 0
    cascadeFile = []
    
    with open(inputFile,'r') as f:
        for line in f.readlines():
            if "<CIRCUIT>" in line:
                circuitCheck = 1
            if "</CIRCUIT>" in line:
                circuitCheck = circuitCheck + 1
            if "<TERMS>" in line:
                termsCheck = 1
            if "</TERMS>" in line:
                termsCheck = termsCheck + 1
            if "<OUTPUT>" in line:
                outputCheck = 1
            if "</OUTPUT>" in line:
                outputCheck = outputCheck + 1
            if "#" in line:
                continue
            else:
                cascadeFile.append(line)
    if circuitCheck %2 != 0:
        returnDict = {cascadeFile}



ReadCascadeFile("file.txt")
