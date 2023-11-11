from openai import OpenAI
import openai

from dotenv import load_dotenv
import os
import requests
from pydub import AudioSegment
from PIL import Image


def openai_whisper_trascrever(caminho_audio, nome_arquivo,modelo_whisper, openai):
    print("Transcrevendo o audio...")
    
    audio = open(caminho_audio, "rb")
    
    resposta = openai.Audio.transcribe(
        api_key=openai.api_key,
        model=modelo_whisper,
        file =audio
        
    
        
 ) 
    transcricao = resposta.text
    
    with open(f"transcricoes/{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(transcricao)
        
    return transcricao
    


def openai_gpt_resumir_texto(transcricao_completa, nome_arquivo):
    print("Resumindo com o gpt para um post do instagram ...")

    prompt_sistema = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma persona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.
    """
    
    prompt_usuario = f"{prompt_sistema} {transcricao_completa} \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
         messages=[
        {
            "role": "user",
            "content": prompt_usuario,
        },
    ],
    )
    
    resumo_instagram = response.choices[0].message.content
    
    with open(f"resumo_instagram/{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(resumo_instagram)
        
    return resumo_instagram
def ferramenta_ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")


def openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai):
    print("Gerando as hashtags com a open ai ... ")

    prompt_sistema = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.
    - A saída deve conter 5 hashtags.

    """

    prompt_usuario =f'Aqui está um resumo de um texto "{resumo_instagram}". Por favor, gere 5 hashtags que sejam relevantes para este texto e que possam ser publicadas no Instagram.  Por favor, faça isso em português do Brasil '
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
         messages=[
        {
            "role": "user",
            "content": prompt_usuario,
        },
    ],
    )
    
    hashtags = response.choices[0].message.content

    

    
    with open(f"hashtags/{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(hashtags)
    
    return hashtags


def openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai):
    print("Gerando a saida de texto para criacao de imagens com o GPT ...")

    prompt_sistema = """

    - A saída deve ser uma única, do tamanho de um tweet, que seja capaz de descrever o conteúdo do texto para que possa ser transcrito como uma imagem.
    - Não inclua hashtags

    """

    prompt_usuario =  f'Reescreva o texto a seguir, em uma frase, para que descrever o texto abaixo em um tweet: {resumo_instagram}'
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
         messages=[
        {
            "role": "user",
            "content": prompt_usuario,
        },
    ],
    )
    
    texto_para_imagem = response.choices[0].message.content
   
    
    with open(f"texto_para_imagem/{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(texto_para_imagem)
    texto_para_imagem = sanitize_filename(texto_para_imagem)
    print("nome do arquivo depois de sanitizar",texto_para_imagem)
    return texto_para_imagem

def sanitize_filename(filename):
    # Substitui espaços por underscores
    sanitized = filename.replace(" ", "_").replace("ç", "c").replace("ã", "a")
    # Adicione aqui mais substituições se necessário, por exemplo:
    # sanitized = sanitized.replace("ç", "c").replace("ã", "a")
    return sanitized

def openai_dalle_gerar_imagem(resolucao, resumo_para_imagem, nome_arquivo, openai, qtd_imagens = 1):
    print("Gerando a imagem com o DALL-E ...")
    
    prompt_user = f"Uma pintura ultra futurista, textless, 3d que retrate: {resumo_para_imagem}"
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.images.generate(
        
       prompt=prompt_user,
        n = qtd_imagens,
        size = resolucao,
        quality="standard"
    )
    
    imagem_url = response.data[0].url
    print("imagem_url",imagem_url)
    
    # lista_nome_imagens = ferramenta_download_imagem(nome_arquivo, [imagem_url], qtd_imagens)
    # print("lista_nome_imagens", lista_nome_imagens)
    return imagem_url
def ferramenta_download_imagem(nome_arquivo, urls_imagens, qtd_imagens=1):
    print("URLs recebidas na função:", urls_imagens)
    lista_nome_imagens = []
    if not urls_imagens:  # Verifica se a lista de URLs está vazia
        print("Nenhuma URL de imagem fornecida.")
        return None

    try:
        for url_imagem in urls_imagens:
            print("Processando URL:", url_imagem)
            resposta = requests.get(url_imagem)
            # Verifica se o índice está dentro do intervalo da lista
            if resposta.status_code == 200:
                nome_arquivo_completo = f"{nome_arquivo}0.png"
                with open(nome_arquivo_completo, "wb") as arquivo_imagem:
                    arquivo_imagem.write(resposta.content)
                lista_nome_imagens.append(nome_arquivo_completo)
            else:
                print(f"Erro ao baixar a imagem: {url_imagem}")
               
    except Exception as e:
        print(f"Ocorreu um erro durante o download: {e}")
        return None

   
    print("lista_nome_imagens", lista_nome_imagens)
    return lista_nome_imagens
def selecionar_imagem(lista_nome_imagens):
    try:
        index = int(input("Qual imagem você deseja selecionar? Informe o sufixo da imagem: "))
        imagem_selecionada = lista_nome_imagens[index]
        return imagem_selecionada
    except ValueError:
        print("Por favor, insira um número válido.")
        return None  # Retorna None ou você pode adicionar uma lógica para nova tentativa ou saída
    except IndexError:
        print("Índice fora do intervalo.")
        return None  # Retorna None ou você pode adicionar uma lógica para nova tentativa ou saída

def ferramenta_converter_png_para_jpg(caminho_imagem_escolhida, nome_arquivo):
    img_png = Image.open(caminho_imagem_escolhida) 
    img_png.save(caminho_imagem_escolhida.split(".")[0]+".jpg") 

    return caminho_imagem_escolhida.split(".")[0] + ".jpg"

def transcricao_completa_nvidia(caminho_audio, nome_arquivo, modelo_whisper, openai):
    print("Transcrevendo o audio...")
    
    audio = open(caminho_audio, "rb")
    
    resposta = openai.Audio.transcribe(
        api_key=openai.api_key,
        model=modelo_whisper,
        file =audio
        
    
        
 ) 
    transcricao = resposta.text
    
    with open(f"transcricoes/{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(transcricao)
        
    return transcricao 

def ferramenta_transcrever_audio_em_partes(caminho_audio_podcast, nome_arquivo):
    print("Iniciando corte .. ")
    audio = AudioSegment.from_mp3(caminho_audio_podcast)

    dez_minutos = 10 * 60 * 1000
    
    contador_pedaco = 1
    arquivos_exportados = []

    while len(audio) > 0:
        pedaco = audio[:dez_minutos]
        nome_pedaco_audio = f"{nome_arquivo}_parte_{contador_pedaco}.mp3"
        pedaco.export(nome_pedaco_audio, format="mp3")
        arquivos_exportados.append(nome_pedaco_audio)
        audio = audio[dez_minutos:]
        contador_pedaco += 1

    return arquivos_exportados
def openai_whisper_trascrever_em_partes(caminho_audio, nome_arquivo,modelo_whisper, openai):
    print("Transcrevendo o audio...")
    lista_arquivos_de_audio = ferramenta_transcrever_audio_em_partes(caminho_audio, nome_arquivo)
    lista_pedacos_de_audio = []
    
    for um_pedacao_de_audio in lista_arquivos_de_audio:
    
        audio = open(um_pedacao_de_audio, "rb")
        
        resposta = openai.Audio.transcribe(
            api_key=openai.api_key,
            model=modelo_whisper,
            file =audio
            
        
            
    ) 
        transcricao = resposta.text
        lista_pedacos_de_audio.append(transcricao)
        
    transcricao = "".join(lista_pedacos_de_audio)
    
    with open(f"transcricoes/{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(transcricao)
        
    return transcricao
def main():
    load_dotenv()
    
    # caminho_audio = "podcasts/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.mp3"
    # nome_arquivo = "ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146"
    caminho_audio = "podcasts/tomp3.cc -Como a Inteligência Artificial IA irá revolucionar empresas e negócios ft Aster  AI 360 02.mp3"
    nome_arquivo = "nome-curto-para-o-video-longo"

    url_podcast = ""
    
    resolucao = "1024x1024"
    qtd_imagens = 1
    
    
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # api_key = os.getenv("OPENAI_API_KEY")
    # openai.api_key = api_key
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    modelo_whisper = "whisper-1"
    
    #transcricao_completa = ferramenta_ler_arquivo("transcricoes/COmo a Inteligenca Aurtificial IA irá revolucionar empresas e negócios ft Aster  AI 360 02.txt")  
    resumo_instagram = ferramenta_ler_arquivo("transcricoes/COmo a Inteligenca Aurtificial IA irá revolucionar empresas e negócios ft Aster  AI 360 02.txt") 
    #transcricao_completa = openai_whisper_trascrever(caminho_audio, nome_arquivo, modelo_whisper, openai)
    
    #resumo_instagram = openai_gpt_resumir_texto(str(transcricao_completa), nome_arquivo)
    
    #hashtags = openai_gpt_criar_hashtag(resumo_instagram,nome_arquivo, openai)
    hashtags = ferramenta_ler_arquivo("hashtags/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.txt")

    #resumo_imagem_instagram = openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai)
    resumo_imagem_instagram = ferramenta_ler_arquivo("texto_para_imagem/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.txt")
    
    imagem_gerada = openai_dalle_gerar_imagem(resolucao,resumo_imagem_instagram, nome_arquivo, openai, qtd_imagens)
    print("imagem_gerada",imagem_gerada)
    lista_imagens_geras = ferramenta_download_imagem(nome_arquivo, [imagem_gerada],qtd_imagens)
    
    caminho_imagem_escolhida = selecionar_imagem(lista_imagens_geras)
    #transcricao_completa_nvidia = openai_whisper_trascrever_em_partes(caminho_audio, nome_arquivo, modelo_whisper, openai)
    
    caminho_imagem_convertida = ferramenta_converter_png_para_jpg(caminho_imagem_escolhida, nome_arquivo)
    
if __name__ == "__main__":
    
    
    main()
   

