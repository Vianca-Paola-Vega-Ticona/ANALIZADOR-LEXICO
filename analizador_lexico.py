# ANALIZADOR LÉXICO
# ================================================================================
# Función: Convierte el código fuente en una secuencia de tokens
# Reconoce: Palabras reservadas, identificadores, números, operadores y símbolos
# ================================================================================

#FUNCIONES AUXILIARES 
def es_letra(c):
    """Verifica si un carácter es una letra (a-z, A-Z)"""
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')

def es_digito(c):
    """Verifica si un carácter es un dígito (0-9)"""
    return '0' <= c <= '9'

def analizar(codigo):
    """
    Analizador léxico principal
    Retorna: (tokens)
    - tokens: Lista de códigos numéricos de tokens
    """
    tokens = []
    i = 0
    linea = 1
    col = 1
    n = len(codigo)

    while i < n:
        c = codigo[i]
        col_inicio = col

        # ----------------------------------------------------------------
        # ESPACIOS EN BLANCO (no generan tokens)
        # ----------------------------------------------------------------
        if c.isspace():
            if c == "\n":
                linea += 1
                col = 1
            else:
                col += 1
            i += 1
            continue

        # ----------------------------------------------------------------
        # OPERADORES DOBLES (deben verificarse ANTES de los simples)
        # Token 120: ==  (igualdad)
        # Token 121: !=  (diferente)
        # Token 123: <=  (menor o igual)
        # Token 125: >=  (mayor o igual)
        # ----------------------------------------------------------------
        if i + 1 < n:
            d = codigo[i+1]

            if c == "=" and d == "=":
                tokens.append(120)  # Token 120: ==
                i += 2
                col += 2
                continue

            if c == "!" and d == "=":
                tokens.append(121)  # Token 121: !=
                i += 2
                col += 2
                continue

            if c == "<" and d == "=":
                tokens.append(123)  # Token 123: <=
                i += 2
                col += 2
                continue

            if c == ">" and d == "=":
                tokens.append(125)  # Token 125: >=
                i += 2
                col += 2
                continue

        # ----------------------------------------------------------------
        # SÍMBOLOS SIMPLES
        # Token 100: =   (asignación)
        # Token 101: (   (paréntesis izquierdo)
        # Token 102: )   (paréntesis derecho)
        # Token 103: -   (resta o menos unario)
        # Token 104: +   (suma)
        # Token 105: ;   (punto y coma)
        # Token 106: *   (multiplicación)
        # Token 107: /   (división)
        # Token 108: ,   (coma)
        # Token 122: <   (menor que)
        # Token 124: >   (mayor que)
        # ----------------------------------------------------------------
        if c == "=":
            tokens.append(100)  # Token 100: =
            i += 1
            col += 1
            continue
        elif c == "(":
            tokens.append(101)  # Token 101: (
            i += 1
            col += 1
            continue
        elif c == ")":
            tokens.append(102)  # Token 102: )
            i += 1
            col += 1
            continue
        elif c == "-":
            tokens.append(103)  # Token 103: -
            i += 1
            col += 1
            continue
        elif c == "+":
            tokens.append(104)  # Token 104: +
            i += 1
            col += 1
            continue
        elif c == ";":
            tokens.append(105)  # Token 105: ;
            i += 1
            col += 1
            continue
        elif c == "*":
            tokens.append(106)  # Token 106: *
            i += 1
            col += 1
            continue
        elif c == "/":
            tokens.append(107)  # Token 107: /
            i += 1
            col += 1
            continue
        elif c == ",":
            tokens.append(108)  # Token 108: ,
            i += 1
            col += 1
            continue
        elif c == "<":
            tokens.append(122)  # Token 122: <
            i += 1
            col += 1
            continue
        elif c == ">":
            tokens.append(124)  # Token 124: >
            i += 1
            col += 1
            continue

        # ----------------------------------------------------------------
        # NÚMEROS (Token 700)
        # Reconoce: Secuencias de dígitos
        # Error: Si un número es seguido por letra o guion bajo
        # ----------------------------------------------------------------
        if es_digito(c):
            numero = ""
            
            while i < n and es_digito(codigo[i]):
                numero += codigo[i]
                i += 1
                col += 1
            
            # Verificar si continúa con letra o guion bajo (ERROR LÉXICO)
            if i < n and (es_letra(codigo[i]) or codigo[i] == '_'):
                lexema_error = numero
                while i < n and (es_letra(codigo[i]) or es_digito(codigo[i]) or codigo[i] == '_'):
                    lexema_error += codigo[i]
                    i += 1
                    col += 1
                
                print(f"Error léxico: símbolo '{lexema_error}' no reconocido (línea {linea}, columna {col_inicio})")
                tokens.append(900)  # Token 900: ERROR
                return tokens
            
            tokens.append(700)  # Token 700: NUMERO
            continue
        # ----------------------------------------------------------------
        # IDENTIFICADORES Y PALABRAS RESERVADAS
        # Identificadores (Token 500): Variables definidas por el usuario
        # Palabras Reservadas (Tokens 1-19): Palabras clave del lenguaje
        # ----------------------------------------------------------------
        if es_letra(c):
            lexema = ""
            
            lexema += c
            i += 1
            col += 1
            
            # Capturar secuencia completa: letras, dígitos y guiones bajos
            while i < n and (es_letra(codigo[i]) or es_digito(codigo[i]) or codigo[i] == "_"):
                lexema += codigo[i]
                i += 1
                col += 1
          
            # ----------------------------------------------------------------
            # PALABRAS RESERVADAS (Tokens 1-19)
            # Token 1: inicio
            # Token 2: fin
            # Token 3: entero
            # Token 4: imprimir
            # Token 5: ingresa
            # Token 6: si
            # Token 7: entonces
            # Token 8: sino
            # Token 9: fin_si
            # Token 10: mientras_que
            # Token 11: hacer
            # Token 12: fin_mientras_que
            # Token 13: repetir
            # Token 14: hasta_que
            # Token 15: para
            # Token 16: fin_para
            # Token 17: no
            # Token 18: y
            # Token 19: o
            # Token 500: IDENTIFICADOR (si no coincide con ninguna palabra reservada)
            # ----------------------------------------------------------------
            if lexema == "inicio":
                tokens.append(1)
            elif lexema == "fin":
                tokens.append(2)
            elif lexema == "entero":
                tokens.append(3)
            elif lexema == "imprimir":
                tokens.append(4)
            elif lexema == "ingresa":
                tokens.append(5)
            elif lexema == "si":
                tokens.append(6)
            elif lexema == "entonces":
                tokens.append(7)
            elif lexema == "sino":
                tokens.append(8)
            elif lexema == "fin_si":
                tokens.append(9)
            elif lexema == "mientras_que":
                tokens.append(10)
            elif lexema == "hacer":
                tokens.append(11)
            elif lexema == "fin_mientras_que":
                tokens.append(12)
            elif lexema == "repetir":
                tokens.append(13)
            elif lexema == "hasta_que":
                tokens.append(14)
            elif lexema == "para":
                tokens.append(15)
            elif lexema == "fin_para":
                tokens.append(16)
            elif lexema == "no":
                tokens.append(17)
            elif lexema == "y":
                tokens.append(18)
            elif lexema == "o":
                tokens.append(19)
            else:
                tokens.append(500)  # Token 500: IDENTIFICADOR
            continue

        # ----------------------------------------------------------------
        # ERROR - CARACTER NO RECONOCIDO (Token 900)
        # ----------------------------------------------------------------
        print(f"Error léxico: símbolo '{c}' no reconocido (línea {linea})")
        tokens.append(900)  # Token 900: ERROR
        return tokens

    return tokens
    
