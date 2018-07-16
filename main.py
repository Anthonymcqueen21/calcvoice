__author__ = 'Alan França, Paulo Henrique,João Paulo Taylor Ienczak Zanette'

import os
from functools import partial
from glob import iglob
from typing import List
import shutil
import os.path
import playsound
import speech_recognition as sr
from gtts import gTTS

folder = 'sfx/'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

audio_pos = 0

def speak(text):
    global audio_pos
    voice_file = f"sfx/voz{audio_pos}.mp3"
    voice = gTTS(text, lang="pt-BR")
    voice.save(voice_file)
    playsound.playsound(voice_file)
    audio_pos = audio_pos +1


def ask(r: sr.Recognizer, source: sr.AudioSource, message: str=None):
    if message:
        speak(message)

    audio = r.listen(source)
    return r.recognize_google(audio, language="pt-BR")


def ask_operand(r: sr.Recognizer,
                source: sr.AudioSource,
                order: str,
                operation_name: str):
    while True:
        try:
            return ask(
                r, source,
                message=f"Fale o {order} valor para {operation_name}")
        except sr.UnknownValueError as e:
            speak("Comando de voz não reconhecido.")


def command_arith(operation,
                  operation_name: str,
                  r: sr.Recognizer,
                  source: sr.AudioSource):
    return operation(*(ask_operand(r,source,order, operation_name=operation_name)
                       for order in ["primeiro", "segundo"]))


def ask_command(r: sr.Recognizer,
                source: sr.AudioSource,
                commands: List[str]):
    while True:
        while True:
            try:
                command_name = ask(r, source, message="Esperando Comando")
            except sr.UnknownValueError as e:
                speak("Comando de voz não reconhecido.")
            else:
                break

        for command in commands:
            if command in command_name:
                return command
        speak("Não consegui entender um comando conhecido.")


if __name__ == "__main__":

    COMMANDS = {
            "somar": partial(
                command_arith,
                lambda x, y: int((int(x) + int(y))),
                "somar"),
            "dividir": partial(
                command_arith,
                lambda x, y: int((int(x) // int(y))),
                "dividir"),
            "multiplicar": partial(
                command_arith,
                lambda x, y: int((int(x) * int(y))),
                "multiplicar"),
            "subtrair": partial(
                command_arith,
                lambda x, y: int((int(x) - int(y))),
                "subtrair"),
    }

   # for path in iglob('sfx/*'):
       # if os.path.isfile(path):
        #    os.unlink(path)

    r = sr.Recognizer()
    with sr.Microphone() as source:
        command = ask_command(r, source, commands=list(COMMANDS))
        speak(f"Comando {command} selecionado")
        result = COMMANDS[command](r, source)

    speak(f"O resultado é {result}")
