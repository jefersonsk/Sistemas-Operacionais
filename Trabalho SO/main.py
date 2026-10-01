import random

MAXIMO_TEMPO_EXECUCAO = 65535
numero_processos = 0


class Processo:
    def __init__(self,
                 numero_processo,
                 tempo_execucao,
                 tempo_espera,
                 tempo_restante,
                 tempo_chegada,
                 prioridade
                 ):
        self.numero_processo = numero_processo
        self.tempo_execucao = tempo_execucao
        self.tempo_espera = tempo_espera
        self.tempo_restante = tempo_restante
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade

    def executar_um_ciclo(self):
        self.tempo_restante -= 1

    def esta_finalizado(self):
        return self.tempo_restante <= 0

    def __str__(self):
        return (f"Processo[{self.numero_processo}]: "
                f"tempo_execucao={self.tempo_execucao} "
                f"tempo_restante={self.tempo_restante} "
                f"tempo_chegada={self.tempo_chegada} "
                f"prioridade={self.prioridade}"
                )

    def resetar(self):
        self.tempo_restante = self.tempo_execucao
        self.tempo_espera = 0

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


class GerenciadorDeFilas:
    def __init__(self):
        self.fila = []
        self.tempo_sistema = 0

    def adicionar_processo(self, processo):
        processo.resetar()
        self.fila.append(processo)

    def executar_ciclo_cpu(self, processo_em_execucao):
        self.tempo_sistema += 1
        auxiliar_tempo = processo_em_execucao.tempo_restante

        processo_em_execucao.executar_um_ciclo()

        return {
            "tempo": self.tempo_sistema,
            "processo": processo_em_execucao.numero_processo,
            "restante": auxiliar_tempo
        }

    def executar_fcfs(self):
        historico = []
        linha_do_tempo = []

        for processo in self.fila:

            tempo_espera = self.tempo_sistema

            while not processo.esta_finalizado():
                linha_do_tempo.append(self.executar_ciclo_cpu(processo))

            historico.append({
                "processo": processo,
                "tempo_espera": tempo_espera
            })

        return {"linha_do_tempo": linha_do_tempo,
                "metricas_processos": historico
                }

    def executar_sjf_nao_preemptivo(self):
        historico = []
        linha_do_tempo = []
        tempo_ocioso = 0

        while self.fila:
            processos_disponiveis = [
                processo for processo in self.fila if
                processo.tempo_chegada <= self.tempo_sistema
            ]

            if processos_disponiveis:
                processo_atual = min(
                    processos_disponiveis,
                    key=lambda processo: processo.tempo_execucao
                )

                tempo_espera = (self.tempo_sistema -
                                processo_atual.tempo_chegada
                                )

                while not processo_atual.esta_finalizado():
                    linha_do_tempo.append(
                        self.executar_ciclo_cpu(processo_atual)
                    )

                historico.append(
                    {"processo": processo_atual,
                     "tempo_espera": tempo_espera}
                )

                self.fila.remove(processo_atual)
            else:
                self.tempo_sistema += 1
                tempo_ocioso += 1
                linha_do_tempo.append({"tempo": self.tempo_sistema,
                                       "processo": "ocioso",
                                       "restante": "-"}
                                      )

        return {"linha_do_tempo": linha_do_tempo,
                "metricas_processos": historico,
                "tempo_ocioso": tempo_ocioso
                }

    def executar_sjf_preemptivo(self):
        historico = []
        linha_do_tempo = []
        tempo_ocioso = 0

        while self.fila:
            processos_disponiveis = [
                processo for processo in self.fila if
                processo.tempo_chegada <= self.tempo_sistema
            ]

            if processos_disponiveis:
                processo_atual = min(
                    processos_disponiveis,
                    key=lambda processo: processo.tempo_restante
                )

                linha_do_tempo.append(
                    self.executar_ciclo_cpu(processo_atual)
                )

                if processo_atual.esta_finalizado():

                    tempo_espera = (self.tempo_sistema -
                                    processo_atual.tempo_chegada -
                                    processo_atual.tempo_execucao
                                    )

                    historico.append(
                        {"processo": processo_atual,
                         "tempo_espera": tempo_espera}
                    )

                    self.fila.remove(processo_atual)
            else:
                self.tempo_sistema += 1
                tempo_ocioso += 1
                linha_do_tempo.append({"tempo": self.tempo_sistema,
                                       "processo": "ocioso",
                                       "restante": "-"}
                                      )

        return {"linha_do_tempo": linha_do_tempo,
                "metricas_processos": historico,
                "tempo_ocioso": tempo_ocioso
                }

    def executar_prioridade_nao_preemptivo(self):
        historico = []
        linha_do_tempo = []
        tempo_ocioso = 0

        while self.fila:
            processos_disponiveis = [
                processo for processo in self.fila if
                processo.tempo_chegada <= self.tempo_sistema
            ]

            if processos_disponiveis:
                processo_atual = min(
                    processos_disponiveis,
                    key=lambda processo: processo.prioridade
                )

                tempo_espera = (self.tempo_sistema -
                                processo_atual.tempo_chegada
                                )

                while not processo_atual.esta_finalizado():
                    linha_do_tempo.append(
                        self.executar_ciclo_cpu(processo_atual)
                    )

                historico.append(
                    {"processo": processo_atual,
                     "tempo_espera": tempo_espera}
                )

                self.fila.remove(processo_atual)
            else:
                self.tempo_sistema += 1
                tempo_ocioso += 1
                linha_do_tempo.append({"tempo": self.tempo_sistema,
                                       "processo": "ocioso",
                                       "restante": "-"}
                                      )

        return {"linha_do_tempo": linha_do_tempo,
                "metricas_processos": historico,
                "tempo_ocioso": tempo_ocioso
                }

    def executar_prioridade_preemptivo(self):
        historico = []
        linha_do_tempo = []
        tempo_ocioso = 0

        while self.fila:
            processos_disponiveis = [
                processo for processo in self.fila if
                processo.tempo_chegada <= self.tempo_sistema
            ]

            if processos_disponiveis:
                processo_atual = min(
                    processos_disponiveis,
                    key=lambda processo: processo.prioridade
                )

                linha_do_tempo.append(
                    self.executar_ciclo_cpu(processo_atual)
                )

                if processo_atual.esta_finalizado():

                    tempo_espera = (self.tempo_sistema -
                                    processo_atual.tempo_chegada -
                                    processo_atual.tempo_execucao
                                    )

                    historico.append(
                        {"processo": processo_atual,
                         "tempo_espera": tempo_espera}
                    )

                    self.fila.remove(processo_atual)
            else:
                self.tempo_sistema += 1
                tempo_ocioso += 1
                linha_do_tempo.append({"tempo": self.tempo_sistema,
                                       "processo": "ocioso",
                                       "restante": "-"}
                                      )

        return {"linha_do_tempo": linha_do_tempo,
                "metricas_processos": historico,
                "tempo_ocioso": tempo_ocioso}

    def executar_round_robin(self, time_slice):
        historico = []
        linha_do_tempo = []
        lista_chegada = sorted(
            self.fila, key=lambda processo: processo.tempo_chegada
        )
        fila_prontos = []

        while lista_chegada or fila_prontos:
            while self.deve_processar(lista_chegada):
                fila_prontos.append(lista_chegada.pop(0))

            if fila_prontos:
                processo_atual = fila_prontos.pop(0)

                # Executa ciclo a ciclo respeitando a fatia de tempo (time_slice)
                for _ in range(time_slice):
                    # Registra 1 ciclo na linha do tempo usando a estrutura padrão
                    linha_do_tempo.append(
                        self.executar_ciclo_cpu(processo_atual))

                    # Checa se novos processos chegaram durante este ciclo
                    while self.deve_processar(lista_chegada):
                        fila_prontos.append(lista_chegada.pop(0))

                    # Se o processo terminou antes de esgotar a fatia de tempo, interrompe o turno
                    if processo_atual.esta_finalizado():
                        break

                # 3. Reinsere no final da fila se ainda houver tempo restante 🔄
                if processo_atual.tempo_restante > 0:
                    fila_prontos.append(processo_atual)
                # 4. Registra métricas se o processo finalizou 🏁
                else:
                    tempo_espera = (
                        self.tempo_sistema -
                        processo_atual.tempo_chegada -
                        processo_atual.tempo_execucao
                    )

                    historico.append({
                        "processo": processo_atual,
                        "tempo_espera": tempo_espera
                    })
            else:
                # CPU Ociosa 💤
                self.tempo_sistema += 1
                linha_do_tempo.append({
                    "tempo": self.tempo_sistema,
                    "processo": "ocioso",
                    "restante": "-"
                })

        return {
            "linha_do_tempo": linha_do_tempo,
            "metricas_processos": historico
        }

    def deve_processar(self, lista_chegada):
        return (
            lista_chegada
            and lista_chegada[0].tempo_chegada <= self.tempo_sistema
        )


