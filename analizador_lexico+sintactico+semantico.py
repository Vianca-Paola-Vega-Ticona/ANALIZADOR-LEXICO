# ANALIZADOR LÉXICO + SINTÁCTICO


# ================================================================================
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
    - lineas: Lista de números de línea donde aparece cada token
    - lexemas: Lista de cadenas originales del código fuente
    """
    tokens = []
    lineas = []
    lexemas = []
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
                lineas.append(linea)
                lexemas.append("==")
                i += 2
                col += 2
                continue

            if c == "!" and d == "=":
                tokens.append(121)  # Token 121: !=
                lineas.append(linea)
                lexemas.append("!=")
                i += 2
                col += 2
                continue

            if c == "<" and d == "=":
                tokens.append(123)  # Token 123: <=
                lineas.append(linea)
                lexemas.append("<=")
                i += 2
                col += 2
                continue

            if c == ">" and d == "=":
                tokens.append(125)  # Token 125: >=
                lineas.append(linea)
                lexemas.append(">=")
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
            lineas.append(linea)
            lexemas.append("=")
            i += 1
            col += 1
            continue
        elif c == "(":
            tokens.append(101)  # Token 101: (
            lineas.append(linea)
            lexemas.append("(")
            i += 1
            col += 1
            continue
        elif c == ")":
            tokens.append(102)  # Token 102: )
            lineas.append(linea)
            lexemas.append(")")
            i += 1
            col += 1
            continue
        elif c == "-":
            tokens.append(103)  # Token 103: -
            lineas.append(linea)
            lexemas.append("-")
            i += 1
            col += 1
            continue
        elif c == "+":
            tokens.append(104)  # Token 104: +
            lineas.append(linea)
            lexemas.append("+")
            i += 1
            col += 1
            continue
        elif c == ";":
            tokens.append(105)  # Token 105: ;
            lineas.append(linea)
            lexemas.append(";")
            i += 1
            col += 1
            continue
        elif c == "*":
            tokens.append(106)  # Token 106: *
            lineas.append(linea)
            lexemas.append("*")
            i += 1
            col += 1
            continue
        elif c == "/":
            tokens.append(107)  # Token 107: /
            lineas.append(linea)
            lexemas.append("/")
            i += 1
            col += 1
            continue
        elif c == ",":
            tokens.append(108)  # Token 108: ,
            lineas.append(linea)
            lexemas.append(",")
            i += 1
            col += 1
            continue
        elif c == "<":
            tokens.append(122)  # Token 122: <
            lineas.append(linea)
            lexemas.append("<")
            i += 1
            col += 1
            continue
        elif c == ">":
            tokens.append(124)  # Token 124: >
            lineas.append(linea)
            lexemas.append(">")
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
                lineas.append(linea)
                lexemas.append(lexema_error)
                return tokens, lineas, lexemas
            
            tokens.append(700)  # Token 700: NUMERO
            lineas.append(linea)
            lexemas.append(numero)
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

            lineas.append(linea)
            lexemas.append(lexema)
            continue

        # ----------------------------------------------------------------
        # ERROR - CARACTER NO RECONOCIDO (Token 900)
        # ----------------------------------------------------------------
        print(f"Error léxico: símbolo '{c}' no reconocido (línea {linea})")
        tokens.append(900)  # Token 900: ERROR
        lineas.append(linea)
        lexemas.append(c)
        return tokens, lineas, lexemas

    return tokens, lineas, lexemas
    

# ================================================================================
# ANALIZADOR SINTÁCTICO
# ================================================================================
# Función: Verifica que la secuencia de tokens cumpla con la gramática
# Método: Análisis descendente recursivo (Recursive Descent Parser)
# Cada función representa una regla de producción de la gramática EBNF
# ================================================================================

# Variables globales del analizador sintáctico
tokens = []
lineas = []
lexemas = []
posicion = 0
token_actual = None
linea_actual = None
lexema_actual = None
hay_error = False

def avanzar():
    """Avanza al siguiente token en la lista"""
    global posicion, token_actual, linea_actual, lexema_actual
    posicion += 1
    if posicion < len(tokens):
        token_actual = tokens[posicion]
        linea_actual = lineas[posicion]
        lexema_actual = lexemas[posicion]
    else:
        token_actual = None
        linea_actual = None
        lexema_actual = None

def simbolo(tok):
    """Convierte código de token a nombre legible para mensajes de error"""
    if tok is None:
        return "fin de archivo"
    if tok == 1: return "inicio"
    elif tok == 2: return "fin"
    elif tok == 3: return "entero"
    elif tok == 4: return "imprimir"
    elif tok == 5: return "ingresa"
    elif tok == 6: return "si"
    elif tok == 7: return "entonces"
    elif tok == 8: return "sino"
    elif tok == 9: return "fin_si"
    elif tok == 10: return "mientras_que"
    elif tok == 11: return "hacer"
    elif tok == 12: return "fin_mientras_que"
    elif tok == 13: return "repetir"
    elif tok == 14: return "hasta_que"
    elif tok == 15: return "para"
    elif tok == 16: return "fin_para"
    elif tok == 17: return "no"
    elif tok == 18: return "y"
    elif tok == 19: return "o"
    elif tok == 100: return "="
    elif tok == 101: return "("
    elif tok == 102: return ")"
    elif tok == 103: return "-"
    elif tok == 104: return "+"
    elif tok == 105: return ";"
    elif tok == 106: return "*"
    elif tok == 107: return "/"
    elif tok == 108: return ","
    elif tok == 120: return "=="
    elif tok == 121: return "!="
    elif tok == 122: return "<"
    elif tok == 123: return "<="
    elif tok == 124: return ">"
    elif tok == 125: return ">="
    elif tok == 500: return "identificador"
    elif tok == 700: return "numero"
    elif tok == 900: return "error"
    else: return str(tok)

def error(mensaje):
    """Reporta un error sintáctico y termina el análisis"""
    global hay_error
    hay_error = True
    if token_actual is None:
        print(f"Error de sintaxis: {mensaje}. Token actual: fin de archivo")
    else:
        print(f"Error de sintaxis en la linea {linea_actual}: se encontro '{lexema_actual}' pero se esperaba {mensaje}")
    exit()

def coincidir(esperado):
    """Verifica que el token actual coincida con el esperado y avanza"""
    global token_actual
    if token_actual == esperado:
        avanzar()
    else:
        error(f"'{simbolo(esperado)}'")

# ================================================================================
# FUNCIONES DE LA GRAMÁTICA
# ================================================================================

def programa():
    """
    Gramática: programa = "inicio", { declaracion }, { sentencia }, "fin" ;
    Representa la estructura principal del programa
    """
    # Verificar que comience con "inicio"
    if token_actual != 1:
        if token_actual == 500 and lexema_actual.lower() == "inicio":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(1)  # Token 1: inicio
    
    # Procesar todas las declaraciones (entero ...)
    while token_actual is not None and token_actual == 3:
        declaracion()
    
    # Verificar error común: usar "Entero" en lugar de "entero"
    if token_actual == 500 and lexema_actual.lower() == "entero":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    
    # Procesar todas las sentencias (asignaciones, imprimir, si, mientras, etc.)
    while token_actual is not None and token_actual in [4, 5, 6, 10, 13, 15, 500]:
        sentencia()
    
    # Verificar que termine con "fin"
    if token_actual != 2:
        if token_actual == 500 and lexema_actual.lower() == "fin":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(2)  # Token 2: fin

def declaracion():
    """
    Gramática: declaracion = "entero", lista_decl, ";" ;
    Declara variables de tipo entero
    """
    if token_actual != 3:
        if token_actual == 500 and lexema_actual.lower() == "entero":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(3)  # Token 3: entero
    lista_decl()
    coincidir(105)  # Token 105: ;

def lista_decl():
    """
    Gramática: lista_decl = identificador, [ "=", expresion ],
                            { ",", identificador, [ "=", expresion ] } ;
    Lista de variables con inicialización opcional
    Ejemplos: x; o x = 5; o x, y = 3, z;
    """
    coincidir(500)  # Token 500: identificador
    
    # Inicialización opcional de la primera variable
    if token_actual is not None and token_actual == 100:
        coincidir(100)  # Token 100: =
        expresion()
    
    # Variables adicionales separadas por comas
    while token_actual is not None and token_actual == 108:
        coincidir(108)  # Token 108: ,
        coincidir(500)  # Token 500: identificador
        
        # Inicialización opcional de variables adicionales
        if token_actual is not None and token_actual == 100:
            coincidir(100)  # Token 100: =
            expresion()

def sentencia():
    """
    Gramática: sentencia = asignacion | imprimir | ingresa | si | mientras | repetir | para ;
    Representa cualquier sentencia ejecutable del programa
    """
    if token_actual is None:
        error("una sentencia valida")
    
    # Determinar qué tipo de sentencia es según el token actual
    if token_actual == 4:
        imprimir()
    elif token_actual == 5:
        ingresa()
    elif token_actual == 6:
        si()
    elif token_actual == 10:
        mientras()
    elif token_actual == 13:
        repetir()
    elif token_actual == 15:
        para()
    elif token_actual == 500:
        # Verificar que no sea una palabra reservada mal escrita
        if lexema_actual.lower() in ["imprimir", "ingresa", "si", "entonces", "sino", "mientras_que", "hacer", "repetir", "hasta_que", "para", "entero", "inicio", "fin", "fin_si", "fin_mientras_que", "fin_para", "no", "y", "o"]:
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
        asignacion()
    else:
        error("una sentencia valida")

def asignacion():
    """
    Gramática: asignacion = identificador, "=", expresion, ";" ;
    Asigna el valor de una expresión a una variable
    Ejemplo: x = 5 + 3;
    """
    coincidir(500)  # Token 500: identificador
    coincidir(100)  # Token 100: =
    expresion()
    coincidir(105)  # Token 105: ;

def imprimir():
    """
    Gramática: imprimir = "imprimir", "(", expresion, { ",", expresion }, ")", ";" ;
    Imprime una o más expresiones
    Ejemplo: imprimir(x, y + 2);
    """
    if token_actual != 4:
        if token_actual == 500 and lexema_actual.lower() == "imprimir":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(4)    # Token 4: imprimir
    coincidir(101)  # Token 101: (
    expresion()
    
    # Expresiones adicionales separadas por comas
    while token_actual is not None and token_actual == 108:
        coincidir(108)  # Token 108: ,
        expresion()
    
    coincidir(102)  # Token 102: )
    coincidir(105)  # Token 105: ;

def ingresa():
    """
    Gramática: ingresa = "ingresa", "(", identificador, ")", ";" ;
    Lee un valor desde la entrada y lo almacena en una variable
    Ejemplo: ingresa(x);
    """
    if token_actual != 5:
        if token_actual == 500 and lexema_actual.lower() == "ingresa":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(5)    # Token 5: ingresa
    coincidir(101)  # Token 101: (
    coincidir(500)  # Token 500: identificador
    coincidir(102)  # Token 102: )
    coincidir(105)  # Token 105: ;

def si():
    """
    Gramática: si = "si", "(", condicion, ")", "entonces", bloque,
                    [ "sino", bloque ], "fin_si", ";" ;
    Estructura condicional if-then-else
    Ejemplo: si (x > 0) entonces ... sino ... fin_si;
    """
    if token_actual != 6:
        if token_actual == 500 and lexema_actual.lower() == "si":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(6)    # Token 6: si
    coincidir(101)  # Token 101: (
    condicion()
    coincidir(102)  # Token 102: )
    
    if token_actual != 7:
        if token_actual == 500 and lexema_actual.lower() == "entonces":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(7)    # Token 7: entonces
    bloque()
    
    # Parte "sino" opcional
    if token_actual is not None and token_actual == 8:
        coincidir(8)  # Token 8: sino
        bloque()
    elif token_actual == 500 and lexema_actual.lower() == "sino":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    
    if token_actual != 9:
        if token_actual == 500 and lexema_actual.lower() == "fin_si":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(9)    # Token 9: fin_si
    coincidir(105)  # Token 105: ;

def mientras():
    """
    Gramática: mientras = "mientras_que", "(", condicion, ")",
                          "hacer", bloque, "fin_mientras_que", ";" ;
    Bucle while
    Ejemplo: mientras_que (x < 10) hacer ... fin_mientras_que;
    """
    if token_actual != 10:
        if token_actual == 500 and lexema_actual.lower() == "mientras_que":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(10)   # Token 10: mientras_que
    coincidir(101)  # Token 101: (
    condicion()
    coincidir(102)  # Token 102: )
    
    if token_actual != 11:
        if token_actual == 500 and lexema_actual.lower() == "hacer":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(11)   # Token 11: hacer
    bloque()
    
    if token_actual != 12:
        if token_actual == 500 and lexema_actual.lower() == "fin_mientras_que":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(12)   # Token 12: fin_mientras_que
    coincidir(105)  # Token 105: ;

def repetir():
    """
    Gramática: repetir = "repetir", bloque, "hasta_que", "(", condicion, ")", ";" ;
    Bucle do-while (se ejecuta al menos una vez)
    Ejemplo: repetir ... hasta_que (x > 10);
    """
    if token_actual != 13:
        if token_actual == 500 and lexema_actual.lower() == "repetir":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(13)   # Token 13: repetir
    bloque()
    
    if token_actual != 14:
        if token_actual == 500 and lexema_actual.lower() == "hasta_que":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(14)   # Token 14: hasta_que
    coincidir(101)  # Token 101: (
    condicion()
    coincidir(102)  # Token 102: )
    coincidir(105)  # Token 105: ;

def para():
    """
    Gramática: para = "para", "(", inicializacion, ";", condicion, ";", actualizacion, ")",
                      "hacer", bloque, "fin_para", ";" ;
    Bucle for con inicialización, condición y actualización
    Ejemplo: para(i = 0; i < 10; i = i + 1) hacer ... fin_para;
    """
    if token_actual != 15:
        if token_actual == 500 and lexema_actual.lower() == "para":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(15)   # Token 15: para
    coincidir(101)  # Token 101: (
    inicializacion()
    coincidir(105)  # Token 105: ;
    condicion()
    coincidir(105)  # Token 105: ;
    actualizacion()
    coincidir(102)  # Token 102: )
    
    if token_actual != 11:
        if token_actual == 500 and lexema_actual.lower() == "hacer":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(11)   # Token 11: hacer
    bloque()
    
    if token_actual != 16:
        if token_actual == 500 and lexema_actual.lower() == "fin_para":
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    coincidir(16)   # Token 16: fin_para
    coincidir(105)  # Token 105: ;

def inicializacion():
    """
    Gramática: inicializacion = [ "entero" ], identificador, "=", expresion ;
    Inicialización en bucle for (puede declarar variable nueva o usar existente)
    Ejemplos: i = 0  o  entero i = 0
    """
    # "entero" es opcional
    if token_actual is not None and token_actual == 3:
        coincidir(3)  # Token 3: entero
    elif token_actual == 500 and lexema_actual.lower() == "entero":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    
    coincidir(500)  # Token 500: identificador
    coincidir(100)  # Token 100: =
    expresion()

def actualizacion():
    """
    Gramática: actualizacion = identificador, "=", expresion ;
    Actualización en bucle for
    Ejemplo: i = i + 1
    """
    coincidir(500)  # Token 500: identificador
    coincidir(100)  # Token 100: =
    expresion()

def bloque():
    """
    Gramática: bloque = { sentencia } ;
    Secuencia de cero o más sentencias
    """
    while token_actual is not None and token_actual in [4, 5, 6, 10, 13, 15, 500]:
        sentencia()

def condicion():
    """
    Gramática: condicion = condicion_simple, { operador_logico_binario, condicion_simple } ;
    Expresión booleana con operadores lógicos (y, o)
    Ejemplo: x > 0 y x < 10
    """
    condicion_simple()
    
    # Operadores lógicos: 18 = y (AND), 19 = o (OR)
    while token_actual is not None and token_actual in [18, 19]:
        avanzar()
        condicion_simple()

def condicion_simple():
    """
    Gramática: condicion_simple = expresion, operador_relacional, expresion
                                  | "no", condicion_simple ;
    Comparación entre dos expresiones o negación
    Ejemplos: x > 5  o  no (x == 0)
    """
    # Negación "no"
    if token_actual is not None and token_actual == 17:
        coincidir(17)  # Token 17: no
        condicion_simple()
    elif token_actual == 500 and lexema_actual.lower() == "no":
        error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
    else:
        # Comparación: expresion operador_relacional expresion
        expresion()
        operador_relacional()
        expresion()

def operador_relacional():
    """
    Gramática: operador_relacional = "==" | "!=" | "<" | "<=" | ">" | ">=" ;
    Operadores de comparación
    Tokens: 120(==), 121(!=), 122(<), 123(<=), 124(>), 125(>=)
    """
    if token_actual is not None and token_actual in [120, 121, 122, 123, 124, 125]:
        avanzar()
    else:
        error("un operador relacional (==, !=, <, <=, >, >=)")

def expresion():
    """
    Gramática: expresion = termino, { ("+" | "-"), termino } ;
    Expresión aritmética con suma y resta (menor precedencia)
    Ejemplo: a + b - c
    """
    termino()
    
    # Operadores de suma/resta: 104 = +, 103 = -
    while token_actual is not None and token_actual in [104, 103]:
        avanzar()
        termino()

def termino():
    """
    Gramática: termino = factor, { ("*" | "/"), factor } ;
    Término con multiplicación y división (mayor precedencia que +/-)
    Ejemplo: a * b / c
    """
    factor()
    
    # Operadores de multiplicación/división: 106 = *, 107 = /
    while token_actual is not None and token_actual in [106, 107]:
        avanzar()
        factor()


def factor():
    if token_actual is None:
        error("un factor (identificador, numero, o expresion entre parentesis)")
    
    if token_actual == 500:
        if lexema_actual.lower() in ["no"]:
            error(f"'{lexema_actual.lower()}' (palabra reservada sensible a minusculas)")
        coincidir(500)
    elif token_actual == 700:
        coincidir(700)
    elif token_actual == 101:
        coincidir(101)
        expresion()
        coincidir(102)
    elif token_actual == 17:
        coincidir(17)
        factor()
    elif token_actual == 103:
        coincidir(103)
        factor()
    else:
        error("un factor (identificador, numero, o expresion entre parentesis)")

def analizar_sintactico(lista_tokens, lista_lineas, lista_lexemas):
    global tokens, lineas, lexemas, posicion, token_actual, linea_actual, lexema_actual, hay_error
    tokens = lista_tokens
    lineas = lista_lineas
    lexemas = lista_lexemas
    posicion = 0
    hay_error = False
    
    if len(tokens) == 0:
        print("Error: no hay tokens para analizar")
        hay_error = True
        return False
    
    token_actual = tokens[posicion]
    linea_actual = lineas[posicion]
    lexema_actual = lexemas[posicion]
    
    try:
        programa()
        
        if token_actual is not None:
            error("fin de programa, no se esperaban mas tokens")
        
        print("El codigo es sintacticamente correcto")
        return True
    except SystemExit:
        return False
    
# ================================================================================
# ANALIZADOR SEMÁNTICO
# ================================================================================
# Función: Interpretar el significado de las sentencias válidas del programa
# Método: Transformación de expresiones a notación prefija y generación de cuádruplos
# Cada operación es representada mediante una estructura de cuatro campos
# que facilita la construcción de código intermedio para etapas posteriores
# ================================================================================

def analizar_semantico(tokens, lineas, lexemas):
    """
    Genera cuádruplos utilizando SOLO tokens numéricos
    Retorna: (cuadruplos, tabla_identificadores_lexemas, tabla_identificadores_indices)
    """
    pos = 0
    cuadruplos = []
    temp_counter = 1
    
    # Tabla de identificadores usando listas paralelas
    tabla_ids_lexemas = []  # Lista de lexemas
    tabla_ids_indices = []  # Lista de índices correspondientes
    
    # UTILIDADES 
    
    def nueva_temp():
        """Genera un nuevo temporal T1, T2, ..."""
        nonlocal temp_counter
        t = "T" + str(temp_counter)
        temp_counter += 1
        return t
    
    def registrar_id(lexema):
        """Registra un identificador y retorna su representación [500,n]"""
        # Buscar si ya existe
        encontrado = False
        indice = 0
        for i in range(len(tabla_ids_lexemas)):
            if tabla_ids_lexemas[i] == lexema:
                encontrado = True
                indice = tabla_ids_indices[i]
                break
        
        if not encontrado:
            # Agregar nuevo identificador
            nuevo_indice = len(tabla_ids_lexemas) + 1
            tabla_ids_lexemas.append(lexema)
            tabla_ids_indices.append(nuevo_indice)
            indice = nuevo_indice
        
        return "[500," + str(indice) + "]"
    
    def token_to_operador(tok):
        """Convierte token numérico a símbolo de operador"""
        if tok == 100:
            return "100"  # =
        elif tok == 103:
            return "103"  # -
        elif tok == 104:
            return "104"  # +
        elif tok == 106:
            return "106"  # *
        elif tok == 107:
            return "107"  # /
        elif tok == 120:
            return "120"  # ==
        elif tok == 121:
            return "121"  # !=
        elif tok == 122:
            return "122"  # 
        elif tok == 123:
            return "123"  # <=
        elif tok == 124:
            return "124"  # >
        elif tok == 125:
            return "125"  # >=
        elif tok == 17:
            return "17"   # no (negación)
        elif tok == 18:
            return "18"   # y (AND)
        elif tok == 19:
            return "19"   # o (OR)
        else:
            return str(tok)
    
    def es_operador(tok):
        """Verifica si el token es un operador aritmético"""
        return tok == 103 or tok == 104 or tok == 106 or tok == 107
    
    def prioridad(tok):
        """Retorna la prioridad del operador"""
        if tok == 104 or tok == 103:  # +, -
            return 1
        if tok == 106 or tok == 107:  # *, /
            return 2
        return 0
    
    def es_menos_unario(tokens_expr, pos_menos):
        """Determina si un '-' es resta o binario"""
        # Es unario si está al inicio o después de operador/paréntesis izquierdo
        if pos_menos == 0:
            return True
        tok_anterior = tokens_expr[pos_menos - 1]
        return tok_anterior in [101, 104, 103, 106, 107]  # (, +, -, *, /
    
    def infijo_a_prefijo(tokens_expr, lexemas_expr):
        """
        Convierte expresión infija a prefija
        Maneja correctamente el menos unario
        Retorna lista de (token, lexema, es_unario)
        """
        pila = []
        salida = []
        
        # Marcar operadores unarios
        tokens_marcados = []
        for i in range(len(tokens_expr)):
            tok = tokens_expr[i]
            lex = lexemas_expr[i]
            es_unario = False
            
            if tok == 103:  # -
                if es_menos_unario(tokens_expr, i):
                    es_unario = True
            
            tokens_marcados.append((tok, lex, es_unario))
        
        # Invertir la expresión
        expr_rev = []
        for i in range(len(tokens_marcados) - 1, -1, -1):
            expr_rev.append(tokens_marcados[i])
        
        for tok, lex, es_unario in expr_rev:
            if tok == 102:  # )
                pila.append((tok, lex, es_unario))
            
            elif tok == 101:  # (
                while len(pila) > 0 and pila[len(pila)-1][0] != 102:
                    salida.append(pila.pop())
                if len(pila) > 0:
                    pila.pop()
            
            elif es_operador(tok) and not es_unario:
                while len(pila) > 0 and prioridad(tok) < prioridad(pila[len(pila)-1][0]):
                    salida.append(pila.pop())
                pila.append((tok, lex, es_unario))
            
            elif es_unario:
                # Menos unario tiene alta precedencia
                pila.append((tok, lex, es_unario))
            
            else:
                salida.append((tok, lex, es_unario))
        
        while len(pila) > 0:
            salida.append(pila.pop())
        
        # Invertir salida
        resultado = []
        for i in range(len(salida) - 1, -1, -1):
            resultado.append(salida[i])
        
        return resultado
    
    def evaluar_prefijo(prefijo):
        """
        Evalúa expresión en prefijo y genera cuádruplos
        Retorna el resultado final (temporal o identificador)
        """
        pila = []
        
        # Procesar en orden inverso
        for i in range(len(prefijo) - 1, -1, -1):
            tok, lex, es_unario = prefijo[i]
            
            if not es_operador(tok) or es_unario:
                if es_unario:
                    # Menos unario: generar cuádruple especial
                    operando = pila.pop()
                    t = nueva_temp()
                    cuadruplos.append(("103u", operando, "", t))  # 103u = menos unario
                    pila.append(t)
                else:
                    # Operando: número o identificador
                    if tok == 500:  # identificador
                        pila.append(registrar_id(lex))
                    elif tok == 700:  # número
                        pila.append(lex)
                    else:
                        pila.append(lex)
            else:
                # Operador binario
                op1 = pila.pop()
                op2 = pila.pop()
                t = nueva_temp()
                op_sym = token_to_operador(tok)
                cuadruplos.append((op_sym, op1, op2, t))
                pila.append(t)
        
        if len(pila) > 0:
            return pila.pop()
        else:
            return ""
    
    def procesar_condicion(cond_tokens, cond_lexemas):
        """
        Procesa una condición y genera cuádruplos
        Soporta operadores lógicos (y, o) y negación (no)
        """
        # Buscar operador lógico de menor precedencia (o tiene menor que y)
        op_logico_pos = -1
        op_logico_tok = -1
        
        # Buscar 'o' primero (menor precedencia)
        nivel_parentesis = 0
        for i in range(len(cond_tokens)):
            if cond_tokens[i] == 101:
                nivel_parentesis += 1
            elif cond_tokens[i] == 102:
                nivel_parentesis -= 1
            elif nivel_parentesis == 0 and cond_tokens[i] == 19:  # o
                op_logico_pos = i
                op_logico_tok = 19
                break
        
        # Si no hay 'o', buscar 'y'
        if op_logico_pos == -1:
            nivel_parentesis = 0
            for i in range(len(cond_tokens)):
                if cond_tokens[i] == 101:
                    nivel_parentesis += 1
                elif cond_tokens[i] == 102:
                    nivel_parentesis -= 1
                elif nivel_parentesis == 0 and cond_tokens[i] == 18:  # y
                    op_logico_pos = i
                    op_logico_tok = 18
                    break
        
        # Si hay operador lógico, dividir y procesar recursivamente
        if op_logico_pos != -1:
            # Dividir en izquierda y derecha
            izq_tokens = []
            izq_lexemas = []
            for i in range(op_logico_pos):
                izq_tokens.append(cond_tokens[i])
                izq_lexemas.append(cond_lexemas[i])
            
            der_tokens = []
            der_lexemas = []
            for i in range(op_logico_pos + 1, len(cond_tokens)):
                der_tokens.append(cond_tokens[i])
                der_lexemas.append(cond_lexemas[i])
            
            # Procesar ambos lados recursivamente
            resultado_izq = procesar_condicion(izq_tokens, izq_lexemas)
            resultado_der = procesar_condicion(der_tokens, der_lexemas)
            
            # Generar cuádruple para operación lógica
            t = nueva_temp()
            op_sym = token_to_operador(op_logico_tok)
            cuadruplos.append((op_sym, resultado_izq, resultado_der, t))
            return t
        
        # Verificar si empieza con 'no' (negación)
        if len(cond_tokens) > 0 and cond_tokens[0] == 17:  # no
            # Procesar el resto de la condición
            resto_tokens = []
            resto_lexemas = []
            for i in range(1, len(cond_tokens)):
                resto_tokens.append(cond_tokens[i])
                resto_lexemas.append(cond_lexemas[i])
            
            resultado_resto = procesar_condicion(resto_tokens, resto_lexemas)
            
            # Generar cuádruple de negación
            t = nueva_temp()
            cuadruplos.append(("17", resultado_resto, "", t))  # 17 = no
            return t
        
        # Buscar operador relacional
        ops_rel = [120, 121, 122, 123, 124, 125]  # ==, !=, <, <=, >, >=
        
        op_pos = -1
        for i in range(len(cond_tokens)):
            tok = cond_tokens[i]
            for op_rel in ops_rel:
                if tok == op_rel:
                    op_pos = i
                    break
            if op_pos != -1:
                break
        
        if op_pos == -1:
            # Sin operador relacional, solo expresión
            if len(cond_tokens) == 1:
                if cond_tokens[0] == 500:
                    return registrar_id(cond_lexemas[0])
                return cond_lexemas[0]
            else:
                prefijo = infijo_a_prefijo(cond_tokens, cond_lexemas)
                return evaluar_prefijo(prefijo)
        
        # Dividir en izquierda y derecha
        izq_tokens = []
        izq_lexemas = []
        for i in range(op_pos):
            izq_tokens.append(cond_tokens[i])
            izq_lexemas.append(cond_lexemas[i])
        
        der_tokens = []
        der_lexemas = []
        for i in range(op_pos + 1, len(cond_tokens)):
            der_tokens.append(cond_tokens[i])
            der_lexemas.append(cond_lexemas[i])
        
        # Evaluar lado izquierdo
        if len(izq_tokens) == 1:
            if izq_tokens[0] == 500:
                op1 = registrar_id(izq_lexemas[0])
            else:
                op1 = izq_lexemas[0]
        else:
            prefijo_izq = infijo_a_prefijo(izq_tokens, izq_lexemas)
            op1 = evaluar_prefijo(prefijo_izq)
        
        # Evaluar lado derecho
        if len(der_tokens) == 1:
            if der_tokens[0] == 500:
                op2 = registrar_id(der_lexemas[0])
            else:
                op2 = der_lexemas[0]
        else:
            prefijo_der = infijo_a_prefijo(der_tokens, der_lexemas)
            op2 = evaluar_prefijo(prefijo_der)
        
        # Generar cuádruple de comparación
        t = nueva_temp()
        op_sym = token_to_operador(cond_tokens[op_pos])
        cuadruplos.append((op_sym, op1, op2, t))
        
        return t
    
    # PROCESAMIENTO PRINCIPAL
    
    while pos < len(tokens):
        tok = tokens[pos]
        lex = lexemas[pos]
        
        # DECLARACIÓN: entero 
        if tok == 3:  # entero
            cuadruplos.append((3, "", "", ""))
            pos += 1
            
            # Procesar lista de identificadores
            while pos < len(tokens) and tokens[pos] != 105:  # hasta ;
                if tokens[pos] == 500:  # identificador
                    id_repr = registrar_id(lexemas[pos])
                    cuadruplos.append(("parametro", id_repr, "", ""))
                    pos += 1
                    
                    # Si hay inicialización (=)
                    if pos < len(tokens) and tokens[pos] == 100:
                        pos += 1  # saltar =
                        
                        # Capturar expresión hasta , o ;
                        expr_tokens = []
                        expr_lexemas = []
                        while pos < len(tokens) and tokens[pos] != 108 and tokens[pos] != 105:
                            expr_tokens.append(tokens[pos])
                            expr_lexemas.append(lexemas[pos])
                            pos += 1
                        
                        # Generar cuádruplos para la expresión
                        if len(expr_tokens) > 0:
                            prefijo = infijo_a_prefijo(expr_tokens, expr_lexemas)
                            resultado = evaluar_prefijo(prefijo)
                            cuadruplos.append(("100", resultado, "", id_repr))
                
                elif tokens[pos] == 108:  # coma
                    pos += 1
                else:
                    pos += 1
            
            if pos < len(tokens) and tokens[pos] == 105:  # ;
                pos += 1
        
        # -------- ASIGNACIÓN: id = expr; --------
        elif tok == 500:
            id_repr = registrar_id(lex)
            pos += 1
            
            if pos < len(tokens) and tokens[pos] == 100:  # =
                pos += 1
                
                # Capturar expresión hasta ;
                expr_tokens = []
                expr_lexemas = []
                while pos < len(tokens) and tokens[pos] != 105:
                    expr_tokens.append(tokens[pos])
                    expr_lexemas.append(lexemas[pos])
                    pos += 1
                
                # Generar cuádruplos
                prefijo = infijo_a_prefijo(expr_tokens, expr_lexemas)
                resultado = evaluar_prefijo(prefijo)
                cuadruplos.append(("100", resultado, "", id_repr))
                
                if pos < len(tokens) and tokens[pos] == 105:
                    pos += 1
        
        # -------- INGRESA: ingresa(id); --------
        elif tok == 5:  # ingresa
            pos += 1
            if pos < len(tokens) and tokens[pos] == 101:  # (
                pos += 1
                if pos < len(tokens) and tokens[pos] == 500:  # identificador
                    id_repr = registrar_id(lexemas[pos])
                    cuadruplos.append((5, "", "", ""))
                    cuadruplos.append(("parametro", id_repr, "", ""))
                    pos += 1
                    if pos < len(tokens) and tokens[pos] == 102:  # )
                        pos += 1
                    if pos < len(tokens) and tokens[pos] == 105:  # ;
                        pos += 1
        
        # -------- IMPRIMIR: imprimir(expr, ...); --------
        elif tok == 4:  # imprimir
            cuadruplos.append((4, "", "", ""))
            pos += 1
            
            if pos < len(tokens) and tokens[pos] == 101:  # (
                pos += 1
                
                while pos < len(tokens) and tokens[pos] != 102:  # hasta )
                    # Capturar expresión hasta , o )
                    expr_tokens = []
                    expr_lexemas = []
                    
                    while pos < len(tokens) and tokens[pos] != 108 and tokens[pos] != 102:
                        expr_tokens.append(tokens[pos])
                        expr_lexemas.append(lexemas[pos])
                        pos += 1
                    
                    # Evaluar expresión
                    if len(expr_tokens) > 0:
                        if len(expr_tokens) == 1:
                            # Expresión simple
                            if expr_tokens[0] == 500:
                                resultado = registrar_id(expr_lexemas[0])
                            else:
                                resultado = expr_lexemas[0]
                        else:
                            # Expresión compleja
                            prefijo = infijo_a_prefijo(expr_tokens, expr_lexemas)
                            resultado = evaluar_prefijo(prefijo)
                        
                        cuadruplos.append(("parametro", resultado, "", ""))
                    
                    if pos < len(tokens) and tokens[pos] == 108:  # ,
                        pos += 1
                
                if pos < len(tokens) and tokens[pos] == 102:  # )
                    pos += 1
                if pos < len(tokens) and tokens[pos] == 105:  # ;
                    pos += 1
        
        # -------- MIENTRAS_QUE --------
        elif tok == 10:  # mientras_que
            cuadruplos.append((10, "", "", ""))
            pos += 1
            
            if pos < len(tokens) and tokens[pos] == 101:  # (
                pos += 1
                
                # Capturar condición hasta )
                cond_tokens = []
                cond_lexemas = []
                nivel_parentesis = 1
                
                while pos < len(tokens) and nivel_parentesis > 0:
                    if tokens[pos] == 101:
                        nivel_parentesis += 1
                    elif tokens[pos] == 102:
                        nivel_parentesis -= 1
                        if nivel_parentesis == 0:
                            break
                    cond_tokens.append(tokens[pos])
                    cond_lexemas.append(lexemas[pos])
                    pos += 1
                
                # Procesar condición
                resultado_cond = procesar_condicion(cond_tokens, cond_lexemas)
                cuadruplos.append(("parametro", resultado_cond, "", ""))
                
                if pos < len(tokens) and tokens[pos] == 102:  # )
                    pos += 1
                if pos < len(tokens) and tokens[pos] == 11:  # hacer
                    pos += 1
            
            # NO SALTAR - continuar procesando
            continue
        
        # -------- FIN_MIENTRAS_QUE --------
        elif tok == 12:  # fin_mientras_que
            cuadruplos.append((12, "", "", ""))
            pos += 1
            if pos < len(tokens) and tokens[pos] == 105:  # ;
                pos += 1
        
        # -------- REPETIR --------
        elif tok == 13:  # repetir
            cuadruplos.append((13, "", "", ""))
            pos += 1
            # NO SALTAR - continuar procesando
            continue
        
        # -------- HASTA_QUE --------
        elif tok == 14:  # hasta_que
            pos += 1
            
            if pos < len(tokens) and tokens[pos] == 101:  # (
                pos += 1
                
                # Capturar condición
                cond_tokens = []
                cond_lexemas = []
                nivel_parentesis = 1
                
                while pos < len(tokens) and nivel_parentesis > 0:
                    if tokens[pos] == 101:
                        nivel_parentesis += 1
                    elif tokens[pos] == 102:
                        nivel_parentesis -= 1
                        if nivel_parentesis == 0:
                            break
                    cond_tokens.append(tokens[pos])
                    cond_lexemas.append(lexemas[pos])
                    pos += 1
                
                # Procesar condición
                resultado_cond = procesar_condicion(cond_tokens, cond_lexemas)
                cuadruplos.append(("parametro", resultado_cond, "", ""))
                cuadruplos.append((14, "", "", ""))
                
                if pos < len(tokens) and tokens[pos] == 102:  # )
                    pos += 1
                if pos < len(tokens) and tokens[pos] == 105:  # ;
                    pos += 1
        
        # -------- PARA --------
        elif tok == 15:  # para
            cuadruplos.append((15, "", "", ""))
            pos += 1
            
            if pos < len(tokens) and tokens[pos] == 101:  # (
                pos += 1
                
                # INICIALIZACIÓN
                # Puede ser: entero i = 0  o  i = 0
                tiene_entero = False
                if pos < len(tokens) and tokens[pos] == 3:  # entero (opcional)
                    tiene_entero = True
                    cuadruplos.append((3, "", "", ""))
                    pos += 1
                
                if pos < len(tokens) and tokens[pos] == 500:  # identificador
                    id_repr = registrar_id(lexemas[pos])
                    if tiene_entero:
                        cuadruplos.append(("parametro", id_repr, "", ""))
                    pos += 1
                    
                    if pos < len(tokens) and tokens[pos] == 100:  # =
                        pos += 1
                        
                        # Capturar valor inicial
                        expr_tokens = []
                        expr_lexemas = []
                        while pos < len(tokens) and tokens[pos] != 105:  # hasta ;
                            expr_tokens.append(tokens[pos])
                            expr_lexemas.append(lexemas[pos])
                            pos += 1
                        
                        if len(expr_tokens) > 0:
                            if len(expr_tokens) == 1:
                                if expr_tokens[0] == 500:
                                    resultado = registrar_id(expr_lexemas[0])
                                else:
                                    resultado = expr_lexemas[0]
                            else:
                                prefijo = infijo_a_prefijo(expr_tokens, expr_lexemas)
                                resultado = evaluar_prefijo(prefijo)
                            cuadruplos.append(("100", resultado, "", id_repr))
                        
                        if pos < len(tokens) and tokens[pos] == 105:  # ;
                            pos += 1
                
                # CONDICIÓN
                cond_tokens = []
                cond_lexemas = []
                while pos < len(tokens) and tokens[pos] != 105:  # hasta ;
                    cond_tokens.append(tokens[pos])
                    cond_lexemas.append(lexemas[pos])
                    pos += 1
                
                resultado_cond = procesar_condicion(cond_tokens, cond_lexemas)
                cuadruplos.append(("parametro", resultado_cond, "", ""))
                
                if pos < len(tokens) and tokens[pos] == 105:  # ;
                    pos += 1
                
                # ACTUALIZACIÓN - AHORA SÍ SE PROCESA
                act_tokens = []
                act_lexemas = []
                while pos < len(tokens) and tokens[pos] != 102:  # hasta )
                    act_tokens.append(tokens[pos])
                    act_lexemas.append(lexemas[pos])
                    pos += 1
                
                # Guardar la actualización para procesarla al final del bloque
                # Por ahora, la guardamos en un cuádruple especial
                if len(act_tokens) > 0:
                    # Buscar el identificador y la expresión
                    if act_tokens[0] == 500 and len(act_tokens) > 2 and act_tokens[1] == 100:
                        id_act = registrar_id(act_lexemas[0])
                        expr_act_tokens = []
                        expr_act_lexemas = []
                        for i in range(2, len(act_tokens)):
                            expr_act_tokens.append(act_tokens[i])
                            expr_act_lexemas.append(act_lexemas[i])
                        
                        if len(expr_act_tokens) == 1:
                            if expr_act_tokens[0] == 500:
                                resultado_act = registrar_id(expr_act_lexemas[0])
                            else:
                                resultado_act = expr_act_lexemas[0]
                        else:
                            prefijo_act = infijo_a_prefijo(expr_act_tokens, expr_act_lexemas)
                            resultado_act = evaluar_prefijo(prefijo_act)
                        
                        # Guardar actualización como cuádruple especial
                        cuadruplos.append(("100", resultado_act, "", id_act))
                
                if pos < len(tokens) and tokens[pos] == 102:  # )
                    pos += 1
                if pos < len(tokens) and tokens[pos] == 11:  # hacer
                    pos += 1
            
            # NO SALTAR - continuar procesando
            continue
        
        # -------- FIN_PARA --------
        elif tok == 16:  # fin_para
            cuadruplos.append((16, "", "", ""))
            pos += 1
            if pos < len(tokens) and tokens[pos] == 105:  # ;
                pos += 1
        
        # -------- SI --------
        elif tok == 6:  # si
            cuadruplos.append((6, "", "", ""))
            pos += 1
            
            if pos < len(tokens) and tokens[pos] == 101:  # (
                pos += 1
                
                # Capturar condición
                cond_tokens = []
                cond_lexemas = []
                nivel_parentesis = 1
                
                while pos < len(tokens) and nivel_parentesis > 0:
                    if tokens[pos] == 101:
                        nivel_parentesis += 1
                    elif tokens[pos] == 102:
                        nivel_parentesis -= 1
                        if nivel_parentesis == 0:
                            break
                    cond_tokens.append(tokens[pos])
                    cond_lexemas.append(lexemas[pos])
                    pos += 1
                
                # Procesar condición
                resultado_cond = procesar_condicion(cond_tokens, cond_lexemas)
                cuadruplos.append(("parametro", resultado_cond, "", ""))
                
                if pos < len(tokens) and tokens[pos] == 102:  # )
                    pos += 1
                if pos < len(tokens) and tokens[pos] == 7:  # entonces
                    pos += 1
            
            # NO SALTAR - continuar procesando
            continue
        
        # -------- SINO --------
        elif tok == 8:  # sino
            cuadruplos.append((8, "", "", ""))
            pos += 1
        
        # -------- FIN_SI --------
        elif tok == 9:  # fin_si
            cuadruplos.append((9, "", "", ""))
            pos += 1
            if pos < len(tokens) and tokens[pos] == 105:  # ;
                pos += 1
        
        else:
            pos += 1
    
    return cuadruplos, tabla_ids_lexemas, tabla_ids_indices

def mostrar_cuadruplos(cuadruplos, tabla_ids_lexemas, tabla_ids_indices):
    """Muestra la tabla de cuádruplos con tokens numéricos"""
    print("")
    print("=" * 70)
    print("TABLA DE CUADRUPLOS")
    print("=" * 70)
    print("No   | Operador        | Operando1    | Operando2    | Resultado")
    print("-" * 70)
    
    for i in range(len(cuadruplos)):
        op, a1, a2, res = cuadruplos[i]
        
        # Convertir operador
        if op == 3:
            op_str = "3"
        elif op == 4:
            op_str = "4"
        elif op == 5:
            op_str = "5"
        elif op == 6:
            op_str = "6"
        elif op == 9:
            op_str = "9"
        elif op == 10:
            op_str = "10"
        elif op == 12:
            op_str = "12"
        elif op == 13:
            op_str = "13"
        elif op == 14:
            op_str = "14"
        elif op == 15:
            op_str = "15"
        elif op == 16:
            op_str = "16"
        elif op == "parametro":
            op_str = "parametro"
        else:
            op_str = str(op)
        
        a1_str = str(a1) if a1 != "" else ""
        a2_str = str(a2) if a2 != "" else ""
        res_str = str(res) if res != "" else ""
        
        # Formatear con espacios
        num_str = str(i + 1)
        while len(num_str) < 4:
            num_str = num_str + " "
        
        while len(op_str) < 15:
            op_str = op_str + " "
        
        while len(a1_str) < 12:
            a1_str = a1_str + " "
        
        while len(a2_str) < 12:
            a2_str = a2_str + " "
        
        while len(res_str) < 12:
            res_str = res_str + " "
        
        print(num_str + " | " + op_str + " | " + a1_str + " | " + a2_str + " | " + res_str)
    
    print("=" * 70)
    
    # Mostrar tabla de identificadores
    if len(tabla_ids_lexemas) > 0:
        print("")
        print("TABLA DE IDENTIFICADORES:")
        print("-" * 40)
        print("Identificador        | Token")
        print("-" * 40)
        for i in range(len(tabla_ids_lexemas)):
            lexema = tabla_ids_lexemas[i]
            idx = tabla_ids_indices[i]
            
            lex_str = lexema
            while len(lex_str) < 20:
                lex_str = lex_str + " "
            
            token_str = "[500," + str(idx) + "]"
            
            print(lex_str + " | " + token_str)
        print("-" * 40)
# ====================================
# FUNCIÓN PRINCIPAL
# ====================================
def ejecutar_analisis_completo(codigo):
    print(" COMPILADOR - ANÁLISIS COMPLETO ".center(68) )
    
    # FASE 1: ANÁLISIS LÉXICO
    print("\nFASE 1: ANÁLISIS LÉXICO")
    tokens_lista, lineas_lista, lexemas_lista = analizar(codigo)
    
    # Verificar si hay error léxico
    if 900 in tokens_lista:
        print("Error léxico detectado. Análisis detenido.\n")
        return
    
    print("Análisis léxico completado exitosamente")
    
    # Mostrar lista de tokens como vector
    print("\n   LISTA DE TOKENS:")
    print(f"   {tokens_lista}")
    
    # FASE 2: ANÁLISIS SINTÁCTICO
    print("\nFASE 2: ANÁLISIS SINTÁCTICO")
    sintaxis_correcta = analizar_sintactico(tokens_lista, lineas_lista, lexemas_lista)
    
    if not sintaxis_correcta:
        print("Error sintáctico detectado. Análisis detenido.\n")
        return
    
    print("Análisis sintáctico completado exitosamente")
    
    # FASE 3: ANÁLISIS SEMÁNTICO
    print("\nFASE 3: ANÁLISIS SEMÁNTICO")
    # AQUÍ ESTÁ EL CAMBIO: Ahora retorna 2 valores
    cuadruplos, tabla_ids_lexemas, tabla_ids_indices = analizar_semantico(tokens_lista, lineas_lista, lexemas_lista)
    print("Análisis semántico completado exitosamente")
    
    # RESULTADOS
    # AQUÍ ESTÁ EL CAMBIO: Ahora recibe 2 argumentos
    mostrar_cuadruplos(cuadruplos, tabla_ids_lexemas, tabla_ids_indices)
  
    print("\n"+"COMPILACIÓN EXITOSA ".center(68) )


    

# ----------------------------------------------
# CASOS DE PRUEBA
# ----------------------------------------------

print("\n" + "="*70)
print("CASO 1: MIENTRAS_QUE - Contador simple")
print("="*70)
codigo1 = """inicio
entero contador;
contador = 0;
mientras_que (contador < 5) hacer
    imprimir(contador);
    contador = contador + 1;
