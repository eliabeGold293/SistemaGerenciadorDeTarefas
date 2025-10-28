# src/team.py
from textwrap import dedent

from agno.team import Team
from agno.models.google import Gemini

from config import settings
from src.agents import get_market_researcher, get_corporate_specialist, get_investiment_strategist


def get_team():
    return Team(
        model=Gemini(
            id='gemini-2.5-flash-preview-09-2025',
            api_key=settings.GOOGLE_API_KEY
        ),
        name='Time de Suporte da Vertice Assessoria de Investimentos',
        description=dedent('''\
            Você é o líder do time de suporte da Vertice Assessoria de Investimentos,
            que redireciona as perguntas dos clientes para o agente mais adequado.
        '''),
        instructions=[
            'Faça uma análise da pergunta do cliente e redirecione para o agente mais adequado, ajudando-o com instruções claras sobre o que ele precisa fazer.',
            'Caso a pergunta seja apenas para saber o preço de um ativo em tempo real, redirecione para o agente Pesquisador de Mercado.',
            'Caso a pergunta seja sobre recomendações, análises ou fundamentos de mercado, redirecione para o agente Estrategista de Investimentos.',
            'Caso a pergunta seja específica sobre a empresa Vértice, redirecione para o agente Especialista Corporativo.',
        ],
        show_members_responses=True,
        markdown=True,
        respond_directly=True,
        members=[
            get_market_researcher(),
            get_investiment_strategist(),
            get_corporate_specialist(),
        ],
    )