from flask import Flask, render_template, request
import numpy as np
from knn import *
import pandas as pd
import json
import plotly
import plotly.express as px
from plotly.graph_objs import *


plotly_csv = pd.read_csv('./plotly.csv')



app = Flask(__name__,template_folder='html_templates')#initialize flask
app.config['secret_key'] = 'afhdihudsjkhcns' #secure the cookie for section data, never share the secret key in production

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/visualizations')
def visualization():
    df=plotly_csv

    fig = px.bar(df, x='fetal_health' , y='values', color='attributes', barmode='group',template='none')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plot.html',graphJSON=graphJSON)

@app.route('/Fetal_Health_Predictor')
def predictor():
    return render_template('predictor.html')

@app.route('/fetal_status', methods=["GET"])
def fetal_status():
    baseline_value=request.args.get("bv")
    accelerations=request.args.get("accelerations")
    fetal_movement=request.args.get("fetalmov")
    uterine_contractions=request.args.get("uterinecont")
    light_decelerations=request.args.get("LDs")
    severe_decelerations=request.args.get("SDs")
    prolonged_decelerations=request.args.get("PDs")
    abnormal_short_term_variability=request.args.get("percentshort")
    mean_value_of_short_term_variability=request.args.get("meanshort")
    percentage_of_time_with_abnormal_long_term_variability=request.args.get("percentlong")
    mean_value_of_long_term_variability=request.args.get("meanlong")
    
    sample_list = [baseline_value,accelerations,fetal_movement,uterine_contractions,light_decelerations,severe_decelerations,prolonged_decelerations,abnormal_short_term_variability,mean_value_of_short_term_variability,percentage_of_time_with_abnormal_long_term_variability,mean_value_of_long_term_variability]
    prediction = knn(X_test=np.array(sample_list).reshape(1,-1))
    try:
        prediction.item() in [1,2,3]
    except:
        raise Exception("Invalid values inputted.")
    finally:
        if prediction == 1:
            message = "Congratulations! KNN prediction shows that the fetal status is Normal!"
        elif prediction == 2:
            message = "KNN prediction shows that the fetal status is suspected to be pathological."
        elif prediction ==3:
            message = "KNN prediction shows that the fetal status is pathological." 
        return render_template('fetal_status.html', message = message)

    
    



        


if __name__ == "__main__":
    app.run(debug=True,port= 5006)
