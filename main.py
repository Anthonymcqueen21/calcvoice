'''Module for testing purposes.'''

__author__ = 'Alan França, Paulo Henrique'

import os
from functools import partial
from glob import iglob
from typing import List

import playsound
import speech_recognition as sr
from gtts import gTTS


def speak(text, audio_pos=0):
    voice = gTTS(text, lang="pt-BR")
    voice.save(f"sfx/voz{audio_pos}.mp3")
    playsound.playsound(f'sfx/voz{audio_pos}.mp3')


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
    return operation(*(ask_operand(order, operation_name=operation_name)
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
    audio_pos = 0

    COMMANDS = {
            "somar": partial(
                command_arith,
                lambda x, y: x + y,
                "somar"),
            "dividir": partial(
                command_arith,
                lambda x, y: x // y,
                "dividir"),
            "multiplicar": partial(
                command_arith,
                lambda x, y: x * y,
                "multiplicar"),
            "subtrair": partial(
                command_arith,
                lambda x, y: x - y,
                "subtrair"),
    }

    for path in iglob('sfx/*'):
        if os.path.isfile(path):
            os.unlink(path)

    r = sr.Recognizer()
    with sr.Microphone() as source:
        command = ask_command(r, source, commands=list(COMMANDS))
        speak(f"Comando {command} selecionado")
        result = COMMANDS[command](r, source)

    print(f"O resultado é {result}")
