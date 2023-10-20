from statements.sequence import Sequence

def getAllIndexesOfSubstringInString(targetString: str, subStringToFind:str):
    return [i for i in range(len(targetString)) if targetString.startswith(subStringToFind, i)]

def isCharAtLevel(codeText: str, charIndex: int, level: int) -> bool:
    currentLevel = 0
    for element in range(0, charIndex):
        if codeText[element] == '(':
            currentLevel += 1
        elif codeText[element] == ')':
            currentLevel -= 1

    return currentLevel == level

def isCharAtLevelZero(codeText: str, charIndex: int) -> bool:
    return isCharAtLevel(codeText, charIndex, 0)


def isSkip(codeText: str) -> [int]:
    if codeText.find("skip") == -1:
        return [-1]
    
    if(len(codeText) > len("skip")):
        return [-1]
    
    return [0]

def isSequence(codeText: str) -> [int]:
    if codeText.find(";") == -1:
        return [-1]

    if codeText[0] == ";":
        raise Exception("Program is not correct syntatically!")
    
    allSemicolonIndexes = getAllIndexesOfSubstringInString(codeText, ";")
    for semicolonIndex in allSemicolonIndexes:
        if isCharAtLevelZero(codeText, semicolonIndex):
            return [semicolonIndex]
        
    return [-1]


def isAssignment(codeText: str) -> [int]:
    if codeText.find(":=") == -1:
        return [-1]

    if codeText[0] == ":=":
        raise Exception("Program is not correct syntatically!")
    
    allSeparatorIndexes = getAllIndexesOfSubstringInString(codeText, ":=")
    for separatorIndex in allSeparatorIndexes:
        if isCharAtLevelZero(codeText, separatorIndex):
            return [separatorIndex]
        
    return [-1]

def isSpawn(codeText: str) -> [int]:
    if codeText.find("spawn") == -1:
        return [-1]

    if codeText[0] != '(' or codeText[len(codeText) -  1] != ')':
        return [-1]
    

    allSpawnIndexes = getAllIndexesOfSubstringInString(codeText, "spawn")
    for spawnIndex in allSpawnIndexes:
        if isCharAtLevel(codeText, spawnIndex, 1):
            return [spawnIndex]
        
    return [-1]

def isIfBlock(codeText: str) -> [int]:
    if codeText.find("if") == -1 or codeText.find("then") == -1 or codeText.find("else") == -1:
        return [-1]

    if codeText[0] != '(' or codeText[len(codeText) -  1] != ')':
        return [-1]
    
    allSeparatorsIndexes = [-1, -1, -1]

    allIfIndexes = getAllIndexesOfSubstringInString(codeText, "if")
    for ifIndex in allIfIndexes:
        if isCharAtLevel(codeText, ifIndex, 1):
            allSeparatorsIndexes.insert(0, ifIndex)
            break
    
    allThenIndexes = getAllIndexesOfSubstringInString(codeText, "then")
    for thenIndex in allThenIndexes:
        if isCharAtLevel(codeText, thenIndex, 1):
            allSeparatorsIndexes.insert(1, thenIndex)
            break
    
    allElseIndexes = getAllIndexesOfSubstringInString(codeText, "else")
    for elseIndex in allElseIndexes:
        if isCharAtLevel(codeText, elseIndex, 1):
            allSeparatorsIndexes.insert(2, elseIndex)
            break
        
    return allSeparatorsIndexes

def isRef(codeText: str) -> [int]:
    if codeText.find("ref") == -1 or codeText.find("=") == -1 or codeText.find("in") == -1:
        return [-1]

    if codeText[0] != '(' or codeText[len(codeText) -  1] != ')':
        return [-1]
    
    allSeparatorsIndexes = [-1, -1, -1]

    allRefIndexes = getAllIndexesOfSubstringInString(codeText, "ref")
    for refIndex in allRefIndexes:
        if isCharAtLevel(codeText, refIndex, 1):
            allSeparatorsIndexes.insert(0, refIndex)
            break
    
    allEqualIndexes = getAllIndexesOfSubstringInString(codeText, "=")
    for equalIndex in allEqualIndexes:
        if isCharAtLevel(codeText, equalIndex, 1):
            allSeparatorsIndexes.insert(1, equalIndex)
            break
    
    allInIndexes = getAllIndexesOfSubstringInString(codeText, "in")
    for inIndex in allInIndexes:
        if isCharAtLevel(codeText, inIndex, 1):
            allSeparatorsIndexes.insert(2, inIndex)
            break
        
    return allSeparatorsIndexes

def isWhileStatement(codeText: str) -> [int]:
    if codeText.find("while") == -1 or codeText.find("do") == -1:
        return [-1]

    if codeText[0] != '(' or codeText[len(codeText) -  1] != ')':
        return [-1]
    
    allSeparatorsIndexes = [-1, -1]

    allWhileIndexes = getAllIndexesOfSubstringInString(codeText, "while")
    for whileIndex in allWhileIndexes:
        if isCharAtLevel(codeText, whileIndex, 1):
            allSeparatorsIndexes.insert(0, whileIndex)
            break
    
    allDoIndexes = getAllIndexesOfSubstringInString(codeText, "do")
    for doIndex in allDoIndexes:
        if isCharAtLevel(codeText, doIndex, 1):
            allSeparatorsIndexes.insert(1, doIndex)
            break
        
    return allSeparatorsIndexes

def isLock(codeText: str) -> [int]:
    if codeText.find("lock") == -1 or codeText.find("in") == -1:
        return [-1]

    if codeText[0] != '(' or codeText[len(codeText) -  1] != ')':
        return [-1]
    
    allSeparatorsIndexes = [-1, -1]

    allLockIndexes = getAllIndexesOfSubstringInString(codeText, "lock")
    for lockIndex in allLockIndexes:
        if isCharAtLevel(codeText, lockIndex, 1):
            allSeparatorsIndexes.insert(0, lockIndex)
            break
    
    allInIndexes = getAllIndexesOfSubstringInString(codeText, "in")
    for inIndex in allInIndexes:
        if isCharAtLevel(codeText, inIndex, 1):
            allSeparatorsIndexes.insert(1, inIndex)
            break
        
    return allSeparatorsIndexes


def isOperation(codeText: str) -> []:
    if codeText[0] != '(' or codeText[len(codeText) -  1] != ')':
        return [-1]

    possibleOperations = ["==", "<=", ">=", "**", "!=", "+", "-", "/", "*", "<", ">"]
    operator = ""
    for operation in possibleOperations:    
        if codeText.find(operation) != -1:
            operator = operation
            break 

    if operator == "":
        return [-1]
    
    if codeText[0] == operator:
        raise Exception("Program is not correct syntatically!")
    
    allSemicolonIndexes = getAllIndexesOfSubstringInString(codeText[1:], operator)
    for semicolonIndex in allSemicolonIndexes:
        if isCharAtLevelZero(codeText[1:], semicolonIndex):
            return [semicolonIndex + 1, operator]
        
    return [-1]

def isRead(codeText: str) -> [int]:
    if codeText[0] == '!':
        if(len(codeText) <= 1):
            raise Exception("Program is not correct syntatically!")
        return [0]
        
    return [-1]

def isIntegerConstant(codeText: str):
    try :
        value = int(codeText)
    except :
        return ["error"]
    
    return [value] 

def isPointer(codeText: str):
    if codeText.find(" ") != -1:
        return [-1]
    
    try :
        int(codeText)
    except :
        return [codeText]
    
    return [-1] 
    

