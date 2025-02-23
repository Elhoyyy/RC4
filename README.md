# RC4

## Descripción:
Implementación del conocido algoritmo rc4, de manera que se vean todos los cambios que se realiza durante el proceso para entender detenidamente el flujo de creación del keystream así como del array S. 

RC4.py: permite únicamente realizar cifrado y descifrado con la clave y cadena en hexadecimal ( para siempre permitir mostrar todos los caracteres).
  Uso del programa:
          rc4.py -c <clave_hex>                : Cifrar un mensaje con la clave proporcionada en hexadecimal.
          rc4.py -d <clave_hex> <cadena_hex>   : Descifrar una cadena hexadecimal con la clave proporcionada.


## Ejemplo de ejecución: 

```bash
python rc4.py -c a0b2c1
```

INTRODUCIMOS LA PALABRA [ p r u e b a ] cuyo resultado será [5a37b7f0e6a6]

```bash
python rc4-py -d aba0b2b2 5a37b7f0e6a6
```

RESULTADO: prueba


