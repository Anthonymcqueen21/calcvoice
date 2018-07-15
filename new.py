import speech_recognition as sr
import os,shutil
import os.path
import playsound
from gtts import gTTS

r = sr.Recognizer()
audio_pos = 0
folder = 'sfx/'

for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

class CallVoice():
    def __init__(self):
        self.n1 = ""
        self.n2 = ""
        self.op = ""
        self.num = 0

    def falar(self, text):
        global audio_pos
        audio_pos = audio_pos + 1
        voz = gTTS(text, lang="pt-BR")
        voz.save(f"sfx/voz{audio_pos}.mp3")
        playsound.playsound(f'sfx/voz{audio_pos}.mp3')

    def audioc(self):
        c = 0
        aud = ''
        try:
            while c < 1:
                with sr.Microphone() as s:
                    r.adjust_for_ambient_noise(s)
                    self.falar("Diga a operação mais outro numero: ")
                    audio2 = r.listen(s)
                    aud = r.recognize_google(audio2, language="pt-BR")
                    return aud
        except Exception as e:
            print(e)

    def calcu(self, s):
        count = 0
        n1 = ""
        n2 = ""
        for c in s:
            if c in "+-/*":
                self.op = c
                count += 1
            else:
                if count == 0:
                    n1 += c
                else:
                    n2 += c
        n1 = float(n1)
        n2 = float(n2)
        self.oper(n1,n2)


    def calcu2(self, s):
        print(s)
        n1 = ""
        for c in s:
            if c in "+-/*":
                self.op = c
            else:
                n1 += c
        n1 = float(n1)
        if self.op == "+":
            self.num += n1
        elif self.op == "-":
            self.num -= n1
        elif self.op == "/":
            self.num /= n1
        elif self.op == "*":
            self.num *= n1

        self.falar("valor: {:.2f}".format(self.num))
        self.continuar()



    def oper(self,n1,n2):

        if self.op == "+":
            self.num += n1 + n2
        elif self.op == "-":
            self.num += n1 - n2
        elif self.op == "/":
            self.num += n1 / n2
        elif self.op == "*":
            self.num += n1 * n2

        self.falar("valor: {:.2f}".format(self.num))
        self.continuar()

    def continuar(self):
        try:
            with sr.Microphone() as s:
                r.adjust_for_ambient_noise(s)
                self.falar("Quer continuar? sim ou não")
                audio = r.listen(s)
                audio = (r.recognize_google(audio, language="pt-BR")).lower()
                print(audio)
        except:
            self.falar("Não entendi, aguarde.")
            self.continuar()
        else:
            if "sim" in audio:
                self.calcu2(self.audioc())
            else:
                self.falar("Obrigado po")



def audio():
    while True:
        try:
            with sr.Microphone() as s:
                r.adjust_for_ambient_noise(s)
                audio = r.listen(s)
                audio = r.recognize_google(audio, language="pt-BR")
                if "divide" in audio or "dividido" in audio:
                    print(audio)
                    audio =  audio.replace('divide','/')
                    audio = audio.replace('dividido por', '/')
                    audio = audio.replace('dividido pra', '/')
                    audio = audio.replace('dividido para', '/')
                    print(audio)
                elif "vezes" in audio or "vez" in audio:
                    print(audio)
                    audio = audio.replace('vez', '*')
                    audio = audio.replace('vezes', '*')
                    print(audio)
                elif "um mais um" in audio or "um mas um" in audio:
                    audio = audio.replace('um mais um','1+1')
                    audio = audio.replace('um mas um', '1+1')
                elif "um menos um" in audio:
                    audio = audio.replace('um menos um','1+1')
        except:
            CallVoice().falar("Não entendi")
        else:
            for c in audio:
                if c in "+-/*":
                    return audio


print('Aguarde...')
CallVoice().falar("Diga um numero a operação mais outro numero")
CallVoice().calcu(audio())
