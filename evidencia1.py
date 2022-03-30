# Fecha: 19-03-22
# Materia: Román Martínez Martínez
# Evidencia #1: Implementación básica de un DSL para ejecutar música en Python
# Creador: Renet de Jesús Pérez Gómez
# Matricula: A01640555

###
# En este script esta implementada la solucion a la situación problema 1.
# La ejecución del programa se realiza de la siguiente manera:
#   1- Lectura del archivo con los datos.
#   2- Ejecución de analizador léxico (y tokenización). 
#   3- Ejecuación de analizador sintactico.
#   4- Ejecución de la musica.
# Este programa funcióna por "etapas", si la etapas anterior esta bien, avanza al siguente etapa, si no lanza error
# y se detiene el programa.  
###


import re
import numpy as np;
import sounddevice as sd


#Variables globales
noteArr = [] #Para guardar la nota
octaveArr = [] #Para guardar la octava
durationArr = []  #Para guardar la duración
c = ""  #Concatenacion de la cadena a analizar
actualInputUnicode = 0 #Para identificar "enter"
flagPosition = 0 #Esta variable nos ayudara a no "repetir posiciones" que ya pasamos en las funciones ciclos
lineError = 0 #Esta variable nos ayudara a saber en que linea del documento estamos (esto es para el manejo de errores)
lexicoValido = True #En caso de haber error esta variable impedira que se reproduzca la canción 
tiempo = 1000 #Variable que nos ayudara a saber a que tiempo se toca la canción
tokenArr = [] #Nos servira para guardar los tokens generados
tokenActual = 0 #Declarando variable para el análisis de los tokens
sintaxisValida = False #Variable para determinar si una sintaxis es valida o no

# ANÁLISIS DE LÉXICO
# Expresiones en Regex
# Lexemas que se usaran en el proyecto
particion = re.compile("\|")


inicioDescanso = re.compile("R[w|h|q|e|s|t|f]([\.]+|[t|3|5|7|9])?")
descanso = re.compile("R[w|h|q|e|s|t|f]([\.]+|[t|3|5|7|9]|)?")

palabraReservadaBAR = re.compile("#BAR")
comentarioMut = re.compile("#[\w\W]*")
name = re.compile("[a-z][\w|\d]*\ *")

iniciomNote = re.compile("[A|B|C|D|E|F|G](b*?|#*?)(-[1,2]|[0|1|2|3|4|5|6|7|8])[w|h|q|e|s|t|f]([\.]+|[t|3|5|7|9|33|tt]|\ )?")
mNote = re.compile("[A|B|C|D|E|F|G](b*?|#*?)(-[1,2]|[0|1|2|3|4|5|6|7|8])[w|h|q|e|s|t|f]([\.]+|[5|7|9]|t{1,2}|3{1,2})?")


#Expresión regular para el caso de los archivos ".txt"
verificarArchivoTxt = re.compile("[\w\W]+\.(txt)")

# funciones musica estaba en 4, 2 se escucha bien
def frec(note: int, octave: int) -> int:
    expo = (octave - 3) * 12 + (note - 10)
    return int(440 * ((2 ** (1/12)) ** expo))

#Para la variable tiempo:
#Canciones rapidas 250
#Canciones lentas 1000 o 2000

#Función que hace el calculo para reproducir la musica
def getWave(note: int, octave: int, duration: int):
    frameRate = 44100

    frecuency = frec(note, octave)
    t = np.linspace(0, duration/tiempo, int(frameRate * duration/tiempo))
    data = np.sin(2 * np.pi * frecuency * t)
    sd.play(data, frameRate)
    sd.wait()

#Funciones para componer una nota (o silencio)
def letter(note):
    if note == "A":
        return 10 
    if note == "B": 
        return 12 
    if note == "C":
        return 1 
    if note == "D":
        return 3 
    if note == "E":
        return 5 
    if note == "F":
        return 6 
    if note == "G":
        return 8 
    return 0

#Función para obtener la octava de una nota
def getOctave(octave):
    if octave == "0":
        return 0
    if octave == "1":
        return 1
    if octave == "2":
        return 2
    if octave == "3":
        return 3
    if octave == "4":
        return 4
    if octave == "5":
        return 5
    if octave == "6":
        return 6
    if octave == "7":
        return 7
    if octave == "8":
        return 8
    return 0

#Función para obtener el accidental de una nota
def accidental(typeAccidental):
    if typeAccidental == "#":
        return 1
    if typeAccidental == "b":
        return -1
    return 0

#Función para obtener el valor de tiempo que sonara una nota o descanso
def valTemp(value):
    if value == "w":
        return 1000
    if value == "h":
        return 500
    if value == "q":
        return 250 
    if value == "e":
        return 125 
    if value == "s":
        return 62.5 
    if value == "t":
        return 33.3
    if value == "f":
        return 16.6
    return 0