def fornecer_informacoes():
    processos_gerados = []

    numero_processos = int(input("Digite o número de processos desejados: "))
    escolha = input("Gerar dados automáticos [S ou N]? ")

    if escolha.upper() == "S":
        processos_gerados = Processo.popular_processo_automatico(
            numero_processos)
    else:
        for i in range(numero_processos):
            numero_processo = i
            tempo_execucao = int(
                input(f"Digite tempo de execução do processo[{i}]: "))
            tempo_chegada = int(
                input(f"Digite tempo de chegada do processo[{i}]: "))
            prioridade = int(
                input(f"Digite a prioridade do processo[{i}]: "))
            tempo_restante = tempo_execucao
            tempo_espera = 0

            processos_gerados.append(Processo(
                numero_processo,
                tempo_execucao,
                tempo_espera,
                tempo_restante,
                tempo_chegada,
                prioridade)
            )

    imprimir_processos(processos_gerados)

    return processos_gerados


def imprimir_processos(lista):
    for processo in lista:
        print(processo)


def imprimir_cabecalho():
    print("=" * 40)
    print("TRABALHO SISTEMAS OPERACIONAIS".center(40))
    print("Algoritmos de Escalonamento".center(40))
    print("=" * 40)


def executar_algoritmo(metodo_algoritmo, lista_processos):
    copia_processos = lista_processos.copy()

    gerenciador = GerenciadorDeFilas()

    for dados in copia_processos:
        gerenciador.adicionar_processo(dados)

    resultados = metodo_algoritmo(gerenciador)

    imprimir_resultados(resultados)