fin_mientras_que;
imprimir(contador);
fin"""
ejecutar_analisis_completo(codigo1)

print("\n" + "="*70)
print("CASO 2: REPETIR-HASTA_QUE - Acumulador")
print("="*70)
codigo2 = """inicio
entero suma, i;
suma = 0;
i = 1;
repetir
    suma = suma + i;
    i = i + 1;
    imprimir(suma);
hasta_que (i > 5);
fin"""
ejecutar_analisis_completo(codigo2)

print("\n" + "="*70)
print("CASO 3: PARA - Con declaración interna")
print("="*70)
codigo3 = """inicio
entero total;
total = 0;
para(entero i = 1; i <= 3; i = i + 1) hacer
    total = total + i;
    imprimir(i, total);
fin_para;
imprimir(total);
fin"""
ejecutar_analisis_completo(codigo3)

print("\n" + "="*70)
print("CASO 4: PARA - Con variable externa")
print("="*70)
codigo4 = """inicio
entero j, resultado;
j = 0;
resultado = 100;
para(j = 0; j < 4; j = j + 1) hacer
    resultado = resultado - 10;
    imprimir(j, resultado);
fin_para;
fin"""
ejecutar_analisis_completo(codigo4)

print("\n" + "="*70)
print("CASO 5: SI-ENTONCES (sin SINO)")
print("="*70)
codigo5 = """inicio
entero edad, mayor;
edad = 20;
mayor = 0;
si (edad >= 18) entonces
    mayor = 1;
    imprimir(mayor);
