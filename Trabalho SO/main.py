import random

MAXIMO_TEMPO_EXECUCAO = 65535
numero_processos = 1


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


def imprime_status(lista):
    tempo_espera_total = 0
    numero_processos = len(lista)
    media

    for dados in lista:
        print(
            f"Processo[{dados.numero_processo}]: "
            f"tempo_espera={dados.tempo_espera}"
        )
        tempo_espera_total += dados.tempo_espera

    print


processos_criados = fornecer_informacoes(2)

for i in processos_criados:
    print(i)

imprime_status(processos_criados)
