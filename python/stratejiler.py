# Bu kodların amacı elimdeki stratejiyi kolayca tanımlamak ona göre backtest yapmak. Backtest edilecek stratejiler oluşturmak






def yüzdeli_işlem_giriş_çıkış(df,Buy_TP,Buy_SL,Sell_TP,Sell_SL):
    işlemler =[]
    
    yön="Buy"
    işleme_giriş_tarihi = df.loc[0].time
    işleme_giriş_fiyatı = df.loc[0].open
    işleme_giriş_index = 0
    işlemden_çıkış_tarih=0
    işlemden_çıkış_fiyat=0.0
    işlemden_çıkış_index = 0
    tp=0
    sl=0

    TARİH = []
    KAPANIŞ = []
    İNDEXKLER = []

    for i in range(15,len(df)):
        if yön=="Buy":   #Long işlemler için tek tek tp ve sl durumları
            if df.loc[i].low <= işleme_giriş_fiyatı * Buy_SL: #Stop olunuyor ise
                işlemden_çıkış_tarih = df.loc[i].time
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı * Buy_SL
                işlemden_çıkış_index = i
                tp=işleme_giriş_fiyatı * Buy_TP*df.loc[i]["ATR"]
                sl=işlemden_çıkış_fiyat
                işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işleme gir 
                yön = "Sell"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
            elif df.loc[i].high >= işleme_giriş_fiyatı * Buy_TP: #Tp olunuyor ise 
                işlemden_çıkış_tarih = df.loc[i].time
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı * Buy_TP
                işlemden_çıkış_index = i 
                tp = işlemden_çıkış_fiyat
                sl = işleme_giriş_fiyatı * Buy_SL
                işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işlem gir
                yön = "Sell"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
        else:    #Short işlemler için tek tek tp ve sl durumları
            if df.loc[i].high >= işleme_giriş_fiyatı * Sell_SL: # Stop olunuyor ise
                işlemden_çıkış_tarih = df.loc[i].time 
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı * Sell_SL
                işlemden_çıkış_index = i
                tp = işleme_giriş_fiyatı * Sell_TP
                sl = işlemden_çıkış_fiyat
                işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işleme gir
                yön = "Buy"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
            elif df.loc[i].low <= işleme_giriş_fiyatı * Sell_TP: # Tp olunuyor ise
                işlemden_çıkış_tarih = df.loc[i].time
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı * Sell_TP
                işlemden_çıkış_index = i
                tp = işlemden_çıkış_fiyat
                sl = işleme_giriş_fiyatı * Sell_SL
                işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işleme gir
                yön = "Buy"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
    for i in range(15,len(df)):
        TARİH.append(df.loc[i].time)
        KAPANIŞ.append(df.loc[i].close)
        İNDEXKLER.append(i)
    return işlemler,TARİH,KAPANIŞ,İNDEXKLER

