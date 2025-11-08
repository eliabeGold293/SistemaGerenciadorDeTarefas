from datetime import datetime

def data_hora_atual():
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y %H:%M:%S")