def imprimir_resultados(dados):
    if dados["linha_do_tempo"]:
        for informacoes in dados["linha_do_tempo"]:
            print(f"tempo[{informacoes['tempo']}]: "
                  f"processo[{informacoes['processo']}] "
                  f"restante={informacoes['restante']}"
                  )

    if dados["metricas_processos"]:
        soma_espera = 0
        for informacoes in dados["metricas_processos"]:
            informacao_processo = informacoes["processo"]
            informacao_espera = informacoes["tempo_espera"]
            soma_espera += informacao_espera
            print(f"Processo[{informacao_processo.numero_processo}] "
                  f"tempo espera={informacao_espera}"
                  )

        numero_processos = len(dados["metricas_processos"])
        media_espera = soma_espera / numero_processos
        print(f"Tempo médio de espera: {media_espera:.2f}")

    if "tempo_ocioso" in dados:
        tempo_ocioso = dados["tempo_ocioso"]
        print(f"Tempo total ocioso da CPU={tempo_ocioso}")


def main():
    imprimir_cabecalho()

    processos_criados = fornecer_informacoes()

    while True:
        escolha_algoritmo = int(input(
            "Escolha o algoritmo: [1=FCFS "
            "2=SJF Preemptivo "
            "3=SJF Não Preemptivo "
            "4=Prioridade Preemptivo "
            "5=Prioridadde Não Preemptivo "
            "6=Round Robin "
            "7=Imprime lista de processos "
            "8=Popular processos novamente "
            "9=Sair]: "
        ))

        if escolha_algoritmo == 1:
            executar_algoritmo(
                GerenciadorDeFilas.executar_fcfs,
                processos_criados
            )
        elif escolha_algoritmo == 2:
            executar_algoritmo(
                GerenciadorDeFilas.executar_sjf_preemptivo,
                processos_criados
            )
        elif escolha_algoritmo == 3:
            executar_algoritmo(
                GerenciadorDeFilas.executar_sjf_nao_preemptivo,
                processos_criados
            )
        elif escolha_algoritmo == 4:
            executar_algoritmo(
                GerenciadorDeFilas.executar_prioridade_preemptivo,
                processos_criados
            )
        elif escolha_algoritmo == 5:
            executar_algoritmo(
                GerenciadorDeFilas.executar_prioridade_nao_preemptivo,
                processos_criados
            )
        elif escolha_algoritmo == 6:
            time_slice = int(input("Digite o time-slice: "))

            executar_algoritmo(
                lambda aux: aux.executar_round_robin(time_slice),
                processos_criados
            )

        elif escolha_algoritmo == 7:
            imprimir_processos(processos_criados)
        elif escolha_algoritmo == 8:
            processos_criados = fornecer_informacoes()
        elif escolha_algoritmo == 9:
            break


if __name__ == "__main__":
    main()
