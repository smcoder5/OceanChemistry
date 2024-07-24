import streamlit as s
import CarbonateChem as ccm
import CarbonateConcn as ccn



s.set_page_config(page_title='Sea Water Chemistry',layout='wide')
with s.sidebar:
    
    rad=s.radio("Ocean Data Set Page",['Carbonate Chemistry','Carbonate Concentration']) 

if(rad=='Carbonate Chemistry'):
    ccm.main()

elif(rad=='Carbonate Concentration'):
    ccn.main()
