# FeiHuaLing-Flask

### 想法来源

本学期伊始我用Java语言写了Android版本的飞花令，第一次写的报告也非常荣幸地成为了模范作业，但几经折腾对Andriod平台有些失望，各种莫名其妙的错误让人很非常头疼，项目也是删了改改了删，于是在做完GPS-Alarm后决心不再开发Andriod平台的项目。

相比于Java，我更加喜欢Python语言，但是苦于找不到个顺手一点的GUI库，曾经想过开发CLI界面，但发现比GUI还要困难，于是开始转战Web开发，这样我的成果也能更好的与同学分享。于是花了两三天的时间自学了Python的Flask框架，主要读的*《Flask Web开发：基于Python的Web应用开发实战》*，这本书还是很不错的，除了前面的基础知识讲解，更多的是全书贯穿着完成了一个博客系统的项目，前端框架用的Bootstrap也非常漂亮。

虽说要写Web，但是我对Html, CSS, JavaScript等技术都不是很熟悉，不过，照猫画虎总是可以的。在知乎上找到了一个专栏，*Hello, Flask!*，挺不错的，其中有个简单的项目是猜数字的，看这个UI设计的挺漂亮挺简洁，就直接拿过来用了。

![](https://github.com/ChenTsuei/FeiHuaLing-Flask/blob/master/ScreenShots/feihualing.png)

### 设计规划

开发一个Web版本的飞花令，具备以下功能：

1. 在《唐诗三百首》中查询带有特定字词的诗句
2. 将查询到的诗句一行一行的列出来
3. 点击自动百度查询此诗句

使用Python的Flask框架进行开发，选用Flask默认的Jinja作为模板语言，Bootstrap作为前端框架。基本的功能非常简单，只需要一个输入框，一个提交按钮，一个显示搜索结果的列表，由于只有唐诗三百首，所以直接使用文本文件进行存储。

### 具体实施

#### 项目结构

```
.
├── app.py
├── poem
├── requirements.txt
├── static
│  └── favicon.ico
└── templates
    ├── 404.html
    ├── 500.html
    ├── base.html
    └── index.html
```

#### 代码实现

##### 核心部分

此项目的核心部分就是一个输入框，用户点击“提交”按钮向服务器发送一个POST请求，服务器在数据库（文件）中搜索，将搜索结果返回给用户，实现如下：

```python
class WordForm(FlaskForm):
    word = StringField(u'请输入您要查询的字或词', validators=[Required()])
    submit = SubmitField(u'提交')


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
        else:
            flash(u'未找到包含"%s"的诗句' % word, 'warning')
    return render_template('index.html', form=form, lines=lines)

def query(word):
    with codecs.open('poem', 'r', encoding='utf8') as f:
        lines = [line.strip() for line in f.readlines() \
        if word in line and not line[0].isdigit()]
    return lines
```

此处的`query()`函数即是从目录下的poem文本中搜索带有word的句子，除去诗的标题和作者的名字，Python的list comprehension的优点就这样显示出来，只需要一行代码就可以返回符合以上特征的所有诗句的列表。

`index()`视图函数用来与前端交互，`@app.route('/', methods=['GET', 'POST'])`表示当用户访问url为'/'时调用该函数，并可以在此页面上发起GET和POST请求，当用户输入字或词，点击提交，此函数就会将word发送给`query()`函数，得到lines传递给前端展示。

核心代码非常简单，其他值得一提的地方也有挺多。

##### Virtualenv

命令`virtualenv`就可以创建一个独立的Python运行环境，我们还加上了参数`--no-site-packages`，这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。

在开发环境中只需使用`pip freeze > requirements.txt`记录第三方模块，然后在运行环境中使用`pip install -r requirements.txt`安装txt文件里所记录的所有第三方模块。

`virtualenv`为应用提供了隔离的Python运行环境，解决了不同应用间多版本的冲突问题。

##### Jinja2

Flask使用jinja2作为框架的模板系统，和Python交互的时候非常方便，比如飞花令中列出所有的诗句，为每个诗句创建百度搜索该诗句的链接，只需要写如下的html代码：

```html
<ul class="list-group">
    {% for line in lines %}
        <a href="http://www.baidu.com/s?wd={{ line }} " target="_blank" class="list-group-item">{{ line }}</a>
    {% endfor %}
</ul>
```

##### Flash消息

请求完成后，有时需要让用户知道状态发生了变化。这里可以使用确认消息、警告或者错误提醒。一个典型例子是，用户提交了有一项错误的登录表单后，服务器发回的响应重新渲染了登录表单，并在表单上面显示一个消息，提示用户用户名或密码错误。

这种功能是Flask的核心特性。如上面代码所示，`flash()`函数可实现这种效果。

### 最终效果

*搜索带有“花”的诗句* 

![](https://github.com/ChenTsuei/FeiHuaLing-Flask/blob/master/ScreenShots/feihualing-demo.png) 
