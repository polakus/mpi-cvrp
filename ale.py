import re
import math
import time
from CVRP import CVRP
from Vertice import Vertice

import os
from os import listdir
from os.path import isfile, join
import ntpath
# from mpi4py import MPI

def cargarDesdeFile(pathArchivo):
    #+-+-+-+-+-Para cargar la distancias+-+-+-+-+-+-+-+-
    
    optimo = []
    
    archivo = open(pathArchivo,"r")
    lineas = archivo.readlines()
    
    #Busco la posiciones de...
    indSeccionCoord = lineas.index("NODE_COORD_SECTION\n")
    lineaEOF = lineas.index("DEMAND_SECTION\n")
    
    #Linea optimo y nro de vehiculos
    lineaOptimo = [x for x in lineas[0:indSeccionCoord] if re.search(r"COMMENT+",x)][0]
    parametros = re.findall(r"[0-9]+",lineaOptimo)
    
    nroVehiculos = int(float(parametros[0]))
    optimo = float(parametros[1])

    #Cargo la capacidad
    lineaCapacidad = [x for x in lineas[0:indSeccionCoord] if re.search(r"CAPACITY+",x)][0]
    parametros = re.findall(r"[0-9]+",lineaCapacidad)

    capacidad = float(parametros[0])
    print("Capacidad: "+str(capacidad))

    coordenadas = []
    #Separa las coordenadas en una matriz, es una lista de listas (vertice, coordA, coordB)
    for i in range(indSeccionCoord+1, lineaEOF):
        textoLinea = lineas[i]
        textoLinea = re.sub("\n", "", textoLinea) #Elimina los saltos de linea
        splitLinea = textoLinea.split(" ") #Divide la linea por " " 
        if(splitLinea[0]==""):
            coordenadas.append([splitLinea[1],splitLinea[2],splitLinea[3]]) #[[v1,x1,y1], [v2,x2,y2], ...]
        else:
            coordenadas.append([splitLinea[0],splitLinea[1],splitLinea[2]]) #[[v1,x1,y1], [v2,x2,y2], ...]
    matrizDist = cargaMatrizDistancias(coordenadas)
    
    #+-+-+-+-+-+-+-Para cargar la demanda+-+-+-+-+-+-+-
    seccionDemanda = [x for x in lineas[indSeccionCoord:] if re.findall(r"DEMAND_SECTION+",x)][0]
    indSeccionDemanda = lineas.index(seccionDemanda)
    
    seccionEOF = [x for x in lineas[indSeccionCoord:] if re.findall(r"DEPOT_SECTION+",x)][0]
    indLineaEOF = lineas.index(seccionEOF)

    demandas = []
    for i in range(indSeccionDemanda+1, indLineaEOF):
        textoLinea = lineas[i]
        textoLinea = re.sub("\n", "", textoLinea) #Elimina los saltos de linea
        splitLinea = textoLinea.split(" ") #Divide la linea por " " 
        demandas.append(float(splitLinea[1]))

    return nroVehiculos, optimo, capacidad, matrizDist, demandas
def cargaMatrizDistancias(coordenadas):
    matriz = []
    #Arma la matriz de distancias. Calculo la distancia euclidea
    for coordRow in coordenadas:
        fila = []            
        for coordCol in coordenadas:
            x1 = float(coordRow[1])
            y1 = float(coordRow[2])
            x2 = float(coordCol[1])
            y2 = float(coordCol[2])
            dist = distancia(x1,y1,x2,y2)
            
            #Para el primer caso. Calculando la distancia euclidea entre si mismo da 0
            if(dist == 0):
                dist = 999999999999 #El modelo no deberia tener en cuenta a las diagonal, pero por las dudas
            fila.append(dist)

        #print("Fila: "+str(fila))    
        matriz.append(fila)
    return matriz    #retorna una matriz de distancia
def distancia(x1,y1,x2,y2):
    return round(math.sqrt((x1-x2)**2+(y1-y2)**2),3)

# ['Al azar','Vecino mas cercano','Secuencial']
# ['2-opt', '3-opt']


# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# nproc = comm.Get_size()

# direccion = "/home/alumno/tpfinal/cvrp2/Instancias/Set A/A-n32-k5.vrp"
direccion = "/home/alumno/tpfinal/cvrp2/Instancias/Set E/E-n101-k14.vrp"
# nombre = "A-n32-k5.vrp"
nombre = "E-n101-k14.vrp"

nroVehiculos, optimo, capacidad, matrizDist, demandas = cargarDesdeFile(direccion)
tenureADD = int(len(matrizDist)**(1/2.0))
tenureDROP = int(len(matrizDist)**(1/2.0))+1
time = 10.0
cvrp = CVRP(matrizDist, demandas, nroVehiculos, capacidad, nombre+"_"+str(time)+"min", 0, 2, tenureADD, tenureDROP, time, optimo)
