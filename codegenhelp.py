#!/usr/bin/python

__doc__ = '''Helper functions used by the code generator'''


from regalloc import *
from datalayout import *


REG_FP = 11
REG_SCRATCH = 12
REG_SP = 13
REG_LR = 14
REG_PC = 15

REGS_CALLEESAVE = [4, 5, 6, 7, 8, 9, 10]
REGS_CALLERSAVE = [0, 1, 2, 3]


def getRegisterString(regid):
  if regid == REG_LR:
    return 'lr'
  if regid == REG_SP:
    return 'sp'
  return 'r'+`regid`
  
  
def saveRegs(reglist):
  if len(reglist) == 0:
    return ''
  res = '\tpush {'
  for i in range(0, len(reglist)):
    if i > 0:
      res += ', '
    res += getRegisterString(reglist[i])
  res += '}\n'
  return res
  
  
def restoreRegs(reglist):
  if len(reglist) == 0:
    return ''
  res = '\tpop {'
  for i in range(0, len(reglist)):
    if i > 0:
      res += ', '
    res += getRegisterString(reglist[i])
  res += '}\n'
  return res


def comment(cont):
  return '@ ' + cont + '\n'
  
  
def codegenAppend(vec, code):
  if type(code) is list:
    return [vec[0] + code[0], vec[1] + code[1]]
  return [vec[0] + code, vec[1]]
  

# class RegisterAllocation:


def enterFunctionBody(self, block):
  self.curfun = block
  self.spillvarloc = dict()
  self.spillvarloctop = -block.stackroom
  

def genSpillLoadIfNecessary(self, var):
  self.dematerializeSpilledVarIfNecessary(var)
  if not self.materializeSpilledVarIfNecessary(var):
    # not a spilled variable
    return ''
  offs = self.spillvarloctop - self.vartospillframeoffset[var] - 4
  rd = self.getRegisterForVariable(var)
  res = '\tldr ' + rd + ', [' + getRegisterString(REG_FP) + ', #' + `offs` + ']'
  res += '\t' + comment('<<- fill')
  return res
  
  
def getRegisterForVariable(self, var):
  self.materializeSpilledVarIfNecessary(var)
  res = getRegisterString(self.vartoreg[var])
  return res


def genSpillStoreIfNecessary(self, var):
  if not self.materializeSpilledVarIfNecessary(var):
    # not a spilled variable
    return ''
  offs = self.spillvarloctop - self.vartospillframeoffset[var] - 4
  rd = self.getRegisterForVariable(var)
  res = '\tstr ' + rd + ', [' + getRegisterString(REG_FP) + ', #' + `offs` + ']'
  res += '\t' + comment('<<- spill')
  self.dematerializeSpilledVarIfNecessary(var)
  return res


RegisterAllocation.enterFunctionBody = enterFunctionBody
RegisterAllocation.genSpillLoadIfNecessary = genSpillLoadIfNecessary
RegisterAllocation.getRegisterForVariable = getRegisterForVariable
RegisterAllocation.genSpillStoreIfNecessary = genSpillStoreIfNecessary

