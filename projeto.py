from string import ascii_letters
import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'



def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):#adicionar tarefa
    if descricao  == '' :
        return False
    novaAtividade=[]

    if dataValida(extras[0]):
        novaAtividade.append(extras[0]+' ')

    if horaValida(extras[1]):
        novaAtividade.append(extras[1]+' ')
    desc=''

    for x in descricao:#verificando funções
        desc += x
    novaAtividade.append(desc+' ')

    if prioridadeValida(extras[2]):
        novaAtividade.append(extras[2]+' ')
        
    if contextoValido(extras[3]):
        novaAtividade.append(extras[3]+ ' ')

    if projetoValido(extras[4]):
       novaAtividade.append(extras[4]+ ' ')
    string=''  
    for x in novaAtividade:
      if x != '':
          string += x




  # Escreve no TODO_FILE. 
    try: 
        fp = open(TODO_FILE, 'a')
        fp.write(string + "\n")
        fp.close()
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False

    return True


# Valida a prioridade.
def prioridadeValida(pri):

  if len(pri) == 3 and pri[0]=='(' and pri[2]==')' and pri[1] in ascii_letters :
      return True
  
  return False

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin):
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  elif ((horaMin[:2] >= '0') and (horaMin[:2] <= '23')) and ((horaMin[2:4] >= '0') and (horaMin[2:4] <= '59')):
    return True
  else:
    return False
  
##se os dois primeiros formam um número entre 00 e 23 e
##se os dois últimos formam um número inteiro entre 00 e 59

  
# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto.



def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):#separando data de acordo com o tamanho.
    return False
  dia=data[:2];  mes=data[2:4];  ano=data[4:]
  trintaDias=['04','06','09','11']
  if not ano >= '2017':
    return False   
  if mes in trintaDias:#numero de dias de acordo com o mes.
    if(dia >= '01') and (dia <= '30'):
        return True
  elif mes == '02':
    if(dia >= '01') and (dia <= '29'):
        return True
  elif (dia >= '01') and (dia <= '31'):
        return True
  else:
      return False

    

  return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) > 1 and proj[0]=='+':
    return True

  return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont) > 1 and cont[0]=='@':
      return True

  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
    itens=[]
    for l in linhas:
        l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
        tokens = l.split()
        prioridade = ''
        desc = ''
        data = ''
        hora = ''
        intens = ''
        contexto = ''
        projeto = ''
        for x in tokens:#verificando se as funções estão validas.    
            if dataValida(x):
                data = x
                tokens[tokens.index(x)]=''
            if horaValida(x):
                hora = x
                tokens[tokens.index(x)]=''
            if prioridadeValida(x):
                prioridade = x
                tokens[tokens.index(x)]=''
            if contextoValido(x):
                contexto = x
                tokens[tokens.index(x)]=''
            if projetoValido(x):
                projeto = x
                tokens[tokens.index(x)]=''
        for x in tokens:
            if x!='':
                desc+=x+' '
        desc=desc[:-1]
        itens.append((desc, (data, hora, prioridade, contexto, projeto)))
    return itens
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 
  
    


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
    fp = open(TODO_FILE, 'r')
    linhas = fp.readlines()
    fp.close()
    
    itens = ordenarPorPrioridade(ordenarPorDataHora(organizar(linhas)))
    fp = open(TODO_FILE, 'w')
    for x in itens:
      adicionar(x[0],x[1])
    fp.close()
    
    organizadoSemP = []
    organizadoComP = []
    cont=1
    for x in itens:#listando data da meneira padrão.ex:22/08/1995.
      string = str(cont)+' '
      if x[1][0] != '':
        string += x[1][0][:2]+'/'+x[1][0][2:4]+'/'+x[1][0][4:8]+' '
      if x[1][1] != '':
        string += x[1][1][:2]+'h'+x[1][1][2:]+'m'+ ' '
      if x[1][2] != '':
        string += x[1][2]+ ' '
        if x[1][2] != '' and x[1][2][1] == 'A':#verificando prioridade.
          string = "-A" + string
        elif x[1][2] != '' and x[1][2][1] == 'B':
          string = "-B" + string
        elif x[1][2] != '' and x[1][2][1] == 'C':
          string = "-C" + string
        elif x[1][2] != '' and x[1][2][1] == 'D':
          string = "-D" + string
      string += x[0]+' '
      if x[1][3] != '':
        string += x[1][3]+' '
      if x[1][4] != '':
        string += x[1][4]+' '
      if string[0] == '-':
          organizadoComP.append(string)       
      else:
          
          organizadoSemP.append(string)
      cont += 1
    
    for x in organizadoComP:#adicionando cor para  cada prioridade.
      
      if x[1] == 'A':
          printCores(x[2:], RED)
      elif x[1] == 'B':
          printCores(x[2:], YELLOW)
      elif x[1] == 'C':
          printCores(x[2:], GREEN)
      elif x[1] == 'D':
          printCores(x[2:], CYAN)

    for x in organizadoSemP:
      printCores(x, BLUE)

    
