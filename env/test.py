from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

test = Flask(__name__)
test.config['SQLALCHEMY_DATABASE_URI']='sqlite:///new.db'
db=SQLAlchemy(test)

class abcd(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	completed = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id



@test.route('/', methods=['POST','GET'])
def index():
	if request.method == 'POST':
		names=request.form['content']
		new_name=abcd(content=names)
		try:
			db.session.add(new_name)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue adding the student';
	else:
		tasks = abcd.query.order_by(abcd.date_created).all()
		return render_template('index.html', tasks=tasks)

@test.route('/delete/<int:id>')
def delete(id):
	del_s = abcd.query.get_or_404(id)
	
	try:
		db.session.delete(del_s)
		db.session.commit()
		return redirect('/')
	except:
		return 'There was an issue';			
		
if __name__=="__main__":
	test.run(debug=True)