from errbot import BotPlugin, re_botcmd
from random import randint


class Roleta(BotPlugin):
    """
    O intuito do chatbot é ser um jogo dinamico de sorte, 
    no qual um unico individuo ou um grupo de pessoas 
    possa jogar simultanemente.
     A ideia do jogo é ser uma 'roleta russa' no qual cada 
     jogador ira ativar a roleta e tentar a sorte em descobir
    se sobrevive ou esta fora do jogo. Para ativar essa 
    funcionalidade basta diditar 'roleta' que logoem seguida 
    recebira uma respostar se você sobrevive ou não.

Comandos de entreterimento: 
BOM DIA - Bot responde bom dia + user 
TESTE - Bot respnde TESTADO + user 
ALO - Bot responde OLÁ + user
    """

    @botcmd  # flags a command
    def tryme(self, msg, args):  # a command callable with !tryme
        """
        Execute to check if Errbot responds to command.
        Feel free to tweak me to experiment with Errbot.
        You can find me in your init directory in the subdirectory plugins.
        """
        return "It *works* !"  # This string format is markdown.
