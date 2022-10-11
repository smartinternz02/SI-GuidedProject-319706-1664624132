from flask import Flask,render_template,request
import os
import numpy as np 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__,template_folder="templates") 
model=load_model('rock.h5')
print("Loaded model from disk")


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/intro') 
def intro():
    return render_template('intro.html')

@app.route('/image1',methods=['GET','POST'])
def image1():
    return render_template("image.html")

@app.route('/predict',methods=['GET', 'POST'])
def launch():
    if request.method=='POST':
        f=request.files['file'] 
        basepath=os.path.dirname('__file__')
        filepath=os.path.join(basepath,"uploads",f.filename)
        f.save(filepath)
        
        img=image.load_img(filepath,target_size=(64,64))
        x=image.img_to_array(img)
        x=np.expand_dims(x,axis=0)
        pred=model.predict(x)
        pred=np.argmax(pred,axis=1)
        print("prediction",pred)
        index=['Blue Calcite', 'Limestone', 'Marble', 'Olivine', 'Red Crystal']
        result=str(index[pred[0]])
        
        if (result=='Blue Calcite'):
            return render_template("0.html",showcase =  str(result))
        elif (result=='Limestone'):
            return render_template("1.html",showcase =  str(result))
        elif (result=='Marble'):
            return render_template("2.html",showcase =  str(result))
        elif (result=='Olivine'):
            return render_template("3.html",showcase =  str(result))
        else:
            return render_template("4.html",showcase =  str(result))
        
    else:
        return None
     
if __name__ == "__main__":
   # running the app
    app.run(debug=False,port=8000)