import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests
account_sid = 'ACd5265bb095b5a8a658818c04d54f0cce'
auth_token = '8c0c9a72e606c7a4d2e68b1954905537'
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def registration_form():
    return render_template('form.html')

@app.route('/form', methods=['POST', 'GET'])
def registration_details():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['destination_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phone']
    id_proof = request.form['aadhar']
    date = request.form['date']
    full_name = first_name + " " + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(from_='whatsapp:+14155238886',
                               to='whatsapp:+918338909090',
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " " + "To" + " " + destination_dt + " "
                                      + "Has" + " " + status + " On" + " " + date + " " )

        return render_template('display.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)

    else:
        status = 'NOT CONFIRMED'
        client.messages.create(from_='whatsapp:+14155238886',
                               to='whatsapp:+918338909090',
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " " + "To" + " " + destination_dt + " "
                                    + "Has" + " " + status + " On" + " " + date + " " + ", Apply later")

        return render_template('display.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)


if __name__ == '__main__':
    app.run(port=9001, debug=True)