from automata.fa.Moore import Moore
import sys, os
import string
from collections import defaultdict

from myerror import MyError

error_handler = MyError('LexerErrors')

global check_cm
global check_key

#
# ALPHABET
#

alphabet = list(string.ascii_lowercase + string.ascii_uppercase)

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

misc = ['\n', ' ', '(', ')', '{', '}', ';']

fullList = alphabet + numbers + misc

#
# STATES
#

statesInit = ['q0']

statesINT = ['q_INT_1',
             'q_INT_2',
             'q_INT_3'
             ]

statesFLOAT = ['q_FLOAT_1',
             'q_FLOAT_2',
             'q_FLOAT_3',
             'q_FLOAT_4',
             'q_FLOAT_5'
             ]

statesVOID = ['q_VOID_1',
             'q_VOID_2',
             'q_VOID_3'
             'q_VOID_4'
             ]

statesLPAREN = ['q_LPAREN'
             ]

statesRPAREN = ['q_RPAREN'
             ]

statesLBRACES= ['q_LBRACES'
             ]

statesRBRACES= ['q_RBRACES'
             ]

statesSEMICOLON= ['q_SEMICOLON'
             ]

statesNUMBER = ['q_NUMBER_1',
             'q_NUMBER_2'
             ]

statesID = ['q_ID_1',
             'q_ID_2'
             ]

states = statesInit
states += statesINT
states += statesFLOAT
states += statesLPAREN
states += statesRPAREN
states += statesLBRACES
states += statesRBRACES
states += statesSEMICOLON
states += statesVOID
states += statesNUMBER
states += statesID

#
# TRANSTIONS
#

# Função para combinar as transições
def combine_transitions(*transition_dicts):
    # Criar um defaultdict para lidar com a combinação sem sobrescrever as transições
    combined = defaultdict(dict)

    for transition_dict in transition_dicts:
        for state, transitions in transition_dict.items():
            for symbol, next_state in transitions.items():
                # Se a transição já existir, não sobrescreve
                if symbol not in combined[state]:
                    combined[state][symbol] = next_state

    return dict(combined)

