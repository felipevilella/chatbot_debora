from selenium import webdriver
from random import randrange
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from firebase_debora import firebase_debora
from filtro_bot import filtro_bot
import time, re

class WhatsappBot:
    def __init__(self):
        options =  webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', chrome_options=options)
        self.driver.get('https://web.whatsapp.com')
        time.sleep(15)

    def pesquisarNome(self, nome):
        novaConversa = self.driver.find_elements_by_xpath('//div[@class="PVMjB"]')
        novaConversa[1].click()
        participante = self.driver.find_element_by_class_name('_3FRCZ')
        participante.send_keys(nome)
        time.sleep(2)
        user = self.driver.find_element_by_xpath('//span[@title="{}"]'.format(nome))
        user.click()
    
    def enviarMensagem(self, mensagem):  
        mensage_caixa = self.driver.find_element_by_xpath('//div[@class="_3uMse"]')
        mensage_caixa.send_keys(mensagem)

        time.sleep(4)
        try:
            enviar = self.driver.find_element_by_xpath('//button[@class="_1U1xa"]')
            enviar.click()
        except NoSuchElementException:
            pass

    def enviarGif(self, nomeGif) :
        abaconteudos = self.driver.find_elements_by_xpath('//div[@class="weEq5"]')
        abaconteudos[0].click()
        time.sleep(1)

        abaGif = self.driver.find_element_by_class_name('_1oRJg')
        abaGif.click()
        time.sleep(2)

        campo_pesquisa = self.driver.find_element_by_class_name('_2U5s1')
        campo_pesquisa.send_keys(nomeGif)
        time.sleep(2)
        
        abaGif = self.driver.find_elements_by_xpath('//div[@class="zl5TR"]')
        abaGif[randrange(1, 4)].click()
        time.sleep(8)

        enviar = self.driver.find_element_by_xpath('//div[@class="_3nfoJ"]')
        enviar.click()
    
    def obterUltimaMensagem(self):
        # Conteudo mensagem 
        mensagens = self.driver.find_elements_by_class_name("_274yw")
        ultimaMensagem = len(mensagens) - 1

        if mensagens:
            try:
                mensagem = mensagens[ultimaMensagem].find_element_by_css_selector('span.selectable-text').text
                # Rementente
                Rementente_mensagem = self.driver.find_elements_by_xpath('//div[@class="copyable-text"]')
                ultimoRemetente = len(Rementente_mensagem) -1 
                rementente = Rementente_mensagem[ultimoRemetente].get_attribute('data-pre-plain-text')
                nome = re.findall(r"[a-zA-Z]", rementente)
                return ['success', nome, mensagem] 
            except NoSuchElementException:
                return ['alert', '', 'Infelizmente ainda não consigo entender o tipo de mensagem que você me enviou.']

    def abrirAba(self):
        self.driver.execute_script("window.open('https://accounts.google.com/signin/oauth/oauthchooseaccount?state=%7B%22csrf_token%22%3A%20%22628b041b6c99b29d0846867ba5626ce3863a25ae29c72b1c7a3c5a38ac478506%22%2C%20%22return_url%22%3A%20%22https%3A%2F%2Fdialogflow.com%2F%22%7D&redirect_uri=https%3A%2F%2Fdialogflow.com%2Foauth2callback&prompt=select_account&response_type=code&client_id=157101835696-ooapojlodmuabs2do2vuhhnf90bccmoi.apps.googleusercontent.com&scope=openid%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgoogledevelopers%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&access_type=online&o2v=2&as=GtbyJPnOlpf5qDIzhPFf8Q&flowName=GeneralOAuthFlow', '_blank')")
        self.driver.switch_to_window(self.driver.window_handles[1])

    def loginDialogFlow(self):
        email = self.driver.find_element_by_id("identifierId")
        email.send_keys("chatbotdebora@gmail.com")
        botaoLogin = self.driver.find_element_by_id("identifierNext")
        botaoLogin.click()

        time.sleep(10)

        senha = self.driver.find_element_by_name("password")
        senha.send_keys("caneta!1")
        botaoSenha = self.driver.find_element_by_id("passwordNext")
        botaoSenha.click()
        time.sleep(10)
        self.driver.get("https://dialogflow.cloud.google.com/")
    
    def digitarMensagemDialogFlow(self, mensagem):
        campoMensagem = self.driver.find_element_by_id("test-client-query-input")
        campoMensagem.send_keys(mensagem)
        campoMensagem.send_keys(Keys.ENTER)
    
    def obterRespostaDialogFlow(self):
        respostas = self.driver.find_elements_by_xpath('//span[@class="ng-binding"]')
        respostaDialogFlow = []
        contador = 0

        for resposta in respostas:
            if resposta.text == "input.welcome":
                break
            if resposta.text == "Intents":
                break
            if resposta.text == "input.unknown":
                break
            if contador > 1 :
                respostaDialogFlow.append(resposta.text)
            
            contador = contador + 1
        return respostaDialogFlow

    def mudarAbaWhatssap(self):
        self.driver.switch_to_window(self.driver.window_handles[0])
    
    def mudarAbaDialogFlow(self):
        self.driver.switch_to_window(self.driver.window_handles[1])
        try:
            entrarDialogFlow = self.driver.find_element_by_class_name("md-btn-login-text-wrapper")
            entrarDialogFlow.click()
            time.sleep(2)
        except NoSuchElementException:
            pass
    
    def analisarPerguntaResposta(self, resposta, nome):
        # Firebase
        firebase = firebase_debora()
        gabarito = firebase.getGabarito()
        bancoRespostas = firebase.getRespostas()
        alunos = firebase.getAlunos()

        # Instanciar a classe de filtro
        filtro = filtro_bot()

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
        mensagemRelatorio = []

        for key in alunos:
            if alunos[key]['pergunta_1'] != 'Não realizado':
                quantRespostaPergunta[1] = quantRespostaPergunta[1] + 1
            if alunos[key]['pergunta_2'] != 'Não realizado':
                quantRespostaPergunta[2] = quantRespostaPergunta[2] + 1
            if alunos[key]['pergunta_3'] != 'Não realizado':
                quantRespostaPergunta[3] = quantRespostaPergunta[3] + 1

        respostas = firebase.getRespostas()
        questoes = [1,2,3]

        mensagemRelatorio.append(nome + ", vamos lá para o resultado final do questionário:")

        for numero in questoes:
            
            if quantRespostaPergunta[numero] != 0 :
    
                if respostas["pergunta"+ str(numero)+"_cotas"]['quantAcerto'] != 0:
                    porcetagemAcerto = float(int(quantRespostaPergunta[numero]) / int(respostas["pergunta"+ str(numero)+"_cotas"]['quantAcerto'])* 100)
                else:
                     porcetagemAcerto = 0 

                if respostas["pergunta"+ str(numero)+"_cotas"]['quantErros'] != 0:
                    porcetagemErros = float(int(quantRespostaPergunta[numero]) / int(respostas["pergunta"+ str(numero)+"_cotas"]['quantErros'])* 100) 
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
                   return ['alert',"#pergunta1", aluno+", vamos começar do inicio ;-) ? me envie *#topronto*"]
                elif alunos[key]['pergunta_2'] == "Não realizado":
                    return ['alert',"#pergunta2", aluno+", vi aqui e você parou na pergunta 2, bora continuar ;-) ? me envie *#pergunta2*"]
                elif alunos[key]['pergunta_3'] == "Não realizado":
                    return ['alert',"#pergunta3", aluno+", vi aqui e você parou na pergunta 3, bora continuar ;-) ? me envie *#pergunta3*"]
                else:
                    return ['success', nome+", você já completou o questionario :-) , no momento só posso tirar dúvidas"]


