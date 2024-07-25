import streamlit as s
import numpy as n
import pandas as p
import plotly.express as pe



pK1=lambda T,s:-43.6977-0.0129037*s+1.364*10**-4*s*s+2885.378/T+7.045159*n.log(T)

pK2=lambda T,s:-452.094+13.142162*s-8.101*10**-4*s*s+21263.61/T+68.483143*n.log(T)+(-581.4428*s+0.259601*s*s)/T-1.967035*s*n.log(T)

def hco3(pK1,pK2,pH,dic):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return dic/(h/k1+1+k2/h)

def co3(pK1,pK2,pH,dic):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return dic/(h*h/k1/k2+h/k2+1)

def co2(pK1,pK2,pH,dic):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return dic/(1+k1/h+k1*k2/h/h)
   
def main():
    s.title(" Concentration of Carbon Species in Sea Water ")
    cc=s.columns(3)
    
    with cc[0]:
        temp=s.number_input("Enter the value of Temperature ")
    with cc[1]:
        salt=s.number_input("Enter the value of Salinity")
    with cc[2]:
        dic=s.number_input("Enter the value of Dissolved Inorganic Carbon",min_value=50, max_value=5000, value="min",step=10)
   
   
    temp=temp+273.15
    
    pH=n.arange(1,12,0.01)
    
    df=p.DataFrame({'pH':pH,'Concentration':hco3(pK1(temp,salt),pK2(temp,salt),pH,dic),'Ions':['HCO3−']*pH.shape[0]})
    df=p.concat([df,p.DataFrame({'pH':pH,'Concentration':co3(pK1(temp,salt),pK2(temp,salt),pH,dic),'Ions':['CO3−']*pH.shape[0]})])
    df=p.concat([df,p.DataFrame({'pH':pH,'Concentration':co2(pK1(temp,salt),pK2(temp,salt),pH,dic),'Ions':['CO2']*pH.shape[0]})])
    
    print(df.info()) 
    fig=pe.line(df,x='pH',y='Concentration',color='Ions')
    s.plotly_chart(fig,use_container_width=True) 


    



if __name__=="__main__":
    s.set_page_config(page_title='Sea Water Dataset',layout='wide')
    main()
