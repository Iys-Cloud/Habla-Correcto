import sounddevice as sd  #grabar audio desde microfono
import numpy as np  #manejo numerico
import scipy.io.wavfile as wav  #escribir archivos wav
import speech_recognition as sr  #reconocimiento de voz
from googletrans import Translator
import random
import time 

#variables de jugabilidad o lo que sea
playing = ""
dif = 0
mistakes = 3 #vidas lol, me da mammera cambiarlo en toda parte
points = 0

translator = Translator()
recognizer = sr.Recognizer()    #crea el objeto reconocedor

#funciones
def intro():
    print("________________________________________________________________________________\n")
    print("| ¤Bienvenido a Habla Correcto! un juego donde tu puedes practicar tu ingles! ¤ |\n")
    print("________________________________________________________________________________\n")
    print("Tu misión? identificar la traducción de todas estas palabras y decirlas en voz alta!")
    print("Por cada palabra correcta que tengas vas a ganar un punto")
    print("... y por cada palabra incorrecta vas a perder uno.")
    print("y eso no es todo! cada error te va a costar una vida, entonces ten cuidado porque solo tienes tres de esas")
    print("pero no te asustes! tu puedes escojer el nivel de dificultad que deseas jugar:")
    print(" ")
    print("si deseas algo sencillo y tranquilo para principiantes, el primer nivel es para ti")
    print("Si quieres algo que te rete para ir mejorando tu nivel, el segundo nivel es tu opción")
    print("Si quieres una practica avanzada para mejorar tu agilidad, el tercer nivel es perfecto")
def perdiste():
    global points, mistakes
    points -= 1 
    mistakes -= 1
    print(f"tienes {points} puntos y {mistakes} vidas")
    print(" ")
    time.sleep(2)
def ganaste():
    global points, mistakes
    points += 1 
    print(f"Correcto! muy bien, tienes {points} puntos y {mistakes} vidas") 
    print("")
    time.sleep(2)
def escoger_nivel():
    global niv, dif
    niv = int(input("Que nivel deseas jugar?(ingresa 1, 2 o 3): "))
    if niv == 1:
        dif = 15
    elif niv == 2:
        dif = 10
    elif niv == 3:
        dif = 5
    else:
        print("este nivel no existe. ingresa un nivel valido.")

intro() #introduccion castrosa
#inicia juego
playing = True
while playing == True:
    #escogiendo nivel
    escoger_nivel()
    print(f"Listo! vamos a jugar, te vamos a dar una palabra y tu tienes {dif} segundos para responder!")

    while mistakes > 0:
        #las palabras por dificultad y escojiendolas por nivel
        words_by_level = {
            1:["gato", "perro", "cabeza", "creer", "amor", "café","raton", "carro", "corazón", "dia", "noche", "musica", "manzana", "leche", "sol"],
            2: ["banano","celular" ,"lampara", "familiar", "ejercicio", "practica", "libertad", "escuela","esperanza", "alegria", "amigo", "ventana", "amarillo"],
            3: ["humanidad", "reconciliación", "gimnasia", "individuo" ,"tecnologia", "compasión", "enamorado","estudio","universidad", "informacion", "pronunciacion", "imaginacion"]
        }
        word = random.choice(words_by_level[niv])
        print (word)
        print(f"Cual es la traducción (habla): ")
        #palabra a comparar
        trns = translator.translate(word, src="es", dest="en").text.lower() 

        duration = dif  #duracion del audio
        sample_rate = 44100  #calidad cd
        #whatever this tomfoolery
        recording = sd.rec(int(duration * sample_rate),
                           samplerate = sample_rate,
                           channels = 1,
                           dtype = "int16")

        sd.wait()         #esperar a que la grabación termine
        wav.write("audio.wav", sample_rate, recording)
        print ("Recibido! veamos si es correcto...")


        with sr.AudioFile("audio.wav") as source:     #abre el archivo de audio como fuente de entrada
            audio = recognizer.record(source)         #carga todo el audio en memoria

        try:                                          #nloque de majeo de errores
            text = recognizer.recognize_google(audio, language = "en-GB")
            text = text.lower()
            

        except:
            print ("No se te entendio :(")
            perdiste()
            continue

        if text == trns:#caso donde ganan la ronda
            ganaste()
            continue
        else:
            print(f"Incorrecto, debias decir {trns} y dijiste {text}.")
            perdiste()
            continue
    #reiniciar
    print ("aw ;'( has perdido")
    cont = input("Deseas continuar? ").lower()
    if cont == "no":
        playing = False
    else:
        points = 0
        mistakes = 0
        escoger_nivel()

print("Gracias por jugar!!!")