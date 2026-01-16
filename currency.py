# import requests
# response=requests.get(url="https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.json")
# data=response.json()
# print((data)['eur']['pkr'])
input1="United States (US) : USD - US Dollar"
country1=input1.split(':')[0].split(' ')[-2].strip("()").lower()
print(country1)