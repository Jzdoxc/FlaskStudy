from flask import Flask,render_template
from flask.ext.script import Manager
app=Flask(__name__)

@app.route('/')
def index():
	return  render_template('index.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

manager = Manager(app)

if __name__=='__main__':
	manager.run()