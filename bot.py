import requests

from bottle import (  
    Bottle,run, post, response, request as bottle_request
)
from PyDictionary import PyDictionary




class BotHandler:
    BOT_URL=None

    def get_chat_id(self,data):  
        """
        Method to extract chat id from telegram request.
        """
        chat_id = data['message']['chat']['id']

        return chat_id


    def get_message(self,data):  
        """
        Method to extract message id from telegram request.
        """
        message_text = data['message']['text']
        return message_text

    def send_message(self,prepared_data):  
        """
        Prepared data should be json which includes at least `chat_id` and `text`
        """ 
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)

class TelegramBot(BotHandler,Bottle):
    BOT_URL = 'https://api.telegram.org/bot787655486:AAHaislMJxQziBM4Rsv0CTcT3i1wvLkjk5s/'

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")

    def change_text_message(self,text):  
        """
        To Get the Word Meaning 
        """
        dictionary=PyDictionary()
        # try:
        dict=dictionary.meaning(text)
        keys=dict.keys()
        stri=''
        for key in keys:
            stri = stri + 'the part of speech is '
            stri = stri + key
            stri = stri + ' and the meaning is '
            ar=dict[key]
            y=len(ar)
            t=0
            for mean in ar:
                if t<y-1:
                    stri = stri + ' '
                    stri = stri + mean
                    stri = stri + ' and other meaning may be  '
                else :
                    stri = stri + mean
                    stri = stri +' .'

                t=t+1

        return stri
        # except:
        #     return "Word Meaning Not found, sorry !!!"
    

    def prepare_data_for_answer(self,data):  
        answer = self.change_text_message(self.get_message(data))

        json_data = {
            "chat_id": self.get_chat_id(data),
            "text": answer,
        }

        return json_data

    def post_handler(self):
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)

        return response


if __name__ == '__main__':  
    app = TelegramBot()
    app.run(host='localhost', port=8080)