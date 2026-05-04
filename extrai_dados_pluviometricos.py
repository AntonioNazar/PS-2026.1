import pandas as pd
import glob
import os
import traceback
# Define as pastas de entrada e saída
pasta_entrada = 'dados_pluviometricos'
pasta_saida = 'dados_pluviometricos_extraidos'

# Cria a pasta de saída automaticamente caso ela ainda não exista
os.makedirs(pasta_saida, exist_ok=True)

# Busca todos os arquivos .txt na pasta de entrada
arquivos_txt = glob.glob(os.path.join(pasta_entrada, '*.txt'))

# Nomes das colunas conforme a sua indicação
colunas = ["Dia", "Hora", "15 min", "01 h", "04 h", "24 h", "96 h"]

if not arquivos_txt:
    print(f"Nenhum arquivo .txt encontrado na pasta '{pasta_entrada}'.")

for arquivo in arquivos_txt:
    try:
        # 1. Lê o arquivo, pula as 5 primeiras linhas e ignora múltiplos espaços
        df = pd.read_csv(
            arquivo,
            skiprows=4,
            header=0,
            sep=r'\s+', # Pega qualquer quantidade de espaços
            #usecols=colunas,
            na_values=['ND'] # Transforma 'ND' em nulo
        )
        print(df)
        if len(df.columns) == 7: 
            df.rename(columns={
                df.columns[0]: "Dia",
                df.columns[1]: "Hora",
                df.columns[2]: "15 min",
                df.columns[3]: "01 h",
                df.columns[4]: "04 h",
                df.columns[5]: "24 h",
                df.columns[6]: "96 h",
                }, 
                inplace = True)
        else:
            df.rename(columns={
                df.columns[0]: "Dia",
                df.columns[1]: "Hora",
                df.columns[2]: "5 min",
                df.columns[3]: "10 min",
                df.columns[4]: "15 min",
                df.columns[5]: "01 h",
                df.columns[6]: "04 h",
                df.columns[7]: "24 h",
                df.columns[8]: "96 h",
                }, 
                inplace = True)

        print(df)
        df = df[['Dia','Hora','24 h']]
        print(df)
        # 2. Transforma os tipos de dados conforme solicitado
        df['Dia'] = pd.to_datetime(df['Dia'], format='%d/%m/%Y').astype('datetime64[us]')
        df['Hora'] = df['Hora'].astype('string')
        df['24 h'] = df['24 h'].astype(float)

        # 3. Define o nome e o caminho do arquivo de saída (.csv)
        nome_arquivo = os.path.basename(arquivo) # Extrai apenas o nome do arquivo, ex: "arquivo1.txt"
        nome_base = os.path.splitext(nome_arquivo)[0] # Tira a extensão .txt
        nome_csv = f"{nome_base}.csv"
        
        # Cria o caminho final para salvar na nova pasta
        caminho_saida = os.path.join(pasta_saida, nome_csv)

        # 4. Salva o DataFrame como CSV
        df.to_csv(caminho_saida, index=False)
        

    except Exception as e:
        print(f"Erro ao processar o arquivo {arquivo}: {e}")
        print("Detalhes do erro e linha:")
        print(traceback.format_exc())
        print("-" * 50)