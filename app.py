import streamlit as st
import pandas as pd 
import numpy as np
import joblib
from PIL import Image,ImageEnhance
import matplotlib.pyplot as plt
import seaborn as sns


def main():       
    predict()
           

def predict():

    # Markalar ve Modellerin yüklenmesi
    markalar = load_data()
    
    # Kullanıcı arayüzü ve değer alma
    st.title('Salom, * Streamlit! Mashinani organish telefonini bashorat qilish ilovasiga xush kelibsiz!* 👨‍💻')

    selected_brand = marka_index(markalar,st.selectbox('Brendni tanlang.',markalar))
    
    selected_os=isletim_sistemi(st.radio("Operatsion tizim",["Android","IOS"]))

    selected_cpu = st.slider('CPU',min_value=1.0,max_value=3.5,step=0.2)
    st.write("CPU :"+str(selected_cpu)+" GHz")

    selected_dahili_hafiza = st.number_input('Ichki xotira',min_value=4,max_value=1024)
    st.write("Ichki xotira :"+str(selected_dahili_hafiza)+" GB")

    selected_ekran_boyutu = st.slider("Ekran o'lchami",min_value=4.5,max_value=14.0)
    st.write("Ekran o'lchami:"+str(selected_ekran_boyutu)+" dyuym")

    selected_kamera_cozunurlugu = st.slider("Orqa kamera ruxsati",min_value=5,max_value=210)
    st.write(" :"+str(selected_kamera_cozunurlugu)+"Orqa kamera ruxsati MP")

    selected_mobil_baglanti_hizi = st.slider("Mobil aloqa tezligi",min_value=3.5,max_value=5.5,step=0.5)
    st.write("Mobil aloqa tezligi :"+str(selected_mobil_baglanti_hizi)+" G")

    selected_pil_gucu = st.slider("Batareya quvvati",min_value=1500,max_value=20000)
    st.write("Batareya quvvati :"+str(selected_pil_gucu)+" mAh")

    selected_ram_kapasitesi= st.number_input('Ram sigimi',min_value=1,max_value=32)
    st.write("Ram sig'imi :"+str(selected_ram_kapasitesi)+" GB")

    selected_on_kamera_cozunurluk = st.slider("Old kamera",min_value=5,max_value=120)
    st.write("Old kamera:"+str(selected_on_kamera_cozunurluk)+" MP")

    selected_model = st.selectbox('Prognoz modelini tanlang.',["Random Forest","Gradient Boosting"])


    prediction_value = create_prediction_value(selected_cpu,selected_dahili_hafiza,selected_ekran_boyutu,
                                               selected_kamera_cozunurlugu,selected_mobil_baglanti_hizi,selected_pil_gucu,selected_ram_kapasitesi,selected_on_kamera_cozunurluk,selected_os,selected_brand)
    prediction_model = load_models(selected_model)


    if st.button("Bashorat qiling"):
            result = predict_models(prediction_model,prediction_value)
            if result != None:
                st.success('Bashorat muvaffaqiyatli')
                st.balloons()
                st.write("Taxminiy narx: "+ result + "TL")
            else:
                st.error('Bashorat qilishda xatolik yuz berdi..!')
    

#Brendlar uchun csv fayli
def load_data():
    markalar = pd.read_csv("brands.csv")
    return markalar

#
def load_models(modelName):
    if modelName == "Random Forest":  
        rf_model = joblib.load("phones_random_forest.pkl")
        return rf_model
    if modelName=="Gradient Boosting":
        rf_model=joblib.load("phones_gradient_boosting.pkl")
        return rf_model
    else:
        st.write("Modelni yuklashda xatolik yuz berdi..!")
        return 0

#marka indexi bulma
def marka_index(markalar,marka):
    index = int(markalar[markalar["brands"]==marka].index.values)
    return index

#isletim sistemi için sayısal değer atama
def isletim_sistemi(isletim_sistemi):
    if isletim_sistemi == "Android":
        return 0
    else:
        return 1


def create_prediction_value(cpu,dahili_hafiza,ekran_boyutu,kamera_cozunurlugu,mobil_baglanti_hizi,pil_gucu,ram_kapasitesi,on_kamera_cozunurluk,isletim_sistemi,brands):
    res = pd.DataFrame(data = 
            {"cpu":[cpu],"ichki_xotira":[dahili_hafiza],"ekran_olchami":[ekran_boyutu],
                    "kamera_olchamlari":[kamera_cozunurlugu],"mobil_ulanish_tezligi":[mobil_baglanti_hizi],"batareya_quvvati":[pil_gucu],"RAM_sigimi":[ram_kapasitesi],
                    "kameradagi_ravshanlik":[on_kamera_cozunurluk],"operatsion_tizim":[isletim_sistemi],"brendlar":[brands]})
    return res

#modelni ishga tushiring
def predict_models(model,res):
    result = str(int(model.predict(res))).strip('[]')
    return result

if __name__ == "__main__":
    main()