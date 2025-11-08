import redis

redis_url = 'redis://default:I1CQgkZiDQz6NMivXMGvG9AuLyJCEPQQ@redis-19974.c89.us-east-1-3.ec2.redns.redis-cloud.com:19974'

redis_client = redis.from_url(redis_url, decode_responses=True)

try:
    redis_client.ping()
    print('Conexão bem sucedida')
except redis.exceptions.ConnectionError as e:
    print(f'Problema ao tentar conectar com o banco na nuvem. Erro: {e}')