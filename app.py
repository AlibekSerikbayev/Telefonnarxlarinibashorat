import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def main():
    predict()

def predict():
    markalar = load_data()

    st.title('Telefon narxini bashorat qilish ilovasi 📱')

    selected_brand = marka_index(markalar, st.selectbox('Brendni tanlang.', markalar['brands'].tolist()))
    selected_os = isletim_sistemi(st.radio("Operatsion tizim", ["Android", "IOS"]))
    selected_cpu = st.slider('CPU', 1.0, 3.5, 0.2)
    selected_dahili_hafiza = st.number_input('Ichki xotira (GB)', 4, 1024)
    selected_ekran_boyutu = st.slider("Ekran o'lchami", 4.5, 14.0)
    selected_kamera_cozunurlugu = st.slider("Orqa kamera ruxsati", 5, 210)
    selected_mobil_baglanti_hizi = st.slider("Mobil aloqa tezligi", 3.5, 5.5, 0.5)
    selected_pil_gucu = st.slider("Batareya quvvati (mAh)", 1500, 20000)
    selected_ram_kapasitesi = st.number_input('RAM sig\'imi (GB)', 1, 32)
    selected_on_kamera_cozunurluk = st.slider("Old kamera (MP)", 5, 120)
    selected_model = st.selectbox('Prognoz modelini tanlang.', ["Random Forest", "Gradient Boosting"])

    prediction_value = create_prediction_value(
        selected_cpu, selected_dahili_hafiza, selected_ekran_boyutu,
        selected_kamera_cozunurlugu, selected_mobil_baglanti_hizi,
        selected_pil_gucu, selected_ram_kapasitesi,
        selected_on_kamera_cozunurluk, selected_os, selected_brand
    )
    prediction_model = load_models(selected_model)

    if st.button("Bashorat qiling"):
        result = predict_models(prediction_model, prediction_value)
        if result is not None:
            st.success('Bashorat muvaffaqiyatli')
            st.balloons()
            st.write(f"Taxminiy narx: {result} TL")
        else:
            st.error('Bashorat qilishda xatolik yuz berdi..!')

def load_data():
    try:
        markalar = pd.read_csv("brands.csv")
        return markalar
    except Exception as e:
        st.error(f"Ma'lumotlarni yuklashda xatolik: {e}")
        return pd.DataFrame()

def load_models(modelName):
    try:
        if modelName == "Random Forest":  
            return joblib.load("phones_random_forest.pkl")
        elif modelName == "Gradient Boosting":
            return joblib.load("phones_gradient_boosting.pkl")
    except Exception as e:
        st.error(f"Modelni yuklashda xatolik: {e}")
        return None

def marka_index(markalar, marka):
    return markalar[markalar["brands"] == marka].index.values[0]

def isletim_sistemi(isletim_sistemi):
    return 0 if isletim_sistemi == "Android" else 1

def create_prediction_value(cpu, dahili_hafiza, ekran_boyutu, kamera_cozunurlugu, mobil_baglanti_hizi, pil_gucu, ram_kapasitesi, on_kamera_cozunurluk, isletim_sistemi, brands):
    return pd.DataFrame({
        "cpu": [cpu],
        "ichki_xotira": [dahili_hafiza],
        "ekran_olchami": [ekran_boyutu],
        "kamera_olchamlari": [kamera_cozunurlugu],
        "mobil_ulanish_tezligi": [mobil_baglanti_hizi],
        "batareya_quvvati": [pil_gucu],
        "RAM_sigimi": [ram_kapasitesi],
        "kameradagi_ravshanlik": [on_kamera_cozunurluk],
        "operatsion_tizim": [isletim_sistemi],
        "brendlar": [brands]
    })

def predict_models(model, res):
    try:
        return str(model.predict(res)[0])
    except Exception as e:
        st.error(f"Bashorat qilishda xatolik: {e}")
        return None

if __name__ == "__main__":
    main()



# import streamlit as st
# import pandas as pd 
# import numpy as np
# import joblib

# def main():       
#     predict()

# def predict():
#     # Markalar va modellarni yuklash
#     markalar = load_data()
    
#     # Foydalanuvchi interfeysi va qiymatlarni olish
#     st.title('Salom, *Streamlit! Mashinani o\'rganish telefonini bashorat qilish ilovasiga xush kelibsiz!* 👨‍💻')

#     selected_brand = marka_index(markalar, st.selectbox('Brendni tanlang.', markalar['brands'].tolist()))
    
#     selected_os = isletim_sistemi(st.radio("Operatsion tizim", ["Android", "IOS"]))

#     selected_cpu = st.slider('CPU', min_value=1.0, max_value=3.5, step=0.2)
#     st.write("CPU: " + str(selected_cpu) + " GHz")

