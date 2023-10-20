import sys
from programToEvaluate import ProgramToEvaluate


def main():
    programFileName = sys.argv[1]
    importedVariablesFileName = sys.argv[2]
    with open(importedVariablesFileName) as f:
        importedVariablesText = f.read()
    ProgramToEvaluate.loadImportedVariables(importedVariablesText)
    
    with open(programFileName) as f:
        programText = f.read()
    #The program works without taking out multiple spaces and \n
    #programText = ' '.join(programText.split()) #multiple whitespaces into one
    #programText = programText.replace('\n', ' ')
    
    ProgramToEvaluate.startAst(programText)
    #print("AST Tree:")
    #print(ProgramToEvaluate.toString())
    ProgramToEvaluate.evaluate()

if __name__ == '__main__':
    main()