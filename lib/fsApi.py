import requests
import json
import time
import os

FS_API ='https://ai.factura.city/chat/fs'
TOKEN = app_id=os.environ['FS_ACCESS_TOKEN']

def esperar_respuesta_bot(chat_id, maxTries=10, awaitInterval=1, chatLength=2):
    for _ in range(maxTries):
        print(f'{_}')
        chat = requests.get(
            f'{FS_API}/{chat_id}',
            headers={
                'Content-Type': 'application/json', 
                'token': TOKEN
            }
        ).json()
        
        if len(chat.get('messages', [])) >= chatLength:
            return chat
        
        time.sleep(awaitInterval)

    raise Exception("No se recibieron respuestas del bot en la API")

def sendMessageToAI(message):
    response = requests.post(
        FS_API,
        json={
            'content': message
            },
        headers={
        'Content-Type': 'application/json',
        'token': TOKEN
        }
    ).json()

    chatId = response['id']

    chat = esperar_respuesta_bot(chatId)

    return {
        'chatId': chatId,
        'aiResponse': chat['messages'][1]['content']
    }

