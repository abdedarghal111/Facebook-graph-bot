from dotenv import load_dotenv
from pyfacebook import GraphAPI, FacebookApi
import requests
import os

load_dotenv()

# api = GraphAPI(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], application_only_auth=True)
# fb = FacebookApi(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], application_only_auth=True)
# graph = GraphAPI(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], access_token=os.environ['USER_ACCESS_TOKEN'])
userFB = FacebookApi(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], access_token=os.environ['USER_ACCESS_TOKEN'])


user = userFB.user.get_info(user_id="me")


# obtener token de publicación
response = requests.get(f"https://graph.facebook.com/{user.id}/accounts?access_token={os.environ['USER_ACCESS_TOKEN']}")

pageFB = FacebookApi(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], access_token=response.json()['data'][0]['access_token'])

# print(user)

accounts = userFB.user.get_accounts(user_id=user.id)
# print(accounts)
page = accounts.data[0]
# print(page)

# graph.get_full_connections(page.id)
posts = pageFB.page.get_posts(object_id=page.id)

for post in posts.data:
    pageFB.comment.create(object_id=post.id, message="hola")

    comments = pageFB.page.get_comments(object_id=post.id)
    for comment in comments.data:
        print(comment)
        # pageFB.delete_object(object_id=comment.id)
    # pageFB.comment.get_info(comment_id=post.id)
# print(posts, type(posts))

print("Fin programa")
