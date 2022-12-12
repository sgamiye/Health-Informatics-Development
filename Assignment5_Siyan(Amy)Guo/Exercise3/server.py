import pandas as pd
import csv
from flask import Flask, render_template, request

data=pd.read_csv('./original_data.csv',header=4)#start from where the column titles are

data=data[0:53] # clean out unecessary content at the end

data['State'] = data['State'].map(lambda x: str(x)[:-3]) # clean out the source number 

#simplify some column names
data=data.rename(columns={'Age-Adjusted Incidence Rate([rate note]) - cases per 100,000' : 'Age-Adjusted Incidence Rate- cases per 100k',
                         'Recent 5-Year Trend ([trend note]) in Incidence Rates' : 'Recent 5-Year Trend in Incidence Rates'})

data['State']=[st.lower() for st in data['State']] #make state names lower-cased in order to make search for state case-insensitive

pd.DataFrame.to_csv(data,'./cleaned_data.csv')

state_lst=["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


app = Flask(__name__,template_folder='html_templates')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/info", methods=["GET"])
def info():
    state=request.args.get("state")
    try:
        state.lower() in [statename.lower() for statename in state_lst]
        state=state.lower()
        aarate = data[data['State']==state]['Age-Adjusted Incidence Rate- cases per 100k'].item()
        return render_template("state.html", state=state,aarate=aarate)
    except:
        state.lower() not in [statename.lower() for statename in state_lst]
        raise Exception("The state name inputted is invalid.")

@app.route("/state")
def state_page():
    return render_template("index.html")

@app.route("/state/<string:state>")
def state_api(state):
    return {
        'state' : state.lower(),
        'age-adjusted incidence rate (cases per 100k)' : data[data['State']==state]['Age-Adjusted Incidence Rate- cases per 100k'].item()
    }

if __name__ == "__main__":
    app.run(debug=True,port= 5003)