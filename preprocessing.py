import re
from qalsadi import *
from pyarabic import *
from Morphology import *


class Section(object):
    OriginalString = ""
    Paragraphs = []
    #List of instances of the Sentence class:
    def __init__(self, string):
        self.OriginalString = string
        #write code to fill Sections>>Paragraphs>>Sentences>>Words

class Paragraph(object):
    OriginalString = ""   
    Sentences = []
    #List of instances of the Section class:
    def __init__(self, string): 
        self.OriginalString = string

class Word(object):
    OriginalString = ''
    #Original String:  
    String = ''
    #String in manipulation. 
    TokenType = TokenType()
    #Token Type:
    MorphologicalParsingCompleted = False
    #To be set to True if the word is completely finished Morphological Parsing.
    #For example if it is detected as a compound word and parsed completely at the stage of Compound Parsing.
    
    PrematureTags = {}
    #Possible Premature Tags assigned by Premature Tagger. It takes it values from PrematureTagsSet.    
    GreedyMorphemes = GreedyMorphemes([],None,[])   
    
    SurfaceFormMorphemes = []
    #Possible sequences of the analyzed word:
    #This an array of instances of Morphology.Entities.SurfaceFormMorphemes
    #Optionally used to expose the lemmas on Word level
    Lemmas = []
       
    def GetAffixationPosibilities(self):
        '''
        Return a list of all possibilities of word segmentation. 
            (That is all possible forms of the word with clitics)
        Number of possibilities = 1 + (Number of Proclitics + 1) * (Number of Enclitics + 1) 
        For example: أوبعلمائكم
            [[], 'أوبعلمائكم', []]  
            [[], 'أوبعلمائك', ['م']], 
            [[], 'أوبعلمائ', ['ك', 'م']], 
            [['أ'], 'وبعلمائكم', []], 
            [['أ'], 'وبعلمائك', ['م']], 
            [['أ'], 'وبعلمائ', ['ك', 'م']], 
            [['أ', 'و'], 'بعلمائكم', []], 
            [['أ', 'و'], 'بعلمائك', ['م']], 
            [['أ', 'و'], 'بعلمائ', ['ك', 'م']],
            [['أ', 'و', 'ب'], 'علمائكم', []], 
            [['أ', 'و', 'ب'], 'علمائك', ['م']], 
            [['أ', 'و', 'ب'], 'علمائ', ['ك', 'م']]
        '''        
        tempList = []
        tempList.append([[('','c')], self.String, [('','c')]])
        tempP = [('','c')]
        procliticsCutIndex = 0
        for i in range(-1,len(self.GreedyMorphemes.Proclitics)):
            tempS = [('','c')]
            if i > -1:            
                tempP = list(tempP)
                tempP.append([x for x in self.GreedyMorphemes.Proclitics[i]])
                procliticsCutIndex += len(self.GreedyMorphemes.Proclitics[i][0])
                tempList.append([tempP,self.String[procliticsCutIndex:], tempS])
            encliticsCutIndex = 0
            for j in range(len(self.GreedyMorphemes.Enclitics)):
                li = [[x for x in self.GreedyMorphemes.Enclitics[j]]]
                li.extend(tempS)                                
                tempS = li
                encliticsCutIndex += len(self.GreedyMorphemes.Enclitics[j][0])
                tempList.append([tempP,self.String[procliticsCutIndex:len(self.String)-(encliticsCutIndex)], tempS])
        return tempList
    pass
    
    def __init__(self, string):
        self.OriginalString = string
        self.String = string
        self.TokenType = TokenType()
        self.PrematureTags = {}
        self.Tags = []
        self.SurfaceFormMorphemes = []
        self.GreedyMorphemes = GreedyMorphemes([],None,[])
        self.MorphologicalParsingCompleted = False
    pass

    def GetDiacratic(self, procliticString, searchFromRight = False):
        return ArabicStringUtility.GetDiacratic(ArabicStringUtility, self.FirstNormalizationForm, procliticString, 0, searchFromRight)        
    pass