#Función para obtener el modificador de tiempo
def modTemp(valueTemp):
    if valueTemp == "t":
        return 2/3
    if valueTemp == "3":
        return 2/3
    if valueTemp == "5":
        return 4/5
    if valueTemp == "7":
        return 6/7 
    if valueTemp == "9":
        return 8/9 
    if valueTemp == ".":
        return .25
    if valueTemp == "tt" or valueTemp == "33":
        return 4/9
    return 1

#Función que crea la nota tomando (nota, octava, tiempo) y las almacena en "noteArr, octaveArr, durationArr" respectivamente.
def createNote(c):
    getNote = 0
    octaveResult = 0
    getDuration = 0

    # Variables auxiliares
    modDot = 1.25
    modDotApply = False
    for i in range(0,  len(c)):
        #Obtenemos notas
        getNote += letter(c[i])
        getNote += accidental(c[i])

        #Otenemos octavas
        # Para el caso de las octavas negaticas
        if c[i] == "-":
            octaveResult += getOctave(c[i+1]) * -1
            i += 1
        else:
            if octaveResult == 0: 
                octaveResult += getOctave(c[i])
        
        #Obtenemos duración
        getDuration += valTemp(c[i])

        #Para el caso del modificador "."
        if c[i] == ".":
            modDotApply = True
            modDot += modTemp(c[i])
        
        if modDotApply == True and len(c) == i+1:
            getDuration *= modDot
        else:
            # Para el caso de "tt" o "33"
            if (c[i] == "3" or c[i] == "t") and len(c) != i+1: 
                getDuration *= modTemp(c[i]+c[i+1])
                i+1
            else:
                getDuration *= modTemp(c[i])
            

    #Guardamos en array
    # print("\nnote | octave | duration")
    # print(getNote, " | ", octaveResult, " | ", getDuration)
    noteArr.append(getNote)
    octaveArr.append(octaveResult)
    durationArr.append(getDuration)
    # Solo para testing
    # getWave(getNote, octaveResult, getDuration)

# Funciones adicionales para el analisis de léxico
# Función para la deteccion de errores
def inputError(c):
    print("\nError en la linea ", lineError)
    print("Input no reconocido: ", c, "\n")
    return "" 

# Función para la deteccion de un estado aceptor
def estadoAceptor(caso):
    # print("\n") 
    # print(caso)
    return ""

# Función para poder crear una nota o descanso
def ciclo(iteration, actualInput):
    inputCiclo = ""
    iteration += 1
    for i in range(iteration, len(actualInput)):
        actualInputUnicode = ord(actualInput[i]) #Guardamos su codigo unicode
        if actualInputUnicode != 13 and actualInput[i] != " ": 
            inputCiclo += actualInput[i]
        else:
            return inputCiclo

# Función para poder crear un comentario
def cicloComentario(iteration, actualInput):
    inputCiclo = ""
    iteration += 1
    for i in range(iteration, len(actualInput)):
        actualInputUnicode = ord(actualInput[i]) #Guardamos su codigo unicode
        if actualInputUnicode != 13: 
            inputCiclo += actualInput[i]
        else:
            return i, inputCiclo
        
# LECTURA DE ARCHIVO TXT
def loadData(file):
    if not verificarArchivoTxt.fullmatch(file):
        file += ".txt"
    #Abrimos archivo y extramos la informacion
    with open(file, 'r') as inputFile:

        #Guardamos los datos extraidos en una variable
        header = inputFile.readline()
        isHeader = True #Para poder agregar al "header" en el array 
        list = []
        for line in inputFile:
            if isHeader == True:
                list.append(header)
                isHeader = False

            list.append(line)

        listData = "" #Variable que contendra los datos para utilizar
        
        #Convertimos las lineas del archivo en strings
        for element in list:
            newElement = element.strip().split(",")
            listData += newElement[0] + chr(13)

        return listData


# ANÁLISIS DE SINTAXIS
#Función que nos permite avanzar en la cadena de tokens
def continuar():
    global tokenActual
    global sintaxisValida
    global lineError
    if(len(tokenArr) > 0):
        tokenActual = tokenArr.pop()
        if tokenActual == 5:
            lineError += 1
    else:
        sintaxisValida = True 

#Funciones necesarias para el analizador sintactico (con el método descenso recursivo)
def partitura():
    if not sintaxisValida:
        if tokenActual == 0:
            continuar()
            primeraNota()
        elif tokenActual == 5:
            continuar()
            partitura()
        elif tokenActual == 4:
            continuar()
            comentario()
        else:
            print("Error en la linea: ", lineError, " Se esperaba una \"nombre\" o un \"comentario\"")
            exit()

def primeraNota():
    if tokenActual == 1 or tokenActual == 2:
        continuar()
        nota()    
    else: 
        print("Error en la linea: ", lineError, " Se esperaba un \"nota\" o un \"descanso\"")
        exit()