transitionsInit = {
    'q0': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsINT = {
    'q0': {
        'i': 'q_INT_1',
    },
    'q_INT_1': {
        'n': 'q_INT_2',
    },
    'q_INT_2': {
        't': 'q_INT_3',
    },
    'q_INT_3': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsFLOAT = {
    'q0': {
        'f': 'q_FLOAT_1',
    },
    'q_FLOAT_1': {
        'l': 'q_FLOAT_2',
    },
    'q_FLOAT_2': {
        'o': 'q_FLOAT_3',
    },
    'q_FLOAT_3': {
        'a': 'q_FLOAT_4',
    },
    'q_FLOAT_4': {
        't': 'q_FLOAT_5',
    },
    'q_FLOAT_5': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsVOID = {
    'q0': {
        'v': 'q_VOID_1',
    },
    'q_VOID_1': {
        'o': 'q_VOID_2',
    },
    'q_VOID_2': {
        'i': 'q_VOID_3',
    },
    'q_VOID_3': {
        'd': 'q_VOID_4',
    },
    'q_VOID_4': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsLPAREN = {
    'q0': {
        '(': 'q_LPAREN',
    },
    'q_LPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        ')' : 'q_RPAREN',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
    },
    'q_INT_3': {
        '(': 'q_LPAREN',
    },
    'q_FLOAT_5': {
        '(': 'q_LPAREN',
    },
    'q_VOID_4': {
        ')': 'q_RPAREN',
    },
    'q_NUMBER_1': {
        '(': 'q_LPAREN',
    },
    'q_NUMBER_2': {
        '(': 'q_LPAREN',
    },
    'q_ID_1': {
        '(': 'q_LPAREN',
    },
    'q_ID_2': {
        '(': 'q_LPAREN',
    }
}

# Adicionar conexões de q_LPAREN para q_ID_1 com todas as letras do alfabeto
transitionsLPAREN['q_LPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_LPAREN para q_NUMBER_1 com todos os numeros
transitionsLPAREN['q_LPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_LPAREN para 'i': 'q_INT_1'
transitionsLPAREN['q_LPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_LPAREN para 'f': 'q_FLOAT_1'
transitionsLPAREN['q_LPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_LPAREN para 'v': 'q_VOID_1'
transitionsLPAREN['q_LPAREN'].update({'v': 'q_VOID_1'})

transitionsRPAREN = {
    'q0': {
        ')': 'q_RPAREN',
    },
    'q_RPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
    },
    'q_INT_3': {
        ')': 'q_RPAREN',
    },
    'q_FLOAT_5': {
        ')': 'q_RPAREN',
    },
    'q_VOID_4': {
        ')': 'q_RPAREN',
    },
    'q_NUMBER_1': {
        ')': 'q_RPAREN',
    },
    'q_NUMBER_2': {
        ')': 'q_RPAREN',
    },
    'q_ID_1': {
        ')': 'q_RPAREN',
    },
    'q_ID_2': {
        ')': 'q_RPAREN',
    }
}

# Adicionar conexões de q_RPAREN para q_ID_1 com todas as letras do alfabeto
transitionsRPAREN['q_RPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_RPAREN para q_NUMBER_1 com todos os numeros
transitionsRPAREN['q_RPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_RPAREN para 'i': 'q_INT_1'
transitionsRPAREN['q_RPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_RPAREN para 'f': 'q_FLOAT_1'
transitionsRPAREN['q_RPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_RPAREN para 'v': 'q_VOID_1'
transitionsRPAREN['q_RPAREN'].update({'v': 'q_VOID_1'})

transitionsLBRACES = {
    'q0': {
        '{': 'q_LBRACES',
    },
    'q_LBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsRBRACES = {
    'q0': {
        '}': 'q_RBRACES',
    },
    'q_RBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsSEMICOLON = {
    'q0': {
        ';': 'q_SEMICOLON',
    },
    'q_SEMICOLON': {
        '\n': 'q0',
        ' ' : 'q0',
    },
    'q_INT_3': {
        ';': 'q_SEMICOLON',
    },
    'q_FLOAT_5': {
        ';': 'q_SEMICOLON',
    },
    'q_VOID_4': {
        ';': 'q_SEMICOLON',
    },
    'q_NUMBER_1': {
        ';': 'q_SEMICOLON',
    },
    'q_ID_1': {
        ';': 'q_SEMICOLON',
    },
    'q_NUMBER_2': {
        ';': 'q_SEMICOLON',
    },
    'q_ID_2': {
        ';': 'q_SEMICOLON',
    }
}

transitionsNUMBER = {
    'q0': {
        
    },
    'q_NUMBER_1': {
        
    },
    'q_NUMBER_2': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

# Adicionar conexões de q0 para q_NUMBER_1 com todos os numeros
transitionsNUMBER['q0'].update({number: 'q_NUMBER_1' for number in numbers})

# Adicionar conexões de q_NUMBER_1 para q_NUMBER_2 com todos os numeros
transitionsNUMBER['q_NUMBER_1'].update({number: 'q_NUMBER_2' for number in numbers})

# Adicionar conexões de q_NUMBER_2 para q_NUMBER_2 com todos os numeros
transitionsNUMBER['q_NUMBER_2'].update({number: 'q_NUMBER_2' for number in numbers})

transitionsID = {
    'q0': {
        
    },
    'q_ID_1': {
        '\n': 'q0',
        ' ' : 'q0',
    },
    'q_ID_2': {
        '\n': 'q0',
        ' ' : 'q0',
    },
    'q_INT_1': {
        
    },
    'q_INT_2': {
        
    },
    'q_INT_3': {
        
    },
    'q_FLOAT_1': {
        
    },
    'q_FLOAT_2': {
        
    },
    'q_FLOAT_3': {
        
    },
    'q_FLOAT_4': {
        
    },
    'q_FLOAT_5': {
        
    },
    'q_VOID_1': {
        
    },
    'q_VOID_2': {
        
    },
    'q_VOID_3': {
        
    },
    'q_VOID_4': {
        
    }
}

# Adicionar conexões de q0 para q_ID_1 com todas as letras do alfabeto
transitionsID['q0'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_1 para q_ID_2 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ID_1'].update({letter: 'q_ID_2' for letter in alphabet})
transitionsID['q_ID_1'].update({number: 'q_ID_2' for number in numbers})

# Adicionar conexões de q_ID_2 para q_ID_2 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ID_2'].update({letter: 'q_ID_2' for letter in alphabet})
transitionsID['q_ID_2'].update({number: 'q_ID_2' for number in numbers})

"""
Busca de ID em meio a busca INT
"""

# Adicionar conexões de q_INT_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_INT_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_INT_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_INT_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_INT_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_INT_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_INT_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_INT_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_INT_3'].update({number: 'q_ID_1' for number in numbers})

"""
Busca de ID em meio a busca FLOAT
"""

# Adicionar conexões de q_FLOAT_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_3'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_4 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_4'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_4'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_5 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_5'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_5'].update({number: 'q_ID_1' for number in numbers})

"""
Busca de ID em meio a busca VOID
"""

# Adicionar conexões de q_VOID_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_VOID_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_VOID_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_3'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_VOID_4 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_4'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_4'].update({number: 'q_ID_1' for number in numbers})

transitions = combine_transitions(
    transitionsInit,
    transitionsINT,
    transitionsFLOAT,
    transitionsVOID,
    transitionsLPAREN, 
    transitionsRPAREN,
    transitionsLBRACES,
    transitionsRBRACES,
    transitionsSEMICOLON,
    transitionsNUMBER,
    transitionsID
    )

#print(transitions)

#
# TOKENS
#

tokens = ['INT',
          'FLOAT',
          'VOID',
          'LPAREN',
          'RPAREN',
          'LBRACES',
          'RBRACES',
          'SEMICOLON',
          'NUMBER',
          'ID'
          ]

#
# OUTPUTS
#

outputsInit = {
                'q0' : ''
                }

outputsINT = {
                'q_INT_1' : '',
                'q_INT_2' : '',
                'q_INT_3' : 'INT\n'
                }

outputsFLOAT = {
                'q_FLOAT_1' : '',
                'q_FLOAT_2' : '',
                'q_FLOAT_3' : '',
                'q_FLOAT_4' : '',
                'q_FLOAT_5' : 'FLOAT\n'
                }

outputsVOID = {
                'q_VOID_1' : '',
                'q_VOID_2' : '',
                'q_VOID_3' : '',
                'q_VOID_4' : 'VOID\n'
                }

outputsLPAREN = {
                'q_LPAREN' : 'LPAREN\n'
                }

outputsRPAREN = {
                'q_RPAREN' : 'RPAREN\n'
                }

outputsLBRACES = {
                'q_LBRACES' : 'LBRACES\n'
                }

outputsRBRACES = {
                'q_RBRACES' : 'RBRACES\n'
                }

outputsSEMICOLON = {
                'q_SEMICOLON' : 'SEMICOLON\n'
                }

outputsNUMBER = {
                'q_NUMBER_1' : 'NUMBER\n',
                'q_NUMBER_2' : ''
                }

outputsID = {
                'q_ID_1' : 'ID\n',
                'q_ID_2' : ''
                }

outputs = outputsInit.copy()
outputs.update(outputsINT)
outputs.update(outputsFLOAT)
outputs.update(outputsVOID)
outputs.update(outputsLPAREN)
outputs.update(outputsRPAREN)
outputs.update(outputsLBRACES)
outputs.update(outputsRBRACES)
outputs.update(outputsSEMICOLON)
outputs.update(outputsNUMBER)
outputs.update(outputsID)

#
# MOORE MACHINE
#

moore = Moore(states,
              fullList,
              tokens,
              transitions,
              'q0',
              outputs
              )

def main():
    check_cm = False
    check_key = False
    
    for idx, arg in enumerate(sys.argv):
        # print("Argument #{} is {}".format(idx, arg))
        aux = arg.split('.')
        if aux[-1] == 'cm':
            check_cm = True
            idx_cm = idx

        if(arg == "-k"):
            check_key = True
    
    # print ("No. of arguments passed is ", len(sys.argv))

    if(len(sys.argv) < 3):
        raise TypeError(error_handler.newError(check_key, 'ERR-LEX-USE'))

    if not check_cm:
      raise IOError(error_handler.newError(check_key, 'ERR-LEX-NOT-CM'))
    elif not os.path.exists(sys.argv[idx_cm]):
        raise IOError(error_handler.newError(check_key, 'ERR-LEX-FILE-NOT-EXISTS'))
    else:
        data = open(sys.argv[idx_cm])
        source_file = data.read()

        if not check_cm:
            print("Definição da Máquina")
            print(moore)
            print("Entrada:")
            print(source_file)
            print("Lista de Tokens:")
        
        #print(moore)

        print(moore.get_output_from_string(source_file).rstrip('\n'))


if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        print(e)
    except (ValueError, TypeError):
        print(e)