def ordenarPorDataHora(itens):
    dataHora = []
    semdataHora = []
    
    def ehMaior(data1,data2):#ordenando por data olahndo posição dos numeros.
        primeiro=''
        segundo=''
        if len(data1)==8:
        	primeiro= data1[4:8] + data1[2:4] +data1[:2]
        elif len(data1)==12:
        	primeiro= data1[4:8] + data1[2:4] + data1[:2] +data1[8:]
        if len(data2)==8:
        	segundo= data2[4:8] + data2[2:4] +data2[:2]
        elif len(data2)==12:
        	segundo= data2[4:8] + data2[2:4] +data2[:2]
        return primeiro>segundo
    
    for datas in itens:
        if datas[1][0] != '' or datas[1][1] != '':
            dataHora.append(datas)
        else:
            semdataHora.append(datas)

    def bubbleSort(ordenar):
        for i in range(len(ordenar)-1):
            for j in range(len(ordenar) -1 - i):
                x = ordenar[j][1][0]+ordenar[j][1][1]
                y = ordenar[j+1][1][0]+ordenar[j+1][1][1]
                if ehMaior(x,y):
                    ordenar[j], ordenar[j+1]= ordenar[j+1],ordenar[j]
        return ordenar
    itens = bubbleSort(dataHora)+semdataHora
  	
    
    return itens



   
def ordenarPorPrioridade(itens):
    ordenar = []
    nordenar = []
    
    for prioridade in itens:
         if prioridade[1][2] != '':
             ordenar.append(prioridade)
         else:
             nordenar.append(prioridade)


    def bubbleSort(ordenar):
        for i in range(len(ordenar)-1):
            for j in range(len(ordenar) -1 - i):
                if ordenar[j][1][2] >  ordenar[j+1][1][2]:
                    ordenar[j], ordenar[j+1]= ordenar[j+1],ordenar[j]
        return ordenar
    
    listaordenada = bubbleSort(ordenar)+ nordenar
    return listaordenada

def fazer(num):#tarefas que ja foram feitas.
    num=num-1
    arq = open('todo.txt','r')
    linhas = arq.readlines()
    arq.close()
    feito = linhas.pop(num)

    arq=open('todo.txt','w')
    arq.writelines(linhas)
    arq.close()

    arq=open('done.txt','a')#fechar para não  ocupar espaço na memoria.
    arq.writelines(feito)
    arq.close()
    return 

def remover(num):
    num=num-1
    arq=open('todo.txt','r')
    linhas=arq.readlines()
    arq.close()
    if int(num)>len(linhas)-1:
        return 'Numero Inválido'
    linhas.remove(linhas[num])
    arq=open('todo.txt','w')
    arq.writelines(linhas)
    arq.close()
    return 

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
    num = num-1

    arq = open('todo.txt','r')
    linhas = arq.readlines()
    arq.close()
    organizadas = organizar([linhas[num]])
    desc = organizadas[0][0]

    v = [x for x in organizadas[0][1]]
    v[2] = '('+prioridade+')'
    
    organizadas = (desc,(v[0],v[1],v[2],v[3],v[4]))
    remover(num+1)
    adicionar(organizadas[0],organizadas[1])
    
    return 


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :#organixar programa,comandos para o programa.
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    
    
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:

    listar()
    return    
    

  elif comandos[1] == REMOVER:#remover de acordo com as posições.
    remover(int(comandos[2]))
    return    
      

  elif comandos[1] == FAZER:
    fazer(int(comandos[2]))
    return

    

  elif comandos[1] == PRIORIZAR: 
    comandos.pop(0)
    comandos.pop(0)

    priorizar(int(comandos[0]),comandos[1])
    



  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
