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

misc = ['\n', ' ', '(', ')']

fullList = alphabet + numbers + misc

#
# STATES
#

statesInit = ['q0']

statesINT = ['q_INT_1',
             'q_INT_2',
             'q_INT_3'
             ]

statesID = ['q_ID_1',
             'q_ID_2'
             ]

statesLPAREN = ['q_ID_1',
             'q_ID_2'
             ]

states = statesInit + statesINT + statesID + statesLPAREN

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

transitionsID = {
    'q0': {
        
    },
    'q_ID_1': {
        
    },
    'q_ID_2': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

# Adicionar conexões de q0 para q_ID_1 com todas as letras do alfabeto menos as letras i
transitionsID['q0'].update({letter: 'q_ID_1' for letter in alphabet if letter not in ['i']})

# Adicionar conexões de q_ID_1 para q_ID_2 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ID_1'].update({letter: 'q_ID_2' for letter in alphabet})
transitionsID['q_ID_1'].update({letter: 'q_ID_2' for letter in numbers})

# Adicionar conexões de q_ID_2 para q_ID_2 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ID_2'].update({letter: 'q_ID_2' for letter in alphabet})
transitionsID['q_ID_2'].update({number: 'q_ID_2' for number in numbers})

transitions = combine_transitions(transitionsInit, transitionsINT, transitionsID)

#
# TOKENS
#

tokens = ['INT',
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

outputsID = {
                'q_ID_1' : 'ID',
                'q_ID_2' : ''
                }

outputs = outputsInit.copy()
outputs.update(outputsINT)
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