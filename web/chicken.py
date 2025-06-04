from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_timer_time(text):
    url = 'https://myfuncapp1111.azurewebsites.net/api/smart_timer_trigger?code=Pm4ivGYiHoYj9WCVvm73lT35lILnSTahESELxZiFKFunAzFux_MHTA=='

    body = {'text': text}

    response = requests.post(url, json=body)
    print(f"Response status: {response.status_code}, Response body: {response.text}")

    if response.status_code != 200:
        payload = {
            'seconds' : 0,
            'index' : [],
            'timer_names': [],
            'message' : 'Did not recognize intent, please try again.'
        }
        return payload
    
    payload = response.json()
    return payload #return payload a list [total_seconds:int, message:str]


def create_timer(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours >= 1:
        timer_message = (f"Timer started for {hours} hours, {minutes} minutes and {seconds} seconds")
    elif minutes >= 1:
        timer_message = (f"Timer started for {minutes} minutes and {seconds} seconds")    
    else:
        timer_message = (f"Timer started for {seconds} seconds")
    
    print(timer_message)
    return timer_message

@app.route('/process_text', methods=['POST'])
def process_text():
    
    data = request.json
    text = data.get('text', '')
    
    if text != "":
        timer_message = ''
        index = []
        timer_names = []
        
        response_data= get_timer_time(text)
        print(response_data)
        
        print(f"Processing text: {text}")
        seconds = response_data['seconds']
        if seconds > 0:
            timer_message = create_timer(seconds)
        elif seconds == 0:
            timer_message = response_data['message']
            index = response_data['index']
            timer_names = response_data['timer_names']
            
        response = {
            'seconds': seconds,
            'timerMessage': timer_message,
            'index': index,
            'timerNames': timer_names
        }
        return jsonify(response)    

if __name__ == '__main__':
    app.run(debug=True)