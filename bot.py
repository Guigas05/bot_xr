import os
from twilio.rest import Client
from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import Levenshtein
from openai import OpenAI
import openai

client_openai = OpenAI(
    #defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
)

apbot = Flask(__name__)
def sendMessage(text : str, to: str, fromwwp: str):

    account_sid = ""
    auth_token = ""
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        from_ ='whatsapp:+14155238886',
        body=text,
        to=to
        )
    print(message.sid)

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",  
  messages=[
    {"role": "assistant", "content": "Só me responda coisas relacionadas á festa da XR-Adventure, localizada em fortaleza-Ceará., caso nao saiba a informação solicite ao usúario para checar contato com algum responsável através dos links: https://www.instagram.com/xr.adventure/, https://instagram.com/duoo.eventos/"},
  ]
)
    

@apbot.route("/sms",methods = ["get","post"])
def reply():
    msgt = request.form.get("Body")
    msgt.lower()
    sen_num= request.form.get("From")
    me_num = request.form.get("To")
    print(msgt)
    print(sen_num)

    
    
    chat_completion = client_openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": msgt,
            }
        ],
        model="gpt-3.5-turbo",
    )

 
    if(msgt == "1" or msgt == "2" or msgt == "3" or msgt == "4" or msgt == "5"):
             secondReply(msgt)
    elif(msgt == "sim"):
        ajuda()
    elif(msgt == "não"):
        msg = "Muito obrigado por estar conosco!!, Se precisar de algo a mais so mandar um olá!"
        sendMessage(msg, sen_num, me_num)
    elif(msgt == "olá"):
        intro()
        ajuda()
    

def secondReply(inte):
    sen_num = request.form.get("From")
    me_num = request.form.get("To")
    if(inte == "1"):
        msg = "vai acontecer no incrivel shooping iguatemi no piso L4, um espaço feito apenas para nosso evento!"
        sendMessage(msg, sen_num,me_num)
        loop()
    if(inte == "2"):
        msg = "Estamos na Pre-venda ate segunda as 22:00"
        sendMessage(msg, sen_num,me_num)
        loop()
    if(inte == "3"):
        msg = "No nosso openbar exclusivo: Tanquery,Redbull,Budweiser,Johnny walker ate o sol raiar!"
        sendMessage(msg, sen_num,me_num)
        loop()
    if(inte == "4"):
        msg = "Conheça DJ Heverton, o astro das pistas que já agitou multidões em eventos renomados como Kiss Me e Aviões Fantasy. Sua habilidade única em misturar ritmos transforma cada festa em uma experiência inesquecível. Não perca a chance de ser envolvido pelas batidas vibrantes e energia contagiante de DJ Heverton!, além dos DJS: MG, e Dj nawak"
        sendMessage(msg, sen_num,me_num)
        loop()
    if(inte == "5"):
        msg = "Exclusividade do Público: Ao contrário dos tradicionais pubs de Fortaleza, a festa Duoo se destaca por seu foco em um público selecionado, garantindo uma atmosfera mais personalizada e exclusiva. Essa abordagem cria um ambiente único, onde os participantes compartilham interesses similares, elevando a qualidade da interação social - Nível Superior de Open Bar: Enquanto muitos estabelecimentos em Fortaleza oferecem open bars padrão, a Duoo eleva a experiência com uma seleção premium de bebidas. O open bar desta festa é inédito na cidade, com uma variedade e qualidade de bebidas que superam as expectativas, proporcionando aos convidados uma degustação de alto padrão. -  Ambiente e Experiência Únicos: A festa Duoo não é apenas um evento, mas uma experiência imersiva. Diferente dos pubs comuns de Fortaleza, cada detalhe é cuidadosamente planejado para criar uma atmosfera inigualável, desde a decoração sofisticada até a programação musical exclusiva, garantindo uma noite memorável e diferenciada para seu público seleto."
        sendMessage(msg, sen_num,me_num)
        loop()

def loop():
    
    sen_num = request.form.get("From")
    me_num = request.form.get("To")

    msg = "Você precisa de mais alguma ajuda?\n (digite 'sim' ou 'não')"
    sendMessage(msg, sen_num, me_num)     

def intro():
    sen_num = request.form.get("From")
    me_num = request.form.get("To")

    msg = 'Olá, tudo bem?'
    sendMessage(msg, sen_num, me_num)
    msg = "Prazer eu sou o assistente da XR-Adventure e estou aqui para lhe ajudar."
    msg = 'Qual serviço você deseja?'
    sendMessage(msg, sen_num, me_num)  

def ajuda():
    sen_num = request.form.get("From")
    me_num = request.form.get("To")
    msg = "Como posso ajuda-lo?"
    sendMessage(msg, sen_num,me_num)
    msg = " ATENDIMENTO DA XR : 1. onde vai acontecer o local 2. me diga qual o valor do lote atual 3. quais sao as bebidas disponibilizadas no openbar 4.quem sao as atraçoes do proximo evento 16/12 5.quais sao os diferenciais da festa"
    sendMessage(msg, sen_num,me_num)   

def find_closest_match(user_input, valid_words):
   
    closest_match = min(valid_words, key=lambda word: Levenshtein.distance(user_input, word))
    return closest_match

    sendMessage(msg, sen_num, me_num)
if(__name__=="__main__"):
    port = int(os.environ.get("PORT", 5000))
    apbot.run(host='0.0.0.0', port=port)