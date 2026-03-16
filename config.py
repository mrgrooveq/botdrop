# ============================================
# config.py — ÁREA DE CONFIGURAÇÃO
# ============================================

TOKEN = 'MTQ4MjgzMzcxOTQ0NTQyNjMyNw.GgBNz4.rD6NT4Enan77eEbGUNWbNbRTLEYuZiFbo_zJHM'

GUILD_ID = 1474506579247104002

DROP_CHANNEL_ID = 1474513504072372437

# Cooldown em segundos entre drops
DROP_COOLDOWN = 10

# Cargos dos prêmios do drop
TEMPORARY_ROLES = {
    '1': 1482810875843969285,  # CAM 10
    '2': 1482810990218187057,  # CAPITÃO
    '3': None                  # Pic Perm
}

ROLE_NAMES = {
    '1': 'CAM 10',
    '2': 'CAPITÃO',
    '3': 'Pic Perm'
}

# Cargos autorizados a usar /startdrop, /stopdrop e /cargosdrops
AUTHORIZED_ROLES = {
    1482822176737595597,
    1474506816804093965,
    1480951816354004992
}

# Perguntas automáticas do drop
QUESTIONS = [
    {"question": "Qual é a capital do Brasil?", "answers": ["brasilia", "bsb", "distrito federal", "df"]},
    {"question": "Quanto é 7 x 8?", "answers": ["56", "cinquenta e seis"]},
    {"question": "Qual é a cor do céu em um dia limpo?", "answers": ["azul", "azul claro"]},
    {"question": "Em que ano o homem pisou na Lua?", "answers": ["1969", "69"]},
    {"question": "Qual é o maior planeta do sistema solar?", "answers": ["jupiter"]},
    {"question": "Em qual país se originou o sushi?", "answers": ["japao", "japan"]},
    {"question": "Quantos lados tem um hexágono?", "answers": ["6", "seis"]},
    {"question": "Qual é o menor país do mundo?", "answers": ["vaticano", "cidade do vaticano", "vatican"]},
    {"question": "Qual é o animal mais rápido do mundo?", "answers": ["guepardo", "cheetah", "gepardo"]},
    {"question": "Qual é o idioma mais falado no mundo?", "answers": ["ingles", "english"]},
    {"question": "Quantos continentes existem no mundo?", "answers": ["7", "sete"]},
    {"question": "Qual é o maior oceano do mundo?", "answers": ["pacifico", "oceano pacifico"]},
    {"question": "Qual é a fórmula da água?", "answers": ["h2o"]},
    {"question": "Quantos estados tem o Brasil?", "answers": ["26", "vinte e seis"]},
    {"question": "Qual é o país mais populoso do mundo?", "answers": ["china"]},
    {"question": "Quanto é a raiz quadrada de 144?", "answers": ["12", "doze"]},
    {"question": "Em que continente fica o Brasil?", "answers": ["america do sul", "sul"]},
    {"question": "Qual é o metal mais precioso do mundo?", "answers": ["ouro"]},
    {"question": "Quantos jogadores tem um time de futebol em campo?", "answers": ["11", "onze"]},
    {"question": "Qual é o país com a maior área territorial do mundo?", "answers": ["russia"]},
    {"question": "Qual é o planeta mais próximo do Sol?", "answers": ["mercurio"]},
    {"question": "Quantas horas tem um dia?", "answers": ["24", "vinte e quatro"]},
    {"question": "Qual é a capital da Argentina?", "answers": ["buenos aires"]},
    {"question": "Quanto é 15 x 15?", "answers": ["225", "duzentos e vinte e cinco"]},
    {"question": "Qual é a capital do Japão?", "answers": ["toquio", "tokyo"]},
    {"question": "Em que ano o Brasil foi descoberto?", "answers": ["1500"]},
    {"question": "Qual animal é conhecido como o rei da selva?", "answers": ["leao"]},
    {"question": "Quantos minutos tem uma hora?", "answers": ["60", "sessenta"]},
    {"question": "Qual é o maior país da América do Sul?", "answers": ["brasil"]},
    {"question": "Quanto é 100 dividido por 4?", "answers": ["25", "vinte e cinco"]},
    {"question": "Qual é a capital da França?", "answers": ["paris"]},
    {"question": "Quantos planetas tem o sistema solar?", "answers": ["8", "oito"]},
    {"question": "Qual é o rio mais longo do mundo?", "answers": ["nilo", "amazonas"]},
    {"question": "Qual é o esporte mais popular do mundo?", "answers": ["futebol", "football", "soccer"]},
    {"question": "Qual é a capital da Itália?", "answers": ["roma", "rome"]},
    {"question": "Quanto é 9 x 9?", "answers": ["81", "oitenta e um"]},
    {"question": "Qual é o país de origem do McDonald's?", "answers": ["estados unidos", "eua", "usa", "estados unidos da america"]},
    {"question": "Quantos segundos tem um minuto?", "answers": ["60", "sessenta"]},
    {"question": "Qual é a capital da Alemanha?", "answers": ["berlim", "berlin"]},
    {"question": "Qual é o maior deserto do mundo?", "answers": ["saara", "sahara"]},
    {"question": "Quantos ossos tem o corpo humano adulto?", "answers": ["206", "duzentos e seis"]},
    {"question": "Qual é a capital do Egito?", "answers": ["cairo"]},
    {"question": "Em que ano começou a Segunda Guerra Mundial?", "answers": ["1939"]},
    {"question": "Qual é o país símbolo do carnaval mais famoso do mundo?", "answers": ["brasil"]},
    {"question": "Quanto é 2 elevado a 10?", "answers": ["1024"]},
]