fin_si;
imprimir(edad);
fin"""
ejecutar_analisis_completo(codigo5)

print("\n" + "="*70)
print("CASO 6: SI-ENTONCES-SINO completo")
print("="*70)
codigo6 = """inicio
entero numero, positivo;
numero = -5;
si (numero > 0) entonces
    positivo = 1;
    imprimir(positivo);
sino
    positivo = 0;
    imprimir(positivo);
fin_si;
fin"""
ejecutar_analisis_completo(codigo6)

print("\n" + "="*70)
print("CASO 7: PROGRAMA LARGO - Factorial")
print("="*70)
codigo7 = """inicio
entero n, factorial, i;
n = 5;
factorial = 1;
i = 1;
si (n > 0) entonces
    mientras_que (i <= n) hacer
        factorial = factorial * i;
        imprimir(i, factorial);
        i = i + 1;
    fin_mientras_que;
sino
    factorial = 0;
fin_si;
imprimir(factorial);
fin"""
ejecutar_analisis_completo(codigo7)

print("\n" + "="*70)
print("CASO 8: PROGRAMA LARGO - Suma pares e impares")
print("="*70)
codigo8 = """inicio
entero limite, suma_pares, suma_impares, resto;
limite = 10;
suma_pares = 0;
suma_impares = 0;
para(entero num = 1; num <= limite; num = num + 1) hacer
    resto = num - num / 2 * 2;
    si (resto == 0) entonces
        suma_pares = suma_pares + num;
        imprimir(num, suma_pares);
    sino
        suma_impares = suma_impares + num;
        imprimir(num, suma_impares);
    fin_si;
