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

# print(response.text)
pageFB = FacebookApi(app_id=os.environ['APP_ID'], app_secret=os.environ['APP_SECRET_TOKEN'], access_token=response.json()['data'][0]['access_token'])

# exit()

print(user)

accounts = userFB.user.get_accounts(user_id=user.id)
# print(accounts)
page = accounts.data[0]
print(page)

print(pageFB.get_object(object_id=f"{page.id}/posts"))
# graph.get_full_connections(page.id)
# posts = fb.page.get_posts(object_id=page.id)
# print(posts)
