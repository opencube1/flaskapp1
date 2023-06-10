from flask import Flask, render_template, request
import streamlit as st
import pandas as pd
import numpy as np

app = Flask(__name__,template_folder='Template')

@app.route('/', methods=['GET', 'POST'])
 
def main():
    adress_list = []   
    # If a form is submitted
    if request.method == "POST":
          
        # Get values through input bars
        PC = request.form.get("height")
        
        
        df = pd.read_csv(r"C:\Users\ASUS\Desktop\App\PSD.csv")
        column_names=  ["Unique","Price",'Date',"Postcode",'Property_Type','Old_New','Duration','PAON','SAON','Street','Locality','Town_City','District','County','PPD','RecordStatus']
        df.columns = column_names
        df['Date'] = pd.to_datetime(df['Date'])
        df['Adress'] = df['PAON'].fillna('') +'  ' + df['Street'].fillna('') + '  ' + df['Locality'].fillna('') + '  ' + df['Town_City'].fillna('')
        df['Unique_House'] = df['PAON'].astype(str) + df['Postcode'].astype(str)
        df.rename(columns = {'Property_Type':'Property Type'}, inplace = True) 
        df.loc[df['Property Type'] =='T','Property Type'] = 'Terraced'
        df.loc[df['Property Type'] == 'S','Property Type'] = 'Semi-Detached'
        df.loc[df['Property Type']== 'D','Property Type'] = 'Detached'     
        df.loc[df['Property Type'] == 'F','Property Type'] = 'Flat'
        df.loc[df['Property Type'] == 'O','Property Type'] = 'Other'
        df.loc[df['Duration'] == 'F','Duration'] = 'Freehold'
        df.loc[df['Duration'] == 'L','Duration'] = 'Leasehold'
        adress_list = df[df['Postcode']==PC]['Adress']
        adress_list = list(dict.fromkeys(adress_list))
        opt = request.form.get("option")
        target = df[df['Adress']==opt][['Date','Property Type','Price','Duration']]
        target['Date'] = pd.to_datetime(target['Date'])
        target['Date'] = target['Date'].dt.strftime("%d %b %Y")
        target = target.set_index(target.columns[0]).reset_index()
        table_html = target.to_html()
        return render_template("website.html", adress_list=adress_list,table_html=table_html)
        
    else:
        return render_template("website.html", adress_list=adress_list)
        
        
    
    



# Running the app
if __name__ == '__main__':
    app.run(debug = True)