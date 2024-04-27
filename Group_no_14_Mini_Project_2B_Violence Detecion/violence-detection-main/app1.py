from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Here you can perform authentication logic
    # For simplicity, let's assume any username/password is valid
    if username and password:
        return redirect(url_for('main'))
    else:
        return render_template('index.html', message='Invalid username or password')


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