fin_para;
imprimir(suma_pares, suma_impares);
fin"""
ejecutar_analisis_completo(codigo8)

print("\n" + "="*70)
print("CASO 9: PROGRAMA LARGO - Búsqueda y validación")
print("="*70)
codigo9 = """inicio
entero buscar, encontrado, actual, intentos, max_intentos;
buscar = 7;
encontrado = 0;
actual = 1;
intentos = 0;
max_intentos = 10;
repetir
    si (actual == buscar) entonces
        encontrado = 1;
        imprimir(actual, encontrado);
    sino
        actual = actual + 1;
        intentos = intentos + 1;
    fin_si;
hasta_que (encontrado == 1 o intentos >= max_intentos);
si (encontrado == 1) entonces
    imprimir(actual);
sino
    imprimir(intentos);
fin_si;
fin"""
ejecutar_analisis_completo(codigo9)

print("\n" + "="*70)
print("CASO 10: PROGRAMA LARGO - Sistema de calificaciones")
print("="*70)
codigo10 = """inicio
entero nota1, nota2, nota3, promedio, aprobado, total;
ingresa(nota1);
ingresa(nota2);
ingresa(nota3);
total = nota1 + nota2 + nota3;
promedio = total / 3;
aprobado = 0;
si (promedio >= 60) entonces
    aprobado = 1;
    imprimir(promedio, aprobado);
    si (promedio >= 90) entonces
        imprimir(1);
    sino
        si (promedio >= 70) entonces
            imprimir(2);
        sino
            imprimir(3);
        fin_si;
    fin_si;
