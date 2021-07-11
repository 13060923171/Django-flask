from flask import *


app = Flask(__name__)

name = ''
login = ''
@app.route('/<int:id>', methods=['GET', 'POST'])
@app.route('/', methods=('GET', 'POST'))
def index(id=None):
    global name, login
    if request.method == 'POST':
        if request.form.get('username') == 'Ansel&Kant' and request.form.get('password') == '120823':
            login = 'success'
            name = 'admin'
            return render_template('myhouse-2.html', name=name, login=login)
        else:
            login = 'fail'
        if id == 2:
            return render_template('love-3.html')
        if id == 3:
            return render_template('timelines-4.html')
        if id == 4:
            return render_template('circuit-5.html')
        if id == 5:
            return render_template('heartbeat-6.html')
        if id == 6:
            return render_template('record-7.html')
        if id == 7:
            return render_template('wish_list-8_1.html')
        if id == 8:
            return render_template('finally-9.html')

    return render_template('register-1.html')

if __name__ == '__main__':
    app.run()