def sayı_ile_işlem_giriş_çıkış(df,Buy_TP,Buy_SL,Sell_TP,Sell_SL,iz_süren_devreye_giriş,iz_süren_takip_mesafe):
    yön = "Buy"
    işlemler =[]
    işleme_giriş_tarihi = df.loc[0].time
    işleme_giriş_fiyatı = df.loc[0].open
    işleme_giriş_indexi = 0
    işlemden_çıkış_tarihi=0
    işlemden_çıkış_fiyatı=0.0
    işlemden_çıkış_indexi = 0
    tp=işleme_giriş_fiyatı + Buy_TP
    sl=işleme_giriş_fiyatı - Buy_SL
    TARİH = []
    KAPANIŞ = []
    İNDEXKLER = []
    iz_süren_stop_sayısı=0
    iz_süren_sl = 0
    iz_süren_sl2 = 10000
    iz_süren_sl3 = 10000

    for i in range(len(df)):
        # Buy yönlü tp olma durumu
        if yön == "Buy" and df.loc[i].high >= tp:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = tp
            işlemden_çıkış_indexi = i
            sl = işleme_giriş_fiyatı-Buy_SL
            işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                             işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            iz_süren_sl = 0     
            
        # Burdan ters yönlü işlem girecek
            yön="Sell"
            işleme_giriş_tarihi=df.loc[i].time
            işleme_giriş_fiyatı = işlemden_çıkış_fiyatı
            işleme_giriş_indexi = i
            tp = işleme_giriş_fiyatı - Sell_TP
            sl= işlemden_çıkış_fiyatı + Sell_SL
            
        # Buy işlemin iz süren stop oluşma durumu 
        if yön == "Buy" and df.loc[i].close - işleme_giriş_fiyatı >=iz_süren_devreye_giriş:
            iz_süren_sl1 = df.loc[i].close -iz_süren_takip_mesafe
            if iz_süren_sl1 >= iz_süren_sl:
                iz_süren_sl=iz_süren_sl1
            
        # Buy işlemin iz süren stop olma durumu 
        if yön=="Buy" and df.loc[i].low <= iz_süren_sl:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = iz_süren_sl
            işlemden_çıkış_indexi = i
            işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            iz_süren_stop_sayısı +=1
           
        # Burdan ters yönlü işlem girecek (iz süren stop olduk)
            yön="Sell"
            işleme_giriş_tarihi=df.loc[i].time
            işleme_giriş_fiyatı = işlemden_çıkış_fiyatı
            işleme_giriş_indexi = i
            tp = işleme_giriş_fiyatı - Sell_TP
            sl= işlemden_çıkış_fiyatı + Sell_SL
            
            iz_süren_sl = 0
        # BUY YÖN SL OLMA DURUMU
        if yön == "Buy" and df.loc[i].low <= sl:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = sl
            işlemden_çıkış_indexi = i
            işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            iz_süren_sl = 0
            
            # Burdan ters yönlü işlem girecek
            yön="Sell"
            işleme_giriş_tarihi=df.loc[i].time
            işleme_giriş_fiyatı = işlemden_çıkış_fiyatı
            işleme_giriş_indexi = i
            tp = işleme_giriş_fiyatı - Sell_TP
            sl= işlemden_çıkış_fiyatı + Sell_SL
           
        
        #Sell işlem tp olma durumu
        if yön =="Sell" and df.loc[i].low <= tp:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = tp
            işlemden_çıkış_indexi = i
            işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            iz_süren_sl2 = 10000
            iz_süren_sl3 = 10000
            
        #Burada ters yönlü işlem girecek(tp olduk diye)
            yön = "Buy"
            işleme_giriş_tarihi=işlemden_çıkış_tarihi
            işleme_giriş_fiyatı = işlemden_çıkış_fiyatı
            işleme_giriş_tarihi = i
            tp = işleme_giriş_fiyatı + Buy_TP
            sl = işleme_giriş_fiyatı - Buy_SL
            

        # Sell işlemin iz süren stop oluşma durumu 
        if yön == "Sell" and işleme_giriş_fiyatı-df.loc[i].close >=iz_süren_devreye_giriş:
            iz_süren_sl2 = df.loc[i].close +iz_süren_takip_mesafe
            if iz_süren_sl2 <= iz_süren_sl3:
                iz_süren_sl3=iz_süren_sl2
            
 

        # Sell işlemin iz süren stop olma durumu 
        if yön=="Sell" and df.loc[i].high >= iz_süren_sl2:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = iz_süren_sl2
            işlemden_çıkış_indexi = i
            işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            iz_süren_stop_sayısı +=1
            iz_süren_sl2 = 10000
            iz_süren_sl3 = 10000
            
        # Burdan ters yönlü işlem girecek (iz süren stop olduk)
            yön="Buy"
            işleme_giriş_tarihi=işlemden_çıkış_tarihi
            işleme_giriş_fiyatı = işlemden_çıkış_fiyatı
            işleme_giriş_indexi = i
            tp = işleme_giriş_fiyatı + Buy_TP
            sl= işlemden_çıkış_fiyatı - Buy_SL
            
        # SELL YÖN SL OLMA DURUMU
        if yön=="Sell" and df.loc[i].high >= sl:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = sl
            işlemden_çıkış_indexi = i
            işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            
            iz_süren_sl2 = 10000
            iz_süren_sl3 = 10000
            # Burdan ters yönlü işlem girecek (stop olduk)
            yön="Buy"
            işleme_giriş_tarihi=işlemden_çıkış_tarihi
            işleme_giriş_fiyatı = işlemden_çıkış_fiyatı
            işleme_giriş_indexi = i
            tp = işleme_giriş_fiyatı + Buy_TP
            sl= işlemden_çıkış_fiyatı - Buy_SL
            
    for i in range(len(df)):
        TARİH.append(df.loc[i].time)
        KAPANIŞ.append(df.loc[i].close)
        İNDEXKLER.append(i)
    # print(iz_süren_stop_sayısı,"sayıda iz süren sl oldu")
    return işlemler,TARİH,KAPANIŞ,İNDEXKLER