if __name__ == "__main__":
    # ABRIR WhatsApp 
    WhatsappBot = WhatsappBot()
    time.sleep(10)
    alunos = ["Wesley"]
     
    #Abrir dialogFlow
    WhatsappBot.abrirAba()
    WhatsappBot.loginDialogFlow()
    time.sleep(10)

    WhatsappBot.mudarAbaWhatssap()
    time.sleep(3)
    
    while True:

        for aluno in alunos:
            WhatsappBot.pesquisarNome(aluno)
            time.sleep(3)

            # Formatar nome aluno em array
            nomeAluno = re.findall(r"[a-zA-Z]", aluno)
            destinatario = True

            mensagem = WhatsappBot.obterUltimaMensagem()
            if mensagem:
                for letra in nomeAluno :
                    if(letra not in mensagem[1]) :
                        destinatario = False

                if(destinatario):
                    
                    if mensagem[0] == 'success':
                        mensagem[2] = mensagem[2].lower()
                        
                        # Verificar se o aluno respondeu todas as questões
                        liberarConversa = True                    
                        if mensagem[2] == "#topronto" or mensagem[2] == "#pergunta2" or mensagem[2] == "#pergunta3":
                            
                            WhatsappBot.adicionarAluno(aluno)
                            questionario = WhatsappBot.verificaQuestionarioRespondido(aluno)

                            if questionario[0] == "alert":
                                if questionario[1] == "#pergunta1" and "#topronto" != mensagem[2]:
                                    WhatsappBot.enviarMensagem(questionario[2]) 
                                    liberarConversa = False
                                
                                if questionario[1] == "#pergunta2" and questionario[1] != mensagem[2]:
                                    WhatsappBot.enviarMensagem(questionario[2]) 
                                    liberarConversa = False
                                
                                if questionario[1] == "#pergunta3" and questionario[1] != mensagem[2]:
                                    WhatsappBot.enviarMensagem(questionario[2])
                                    liberarConversa = False
                            
                            elif questionario[0] == "success":
                                WhatsappBot.enviarMensagem(questionario[1])
                                liberarConversa = False

                        # Gerar Relatorio
                        relatorio = re.findall('#relatorio', mensagem[2])

                        if relatorio:
                            mensagemRelatorio = WhatsappBot.gerarRelatorio(aluno)
                            
                            for mensagem in mensagemRelatorio :  
                                WhatsappBot.enviarMensagem(mensagem)
                                time.sleep(1)
                            
                            liberarConversa = False

                        if liberarConversa:                          
                            # Analisar pergunta de quiz
                            WhatsappBot.analisarPerguntaResposta(mensagem[2], aluno)
                            
                            WhatsappBot.mudarAbaDialogFlow()
                            time.sleep(2)
                            
                            WhatsappBot.digitarMensagemDialogFlow(mensagem[2])
                            time.sleep(2)
                            
                            mensagensRobo = WhatsappBot.obterRespostaDialogFlow()
                            WhatsappBot.mudarAbaWhatssap()
                            time.sleep(2)
        
                            for mensagemRobo in mensagensRobo :  
                                if re.findall('enviar-gif-ok', mensagem[2]):
                                    WhatsappBot.enviarGif(mensagemRobo)
                                else:
                                    WhatsappBot.enviarMensagem(mensagemRobo)
                                time.sleep(1)
                            
                    else:
                        WhatsappBot.enviarMensagem(mensagem[2])

            time.sleep(4)