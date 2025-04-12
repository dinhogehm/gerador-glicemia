# gerador-glicemia
#Gerador de base de dados para estudos de ciência de dados

import csv
import random
import datetime
import string
from pathlib import Path

# Função para gerar um valor de glicemia com "sujeira"
def gerar_valor_glicemia(com_erro=False):
    if com_erro and random.random() < 0.05:  # 5% de chance de ter erro
        erro_tipo = random.choice(['vazio', 'texto', 'negativo', 'extremo'])
        if erro_tipo == 'vazio':
            return ''
        elif erro_tipo == 'texto':
            return random.choice(['Erro', 'NA', 'NULL', 'sem leitura', '???'])
        elif erro_tipo == 'negativo':
            return -random.randint(50, 400)
        elif erro_tipo == 'extremo':
            return random.randint(600, 1500)
    else:
        # Valores normais ou ligeiramente alterados
        if random.random() < 0.7:  # 70% para valores normais
            return random.randint(70, 180)
        else:  # 30% para valores alterados
            return random.choice([random.randint(40, 69), random.randint(181, 500)])

# Função para gerar uma data e hora com "sujeira"
def gerar_data_hora(com_erro=False, data_inicio=None):
    if com_erro and random.random() < 0.03:  # 3% de chance para erros de data
        erro_tipo = random.choice(['formato_invalido', 'futuro', 'passado_distante'])
        if erro_tipo == 'formato_invalido':
            return random.choice(['01/13/2023', '2023-13-01', 'ontem', '???'])
        elif erro_tipo == 'futuro':
            ano_futuro = random.randint(2026, 2030)
            mes = random.randint(1, 12)
            dia = random.randint(1, 28)
            return f"{ano_futuro}-{mes:02d}-{dia:02d} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        elif erro_tipo == 'passado_distante':
            ano_passado = random.randint(1990, 2010)
            mes = random.randint(1, 12)
            dia = random.randint(1, 28)
            return f"{ano_passado}-{mes:02d}-{dia:02d} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
    else:
        if data_inicio is None:
            data_inicio = datetime.datetime.now() - datetime.timedelta(days=365)
            
        data_aleatoria = data_inicio + datetime.timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        return data_aleatoria.strftime("%Y-%m-%d %H:%M")

# Função para gerar um ID de paciente com "sujeira"
def gerar_id_paciente(com_erro=False):
    if com_erro and random.random() < 0.02:  # 2% de chance para erros de ID
        erro_tipo = random.choice(['formato_invalido', 'vazio'])
        if erro_tipo == 'formato_invalido':
            caracteres = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choice(caracteres) for _ in range(random.randint(5, 15)))
        elif erro_tipo == 'vazio':
            return ''
    else:
        return f"P{random.randint(1000, 9999)}"

# Função para gerar um valor de hemoglobina glicada com "sujeira"
def gerar_hba1c(com_erro=False):
    if com_erro and random.random() < 0.1:  # 10% de chance para erros de HbA1c
        erro_tipo = random.choice(['vazio', 'texto', 'extremo'])
        if erro_tipo == 'vazio':
            return ''
        elif erro_tipo == 'texto':
            return random.choice(['desconhecido', 'NA', 'não medido'])
        elif erro_tipo == 'extremo':
            return round(random.uniform(15.0, 25.0), 1)
    else:
        # Valores normais ou alterados de HbA1c
        if random.random() < 0.6:  # 60% para valores razoáveis
            return round(random.uniform(5.0, 8.0), 1)
        else:  # 40% para valores alterados
            return round(random.uniform(8.1, 14.0), 1)

# Função para criar dados duplicados ocasionalmente
def criar_linha_duplicada(linha_base, com_modificacao=False):
    nova_linha = linha_base.copy()
    if com_modificacao:
        # Duplicata com pequena modificação
        if random.random() < 0.5:
            # Modifica o valor de glicemia levemente
            try:
                valor_original = int(linha_base['valor_glicemia'])
                nova_linha['valor_glicemia'] = str(valor_original + random.randint(-5, 5))
            except:
                pass
        else:
            # Modifica ligeiramente a data/hora
            try:
                data_hora = datetime.datetime.strptime(linha_base['data_hora'], "%Y-%m-%d %H:%M")
                nova_data = data_hora + datetime.timedelta(minutes=random.randint(-5, 5))
                nova_linha['data_hora'] = nova_data.strftime("%Y-%m-%d %H:%M")
            except:
                pass
    return nova_linha

# Função para gerar metadados inconsistentes
def gerar_metadados():
    fonte = random.choice(['Glicosímetro A', 'Glicosímetro B', 'Glicosímetro C', 
                          'Lab X', 'Lab Y', 'Auto-monitoramento', '', 'desconhecido'])
    jejum = random.choice(['sim', 'não', 'S', 'N', 'true', 'false', '1', '0', ''])
    
    # Ocasionalmente dados inconsistentes para o tipo
    if random.random() < 0.05:
        tipo = random.choice(['casual', 'jejum', 'pós-prandial', 'desconhecido', 
                             'Pós jantar', 'Após almoço', '??', ''])
    else:
        tipo = random.choice(['casual', 'jejum', 'pós-prandial'])
        
    return fonte, jejum, tipo

