import openai
from dotenv import load_dotenv
import os
import requests
from pydub import AudioSegment
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
    


def openai_gpt_resumir_texto(transcricao_completa, nome_arquivo, openai):
    print("Resumindo com o gpt para um post do instagram ...")

    prompt_sistema = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.

    """
    prompt_usuario = ". \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             
             "content": prompt_sistema
             },
            {
                "role": "user",
                "content": transcricao_completa + prompt_usuario
            }
        ],
        temperature=0.6
    )
    
    resumo_instagram = resposta["choices"][0]["message"]["content"]
    
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

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             
             "content": prompt_sistema
             },
            {
                "role": "user",
                "content":  prompt_usuario
            }
        ],
        temperature=0.6
    )
    
    hashtags = resposta["choices"][0]["message"]["content"]
    
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
    
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             
             "content": prompt_sistema
             },
            {
                "role": "user",
                "content":  prompt_usuario
            }
        ],
        temperature=0.6
    )
    
    texto_para_imagem = resposta["choices"][0]["message"]["content"]
    
    with open(f"texto_para_imagem/{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(texto_para_imagem)
    
    return texto_para_imagem

def openai_dalle_gerar_imagem(resolucao, resumo_para_imagem, nome_arquivo, openai, qtd_imagens = 1):
    print("Gerando a imagem com o DALL-E ...")
    
    prompt_user = f"Uma pintura ultra futurista, textless, 3d que retrate: {resumo_para_imagem}"
    
    resposta = openai.Image.create(
        prompt=prompt_user,
        n = qtd_imagens,
        size = resolucao
    )
    
    return resposta["data"]

def ferramenta_download_imagem(nome_arquivo, imagem_gerada,qtd_imagens = 1):
  lista_nome_imagens = []
  try:
    for contador_imagens in range(0,qtd_imagens):
        caminho = imagem_gerada[contador_imagens].url
        imagem = requests.get(caminho)

        with open(f"{nome_arquivo}_{contador_imagens}.png", "wb") as arquivo_imagem:
            arquivo_imagem.write(imagem.content)

        lista_nome_imagens.append(f"{nome_arquivo}_{contador_imagens}.png")
    return lista_nome_imagens
  except:
    print("Ocorreu um erro!")
    return  None

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
def main():
    load_dotenv()
    
    # caminho_audio = "podcasts/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.mp3"
    # nome_arquivo = "ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146"
    caminho_audio = "podcasts/tomp3.cc -Como a Inteligência Artificial IA irá revolucionar empresas e negócios ft Aster  AI 360 02.mp3"
    nome_arquivo = "COmo a Inteligenca Aurtificial IA irá revolucionar empresas e negócios ft Aster  AI 360 02"

    url_podcast = "https://www.youtube.com/watch?v=YZ6YZAvDHXA"
    
    resolucao = "1024x1024"
    qtd_imagens = 4
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    
    modelo_whisper = "whisper-1"
    
    transcricao_completa = ferramenta_ler_arquivo("transcricoes/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.txt")  
    resumo_instagram = ferramenta_ler_arquivo("transcricoes/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.txt") 
    # transcricao_completa = openai_whisper_trascrever(caminho_audio, nome_arquivo, modelo_whisper, openai)
    # resumo_instagram = openai_gpt_resumir_texto( transcricao_completa, nome_arquivo, openai)
    
    # hashtags = openai_gpt_criar_hashtag(resumo_instagram,nome_arquivo, openai)
   # hashtags = ferramenta_ler_arquivo("hashtags/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.txt")

    # resumo_imagem_instagram = openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai)
    #resumo_imagem_instagram = ferramenta_ler_arquivo("texto_para_imagem/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.txt")
    
    #imagem_gerada = openai_dalle_gerar_imagem(resolucao,resumo_imagem_instagram, nome_arquivo, openai, qtd_imagens)
    
    #ferramenta_download_imagem(nome_arquivo, imagem_gerada,qtd_imagens)
    
    transcricao_completa_nvidia = openai_whisper_trascrever(caminho_audio, nome_arquivo, modelo_whisper, openai)
    
if __name__ == "__main__":
    
    
    main()
   