def nota():
    if tokenActual == 1 or tokenActual == 2:
        continuar()
        nota()
    elif tokenActual == 3:
        continuar()
        limitador()
    elif not tokenActual == 5:
        print("Error en la linea: ", lineError, " Se esperaba un \"nota\" o un \"descanso\" o \"limitador de linea\" \"|\"")
        exit()

def limitador():
    if tokenActual == 1 or tokenActual == 2:
        continuar()
        nota()
    elif not tokenActual == 5:
        print("Error en la linea: ", lineError, "Se esperaba un \"nota\" o un \"descanso\"")
        exit()

def comentario():
    if not tokenActual == 5:
        print("Error en la linea: ", lineError, "Se esperaba un enter para finalizar comentario")
        exit()

#Función que inicia el análisis sintactico  
def analisisSintaxis():
    continuar()
    partitura()

    if sintaxisValida != True:
        analisisSintaxis()

#Función adicional
#Esta función imprime el documento tokenizado - Meramente informativo
def visualizarTokens():
    for i in tokenArr:
        print(i, end="")
    print("\n")
    for i in tokenArr:
        print(i, end=",")


####### COMIENZO DE EJECUCIÓN PRINCIPAL #######

#Obtenemos datos del txt
file = input("Escribe el nombre del archivo para compilarlo: ")

print("Procesando archivo...")
actualInput = loadData(file)

#Comienza ejecución principal
print("\nComenzando análisis de lexico...")
for i in range(0, len(actualInput)):
    #Este if nos ayuda a no repetir posiciones que ya se pasaron en los ciclos
    if i <= flagPosition and i != 0:
        continue
        
    actualInputUnicode = ord(actualInput[i])
    
    #Validamos para no guardar "Enter"
    if actualInputUnicode != 13:
        c += actualInput[i]
    else:
        tokenArr.append(5)
        lineError += 1
        
    #Comienzo funcionalidades de lexema
    #Inicio de comentario
    if c == "#":
        resComentario = cicloComentario(i, actualInput)
        flagPosition = resComentario[0]
        c += resComentario[1]
        #Palabra reservada #BAR
        if palabraReservadaBAR.fullmatch(c):
            tokenArr.append(4)
            c = estadoAceptor("\nSe detecto palabra reservada #BAR")
            tokenArr.append(5)

        #Comentario
        if comentarioMut.fullmatch(c):
            messageAceptor = "Se identifico comentario:  " + c
            c = estadoAceptor(messageAceptor)
            lineError += 1
            tokenArr.append(4)
            tokenArr.append(5)
            continue
        
        # tokenArr.append(5)
        lineError += 1

    #Deteccion de nota
    if iniciomNote.fullmatch(c):
        # print("Esto es actualInput: ", actualInput[i])
        if actualInput[i] == "s":
            tiempo = 250

        c += ciclo(i, actualInput)
        if mNote.fullmatch (c):
            createNote(c)
            messageAceptor = "Se detecto una nota musical:  " + c
            c = estadoAceptor(messageAceptor)
            tokenArr.append(1)
            continue
        else:
            lineError += 1
            c = inputError(c)
            lexicoValido = False
            break

    #Deteccion de descanso
    if inicioDescanso.fullmatch(c):
        c += ciclo(i, actualInput)

        if descanso.fullmatch(c):
            createNote(c)
            messageAceptor = "Se detecto un descanso:  " + c
            c = estadoAceptor(messageAceptor)
            tokenArr.append(2)
            continue
        else:
            lineError += 1
            c = inputError(c)
            lexicoValido = False
            break

    #Deteccion de partición
    if particion.fullmatch(c):
        c = estadoAceptor("\nLimitador de medida")
        tokenArr.append(3)
        continue

    #Deteccion de nombre
    if actualInputUnicode == 13 or actualInput[i] == " ":
        if name.fullmatch(c):
            messageAceptor = "Se detecto nombre:  " + c
            c = estadoAceptor(messageAceptor)
            tokenArr.append(0)
            # if actualInputUnicode == 13: tokenArr.append(5)
            continue

        if c == " " or c == "":
            c = ""
        else:
            #Este if es para detecar un error en la misma linea
            if actualInputUnicode != 13:
                lineError += 1
            c = inputError(c)
            lexicoValido = False
            break

if lexicoValido == True:
    print("\nComenzamos análisis de sintaxis...")

    # visualizarTokens()
    tokenArr.reverse() #Invertimos array para crear fila 
    lineError = 1
    analisisSintaxis()

if sintaxisValida == True:
    print("\nReproduciendo canción...")
    # print("Valores: ", noteArr)
    # print("Valores: ", octaveArr)
    # print("Valores: ", durationArr)
    for i in range(0, len(noteArr)):
        getWave(noteArr[i], octaveArr[i], durationArr[i])
    
print("\nFin de análisis")