# Função principal para gerar o arquivo CSV
def gerar_arquivo_csv(numero_linhas, tamanho_alvo_mb=100):
    arquivo_saida = 'dados_glicemia_sujos.csv'
    
    # Colunas do CSV
    colunas = ['id_paciente', 'data_hora', 'valor_glicemia', 'unidade', 'hba1c', 
               'fonte_dados', 'jejum', 'tipo_medicao', 'observacoes']
    
    # Contador para acompanhar progresso
    progresso_passo = numero_linhas // 10
    
    linhas_geradas = []
    
    print(f"Gerando {numero_linhas} linhas de dados...")
    
    # Gerar dados básicos
    for i in range(numero_linhas):
        if i % progresso_passo == 0:
            print(f"Progresso: {i / numero_linhas * 100:.1f}%")
        
        com_erro = random.random() < 0.15  # 15% de chance de ter algum erro
        
        fonte, jejum, tipo = gerar_metadados()
        
        linha = {
            'id_paciente': gerar_id_paciente(com_erro),
            'data_hora': gerar_data_hora(com_erro),
            'valor_glicemia': gerar_valor_glicemia(com_erro),
            'unidade': random.choice(['mg/dL', 'mg/dL', 'mg/dL', 'mmol/L', '']),  # Maioria mg/dL
            'hba1c': gerar_hba1c(com_erro),
            'fonte_dados': fonte,
            'jejum': jejum,
            'tipo_medicao': tipo,
            'observacoes': ''
        }
        
        # Adicionar observações aleatórias ocasionalmente
        if random.random() < 0.1:
            observacoes = [
                "Paciente relatou tontura", 
                "Após exercício físico",
                "Esqueceu medicação",
                "Após consumo de álcool",
                "Pós refeição rica em carboidratos",
                "Estresse elevado",
                "Possível erro de medição",
                "Paciente com sintomas de hipoglicemia"
            ]
            linha['observacoes'] = random.choice(observacoes)
        
        linhas_geradas.append(linha)
        
        # Adicionar dados duplicados ocasionalmente (5% de chance)
        if random.random() < 0.05:
            linhas_geradas.append(criar_linha_duplicada(linha, com_modificacao=random.random() < 0.5))
            
    # Adicione algumas linhas com cabeçalhos incorretos ou mal formatados
    if random.random() < 0.5:
        for _ in range(random.randint(1, 5)):
            indice = random.randint(0, len(linhas_geradas) - 1)
            linha_problema = linhas_geradas[indice]
            # Escolha aleatória de problema
            problema = random.choice(['valores_trocados', 'formato_alterado'])
            if problema == 'valores_trocados':
                # Troca valores entre colunas
                colunas_aleatorias = random.sample(['id_paciente', 'valor_glicemia', 'unidade', 'jejum'], 2)
                temp = linha_problema[colunas_aleatorias[0]]
                linha_problema[colunas_aleatorias[0]] = linha_problema[colunas_aleatorias[1]]
                linha_problema[colunas_aleatorias[1]] = temp
            elif problema == 'formato_alterado':
                if 'valor_glicemia' in linha_problema and linha_problema['valor_glicemia']:
                    try:
                        valor = int(linha_problema['valor_glicemia'])
                        linha_problema['valor_glicemia'] = f"{valor} mg/dL"
                    except:
                        pass
    
    # Salvar o arquivo
    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(linhas_geradas)
    
    # Verificar tamanho do arquivo
    tamanho_arquivo = Path(arquivo_saida).stat().st_size / (1024 * 1024)  # Tamanho em MB
    print(f"Arquivo gerado: {arquivo_saida}")
    print(f"Tamanho atual: {tamanho_arquivo:.2f} MB")
    
    # Se o arquivo for menor que o tamanho alvo, gerar mais linhas
    while tamanho_arquivo < tamanho_alvo_mb:
        linhas_adicionais = int((tamanho_alvo_mb - tamanho_arquivo) / tamanho_arquivo * len(linhas_geradas))
        print(f"Adicionando aproximadamente {linhas_adicionais} linhas para atingir {tamanho_alvo_mb} MB...")
        
        with open(arquivo_saida, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            
            # Gerar mais linhas
            for _ in range(linhas_adicionais):
                com_erro = random.random() < 0.15
                fonte, jejum, tipo = gerar_metadados()
                
                linha = {
                    'id_paciente': gerar_id_paciente(com_erro),
                    'data_hora': gerar_data_hora(com_erro),
                    'valor_glicemia': gerar_valor_glicemia(com_erro),
                    'unidade': random.choice(['mg/dL', 'mg/dL', 'mg/dL', 'mmol/L', '']),
                    'hba1c': gerar_hba1c(com_erro),
                    'fonte_dados': fonte,
                    'jejum': jejum,
                    'tipo_medicao': tipo,
                    'observacoes': ''
                }
                
                if random.random() < 0.1:
                    observacoes = [
                        "Paciente relatou tontura", 
                        "Após exercício físico",
                        "Esqueceu medicação",
                        "Após consumo de álcool",
                        "Pós refeição rica em carboidratos"
                    ]
                    linha['observacoes'] = random.choice(observacoes)
                
                writer.writerow(linha)
        
        # Atualizar tamanho
        tamanho_arquivo = Path(arquivo_saida).stat().st_size / (1024 * 1024)
        print(f"Novo tamanho: {tamanho_arquivo:.2f} MB")
    
    print(f"Arquivo finalizado: {arquivo_saida}")
    print(f"Tamanho final: {tamanho_arquivo:.2f} MB")

# Executar a geração
if __name__ == "__main__":
    # Começar com 500.000 linhas e depois ajustar se necessário
    gerar_arquivo_csv(numero_linhas=500000, tamanho_alvo_mb=100)
