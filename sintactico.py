import sys

import ply.yacc as yacc
from lexer import tokens
from lexer import lexer
# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right','IGUAL'),
    ('left', 'SUMA', 'MENOS'),
    ('left', 'MULTIPLICAR', 'DIVISION'),
    ('right','WHERE','FILTER'),
    #('right','filter')
    #('right', 'UMINUS'),
)
nombres = {}

#def p_filter(t):
#    '''
#    expresion  : FILTER PARENTESISIZ MENOSQUE expresion PARENTESISDE
#                | FILTER PARENTESISIZ MAYOROIGUAL expresion PARENTESISDE
#    '''
#    t[0] = t[2]

def p_declaracion_asignar(t):
    'declaracion : ID IGUAL expresion PUNTOYCOMA'
    nombres[t[1]] = t[3]

def p_declaracion_expr(t):
    'declaracion : expresion'
    # print("Resultado: " + str(t[1]))
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion  :   expresion SUMA expresion
                |   expresion MENOS expresion
                |   expresion MULTIPLICAR expresion
                |   expresion DIVISION expresion

                |   expresion MOD expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]

#def p_expresion_uminus(t):
#    'expresion : RESTA expresion %prec UMINUS'
#    t[0] = -t[2]

def p_expresion_grupo(t):
    '''
    expresion  : PARENTESISIZ expresion PARENTESISDE
                | LBLOCK expresion RBLOCK
                | CORCHETEIZ expresion CORCHETEDE
    '''
    t[0] = t[2]
# sintactico de expresiones logicas
def p_expresion_logicas(t):
    '''
    expresion   :  expresion MENOSQUE expresion
                |  expresion MAYORQUE expresion
                |  expresion MENOSOIGUAL expresion
                |   expresion MAYOROIGUAL expresion
                |   expresion IGUAL expresion

                |  PARENTESISIZ expresion PARENTESISDE MENOSQUE PARENTESISIZ expresion PARENTESISDE
                |  PARENTESISIZ expresion PARENTESISDE MAYORQUE PARENTESISIZ expresion PARENTESISDE
                |  PARENTESISIZ expresion PARENTESISDE MENOSOIGUAL PARENTESISIZ expresion PARENTESISDE
                |  PARENTESISIZ  expresion PARENTESISDE MAYOROIGUAL PARENTESISIZ expresion PARENTESISDE
                |  PARENTESISIZ  expresion PARENTESISDE IGUAL PARENTESISIZ expresion PARENTESISDE

    '''
    if t[2] == "<": t[0] = t[1] < t[3]
    elif t[2] == ">": t[0] = t[1] > t[3]
    elif t[2] == "<=": t[0] = t[1] <= t[3]
    elif t[2] == ">=": t[0] = t[1] >= t[3]
    elif t[2] == "=": t[0] = t[1] is t[3]

    elif t[3] == "<":
        t[0] = t[2] < t[4]
    elif t[2] == ">":
        t[0] = t[2] > t[4]
    elif t[3] == "<=":
        t[0] = t[2] <= t[4]
    elif t[3] == ">=":
        t[0] = t[2] >= t[4]
    elif t[3] == "=":
        t[0] = t[2] is t[4]


    # print('logica ',[x for x in t])

# gramatica de expresiones booleanadas
#def p_expresion_booleana(t):
#    '''
#    expresion   :   expresion AND expresion
#                |   expresion OR expresion
#                |   expresion NOT expresion
#                |  PARIZQ expresion AND expresion PARDER
#                |  PARIZQ expresion OR expresion PARDER
#                |  PARIZQ expresion NOT expresion PARDER
#    '''
#    if t[2] == "&&":
#        t[0] = t[1] and t[3]
#    elif t[2] == "||":
#        t[0] = t[1] or t[3]
#    elif t[2] == "!":
#        t[0] =  t[1] is not t[3]
#        t[0] = t[2] and t[4]
#    elif t[3] == "||":
#        t[0] = t[2] or t[4]
#    elif t[3] == "!":
#        t[0] =  t[2] is not t[4]

def p_filter(t):
    'expresion : FILTER PARENTESISIZ MENOSQUE expresion PARENTESISDE'
    t[0] = t[1]

def p_where(t):
    'expresion : WHERE expresion'
    t[0] = t[1]
def p_expresion_numero(t):
    'expresion : NUMBER'
    t[0] = t[1]

def p_expresion_cadena(t):
    'expresion : COMILLASDOBLES expresion COMILLASDOBLES'
    t[0] = t[2]
def p_cadenavacia(t):
    'expresion : CADENAVACIA IGUAL CADENAVACIA'
    t[0] = t[1]
def p_comentariosenlinea(t):
    'expresion : COMENTARIOSENLINEA'
    t[0] = t[1]
def p_comentarioenlineas(t):
    'expresion : COMENTARIOENLINEAS'
    t[0] = t[1]

def p_variable(t):
    'expresion : VARIABLE'
    t[0] = t[1]
def p_cons(t):
    'expresion : CONS'
    t[0] = t[1]

def p_expresion_ID(t):
    'expresion : ID'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print("Nombre desconocido ", t[1])
        t[0] = 0

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {} en el valor {}".format( str(t.type),str(t.value))
        print(resultado)
    else:
        resultado = "Error sintactico {}".format(t)
        print(resultado)
    resultado_gramatica.append(resultado)



parser = yacc.yacc()


def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()

    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else: print("data vacia")

    #print("result: ", resultado_gramatica)
    return resultado_gramatica


'''try:
    file_name = 'qsort.hs'
    archivo = open(file_name, "r")
except:
    print("No hay archivo con ese archivo")
    quit()

text = ""
for linea in archivo:
    text += linea
prueba_sintactica(text)
print('-----ERRORES----')
print('\n'.join(list(map(''.join,resultado_gramatica))))'''
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        fin = 'qsort.hs'
    else:
        fin = sys.argv[1]
    f = open(fin, 'r')
    data = f.read()
    # print (data)
    # lexer.input(data)
    prueba_sintactica(data)
print('------ERRORES----')
print('\n'.join(list(map(''.join,resultado_gramatica))))