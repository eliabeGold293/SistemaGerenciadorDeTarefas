# main.py
from src.team import get_team


team = get_team()

team.print_response('Como os fundos do nosso portifólio estão se relacionando com o desempenho atual do Ibovespa?', markdown=True)