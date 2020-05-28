import flask

app = flask.Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    form = flask.request.form.to_dict()
    # replace with checking user id and password in sql database
    # password hashing/salting
    if form['id'] == 'adv' and form['password'] == '123':
        return flask.render_template('advisor_home.html')
    else:
        return flask.render_template('index.html')

@app.route('/advisor_home')
def advisor_home():
    return flask.render_template('advisor_home.html')

@app.route('/forms')
def forms():
    return flask.render_template('forms.html')

@app.route('/students')
def students():
    return flask.render_template('students.html')

@app.route('/')
def main():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()