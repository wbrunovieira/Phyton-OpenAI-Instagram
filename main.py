import openai
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    
    caminho_audio = "podcasts/ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146.mp3"
    nome_arquivo = "ESSA_A_ PREVISÃO_ MAIS_ BIZARRA_PARA_O _FUTURO_ Os_Sócios_146"

    url_podcast = "https://www.youtube.com/watch?v=YZ6YZAvDHXA"
    
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

if __name__ == "__main__":
    
    main()
   

