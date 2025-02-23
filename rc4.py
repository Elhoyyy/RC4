from sys import argv
import numpy as np
def KSA(key, op):
    T= len(key) #Como en RC4 es tipico usar una clave de 128 bits esto es 16 caracteres ASCII, esto se repetira 16 veces hasta completar el vector de 256 bytes .
    S=list(range(256))  # elementos secuenciales del 1 al 256
    if(op=='-c'): #Básicamente para que solo lo imprima si es para cifrar, para descifrar no nos interesa ver el array S. 
        print("VALOR INICIAL DE S:\n",S, "\n")
    j=0
    
    for i in range(256):
        j = (j + S[i] + key[i % T]) % 256
        S[i], S[j] = S[j], S[i]
    return S

#Hacer función XOR entre arrays.
def lista_xor(list1, list2):
    return [a ^ b for a, b in zip(list1, list2)]

def hex_to_key(hex_string):
    # Convertir una cadena hexadecimal a una lista de enteros
    return [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]

def print_matrix(S, columns=16): #imprimir la matriz en 16x16 de forma que se vea ordenado. 
        for i in range(0, len(S), columns):
            print(S[i:i+columns])

def cifrar(clave, S):
    #Inicializamos variables necesarias
    i=0 
    j=0
    k=0
    x=0
    r=0
    cadena=''
    res_hex_total=''
    cadena2=[]
    chiperarray=[]
    keystream=[]
    keystream_paraprint=[]
    rounds_tracking = ['' for _ in range(256)]  # Array para tracking de rondas
    S_copy = S.copy()  # Copia del array S para mostrar con las rondas
    
    while True:
        print("\nCambios de array S en cada generación:\n")
        # Mostrar S con el tracking de rondas
        S_display = [f"{v}{rounds_tracking[idx]}" for idx, v in enumerate(S_copy)]
        print_matrix(S_display)
        print("\nIngresa cada letra (escribe exit para terminar):")
        letra=input()
        if letra == 'exit':
            cifrado=[]
            break
        elif len(letra) == 1:
            cadena += letra
            cadena2.append(ord(letra))
            print("\nCaracter ASCII:" ,letra)
            binario= bin(ord(letra)).replace('0b','')
            if(len(binario) <8 ):
                while (len(binario))<8:
                    binario="0"+binario
                print ("Caracter BINARIO:",binario)
            else:
                print ("Caracter BINARIO:",binario)
            
            L= len(cadena)
            while (k<L):
                i= (i+1)%256
                j=(j+S[i]) %256
                # Actualizar el tracking de rondas
                rounds_tracking[i] = f"->{r}º"
                rounds_tracking[j] = f"->{r}º"
                # Realizar el intercambio en ambos arrays
                S[i], S[j]= S[j], S[i]
                S_copy[i], S_copy[j] = S_copy[j], S_copy[i]
                t= (S[i] + S[j]) %256
                keystream.append(S[t])
                k+=1
                r+=1
            print("\nArray Acumulado Keystream decimal:", keystream)
            
            binario2=bin(keystream[len(keystream)-1]).replace('0b','') #hacemos lo mismo que antes pero con el keystream cogiendo el último elemento para pasarlo a binario
            if(len(binario2) < 8 ):
                while (len(binario2))<8:
                    binario2="0"+binario2
                print ("Keystream binario:" , binario2)
                    
            else:
                print ("Keystream binario:" , binario2)
            
            cifrado= lista_xor(keystream,cadena2) #HACEMOS XOR PARA CIFRAR EL KEYSTREAM CON EL MENSAJE
            print("\nArray Resultado decimal:", cifrado)
            chipertext=''
            for x in cifrado:
                chipertext+=chr(x)
                chiperarray.append(x)

            binario3=bin(cifrado[len(keystream)-1]).replace('0b','') #lo mismo pero con el resultado final del cifrado.
            if(len(binario3) < 8 ):
                while (len(binario3))<8:
                    binario3="0"+binario3
                print ("Resultado binario:" , binario3)
                    
            else:
                print ("Resultado binario:" , binario3)

            res_hex= hex(cifrado[len(keystream)-1]).split('x')[-1] #pasamos el resultado a hexadecimal
            res_hex_total= res_hex_total + str(res_hex) #vamos guardando el resultado en hexadecimal en una variable para mostrarlo al final.
            print("Resultado ASCII:", chipertext[len(keystream)-1])      
            print("Resultado hexadecimal:", res_hex)
            print("\nCadena sin cifrar completa:",cadena)
            print("Cadena cifrada hexadecimal completa:", res_hex_total )


def descifrar(S, cadena):
    i= 0
    j=0
    k=0
    x=0
    L= len(cadena)
    deciphertext=''
    keystream=[]
    cadena_array = hex_to_key(cadena)
    while (k<L): # PRGA como en el cifrado 
        i= (i+1)%256
        j=(j+S[i]) %256
        S[i], S[j]= S[j], S[i]
        t= (S[i] + S[j]) %256
        keystream.append(S[t])
        k+=1
    
    print("KEYSTREAM:",keystream)
    descifrado = lista_xor(cadena_array,keystream) #xor para conseguir el mensaje descifrado.
    print("\nARRAY de DESCIFRADO:",descifrado)
    for x in descifrado:
        deciphertext+=chr(x) #ir concatenando el mensaje descifrado.
    print("Cadena descifrada completa:", deciphertext)
    
    
def main():
    ayuda='''
Uso del programa:
        rc4.py -c <clave_hex>                : Cifrar un mensaje con la clave proporcionada en hexadecimal.
        rc4.py -d <clave_hex> <cadena_hex>   : Descifrar una cadena hexadecimal con la clave proporcionada.
'''
    if len(argv) <2 :

        print(ayuda)
    else:
        #Introducimos los argumentos necesarios. La opción para saber si descifrar, cifrar o hacer hexadecimal.
        script, opcion = argv[:2]
        if opcion == '-c':  #ciframos
            if len(argv) > 2: #si hay más de 2 argumentos se procede a guaradr la clave que estaría en el siguiente argumento.
                clave=argv[2]
                key_int = hex_to_key(clave) #la clave se pasaría en hexadecimal por lo que queremos pasarla a un array de enteros.
                S= KSA(key_int,opcion) #utilizamos algoritmo KSA para generar el array S.
                print("VALOR S DESPUÉS DE FASE INICIAL:\n", S,"\n")
                cifrar(clave, S) #proceso de cifrado con la clave como array de enteros y el array S generado.
            else: 
                print(ayuda)

        elif opcion== '-d': 
            if len(argv) > 3: 
                clave=argv[2] #lo mismo que anteriormente pero guardamos la clave primero
                cadena_hex = argv[3] #y aquí guardamos la cadena a descifrar	
                key_int = hex_to_key(clave)
                S= KSA(key_int,opcion)
                descifrar(S, cadena_hex) #desciframos con la clave y la cadena a descifrar.
            else:
                print(ayuda)

        elif opcion == 'help':
            print(ayuda)
        else:
            print(ayuda)

#Conectar este programa con el de pasarhex.py para saber pasar a hexadecimal una cadena




if __name__ == '__main__':
    main()

