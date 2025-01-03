from flask import Flask, render_template , request , redirect , send_from_directory
import csv


app = Flask(__name__)

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route("/")
def my_home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def works(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email}, {subject}, {message}')                               


def write_to_csv(data):
    try:
        with open('database.csv', mode='a', newline='') as database2:
            email = data['email']
            subject = data['subject']
            message = data['message']
            csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
            csv_writer.writerow([email, subject, message])                                      
    except Exception as e:
        print(f'Error writing to CSV: {e}')



@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return "Did not save to database"
    else:
        return "Something went wrong. Try again"


if __name__ == '__main__':
    app.run(debug=True)