#     selected_dahili_hafiza = st.number_input('Ichki xotira', min_value=4, max_value=1024)
#     st.write("Ichki xotira: " + str(selected_dahili_hafiza) + " GB")

#     selected_ekran_boyutu = st.slider("Ekran o'lchami", min_value=4.5, max_value=14.0)
#     st.write("Ekran o'lchami: " + str(selected_ekran_boyutu) + " dyuym")

#     selected_kamera_cozunurlugu = st.slider("Orqa kamera ruxsati", min_value=5, max_value=210)
#     st.write("Orqa kamera ruxsati: " + str(selected_kamera_cozunurlugu) + " MP")

#     selected_mobil_baglanti_hizi = st.slider("Mobil aloqa tezligi", min_value=3.5, max_value=5.5, step=0.5)
#     st.write("Mobil aloqa tezligi: " + str(selected_mobil_baglanti_hizi) + " G")

#     selected_pil_gucu = st.slider("Batareya quvvati", min_value=1500, max_value=20000)
#     st.write("Batareya quvvati: " + str(selected_pil_gucu) + " mAh")

#     selected_ram_kapasitesi = st.number_input('Ram sig\'imi', min_value=1, max_value=32)
#     st.write("Ram sig'imi: " + str(selected_ram_kapasitesi) + " GB")

#     selected_on_kamera_cozunurluk = st.slider("Old kamera", min_value=5, max_value=120)
#     st.write("Old kamera: " + str(selected_on_kamera_cozunurluk) + " MP")

#     selected_model = st.selectbox('Prognoz modelini tanlang.', ["Random Forest", "Gradient Boosting"])

#     prediction_value = create_prediction_value(selected_cpu, selected_dahili_hafiza, selected_ekran_boyutu,
#                                                selected_kamera_cozunurlugu, selected_mobil_baglanti_hizi, selected_pil_gucu, 
#                                                selected_ram_kapasitesi, selected_on_kamera_cozunurluk, selected_os, selected_brand)
#     prediction_model = load_models(selected_model)

#     if st.button("Bashorat qiling"):
#         result = predict_models(prediction_model, prediction_value)
#         if result is not None:
#             st.success('Bashorat muvaffaqiyatli')
#             st.balloons()
#             st.write("Taxminiy narx: " + result + " TL")
#         else:
#             st.error('Bashorat qilishda xatolik yuz berdi..!')

# # Brendlar uchun csv fayli
# def load_data():
#     try:
#         markalar = pd.read_csv("brands.csv")
#         return markalar
#     except Exception as e:
#         st.error(f"Ma'lumotlarni yuklashda xatolik: {e}")
#         return pd.DataFrame()  # Bo'sh DataFrame qaytarish

# # Modelni yuklash
# def load_models(modelName):
#     try:
#         if modelName == "Random Forest":  
#             rf_model = joblib.load("phones_random_forest.pkl")
#             return rf_model
#         elif modelName == "Gradient Boosting":
#             rf_model = joblib.load("phones_gradient_boosting.pkl")
#             return rf_model
#         else:
#             st.error("Modelni yuklashda xatolik yuz berdi..!")
#             return None
#     except Exception as e:
#         st.error(f"Modelni yuklashda xatolik: {e}")
#         return None

# # Marka indexini olish
# def marka_index(markalar, marka):
#     index = markalar[markalar["brands"] == marka].index.values[0]
#     return index

# # Operatsion tizim uchun raqamli qiymat berish
# def isletim_sistemi(isletim_sistemi):
#     return 0 if isletim_sistemi == "Android" else 1

# # Bashorat qiymatini yaratish
# def create_prediction_value(cpu, dahili_hafiza, ekran_boyutu, kamera_cozunurlugu, mobil_baglanti_hizi, pil_gucu, ram_kapasitesi, on_kamera_cozunurluk, isletim_sistemi, brands):
#     res = pd.DataFrame(data={
#         "cpu": [cpu],
#         "ichki_xotira": [dahili_hafiza],
#         "ekran_olchami": [ekran_boyutu],
#         "kamera_olchamlari": [kamera_cozunurlugu],
#         "mobil_ulanish_tezligi": [mobil_baglanti_hizi],
#         "batareya_quvvati": [pil_gucu],
#         "RAM_sigimi": [ram_kapasitesi],
#         "kameradagi_ravshanlik": [on_kamera_cozunurluk],
#         "operatsion_tizim": [isletim_sistemi],
#         "brendlar": [brands]
#     })
#     return res

# # Modelni bashorat qilish
# def predict_models(model, res):
#     try:
#         # Modeldan bashorat olish
#         result = model.predict(res)
#         return str(result[0])  # Birinchi elementni qaytarish
#     except Exception as e:
#         st.error(f"Bashorat qilishda xatolik: {e}")
#         return None

# if __name__ == "__main__":
#     main()