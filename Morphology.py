import re
from qalsadi import *
from pyarabic import *


class SurfaceFormMorphemes(object):
    VoweledForm = ''    
    Proclitics = []     
    Enclitics = []     
    Cliticless = Cliticless()
    __Certainty = 0
    
    def GetCertainty(self):
        return self.__Certainty
    pass
    
    def AddCertainty(self, value):
        if(self.__Certainty >= 0 and value >= 0):
            self.__Certainty = self.__Certainty + value - self.__Certainty * value
        elif(self.__Certainty <= 0 and value <= 0):
            self.__Certainty = self.__Certainty + value + self.__Certainty * value
        else:
            self.__Certainty = (self.__Certainty + value) / (1 - min(abs(self.__Certainty), abs(value)))            
    pass
    
    
    def __init__(self, proclitics, cliticless, enclitics, fillVoweledForm = True):

        self.Proclitics = proclitics
        self.Cliticless = cliticless
        if(type(self.Cliticless) is DerivedCliticless):
            self.Cliticless.UpdateInternalEnclitic()
            if(self.Cliticless.InternalEnclitic != None):
                enclitics = [x for x in enclitics]
                enclitics.insert(0, self.Cliticless.InternalEnclitic)
        self.Enclitics = enclitics        
        
        self.__Certainty = 0
        if(fillVoweledForm == True):
            self.FillVoweledForm()
        else:
            self.VoweledForm = ''
    pass
    
    def FillVoweledForm(self, forceFilling = True):
        if(self.VoweledForm != '' and forceFilling == False):
            return
        
        proclitics = ''.join([p.VoweledForm for p in self.Proclitics])
        procliticsString = ''.join(proclitics)
        
        enclitics = [p.VoweledForm for p in self.Enclitics]
        if(type(self.Cliticless) is DerivedCliticless and len(enclitics) > 0 \
           and self.Cliticless.InternalEnclitic != None):
            enclitics.remove(enclitics[0])        
        encliticsString = ''.join(enclitics)
        
        self.VoweledForm = ''.join([procliticsString, self.Cliticless.VoweledForm, encliticsString])
    
    pass


class GreedyMorphemes(object):         
    Proclitics = [];   
    Enclitics = [];
    CliticlessWords = [];
    CertaintyOrProbability = None;
    def GetStringWithDiacritics(self):
        raise Exception('Not Implemented!');    
    pass
    
    def __init__(self, proclitics, cliticlessWords, enclitics):

        self.Proclitics = proclitics;
        self.CliticlessWords = cliticlessWords;
        self.Enclitics = enclitics;
        pass


class ParticleConstants:
    class State:
        Unprocessed = 0;
        Proclitic = 1;
        Enclitic = 2;
        StandAlone = 4
        all_Cases = 7;


class Particle(Morpheme):
    State = 0;
    def __init__(self, unvoweledForm, voweledForm, state, pos = None):
        self.UnvoweledForm = unvoweledForm;
        self.VoweledForm = voweledForm;
        self.State = state;
        if(pos == None):
            self.POS = ParticlePOS();
            self.POS.MainClass = POSConstants.MainClass.Particle;
        else:
            self.POS = pos;        
    pass




class POSConstants:
    class MainClass:
        #غير معالج = 0, 
        Unprocessed = 0;
        #اسم = 1, 
        Noun = 1;
        #فعل = 2, 
        Verb = 2;
        #حرف = 4, 
        Particle = 4;
        #حميع الحالات = 7
        all_Cases = 7;
        #عدد البتات اللازمة: 3
        Number_of_bits = 3;


class POS(object):
    MainClass = 0;
    '''
    غير معالج = 0, 
    اسم = 1, 
    فعل = 2, 
    حرف = 4, 
    حميع الحالات = 7    
    عدد البتات اللازمة: 3    
    MainClass: Noun, Verb, Particle
    '''    
    BinaryTag = 0;
    '''
    Empty unless AssignBinaryTag is coaled.
    '''
    def __init__(self):  
        self.MainClass = POSConstants.MainClass.Unprocessed;
    
    def AssignBinaryTag(self):
        self.BinaryTag = self.MainClass;
    pass    


    def WriteMainClassArabicText(self, stringStream):
        stringList = [];
        if(self.MainClass == POSConstants.MainClass.Unprocessed):
            stringList.append('؟');
        else:
            if(self.MainClass & POSConstants.MainClass.Noun != 0):
                stringList.append('اسم');
            elif(self.MainClass & POSConstants.MainClass.Verb != 0):
                stringList.append('فعل');
            elif(self.MainClass & POSConstants.MainClass.Particle != 0):
                stringList.append('حرف');
        stringStream.write(' أو '.join(stringList));
    pass

