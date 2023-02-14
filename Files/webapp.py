from flask import Flask, render_template
app = Flask(__name__)

@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/about')
def about_route():
   return render_template('about.html')

@app.route('/book')
def book_route():
   return render_template('book.html')

@app.route('/login')
def login_route():
   return render_template('login.html')

@app.route('/register')
def register_route():
   return render_template('register.html')
   

if __name__ == '__main__':
    app.run(debug = True)

#Process:
#1. Put html files under templates folder             DONE
#2. Put static files (i.e. css and images and js files) under static folder      DONE
   #2a. you may create sub-folders i.e. css for CSS files, img for Images
#3. Make app i.e. .py file and create decorates/endpoints for each webpage so that you can link them using url_for()          DONE
   #3a. use render_template() to return the html page
#4. Update <link> tag in html files to refer to css by using url_for()
#5. Update <a> tag href attribute to call end point for each page by using url_for()
#6. Update <img> tag src attribute to link to images e.g., 'static/image.jpeg'
#7. Update css file if you're using background images e.g., 'static/image.jpeg'
