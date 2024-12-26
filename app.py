from flask import Flask, render_template, request, redirect, url_for
import requests
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)

app = Flask(__name__)

# Replace with your actual Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = ''
CHAT_ID = ''

def send_to_telegram(name, age, phonenumber, location, color):
    message = f"New Questionnaire Submission:\nName: {name}\nAge: {age}\nPhonenumber: {phonenumber}\nLocation: {location}\nColor: {color}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        print("Message sent to Telegram successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

# Home route to display the questionnaire
@app.route('/', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        # Process the form data
        name = request.form.get('name')
        age = request.form.get('age')
        phonenumber = request.form.get('phonenumber')
        location = request.form.get('location')
        color = request.form.get('color')
        
        print(f"Received data: Name: {name}, Age: {age}, Feedback: {phonenumber}, Location: {location}, Color: {color}")  # Debugging line
        
        # Send data to Telegram
        send_to_telegram(name, age, phonenumber, location, color)
        
        return redirect(url_for('thank_you', name=name, color=color, age=age))  # Redirect to thank you page

    return render_template('web_page.html')

# Thank you route
@app.route('/thank-you')
def thank_you():
    name = request.args.get('name', '')
    color = request.args.get('color', '')
    age = request.args.get('age', '')
    return render_template('happy_birthday.html', name=name, color=color, age=age)
if __name__ == '__main__':
    app.run(debug=True)