def ATR_ile_işlem_giriş_çıkış(df,Buy_TP,Buy_SL,Sell_TP,Sell_SL):
    işlemler =[]
    
    yön="Buy"
    işleme_giriş_tarihi = df.loc[0].time
    işleme_giriş_fiyatı = df.loc[0].open
    işleme_giriş_index = 0
    işlemden_çıkış_tarih=0
    işlemden_çıkış_fiyat=0.0
    işlemden_çıkış_index = 0
    tp=0
    sl=0

    TARİH = []
    KAPANIŞ = []
    İNDEXKLER = []

    for i in range(21,len(df)):
        if yön=="Buy":   #Long işlemler için tek tek tp ve sl durumları
            if df.loc[i].low <= işleme_giriş_fiyatı - Buy_SL*df.loc[i]["ATR"]: #Stop olunuyor ise
                işlemden_çıkış_tarih = df.loc[i].time
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı - Buy_SL*df.loc[i]["ATR"]
                işlemden_çıkış_index = i
                tp=işleme_giriş_fiyatı + Buy_TP*df.loc[i]["ATR"]
                sl=işlemden_çıkış_fiyat
                işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işleme gir 
                yön = "Sell"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
            elif df.loc[i].high >= işleme_giriş_fiyatı + Buy_TP*df.loc[i]["ATR"]: #Tp olunuyor ise 
                işlemden_çıkış_tarih = df.loc[i].time
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı + Buy_TP*df.loc[i]["ATR"]
                işlemden_çıkış_index = i 
                tp = işlemden_çıkış_fiyat
                sl = işleme_giriş_fiyatı - Buy_SL*df.loc[i]["ATR"]
                işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işlem gir
                yön = "Sell"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
        else:    #Short işlemler için tek tek tp ve sl durumları
            if df.loc[i].high >= işleme_giriş_fiyatı + Sell_SL*df.loc[i]["ATR"]: # Stop olunuyor ise
                işlemden_çıkış_tarih = df.loc[i].time 
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı + Sell_SL*df.loc[i]["ATR"]
                işlemden_çıkış_index = i
                tp = işleme_giriş_fiyatı - Sell_TP*df.loc[i]["ATR"]
                sl = işlemden_çıkış_fiyat
                işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işleme gir
                yön = "Buy"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
            elif df.loc[i].low <= işleme_giriş_fiyatı - Sell_TP*df.loc[i]["ATR"]: # Tp olunuyor ise
                işlemden_çıkış_tarih = df.loc[i].time
                işlemden_çıkış_fiyat = işleme_giriş_fiyatı - Sell_TP*df.loc[i]["ATR"]
                işlemden_çıkış_index = i
                tp = işlemden_çıkış_fiyat
                sl = işleme_giriş_fiyatı + Sell_SL*df.loc[i]["ATR"]
                işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarih,
                işlemden_çıkış_fiyat,işleme_giriş_index,işlemden_çıkış_index,tp,sl))
                # Ters yönde işleme gir
                yön = "Buy"
                işleme_giriş_fiyatı = işlemden_çıkış_fiyat
                işleme_giriş_tarihi = işlemden_çıkış_tarih
                işleme_giriş_index = işlemden_çıkış_index
    for i in range(15,len(df)):
        TARİH.append(df.loc[i].time)
        KAPANIŞ.append(df.loc[i].close)
        İNDEXKLER.append(i)
    return işlemler,TARİH,KAPANIŞ,İNDEXKLER

