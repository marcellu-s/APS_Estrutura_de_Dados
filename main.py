import time
import threading
import inspect  
import random

import tkinter as tk
import pandas as pd


df = pd.read_excel("./data/deter-amz-daily-11-10-2026-00_48_24.xlsx")

data = df["areaMunKm"].tolist()

inverse_data = data[::-1]

random_data = random.sample(data, len(data))

class SortingAlgorithmMixin:
    def bubble_sort(self, data):
        dados = data.copy()

        for i in range(len(dados) - 1):
    
            for j in range(len(dados) - 1 - i):
    
                if dados[j] > dados[j + 1]:
    
                    dados[j], dados[j + 1] = dados[j + 1], dados[j]

        return data


    def selection_sort(self, data):
        dados = data.copy()
        
        for i in range(len(dados) - 1):
    
            menor = i
    
            for j in range(i + 1, len(dados)):
    
                if dados[j] < dados[menor]:
                    menor = j
    
            dados[i], dados[menor] = dados[menor], dados[i]

        return dados

    def inserction_sort(self, data):
        dados = data.copy()
        
        for i in range(1, len(dados)):
    
            atual = dados[i]
    
            j = i - 1
    
            while j >= 0 and dados[j] > atual:
    
                dados[j + 1] = dados[j]
    
                j -= 1
    
            dados[j + 1] = atual

        return dados

    def merge_sort(self, data):
        if len(data) <= 1:
            return data.copy()
    
        meio = len(data) // 2
    
        esquerda = self.merge_sort(data[:meio])
        direita = self.merge_sort(data[meio:])
    
        resultado = []
    
        i = 0
        j = 0
    
        while i < len(esquerda) and j < len(direita):
    
            if esquerda[i] <= direita[j]:
    
                resultado.append(esquerda[i])
    
                i += 1
    
            else:
    
                resultado.append(direita[j])
    
                j += 1
    
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])

        return resultado

    def quick_sort(self, data): 
        if len(data) <= 1:
            return data.copy()
    
        pivo = data[len(data) // 2]
    
        menores = []
        iguais = []
        maiores = []
    
        for registro in data:
    
            if registro < pivo:
    
                menores.append(registro)
    
            elif registro > pivo:
    
                maiores.append(registro)
    
            else:
    
                iguais.append(registro)

        return (
            self.quick_sort(menores)
            + iguais
            + self.quick_sort(maiores)
        )

class NamelessApp(SortingAlgorithmMixin):
    def __init__(self, root):
        self.root = root
        self.root.title("NamelessApp")
        self.root.geometry("820x480")

        self.bg_color = "#222526"
        self.text_color = "#E0E0E0"

        self.root.configure(bg=self.bg_color)

        # Pega a lista com os nomes das funções
        self.sorting_algorithms = [
            name for name, func in inspect.getmembers(SortingAlgorithmMixin, predicate=inspect.isfunction)
        ]

        # Separa os tipos de dados a serem ordenados
        self.data_types = {
            "Dados aleatórios": random_data,
            "Dados inversos": inverse_data
        }

        self.labels_aleatorios = []
        self.labels_aleatorios = []

        # Variável para guardar os resultados de tempo
        self.records = {}

        self.start_time = time.perf_counter()
        self.is_running = False

        # Container do lado esquerdo
        self.container_left = tk.Frame(self.root, bg=self.bg_color)
        self.container_left.pack(side="left", expand=True, fill="both")    

        # 2. Sub-container esquerdo
        self.sub_container_left = tk.Frame(self.container_left, bg=self.bg_color)
        self.sub_container_left.pack(expand=True)  # <--- Centraliza no eixo Y e X ao mesmo tempo!

        # CONTEÚDO DO LADO ESQUERDO
        self.lbl_timer = tk.Label(
            self.sub_container_left,
            text="00:00:00",
            font=("Consolas", 36, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )

        self.lbl_timer.pack(pady=(0, 15))

        self.lbl_sorting_algorithm_name = tk.Label(
            self.sub_container_left,
            text="Aguardando início...",
            font=("Segoe UI", 14),
            fg=self.text_color,
            bg=self.bg_color
        )

        self.lbl_sorting_algorithm_name.pack()

        # Botão colocado dentro do container esquerdo
        self.btn_start = tk.Button(
            self.sub_container_left,
            text="Iniciar algoritmos de ordenação",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            activebackground=self.text_color,
            command=self.start_execution_sequence
        )
        
        self.btn_start.pack(pady=20)

        # Container do lado direito
        self.container_right = tk.Frame(self.root, bg="#2a2e30") # Cor ligeiramente diferente para destacar
        self.container_right.pack(side="right", expand=True, fill="both")  

        # -------------------------------------------------------------
        # 1. DIVISÃO DO LADO DIREITO (Em cima e Embaixo)
        # -------------------------------------------------------------
        
        # Sub-container superior (Dados Inversos)
        self.frame_ranking_inversos = tk.Frame(self.container_right, bg="#2a2e30")
        self.frame_ranking_inversos.pack(side="top", expand=True, fill="both", pady=10)

        # Sub-container inferior (Dados Aleatórios)
        self.frame_ranking_aleatorios = tk.Frame(self.container_right, bg="#2a2e30")
        self.frame_ranking_aleatorios.pack(side="bottom", expand=True, fill="both", pady=10)

        # -------------------------------------------------------------
        # 2. CONTEÚDO DA PARTE DE CIMA (Dados Inversos)
        # -------------------------------------------------------------
        
        # Título da parte de cima
        self.lbl_titulo_inversos = tk.Label(
            self.frame_ranking_inversos,
            text="Ranking - Dados Inversos",
            font=("Segoe UI", 13, "bold"),
            fg=self.text_color,
            bg="#2a2e30"
        )
        self.lbl_titulo_inversos.pack(pady=(0, 5))

        # Listas para guardar as referências dos labels de cada bloco
        self.labels_inversos = []
        self.labels_aleatorios = []

        # -------------------------------------------------------------
        # 3. CONTEÚDO DA PARTE DE BAIXO (Dados Aleatórios)
        # -------------------------------------------------------------
        
        # Título da parte de baixo
        self.lbl_titulo_aleatorios = tk.Label(
            self.frame_ranking_aleatorios,
            text="Ranking - Dados Aleatórios",
            font=("Segoe UI", 13, "bold"),
            fg=self.text_color,
            bg="#2a2e30"
        )
        self.lbl_titulo_aleatorios.pack(pady=(0, 5))

    # --- CÁLCULO E ATUALIZAÇÃO DO TIMER ---
    def execution_time_calculation(self):
        elapsed = time.perf_counter() - self.start_time
        minute = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 100)
        return f"{minute:02d}:{seconds:02d}:{milliseconds:02d}"

    def update_algorithm_runtime(self):
        if self.is_running:
            self.lbl_timer.config(text=self.execution_time_calculation())
            # Continua atualizando enquanto a flag is_running for True
            self.root.after(30, self.update_algorithm_runtime)

    # --- INÍCIO DO PROCESSO ---
    def start_execution_sequence(self):
        if self.is_running:
            return  # Evita cliques duplos enquanto já está rodando

        # Bloqueia botão para evitar múltiplos cliques
        self.btn_start.config(state="disabled")

        # Inicia a thread que executará a fila/sequência de algoritmos
        threading.Thread(target=self.run_all_algorithms_in_sequence, daemon=True).start()

    def add_ranking_label(self, current_algorithm_name):
        # 2. Se houver dados aleatórios no registro, atualiza APENAS o bloco de baixo
        if "Dados aleatórios" in self.records[current_algorithm_name]["Tempo"]:
            # Limpa apenas os antigos de aleatórios
            for lbl in self.labels_aleatorios:
                lbl.destroy()
            self.labels_aleatorios.clear()

            ordered_records_random_data = dict(
                sorted(self.records.items(), key=lambda item: item[1]["Tempo"].get("Dados aleatórios", float('inf')))
            )

            for a, b in ordered_records_random_data.items():
                if "Dados aleatórios" in b["Tempo"]: # Garante que o algoritmo já tem esse dado computado
                    tempo_val = b["Tempo"]["Dados aleatórios"]
                    lbl_aleatorios = tk.Label(
                        self.frame_ranking_aleatorios,
                        text=f"{a} - {tempo_val}",
                        font=("Segoe UI", 12),
                        fg=self.text_color,
                        bg="#2a2e30"
                    )
                    lbl_aleatorios.pack(pady=4)
                    self.labels_aleatorios.append(lbl_aleatorios)

        # 3. Se houver dados inversos no registro, atualiza APENAS o bloco de cima
        if "Dados inversos" in self.records[current_algorithm_name]["Tempo"]:
            # Limpa apenas os antigos de inversos
            for lbl in self.labels_inversos:
                lbl.destroy()
            self.labels_inversos.clear()

            ordered_records_inverse_data = dict(
                sorted(self.records.items(), key=lambda item: item[1]["Tempo"].get("Dados inversos", float('inf')))
            )

            for a, b in ordered_records_inverse_data.items():
                if "Dados inversos" in b["Tempo"]: # Garante que o algoritmo já tem esse dado computado
                    tempo_val = b["Tempo"]["Dados inversos"]
                    lbl_inversos = tk.Label(
                        self.frame_ranking_inversos,
                        text=f"{a} - {tempo_val}",
                        font=("Segoe UI", 12),
                        fg=self.text_color,
                        bg="#2a2e30"
                    )
                    lbl_inversos.pack(pady=4)
                    self.labels_inversos.append(lbl_inversos)

        self.root.update()

    # --- GERENCIADOR DA SEQUÊNCIA (RODA EM THREAD DE BACKGROUND) ---
    def run_all_algorithms_in_sequence(self):
        for algorithm_name in self.sorting_algorithms:
            # Cria os valores a serem recordados
            self.records.update({
                f"{algorithm_name}": {
                    "Tempo": {}
                }
            })

            for type, data in self.data_types.items():
                # 1. Registra o início exato PRIMEIRO
                self.start_time = time.perf_counter()
                self.is_running = True
                
                # 2. Atualiza os textos da interface
                self.root.after(0, lambda name=algorithm_name: self.lbl_sorting_algorithm_name.config(text=f"Executando {type.lower()}: {name}"))

                self.root.after(0, self.update_algorithm_runtime)

                # 3. Executa a função
                func = getattr(self, algorithm_name)
                func(data)

                # 4. Trava o tempo imediatamente ao sair da função
                self.is_running = False
                final_elapsed = time.perf_counter() - self.start_time

                # 5. Formata e congela o visor no tempo correto
                minute = int(final_elapsed // 60)
                seconds = int(final_elapsed % 60)
                milliseconds = int((final_elapsed % 1) * 100)
                tempo_final = f"{minute:02d}:{seconds:02d}:{milliseconds:02d}"

                # Atualiza os labels na main thread
                self.root.after(0, lambda tf=tempo_final: self.lbl_timer.config(text=tf))
                self.root.after(0, lambda name=algorithm_name, t=final_elapsed: self.lbl_sorting_algorithm_name.config(
                    text=f"Concluído {type.lower()}:  {name} em {t:.2f}s"
                ))

                # Adiciona o tempo do tipo de dado executado
                self.records[algorithm_name]["Tempo"].update({
                    f"{type}": tempo_final  
                })

                self.add_ranking_label(algorithm_name)
                            
                time.sleep(1.5)  # Intervalo de pausa entre algoritmos

        # Finalização de todos os algoritmos
        self.root.after(0, lambda: self.lbl_timer.config(text="00:00:00"))
        self.root.after(0, lambda: self.lbl_sorting_algorithm_name.config(text="Todos os algoritmos foram executados!"))
        self.root.after(0, lambda: self.btn_start.config(state="normal"))

# Inicialização da janela principal
if __name__ == "__main__":
    root = tk.Tk()
    app = NamelessApp(root)
    root.mainloop()