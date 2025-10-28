import os # biblioteca que permite ler coisas do seu computador

from dotenv import load_dotenv

load_dotenv(
    dotenv_path='secrets/.env',
    override=True
)

GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')