from country import countries_info
from flask import Flask,render_template,request,redirect,url_for
import os
from dotenv import load_dotenv
import requests
load_dotenv()
from datetime import datetime

year=datetime.now().strftime("%Y")

app=Flask(__name__)
app.config["SECRET_KEY"] = os.environ['FLASK_KEY']

@app.context_processor
def inject_now():
    return {'current_year': year}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/currency_converter",methods=['GET','POST'])
def currency_converter():
    
    if request.method=="POST":
        try:
            input1 = str(request.form['country1'])
            # Try parsing strict format "Country (ISO) : CurrencyCode - CurrencyName"
            if ':' in input1 and '-' in input1:
                currency1 = input1.split(':')[1].split('-')[0].strip()
                curr1_to_display = input1.split(':')[1].split('-')[1].strip()
                country1 = input1.split(':')[0].split(' ')[-2].strip('()').lower()
            # specific fix for "Country Name" input
            elif input1.strip() in countries_info:
                country_data = countries_info[input1.strip()]
                currency1 = country_data['currency_code']
                curr1_to_display = country_data['currency_name']
                country1 = country_data['iso_code'].lower()
            else:
                 return render_template("currencyConverter.html", data=countries_info, error="Invalid format for Country 1")

            input2 = str(request.form['country2'])
            if ':' in input2 and '-' in input2:
                currency2 = input2.split(':')[1].split('-')[0].strip()
                curr2_to_display = input2.split(':')[1].split('-')[1].strip()
                country2 = input2.split(':')[0].split(' ')[-2].strip('()').lower()
            elif input2.strip() in countries_info:
                country_data = countries_info[input2.strip()]
                currency2 = country_data['currency_code']
                curr2_to_display = country_data['currency_name']
                country2 = country_data['iso_code'].lower()
            else:
                return render_template("currencyConverter.html", data=countries_info, error="Invalid format for Country 2")

            rate1 = float(request.form['rate1'])
            
            response = requests.get(url=f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currency1.lower()}.json")
            if response.status_code != 200:
                 return render_template("currencyConverter.html", data=countries_info, error="Failed to fetch exchange rates")
            
            rate_data = response.json()[currency1.lower()][currency2.lower()]
            rate = round(rate1 * rate_data, 2)
            
            currency_data = {
                "rate1": rate1,
                "currency1": curr1_to_display,
                "currency2": curr2_to_display,
                "converted_rate": rate,
                "country1_code": country1,
                "country2_code": country2
            }
            return render_template("currencyConverter.html", data=countries_info, currency_info=currency_data)
        except Exception as e:
            print(f"Error: {e}")
            return render_template("currencyConverter.html", data=countries_info, error="An unexpected error occurred. Please try again.")

    return render_template("currencyConverter.html",data=countries_info)

if __name__ == "__main__":
    app.run(debug=True)
