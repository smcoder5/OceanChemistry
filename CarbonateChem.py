import streamlit as s
import numpy as n

pK1=lambda T,s:-43.6977-0.0129037*s+1.364*10**-4*s*s+2885.378/T+7.045159*n.log(T)

pK2=lambda T,s:-452.094+13.142162*s-8.101*10**-4*s*s+21263.61/T+68.483143*n.log(T)+(-581.4428*s+0.259601*s*s)/T-1.967035*s*n.log(T)

henry=lambda T,s:n.exp(-60.2409 + 93.4517*(100/T) + 23.3585*n.log(T/100) + s*(0.023517 - 0.023656*(T/100)+0.0047036*(T/100)))


def pH(a,b,c):
    rt=-b-n.sqrt(b*b-4*a*c) 
    
    rt=rt/(2*a)
    return -1*n.log10(rt)

def hco3(pK1,co2,pH):
    k1,h=10**(-1*pK1) , 10**(-1*pH)
    return co2*k1/h

def co3(pK1,pK2,co2,pH):
    k1,k2,h=10**(-1*pK1) ,10**(-1*pK2) , 10**(-1*pH)
    return co2*k1*k2/h/h

def main():
    temp=s.slider("Enter the Temperature in Degree Celcius",5,45)
    salt=s.slider("Enter the Salinity in ‰",10,45)
    fug=s.slider("Eneter the fugaciy of CO₂ in ",100,1000)
    dic=s.slider("Enter the value of Dissolved Inorganic Carbon in μM",1000,5000) 

    temp=273.15+temp
    co2,dic=henry(temp,salt)*fug*10**-6,dic*10**-6
    #pH=pH(1-dic/co2,10**(-1*pK1(temp,salt)),10**(-1*pK1(temp,salt))*10**(-1*pK2(temp,salt))) 

    ph=pH(1-dic/co2,10**(-1*pK1(temp,salt)),10**(-1*pK1(temp,salt))*10**(-1*pK2(temp,salt)))
    c=s.columns(2)
    with c[0]:
        c[0].metric("pK1",value=round(pK1(temp,salt),2))
    with c[1]:
        c[1].metric("pK2",value=round(pK2(temp,salt),2))

    co=s.columns(3)
    with co[0]:
        co[0].metric("CO₂(aq)",value=round(co2*10**6))  
    with co[1]:
        co[1].metric("HCO₃⁻",value=round(hco3(pK1(temp,salt),co2,pH)*10**6))
    with co[2]:
        co[2].metric("CO₃²⁻",value=round(co3(pK1(temp,salt),pK2(temp,salt),co2,pH)*10**6))
    del co
    co=s.columns(2)
    with co[0]:
        co[0].metric("Carbonate Alkalinity",value=round(hco3(pK1(temp,salt),co2,pH)+2*co3(pK1(temp,salt),pK2(temp,salt),co2,pH)*10**6))  
    with co[1]:
        co[1].metric("pH",value=round(pH,2))
    
    



if __name__=="__main__":
    s.set_page_config(layout="wide") 
    main()
