# Testes

from agno.agent import Agent
from agno.models.google import Gemini

from config import settings

agent = Agent(
    model= Gemini(
        id='gemini-2.5-flash-preview-09-2025',
        api_key=settings.GOOGLE_API_KEY
    ),
    name='Juliano',
    description='Você é Juliano, meu assistente virtual',
    instructions=[
        'responda de maneira clara e consisa.',
        'seja divertido e engraçado'
    ],
    expected_output='Uma resposta divertida para o usuário',
    markdown=True
)

agent.print_response('Qual o seu nome?', markdown=True, stream=True)