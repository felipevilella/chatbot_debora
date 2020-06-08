import re

class filtro_bot: 
    def __init__(self):
        pass

    def filtraRespostaAluno(self, resposta, questao):
        if questao == 1 :
            respostaPergunta = re.findall('a', resposta.lower())
       
        elif questao == 2:
            respostaPergunta = re.findall('c', resposta.lower())
            
            if respostaPergunta :
                respostaPergunta = re.findall('d', resposta.lower())

            if respostaPergunta :
                return "c e d"
            else:
                return respostaPergunta

        
        elif questao == 3:
            respostaPergunta = re.findall('d', resposta.lower())

        if respostaPergunta:
            return respostaPergunta[0]
        else:
            return respostaPergunta