sino
    imprimir(promedio, aprobado);
fin_si;
fin"""
ejecutar_analisis_completo(codigo10)

print("\n" + "="*70)
print("CASO 11: Condiciones con operadores lógicos AND")
print("="*70)
codigo11 = """inicio
entero a, b, resultado;
a = 5;
b = 10;
resultado = 0;
si (a > 0 y b > 0) entonces
    resultado = a + b;
    imprimir(resultado);
fin_si;
fin"""
ejecutar_analisis_completo(codigo11)

print("\n" + "="*70)
print("CASO 12: Condiciones con operadores lógicos OR")
print("="*70)
codigo12 = """inicio
entero x, y, valido;
x = -5;
y = 15;
valido = 0;
si (x > 0 o y > 0) entonces
    valido = 1;
    imprimir(valido);
sino
    imprimir(valido);
fin_si;
fin"""
ejecutar_analisis_completo(codigo12)

print("\n" + "="*70)
print("CASO 13: MIENTRAS con condiciones múltiples")
print("="*70)
codigo13 = """inicio
entero a, b;
a = 1;
b = 10;
mientras_que (a < 5 y b > 5) hacer
    imprimir(a, b);
    a = a + 1;
    b = b - 1;
fin_mientras_que;
fin"""
ejecutar_analisis_completo(codigo13)

print("\n" + "="*70)
print("CASO 14: Expresiones aritméticas complejas")
print("="*70)
codigo14 = """inicio
entero a, b, c, d, resultado;
a = 10;
b = 5;
c = 3;
d = 2;
resultado = a + b * c - d / 2 + (a - b) * c;
imprimir(resultado);
fin"""
ejecutar_analisis_completo(codigo14)

print("\n" + "="*70)
print("CASO 15: Operador NOT en condiciones")
print("="*70)
codigo15 = """inicio
entero activo, resultado;
activo = 0;
resultado = 0;
si (no activo == 1) entonces
    resultado = 1;
    imprimir(resultado);
sino
    resultado = 0;
    imprimir(resultado);
fin_si;
fin"""
ejecutar_analisis_completo(codigo15)
