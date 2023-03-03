import pandas as pd
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
import ta
import xlsxwriter
from incele import analiz
from inceleKO import analizKO
from veriler import Veri
import stratejiler as strj

Veri_düzen = Veri()

df = Veri_düzen.veri_al(ürün_adı="XAUUSD",periyot="1D",uzaklık=2000)


Veri_düzen.veri_indikatör_ekle_ATR(df=df,periyot=21)
"""Veri_düzen.veri_indikatör_ekle_RSI(df=df,periyot=14)
Veri_düzen.veri_indikatör_ekle_EMA(df=df,periyot=14)
Veri_düzen.veri_indikatör_ekle_EMA(df=df,periyot=21)
Veri_düzen.ortalama_kesişimi_veri(df=df,hızlı_ad="EMA14",yavaş_ad="EMA21",column_name="Kesişim")"""

# destekler = Veri_düzen.pivot_destekler(df=df,soldan=6,sağdan=6)




"""işlemler,TARİH,KAPANIŞ,İNDEXKLER = strj.ATR_ile_işlem_giriş_çıkış(df=df,Buy_TP=5,Buy_SL=2,Sell_SL=2,Sell_TP=5)"""

işlemler = Veri_düzen.metatrader_backtest_verisi_al("deneme_oku")
print(len(işlemler),"sayıda işlem var")


denemem2 = analiz("bakalımddd",işlemler=işlemler)
denemem2.excele_yaz()

#denemem2.portföy_işlem_göster(.1)
# denemem1 = analizKO("내 방법1",işlemler=işlemler)
# denemem1.mum_grafiği(df=df,EMA1="EMA8")




# 금 사고 +9달러 이익 되면 팔고,-5달러 손해 되면 또 파는 방법


# Aynı stratejiyi atr ilede dene karşılaştır hangisi daha iyi...