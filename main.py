import openai
from dotenv import load_dotenv
import os

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
    
    print("Transcricão salva com sucesso!")

def main():
    load_dotenv()
    
    caminho_audio = "podcasts/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.mp3"
    nome_arquivo = "ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146"

    url_podcast = "https://www.youtube.com/watch?v=YZ6YZAvDHXA"
    
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    
    modelo_whisper = "whisper-1"
    
    transcricao_completa = openai_whisper_trascrever(caminho_audio, nome_arquivo, modelo_whisper, openai)

if __name__ == "__main__":
    
    main()
   

