from firebase_debora import firebase_debora
from filtro_bot import filtro_bot
import re

class quiz:

    def analisarPerguntaResposta(self, resposta, nome):
        # Firebase
        firebase = firebase_debora()
        gabarito = firebase.getGabarito()
        bancoRespostas = firebase.getRespostas()
        alunos = firebase.getAlunos()

        # Instanciar a classe de filtro
        filtro = filtro_bot()
        # Quantidade de perguntas
        perguntas = [1,2,3]

        for num in perguntas:
            tipo1 = re.findall(str(num) +'\)', resposta)
            tipo2 = re.findall(str(num) +" ", resposta)
            tipo3 = re.findall(str(num) +"-", resposta)
                
            if tipo1 or tipo2  or tipo3:
                respostaPergunta = filtro.filtraRespostaAluno(resposta, num)
        
                if respostaPergunta == gabarito['cotas'][num].lower():
                    totalAcerto = int(bancoRespostas['pergunta'+ str(num) +'_cotas']['quantAcerto'])
                    totalAcerto = totalAcerto + 1
                    firebase.atualizarRespostas("pergunta"+ str(num) +"_cotas", "quantAcerto", totalAcerto)
                    correcao = "acertou"
                else:
                    totalErro = int(bancoRespostas['pergunta'+ str(num )+ '_cotas']['quantErros'])
                    totalErro = totalErro + 1
                    firebase.atualizarRespostas("pergunta"+ str(num) + "_cotas", "quantErros", totalErro)
                    correcao = "errou"
              
                for key in alunos:
                    if alunos[key]['nome'] == nome:
                        firebase.atualizarSituacaoAluno(key, "pergunta_"+ str(num), correcao)

    def gerarRelatorio(self, nome):
        firebase = firebase_debora()
        alunos = firebase.getAlunos()

        quantRespostaPergunta = ["", 0 , 0, 0]
        quantQuizCompletados = 0
        quantQuizNaoCompletados = 0
        quantPessoas = 0
        mensagemRelatorio = []

        for key in alunos:

            # obter o total de respostas respondidas
            if alunos[key]['pergunta_1'] != 'Não realizado' and alunos[key]['pergunta_2'] != 'Não realizado' and alunos[key]['pergunta_3'] != 'Não realizado':
                quantQuizCompletados = quantQuizCompletados + 1
            else: 
                quantQuizNaoCompletados = quantQuizNaoCompletados + 1

            # obter a quantidade de respostas por questão
            if alunos[key]['pergunta_1'] != 'Não realizado':
                quantRespostaPergunta[1] = quantRespostaPergunta[1] + 1
            if alunos[key]['pergunta_2'] != 'Não realizado':
                quantRespostaPergunta[2] = quantRespostaPergunta[2] + 1
            if alunos[key]['pergunta_3'] != 'Não realizado':
                quantRespostaPergunta[3] = quantRespostaPergunta[3] + 1

            quantPessoas = quantPessoas + 1
                    
        respostas = firebase.getRespostas()
        questoes = [1,2,3]

        # porcentagem de pessoas que concluiram e não concluiram o quiz
        if quantPessoas == 0:
            ConclusaoQuiz = 0
            naoConclusaoQuiz = 0
        else :  
            ConclusaoQuiz = round(float(100 * int(quantQuizCompletados) / int(quantPessoas)),2)
            naoConclusaoQuiz = round(float(100 * int(quantQuizNaoCompletados) / int(quantPessoas)),2)

        mensagemRelatorio.append(nome + ", vamos lá para o resultado final do questionário:")
        mensagemRelatorio.append("A porcentagem de aluno que concluiu o quiz foi de "+ str(ConclusaoQuiz)+"% e as que não concluiu foi de "+ str(naoConclusaoQuiz)+"%")
        
        for numero in questoes:
            
            if quantRespostaPergunta[numero] != 0 :
    
                if respostas["pergunta"+ str(numero)+"_cotas"]['quantAcerto'] != 0:
                    porcetagemAcerto = round(float(100 * int(respostas["pergunta"+ str(numero)+"_cotas"]['quantAcerto']) / int(quantRespostaPergunta[numero])),2)
                else:
                     porcetagemAcerto = 0 

                if respostas["pergunta"+ str(numero)+"_cotas"]['quantErros'] != 0:
                    porcetagemErros = round(float( 100 * int(respostas["pergunta"+ str(numero)+"_cotas"]['quantErros']) / int(quantRespostaPergunta[numero])),2) 
                else:
                    porcetagemErros = 0

                mensagemRelatorio.append("O total de resposta da questão " + str(numero) + " foi de "+ str(quantRespostaPergunta[numero]) + ", onde a porcentagem de acerto é "+ str(porcetagemAcerto) +"% e de erro " + str(porcetagemErros) + "%")
            else :
                mensagemRelatorio.append("A questão "+str(numero)+ " ainda não obteve nenhuma resposta.")
        
        return mensagemRelatorio
    
    def adicionarAluno(self, nome):
        firebase = firebase_debora()
        alunos = firebase.getAlunos()
        
        alunoRegistrado = False
        
        for key in alunos:
            if alunos[key]['nome'] == nome:
                alunoRegistrado = True

        if alunoRegistrado == False:
            dados = {
                'nome': nome,
                'pergunta_1': 'Não realizado',
                'pergunta_2': 'Não realizado',
                'pergunta_3': 'Não realizado'
            }

            firebase.salvarRespostasAluno(dados)
    
    def verificaQuestionarioRespondido(self, nome) :
        firebase = firebase_debora()
        alunos = firebase.getAlunos()
              
        for key in alunos:
            if alunos[key]['nome'] == nome:
                if alunos[key]['pergunta_1'] == "Não realizado":
                   return ['alert',"#pergunta1", nome+", vamos começar do inicio ;-) ? me envie *#topronto*"]
                elif alunos[key]['pergunta_2'] == "Não realizado":
                    return ['alert',"#pergunta2", nome+", vi aqui e você parou na pergunta 2, bora continuar ;-) ? me envie *#pergunta2*"]
                elif alunos[key]['pergunta_3'] == "Não realizado":
                    return ['alert',"#pergunta3", nome+", vi aqui e você parou na pergunta 3, bora continuar ;-) ? me envie *#pergunta3*"]
                else:
                    return ['success', nome+", você já completou o questionario :-) , no momento só posso tirar dúvidas"]

    

    def relatorioAluno(self, nome, totalQuestao):
        firebase = firebase_debora()
        alunos = firebase.getAlunos()

        quantAcerto = 0
        quantErro = 0
        quantidade = 1
        mensagem = []

        for key in alunos:
            if alunos[key]['nome'] == nome:
                while quantidade <= totalQuestao :
                    # obter a quantidade de respostas por questão
                    if alunos[key]['pergunta_'+str(quantidade)] == 'acertou':
                        quantAcerto = quantAcerto + 1
                    if alunos[key]['pergunta_'+str(quantidade)] == 'errou':
                        quantErro = quantErro + 1

                    quantidade = quantidade + 1
   
            if int(quantAcerto) == int(totalQuestao):
                mensagem.append("Parabéns , você acertou " + str(quantAcerto) + " das "+ str(totalQuestao) +" das questões")
            elif int(quantAcerto) == int(totalQuestao) - 1:
                mensagem.append("Você foi bem, acertou " + str(quantAcerto) + " das "+ str(totalQuestao) + " das questões, mas o importante e sempre estudar para conseguir melhorar ainda mais ;-)")
            else:
                mensagem.append("Que pena, você acertou "+ str(quantAcerto) + " das "+ str(totalQuestao) + " das questões, mas sabia que para ter sucesso é falhar repetidamente, mas sem perder o entusiasmo.  ;-)")
            
            return mensagem    

        return False

    