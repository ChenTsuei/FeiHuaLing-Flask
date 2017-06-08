# -*- coding:utf-8 -*-
import codecs

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.before_request
def before_request():
    session['word'] = None

class WordForm(FlaskForm):
    word = StringField(u'请输入您要查询的字或词', validators=[Required()])
    submit = SubmitField(u'提交')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    lines = [] 
    form = WordForm()
    if form.validate_on_submit():
        word = form.word.data
        form.word.data = ''
        lines = query(word)
        if len(lines) > 0:
            flash(u'共搜索到%d条包含"%s"的诗句' % (len(lines), word), 'success')
            if u'颖' in word:
                flash(u'颖颖最可爱啦hiahiahia~', 'info')
        else:
            flash(u'未找到包含"%s"的诗句' % word, 'warning')
    return render_template('index.html', form=form, lines=lines)

def query(word):
    with codecs.open('poem', 'r', encoding='utf8') as f:
        lines = [line.strip() for line in f.readlines() if word in line \
                and not line[0].isdigit()]
    return lines

if __name__ == '__main__':
    manager.run()   
