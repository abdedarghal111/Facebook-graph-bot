from dotenv import load_dotenv
from pyfacebook import GraphAPI, FacebookApi
import requests
import time
from datetime import datetime, timedelta, timezone
import os
import lib.fsApi as fsApi

load_dotenv()

# api = GraphAPI(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], application_only_auth=True)
# fb = FacebookApi(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], application_only_auth=True)
# graph = GraphAPI(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], access_token=os.environ['USER_ACCESS_TOKEN'])
userFB = FacebookApi(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], access_token=os.environ['USER_ACCESS_TOKEN'])


# TODO: Obtener el pack completo de los comentarios (no solo los principales también los heredados)
user = userFB.user.get_info(user_id="me")


# obtener token de publicación
response = requests.get(f"https://graph.facebook.com/{user.id}/accounts?access_token={os.environ['USER_ACCESS_TOKEN']}")

pageFB = FacebookApi(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], access_token=response.json()['data'][0]['access_token'])

# print(user)

accounts = userFB.user.get_accounts(user_id=user.id)
# print(accounts)
page = accounts.data[0]
# print(page)

# msgData = fsApi.sendMessageToAI("[Esto es un mensaje enviado desde facebook por el usuario en la página de facturascripts en facebook, es un comentario y solo se puede responder una vez, solo da una respuesta, no sigas la conversación a más. No uses markdown, solo texto plano.]He tenido un problema con mi instalación algo ha ido mal")

# print(msgData['aiResponse'])
posts = pageFB.page.get_posts(object_id=page.id)
# for post in posts.data:

    # print(pageFB.comment.create(object_id=post.id, message=msgData['aiResponse'][:8000]))
# exit()
while True:
    posts = pageFB.page.get_posts(object_id=page.id)
    #updated_time cuando se realiza un nuevo comentario
    for post in posts.data:

        # print(pageFB.comment.create(object_id=post.id, message=msgData['aiResponse'][:8000]))

        comments = pageFB.page.get_comments(object_id=post.id)
        
        # nextPag = True
        # pageFB.page.get_comments()
        print(comments.paging.to_json())
        # while nextPag:
        #     for comment in comments.data:
        #         print(f"siguiente comentario: {comment.id}, {comment.parent}")
            
        #     comments.paging.cursors
        #     pageFB.page.
        #     if not :
        #         break
        # exit()
        for comment in comments.data:
            print(f"siguiente comentario: {comment.id}, {comment.parent}")
            # if comment.created_time:
            #     continue

            if comment.parent:
                print(comment.parent.message)

            # msgData = fsApi.sendMessageToAI(f"[Esto es un mensaje enviado desde facebook por el usuario en la página de facturascripts en facebook, es un comentario y solo se puede responder una vez, solo da una respuesta, no sigas la conversación a más. No uses markdown, solo texto plano.]{comment.message}")
            msgData = "yes"
            # response_create = pageFB.comment.create(object_id=comment.id, message=msgData[:8000])

            creationDate = datetime.fromisoformat(comment.created_time.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            difference = now - creationDate

            # Comprobar si la diferencia es menor que una hora
            oneMinute = timedelta(minutes=1)
            # if(difference < oneMinute):
                
            #    print(comment.created_time)
            # pageFB.delete_object(object_id=comment.id)
        # pageFB.comment.get_info(comment_id=post.id)
        # time.sleep(60)
    break
    
# print(posts, type(posts))

print("Fin programa")
