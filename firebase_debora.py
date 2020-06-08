from firebase import firebase
import requests

class firebase_debora:
    def __init__(self):
        self.firebase_debora= firebase.FirebaseApplication('https://bootteste-urcgpl.firebaseio.com/', None)
    
    def getAlunos(self):
        resultado = self.firebase_debora.get('/debora-fnjowg/aluno', '')
        return resultado
    
    def getGabarito(self):
        resultado = self.firebase_debora.get('/debora-fnjowg/gabarito', '')
        return resultado
    
    def getRespostas(self):
        resultado = self.firebase_debora.get('/debora-fnjowg/resposta', '')
        return resultado

    def salvarRespostasAluno(self, dados):
        resultado = self.firebase_debora.post('/debora-fnjowg/aluno', dados)
        return resultado
    
    def atualizarRespostas(self, key, campo, valor):
        self.firebase_debora.put('/debora-fnjowg/resposta/'+key, campo, valor)
        return 'resposta atualizado com sucesso'
    
    def atualizarSituacaoAluno(self, key, campo, valor):
        self.firebase_debora.put('/debora-fnjowg/aluno/'+key, campo, valor)
        return 'resposta atualizado com sucesso'

