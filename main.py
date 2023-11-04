import openai
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    
main()
   

