from errbot import BotPlugin, botcmd

class Example(BotPlugin):
    """
    classe de metodos de aprendizado.
    """

    @botcmd  
    def bomdia(self, msg, args): 
        """
        Responde educadamente ao usuario.
        """
        
        argumentos = args.split(' ')
        return "bom dia"

    