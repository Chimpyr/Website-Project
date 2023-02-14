from flask import Flask
app = Flask(__name__)   #instatntiating flask app

@app.route('/')         #Decorator / route / View
def index():            #function associated with the decorator
   print ('Hello')      #output on server side only (good for debugging)
   return '<html><body><h1>Hello Flask - Web Development</h1></body></html>'
   #return sends the reponse to client 
   
@app.route('/food')         #Decorator / route / View
def food():            #function associated with the decorator
   print ('Hello1')      #output on server side only (good for debugging)
   return '<html><body><h1>Food</h1></body></html>'
   #return sends the reponse to client 

#if __name__ == '__main__':   
#   app.run(debug = True)
if __name__ == '__main__':    #you can skip this if running app on terminal window
    for i in range(13000, 18000):
      try:
         app.run(debug = True, port = i)
         break
      except OSError as e:
         print("Port {i} not available".format(i))