class DiacriticsConstants:
    Fatha = 'َ'
    DoubleFatha = 'ً'
    Damma = 'ُ'
    DoubleDamma = 'ٌ'
    Kasra = 'ِ'
    DoubleKasra = 'ٍ'
    Sukoon = 'ْ'
    Shadda = 'ّ'
    
    AllDiacritics = []

DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.Fatha)
DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.DoubleFatha)
DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.Damma)
DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.DoubleDamma)
DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.Kasra)
DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.DoubleKasra)
DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.Sukoon)
DiacriticsConstants.AllDiacritics.append(DiacriticsConstants.Shadda)


class HamzaConstants:
    OnAlif = 'أ'
    UnderAlif = 'إ'
    OnWaw = 'ؤ'
    OnYa = 'ئ'
    OnLine = 'ء'
    
    AllHamzas = []

        
HamzaConstants.AllHamzas.append(HamzaConstants.OnAlif)
HamzaConstants.AllHamzas.append(HamzaConstants.UnderAlif)
HamzaConstants.AllHamzas.append(HamzaConstants.OnWaw)
HamzaConstants.AllHamzas.append(HamzaConstants.OnYa)
HamzaConstants.AllHamzas.append(HamzaConstants.OnLine)

class EllaConstants:
    Alif = 'ا'
    AlifMaksora = 'ى'
    Waw = 'و'
    Ya = 'ي'
    AllAhrofElla = []


EllaConstants.AllAhrofElla.append(EllaConstants.Alif)
EllaConstants.AllAhrofElla.append(EllaConstants.AlifMaksora)
EllaConstants.AllAhrofElla.append(EllaConstants.Waw)
EllaConstants.AllAhrofElla.append(EllaConstants.Ya)


class ArabicLetters:    
    AllLetters = []
    


ArabicLetters.AllLetters = []
ArabicLetters.AllLetters.append("ء")
ArabicLetters.AllLetters.append("أ")
ArabicLetters.AllLetters.append("إ")
ArabicLetters.AllLetters.append("آ") 
ArabicLetters.AllLetters.append("ؤ")
ArabicLetters.AllLetters.append("ئ")
ArabicLetters.AllLetters.append("ا")
ArabicLetters.AllLetters.append("ى")
ArabicLetters.AllLetters.append("ب")
ArabicLetters.AllLetters.append("ت")
ArabicLetters.AllLetters.append("ة")
ArabicLetters.AllLetters.append("ث")
ArabicLetters.AllLetters.append("ج")
ArabicLetters.AllLetters.append("ح")
ArabicLetters.AllLetters.append("خ")
ArabicLetters.AllLetters.append("د")
ArabicLetters.AllLetters.append("ذ")
ArabicLetters.AllLetters.append("ر")
ArabicLetters.AllLetters.append("ز")
ArabicLetters.AllLetters.append("س")
ArabicLetters.AllLetters.append("ش")
ArabicLetters.AllLetters.append("ص")
ArabicLetters.AllLetters.append("ض")
ArabicLetters.AllLetters.append("ط")
ArabicLetters.AllLetters.append("ظ")
ArabicLetters.AllLetters.append("ع")
ArabicLetters.AllLetters.append("غ")
ArabicLetters.AllLetters.append("ف")
ArabicLetters.AllLetters.append("ق")
ArabicLetters.AllLetters.append("ك")
ArabicLetters.AllLetters.append("ل")
ArabicLetters.AllLetters.append("م")
ArabicLetters.AllLetters.append("ن")
ArabicLetters.AllLetters.append("ه")
ArabicLetters.AllLetters.append("و")
ArabicLetters.AllLetters.append("ي")

