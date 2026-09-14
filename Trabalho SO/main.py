import random

MAXIMO_TEMPO_EXECUCAO = 65535
numero_processos = 2


class Processo:
    def __init__(self, numero_processo, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
        self.numero_processo = numero_processo
        self.tempo_execucao = tempo_execucao
        self.tempo_espera = tempo_espera
        self.tempo_restante = tempo_restante
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade

    @staticmethod
    def popular_processo_automatico(numero_de_processos):
        lista_processos = []

        for i in range(numero_de_processos):
            numero_processo = i
            tempo_execucao = random.randint(1, 10)
            tempo_espera = 0
            tempo_restante = tempo_execucao
            tempo_chegada = random.randint(1, 10)
            prioridade = random.randint(1, 15)

            lista_processos.append(
                Processo(numero_processo,
                         tempo_execucao,
                         tempo_espera,
                         tempo_restante,
                         tempo_chegada,
                         prioridade
                         ))

        return lista_processos

    def __str__(self):
        return (f"Processo[{self.numero_processo}]: "
                f"tempo_execucao={self.tempo_execucao} "
                f"tempo_restante={self.tempo_restante} "
                f"tempo_chegada={self.tempo_chegada} "
                f"prioridade={self.prioridade}"
                )


def fornecer_informacoes(numero_de_processos):
    processos = []

    escolha = input("Gerar dados automáticos [S ou N]? ")

    if escolha.upper() == "S":
        processos = Processo.popular_processo_automatico(numero_de_processos)
    else:
        for i in range(numero_de_processos):
            numero_processo = i
            tempo_execucao = int(
                input(f"Digite tempo de execução do processo[{i}]: "))
            tempo_chegada = int(
                input(f"Digite tempo de chegada do processo[{i}]: "))
            prioridade = int(
                input(f"Digite a prioridade do processo[{i}]: "))
            tempo_restante = tempo_execucao
            tempo_espera = 0

            processos.append(Processo(
                numero_processo,
                tempo_execucao,
                tempo_espera,
                tempo_restante,
                tempo_chegada,
                prioridade)
            )

    return processos


def imprime_status(tempos_de_espera):
    tempo_espera_total = 0
    numero_processos = len(tempos_de_espera)
    media_espera = 0

    for processo in range(numero_processos):
        print(
            f"Processo[{processo}]: "
            f"tempo_espera={tempos_de_espera[processo]}"
        )
        tempo_espera_total += tempos_de_espera[processo]

    media_espera = tempo_espera_total / numero_processos

    print(f"Tempo medio de espera: {media_espera}")


def fcfs(lista):
    tempo = 0
    tempo_de_espera = 0
    lista_tempos_espera = []

    for processo in lista:
        processo_em_execucao = processo.numero_processo
        tempo_restante = processo.tempo_restante

        tempo += 1
        lista_tempos_espera.append(tempo_de_espera)

        for passo in range(1, MAXIMO_TEMPO_EXECUCAO):
            print(
                f"tempo[{tempo}]: processo[{processo_em_execucao}] "
                f"restante={tempo_restante}"
            )

            # if tempo_execucao == tempo_restante:
            #     tempo_espera = passo - 1

            tempo_de_espera += 1

            if tempo_restante == 1:
                break
            else:
                tempo_restante -= 1

            tempo += 1

    imprime_status(lista_tempos_espera)


processos_criados = fornecer_informacoes(2)

for i in processos_criados:
    print(i)

# imprime_status(processos_criados)

fcfs(processos_criados)
