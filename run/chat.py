import pyrebase
from firebase_admin import db

from datetime import datetime, date

config = {
    'apiKey': "AIzaSyAiDyIos5LDMw90C8qa5yxR7S-VEYwulRc",
    'authDomain': "piyush-chat-app.firebaseapp.com",
    'databaseURL': "https://piyush-chat-app-default-rtdb.firebaseio.com",
    'projectId': "piyush-chat-app",
    'storageBucket': "piyush-chat-app.appspot.com",
    'messagingSenderId': "797215943800",
    'appId': "1:797215943800:web:70a7d29412f8027565918d",
    'measurementId': "G-4JMD5YRQN7"
  }

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
db=firebase.database()


def createchat(user1,user2,chat_id):
  chat_user1 = db.child('user_chat_list').child(user1.id).get()
  chat_user2 = db.child('user_chat_list').child(user2.id).get()
  if(chat_user1.val()) is None:
    db.child('user_chat_list').child(user1.id).set({chat_id[1]:{'name':user2.username,
                                         'lastmessage':'you are now connected',
    }})
  else:
    db.child('user_chat_list').child(user1.id).update({chat_id[1]:{'name':user2.username,
                                                                  'lastmessage':'you are now connected',
    }})
  if(chat_user2.val()) is None:
    db.child('user_chat_list').child(user2.id).set({chat_id[0]:{'name':user1.username,
                                         'lastmessage':'you are now connected',
    }})
  else:
    db.child('user_chat_list').child(user2.id).update({chat_id[0]:{'name':user2.username,
                                                                  'lastmessage':'you are now connected',
    }})

def save_message():
  chat_user1 = db.child('message').child(chat_id_1).get()
  chat_user2 = db.child('message').child(chat_id_2).get()
  if(chat_user1.val()) is None:
    db.child('message').child(chat_id_1).set({'users':[user1.id,user2.id]})
    db.child('message').child(chat_id_1).child('messages').push({'text': msg,
                                                     'time': str(datetime.now().time()),
                                                     'date': str(date.today()),
                                                     'sender': sender_id})
  else:
    db.child('message').child('4512').child('messages').push({'text': msg,
                                                     'time': str(datetime.now().time()),
                                                     'date': str(date.today()),
                                                     'sender': sender_id})
  if(chat_user2.val()) is None:
    db.child('message').child(chat_id_2).set({'users':[user1.id,user2.id]})
    db.child('message').child(chat_id_2).child('messages').push({'text': msg,
                                                     'time': str(datetime.now().time()),
                                                     'date': str(date.today()),
                                                     'sender': sender_id})
  else:
    db.child('message').child('4512').child('messages').push({'text': msg,
                                                     'time': str(datetime.now().time()),
                                                     'date': str(date.today()),
                                                     'sender': sender_id})