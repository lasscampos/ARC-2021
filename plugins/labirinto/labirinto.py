from errbot import BotPlugin, re_botcmd
from random import randint


class Labirinto(BotPlugin):
    """
    Jogo de labirinto feito em matriz de números inteiros.
    O objetivo é fazer com que o jogador saia do labirinto,
    e para isso será preciso movimentar-se pelas salas e
    corredores.
    Internamente, o jogo implementa uma matriz de inteiros
    para armazenar informações como:
    - Parede: 0
    - Sala ou corredor: 1
    - Posição e sentido do jogador:
      -  2: sentido Norte
      -  4: sentido Sul
      -  8: sentido Oeste
      - 16: sentido Leste
    - Jogador está com inventário:
      - Mapa: 32
      - Bússola: 64
    - Final do labirinto: 128
    Assim, o mapa acumula informações com base nessas
    potências de dois, como por exemplo:
    5 = 4 + 1 = jogador no sentido Sul + sala ou corredor.
    """

    """ Dicionário com o mapa por jogador: as partidas. """
    partidas = {}

    def partida(self, jogador, atualizar=None):
        """
        Retornar o mapa de determinado jogador.
        Se o argumento 'atualizar' existe, atualizar no dicionário
        e retornar o próprio valor.
        Caso contrário, verificar se já tem uma partida em curso,
        ou se é preciso criar uma do modelo - e retornar.
        """

        if atualizar:
            self.partidas[jogador] = atualizar
        elif jogador not in self.partidas:
            self.partidas[jogador] = [[0,   0,   0, 101,   0],
                                      [0,   0,   0,   1,   0],
                                      [0,   0,   1,   1,   0],
                                      [0,   0,   1,   1, 129],
                                      [0,   0,   0,   0,   0]]
        return self.partidas[jogador]

    """ Dicionário de mensagens de resposta ao usuário. """
    mensagens = {
        "fora do mapa": "Fora dos limites do mapa 🗺️",
        "parede": "Parede 🧍‍♂️🧱",
        "fim do labirinto": "Fim do labirinto 🏆",
        "um passo a frente": "Um passo a frente 🚶🏽"
    }

    def converter_inteiro_para_binario(self, inteiro):
        """
        Converter número inteiro em string de 32 bits.
        Com base em: https://stackoverflow.com/a/10411108/5167118
        """

        return f"{inteiro:032b}"

    def posicao_do_jogador(self, jogador):
        """
        Informar a posição no mapa:
        - Linha (eixo X)
        - Coluna (eixo Y)
        Também, informar a orientação do jogador em relação ao mapa:
        - Norte (N)
        - Sul (S)
        - Oeste (O)
        - Leste (L)
        Além disso, os itens do inventário:
        - Mapa
        - Bússola
        """

        x = 0
        for linha in self.partida(jogador):
            y = 0
            for coluna in linha:
                sentido = self.converter_inteiro_para_binario(coluna)[27:31]
                """
                Os sentidos estão organizados por bit,
                a contar da direita para a esquerda:
                - N: bit 30 (2^1)
                - S: bit 29 (2^2)
                - O: bit 28 (2^3)
                - L: bit 27 (2^4)
                Como o Python usa limite fechado a esquerda e aberto a direita,
                o intervalo vai de 27 (inclui) a 31 (não inclui).
                """
                if sentido != "0000":
                    """
                    O jogador foi encontrado (qualquer sentido, por enquanto).
                    Agora, ver se tem o mapa no inventário.
                    """
                    if self.converter_inteiro_para_binario(coluna)[26] == "1":
                        mapa = True
                    else:
                        mapa = False
                    """ Se tem a bússola no inventário. """
                    if self.converter_inteiro_para_binario(coluna)[25] == "1":
                        bússola = True
                    else:
                        bússola = False
                    """ E, por fim, o sentido do jogador. """
                    if sentido == "0001":
                        sentido = "N"
                    elif sentido == "0010":
                        sentido = "S"
                    elif sentido == "0100":
                        sentido = "O"
                    else:
                        """ sentido == "1000" """
                        sentido = "L"
                    return x, y, sentido, mapa, bússola
                y += 1
            x += 1

    def atualizar_sentido_do_jogador(self, jogador, rotação):
        """
        Atualiza sentido do jogador no mapa,
        que por se tratar de uma matriz de inteiros é feita
        uma operação de soma/subtração nas células para
        atualizar os dados do jogador.
        """

        partida = self.partida(jogador)
        x, y, sentido_inicial, mapa, bússola = self.posicao_do_jogador(jogador)
        if rotação == "direita":
            if sentido_inicial == "N":
                """
                Norte -> Leste
                - 2 (N) + 16 (L)
                """
                rotacionar = +14
                sentido_final = "L"
            elif sentido_inicial == "S":
                """
                Sul -> Oeste
                - 4 (S) + 8 (O)
                """
                rotacionar = +4
                sentido_final = "O"
            elif sentido_inicial == "O":
                """
                Oeste -> Norte
                - 8 (O) + 2 (N)
                """
                rotacionar = -6
                sentido_final = "N"
            else:
                """
                Último caso é Leste ("L")
                Leste -> Sul
                - 16 (L) + 4 (S)
                """
                rotacionar = -12
                sentido_final = "S"
        else:
            """ Se a rotação não é para direita, então é esquerda. """
            if sentido_inicial == "N":
                """
                Norte -> Oeste
                - 2 (N) + 8 (O)
                """
                rotacionar = +6
                sentido_final = "O"
            elif sentido_inicial == "S":
                """
                Sul -> Leste
                - 4 (S) + 16 (L)
                """
                rotacionar = +12
                sentido_final = "L"
            elif sentido_inicial == "O":
                """
                Oeste -> Sul
                - 8 (O) + 4 (S)
                """
                rotacionar = -4
                sentido_final = "S"
            else:
                """
                Último caso é Leste ("L")
                Leste -> Norte
                - 16 (L) + 2 (N)
                """
                rotacionar = -14
                sentido_final = "N"
        """ Atualiza o mapa de inteiros e informa o usuário o novo sentido. """
        partida[x][y] += rotacionar
        self.partida(jogador, atualizar=partida)
        return x, y, sentido_final

    def atualizar_posicao_do_jogador(self, jogador, movimento):
        """
        Atualiza posição do jogador no mapa,
        que por se tratar de uma matriz de inteiros é feita
        uma operação de soma/subtração nas células para
        atualizar os dados do jogador.
        Há 3 possíveis alternativas:
        - A: a posição adiante está fora do mapa;
        - B: a posição adiante é sala ou corredor;
        - C: a posição adiante é parede.
        Somente na alternativa B fará a movimentação no mapa.
        """

        partida = self.partida(jogador)
        x, y, sentido_inicial, mapa, bússola = self.posicao_do_jogador(jogador)
        """ Levar junto o inventário. """
        inventário = 0
        if mapa:
            inventário += 32
        if bússola:
            inventário += 64
        """ Realizar o movimento relativo ao jogador. """
        if movimento == "frente":
            if sentido_inicial == "N":
                """
                A célula a frente do jogador está uma linha acima (x - 1),
                na mesma coluna. Então, verificar se já está na
                primeira linha e se a próxima célula é sala ou corredor.
                Ou seja, se o primeiro bit (2^0, no. 31) é 1.
                Caso contrário, manter (e retornar) a mesma posição.
                """
                if x - 1 < 0:
                    return self.mensagens["fora do mapa"]
                elif self.converter_inteiro_para_binario(partida[x-1][y])[31] == "1":
                    """ Norte = 2, mover para linha acima: x - 1. """
                    partida[x][y] -= 2 + inventário
                    partida[x-1][y] += 2 + inventário
                    self.partida(jogador, atualizar=partida)
                    if self.converter_inteiro_para_binario(partida[x-1][y])[24] == "1":
                        return self.mensagens["fim do labirinto"]
                    else:
                        return self.mensagens["um passo a frente"]
                else:
                    return self.mensagens["parede"]
            elif sentido_inicial == "S":
                """
                A célula a frente do jogador está uma linha abaixo (x + 1),
                na mesma coluna.
                """
                if x + 1 >= len(partida):
                    return self.mensagens["fora do mapa"]
                elif self.converter_inteiro_para_binario(partida[x+1][y])[31] == "1":
                    """ Sul = 4, mover para linha abaixo: x + 1. """
                    partida[x][y] -= 4 + inventário
                    partida[x+1][y] += 4 + inventário
                    self.partida(jogador, atualizar=partida)
                    if self.converter_inteiro_para_binario(partida[x+1][y])[24] == "1":
                        return self.mensagens["fim do labirinto"]
                    else:
                        return self.mensagens["um passo a frente"]
                else:
                    return self.mensagens["parede"]
            elif sentido_inicial == "O":
                """
                A célula a frente do jogador está na mesma linha,
                uma coluna a esquerda (y - 1).
                """
                if y - 1 < 0:
                    return self.mensagens["fora do mapa"]
                elif self.converter_inteiro_para_binario(partida[x][y-1])[31] == "1":
                    """ Oeste = 8, mover para coluna a esquerda: y - 1. """
                    partida[x][y] -= 8 + inventário
                    partida[x][y-1] += 8 + inventário
                    self.partida(jogador, atualizar=partida)
                    if self.converter_inteiro_para_binario(partida[x][y-1])[24] == "1":
                        return self.mensagens["fim do labirinto"]
                    else:
                        return self.mensagens["um passo a frente"]
                else:
                    return self.mensagens["parede"]
            else:
                """ Sentido é leste (L).
                A célula a frente do jogador está na mesma linha,
                uma coluna a direita (y + 1).
                """
                if y + 1 >= len(partida[0]):
                    return self.mensagens["fora do mapa"]
                elif self.converter_inteiro_para_binario(partida[x][y+1])[31] == "1":
                    """ Leste = 16, mover para coluna a direita: y + 1. """
                    partida[x][y] -= 16 + inventário
                    partida[x][y+1] += 16 + inventário
                    self.partida(jogador, atualizar=partida)
                    if self.converter_inteiro_para_binario(partida[x][y+1])[24] == "1":
                        return self.mensagens["fim do labirinto"]
                    else:
                        return self.mensagens["um passo a frente"]
                else:
                    return self.mensagens["parede"]

    def desenhar_mapa(self, jogador):
        """
        Desenhar o mapa com base no inventário:
        - Jogador não tem mapa ou bússola: não desenhar sequer o mapa.
        - Jogador tem apenas o mapa: desenhar o mapa sem o jogador.
        - Jogador tem mapa e bússola: desenhar o mapa completo.
        """

        x, y, sentido, mapa, bússola = self.posicao_do_jogador(jogador)
        if mapa:
            mapa = ""
            i = 0
            for linha in self.partida(jogador):
                j = 0
                for coluna in linha:
                    if x == i and y == j and bússola:
                        mapa += sentido
                    elif coluna == 0:
                        mapa += "X"
                    else:
                        mapa += "U"
                    j += 1
                mapa += "\n"
                i += 1
            return mapa
        else:
            return "Sem mapa no inventário."

    @re_botcmd(pattern=r"^(.*)([e|E]u|[s|S]entido)(.*)$")
    def jogador(self, msg, match):
        """ Informar a sentido do jogador como ponto cardeal. """

        x, y, sentido, mapa, bússola = self.posicao_do_jogador(msg.frm.person)
        yield "Posição no mapa: [" + str(x) + "," + str(y) + "] 🗺️"
        yield "Sentido: " + sentido + " 🧭"

    @re_botcmd(pattern=r"^(.*)[d|D]ireita(.*)$")
    def direita(self, msg, match):
        """ Rotacionar 90 graus o jogador para a direita - na sua perspectiva.  """

        x, y, sentido = self.atualizar_sentido_do_jogador(
            msg.frm.person, "direita")
        yield "Novo sentido: " + sentido

    @re_botcmd(pattern=r"^(.*)[e|E]squerda(.*)$")
    def esquerda(self, msg, match):
        """ Rotacionar 90 graus o jogador para a esquerda - na sua perspectiva. """

        x, y, sentido = self.atualizar_sentido_do_jogador(
            msg.frm.person, "esquerda")
        yield "Novo sentido: " + sentido

    @re_botcmd(pattern=r"^(.*)[f|F]rente(.*)$")
    def frente(self, msg, match):
        """ Mover uma posição a frente - de forma relativa ao jogador - no mapa. """

        mensagem = self.atualizar_posicao_do_jogador(msg.frm.person, "frente")
        yield mensagem

    @re_botcmd(pattern=r"^(.*)[m|M]apa(.*)$")
    def mapa(self, msg, match):
        """ Apresentar o mapa no bot. """

        return self.desenhar_mapa(msg.frm.person)