#df'in uygun şartı -1 ise sell 1 ise buy olacak şekilde işleme girecek tp ve sl belli olacak (+7 ve -3 ayarlanmış)
def uygun_şarta_göre_giriş_çıkış(df,şart_sütun_isim): 
    işlemdemiyim=0
    işlemler=[]
    TARİH = []
    KAPANIŞ = []
    İNDEXKLER = []
    iz_süren_stop_sayısı=0
    iz_süren_sl = 0
    iz_süren_sl2 = 10000
    iz_süren_sl3 = 10000
    for i in range(len(df)):
        #BUY İŞLEM GİRMEK
        if df.loc[i][şart_sütun_isim] == 1.0 and işlemdemiyim ==0:
            yön = "buy"
            işleme_giriş_tarihi = df.loc[i].time
            işleme_giriş_fiyatı = df.loc[i].close
            işleme_giriş_indexi = i
            işlemdemiyim = 1 #Buy yönlü işlemdeyim
            tp = işleme_giriş_fiyatı + 7*df.loc[i]["ATR"]
            sl = işleme_giriş_fiyatı - 3*df.loc[i]["ATR"]
            # print(f"Buy işleme girdi. Giriş tarihi={işleme_giriş_tarihi}\n giriş fiyatı ={işleme_giriş_fiyatı}\n tp:{tp} \t sl:{sl}")
            # print("iz süren sl:",iz_süren_sl)

            
        # Şimdi Buy yönlü işlemde isem stop ve tp olma durumları
        # Önce Buy TP olma durumu.
        if işlemdemiyim == 1 and df.loc[i].high >= tp:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = tp
            işlemden_çıkış_indexi = i
            işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            işlemdemiyim = 0
            iz_süren_sl = 0
            # print(f"Buy yönlü işlem tp oldu. Çıkış tarihi:{işlemden_çıkış_tarihi}\n Çıkış fiyatı:{işlemden_çıkış_fiyatı}")
            # print("-"*30,end="\n\n")
        # Buy işlemin iz süren stop oluşma durumu 
        if işlemdemiyim == 1 and df.loc[i].high >= işleme_giriş_fiyatı + 5*df.loc[işleme_giriş_indexi]["ATR"]:         
            iz_süren_sl1 = df.loc[i].high - 3*df.loc[işleme_giriş_indexi]["ATR"]
            if iz_süren_sl1 >= iz_süren_sl:
                iz_süren_sl = iz_süren_sl1
            # print("iz süren stop devrede.gördüğü yüksek:",df.loc[i].high,"iz süren sl:",iz_süren_sl,"\n işleme giriş fiyatı: ",işleme_giriş_fiyatı,"\n atr=",df.loc[işleme_giriş_indexi]["ATR"])

        # Buy işlemin iz süren stop olma durumu 
        if işlemdemiyim == 1 and df.loc[i].low <= iz_süren_sl:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = iz_süren_sl
            işlemden_çıkış_indexi = i
            işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            iz_süren_stop_sayısı +=1
            işlemdemiyim = 0
            iz_süren_sl = 0
            # print(f"işlem iz süren stop oldu. Çıkış tarihi:{işlemden_çıkış_tarihi}\nçıkış fiyatı:{işlemden_çıkış_fiyatı}")
            # print("-"*30,end="\n\n")
        # BUY YÖN SL OLMA DURUMU(ATR Stobu)
        if işlemdemiyim == 1 and df.loc[i].low <= sl:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = sl
            işlemden_çıkış_indexi = i
            işlemler.append(("Buy",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            işlemdemiyim = 0
            iz_süren_sl = 0
            # print(f"işlem stop oldu. Çıkış tarihi:{işlemden_çıkış_tarihi}\nçıkış fiyatı:{işlemden_çıkış_fiyatı}")
            # print("-"*30,end="\n\n")
        
        #Sell işlem girmek
        if df.loc[i][şart_sütun_isim] == -1.0 and işlemdemiyim ==0:
            yön = "Sell"
            işleme_giriş_tarihi = df.loc[i].time
            işleme_giriş_fiyatı = df.loc[i].close
            işleme_giriş_indexi = i
            işlemdemiyim = -1 #Sell yönlü işlemdeyim
            tp = işleme_giriş_fiyatı - 7*df.loc[i]["ATR"]
            sl = işleme_giriş_fiyatı + 3*df.loc[i]["ATR"]
            # print(f"SEll işleme girdi. Giriş tarihi={işleme_giriş_tarihi}\n giriş fiyatı ={işleme_giriş_fiyatı}\n tp:{tp} \t sl:{sl}")
            
        # Sell işlem tp olma durumu
        if işlemdemiyim == -1 and df.loc[i].low <= tp:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = tp
            işlemden_çıkış_indexi = i
            işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            işlemdemiyim = 0
            iz_süren_sl3 = 10000
            # print(f"Sell yönlü işlem tp oldu. Çıkış tarihi:{işlemden_çıkış_tarihi}\n Çıkış fiyatı:{işlemden_çıkış_fiyatı}")
            # print("-"*30,end="\n\n")
        
        # Sell işlemin iz süren stop oluşma durumu 
        if işlemdemiyim == -1 and df.loc[i].low < işleme_giriş_fiyatı - 5*df.loc[işleme_giriş_indexi]["ATR"]:
            iz_süren_sl2 = df.loc[i].low + 3*df.loc[i]["ATR"]
            if iz_süren_sl2 <= iz_süren_sl3:
                iz_süren_sl3 = iz_süren_sl2
            # print("iz süren stop devrede.gördüğü düşük:",df.loc[i].low,"iz süren sl:",iz_süren_sl3,"\n işleme giriş fiyatı: ",işleme_giriş_fiyatı,"\n atr=",df.loc[işleme_giriş_indexi]["ATR"])
         # Sell işlemin iz süren stop olma durumu 
        if işlemdemiyim == -1 and df.loc[i].high >= iz_süren_sl3:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = iz_süren_sl3
            işlemden_çıkış_indexi = i
            işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            işlemdemiyim = 0
            iz_süren_sl3 = 10000
            # print(f"işlem iz süren stop oldu. Çıkış tarihi:{işlemden_çıkış_tarihi}\nçıkış fiyatı:{işlemden_çıkış_fiyatı}")
            # print("-"*30,end="\n\n")



        # SELL YÖN SL OLMA DURUMU(ATR Stobu)
        if işlemdemiyim == -1 and df.loc[i].high >= sl:
            işlemden_çıkış_tarihi = df.loc[i].time
            işlemden_çıkış_fiyatı = sl
            işlemden_çıkış_indexi = i
            işlemler.append(("Sell",işleme_giriş_tarihi,işleme_giriş_fiyatı,işlemden_çıkış_tarihi,
                işlemden_çıkış_fiyatı,işleme_giriş_indexi,işlemden_çıkış_indexi,tp,sl))
            işlemdemiyim = 0
            # print(f"işlem stop oldu. Çıkış tarihi:{işlemden_çıkış_tarihi}\nçıkış fiyatı:{işlemden_çıkış_fiyatı}")
            # print("-"*30,end="\n\n")
    for i in range(len(df)):
        TARİH.append(df.loc[i].time)
        KAPANIŞ.append(df.loc[i].close)
        İNDEXKLER.append(i)
    # print(iz_süren_stop_sayısı,"sayıda iz süren sl oldu")
    return işlemler,TARİH,KAPANIŞ,İNDEXKLER
    