# ----------------------------------------------
# CASOS DE PRUEBA
# ----------------------------------------------

print("\nCASO 1: Identificadores válidos")
codigo1 = """inicio
entero var_1, Var_2, num;
fin"""
print(analizar(codigo1))

print("CASO 2: Programa válido")
codigo2 = """inicio
entero a, b, suma;
a = 10;
b = 20;
suma = a + b;
imprimir(suma);
fin"""
print(analizar(codigo2))

print("\nCASO 3: ERROR - símbolo '@'")
codigo3 = """inicio
entero a;
a = 10 @ 20;
fin"""
print(analizar(codigo3))

print("\nCASO 4: Ejemplo completo con ciclo para")
codigo4 = """inicio
entero a;
a = 10;
para(entero i = 0; i < 5; i = i + 1) hacer
    imprimir(i);
fin_para;
fin"""
print(analizar(codigo4))

print("\nCASO 5: ERROR - numero con letras")
codigo5 = """inicio
entero a;
a = 1234ee33;
fin"""
print(analizar(codigo5))

print("\nCASO 6: Condición SI")
codigo6 = """inicio
entero a;
a = 15;
si a > 10 entonces
    imprimir(a);
fin_si
fin"""
print(analizar(codigo6))

print("\nCASO 7: Ciclo MIENTRAS")
codigo7 = """inicio
entero i;
i = 0;
mientras_que i < 5 hacer
    imprimir(i);
    i = i + 1;
fin_mientras_que
fin"""
print(analizar(codigo7))

print("\nCASO 8: Ciclo REPETIR")
codigo8 = """inicio
entero x;
x = 1;
repetir
    imprimir(x);
    x = x + 1;
hasta_que x == 5;
fin"""
print(analizar(codigo8))

print("\nCASO 9: Operadores relacionales")
codigo9 = """inicio
entero a, b;
a = 10;
b = 20;
si a != b entonces
    imprimir(a);
fin_si
si a <= b entonces
    imprimir(b);
fin_si
si b >= a entonces
    imprimir(a);
fin_si
fin"""
print(analizar(codigo9))

print("\nCASO 10: ERROR - carácter '$'")
codigo10 = """inicio
entero total;
total = 50 $ 10;
fin"""
print(analizar(codigo10))