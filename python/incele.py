import xlsxwriter
import matplotlib.pyplot as plt
from IPython import display
import finplot as fplt 
import mplfinance as mpl 



class analiz:
    def __init__(self, name, işlemler):
        self.name = name
        self.işlemler = işlemler


        # Buy giriş indexler
        self.Buy_işleme_giriş_indexleri = []
        self.Buy_işlemden_çıkış_indexleri = []

        # Sell giriş indexler
        self.Sell_işleme_giriş_indexleri = []
        self.Sell_işlemden_çıkış_indexleri = []

        # Buy tarih/fiyat hiriş çıkışar
        self.Buy_işleme_giriş_tarihleri = []
        self.Buy_işleme_giriş_fiyatları = []
        self.Buy_işlemden_çıkış_tarihleri = []
        self.Buy_işlemden_çıkış_fiyatları = []

        # Sell tarih/fiyat hiriş çıkışar
        self.Sell_işleme_giriş_tarihleri = []
        self.Sell_işleme_giriş_fiyatları = []
        self.Sell_işlemden_çıkış_tarihleri = []
        self.Sell_işlemden_çıkış_fiyatları = []

        # Ayrıntılı işlem listesi
        self.Buy_işlemler = []
        self.Sell_işlemler = []

        # Genel tarihler
        self.işleme_giriş_tarihleri = []
        

        # Buy ve Sell işlem listeleri ve ayrıntılı listeler hazırlanması
        for i in self.işlemler:
            if i[0] == "Buy":
                self.Buy_işlemler.append(i)
                self.Buy_işleme_giriş_tarihleri.append(i[1])
                self.işleme_giriş_tarihleri.append(i[1])
                self.Buy_işleme_giriş_fiyatları.append(i[2])
                self.Buy_işlemden_çıkış_tarihleri.append(i[3])
                self.Buy_işlemden_çıkış_fiyatları.append(i[4])
                self.Buy_işleme_giriş_indexleri.append(i[5])
                self.Buy_işlemden_çıkış_indexleri.append(i[6])
            else:
                self.Sell_işlemler.append(i)
                self.Sell_işleme_giriş_tarihleri.append(i[1])
                self.işleme_giriş_tarihleri.append(i[1])
                self.Sell_işleme_giriş_fiyatları.append(i[2])
                self.Sell_işlemden_çıkış_tarihleri.append(i[3])
                self.Sell_işlemden_çıkış_fiyatları.append(i[4])
                self.Sell_işleme_giriş_indexleri.append(i[5])
                self.Sell_işlemden_çıkış_indexleri.append(i[6])

        # Genel işlemleri yorumlama
        self.kârlı_işlem_sayısı = 0
        self.zararlı_işlem_sayısı = 0
        self.sonuçlar = []
        self.kârlar = []
        self.zararlar = []
        for i in range(len(self.işlemler)):
            if self.işlemler[i][0] == "Buy":
                sonuç = self.işlemler[i][4]-self.işlemler[i][2]
                self.sonuçlar.append(sonuç)
                if sonuç > 0:
                    self.kârlı_işlem_sayısı += 1
                    self.kârlar.append(sonuç)
                else:
                    self.zararlı_işlem_sayısı += 1
                    self.zararlar.append(sonuç)
            if self.işlemler[i][0] == "Sell":
                sonuç = self.işlemler[i][2]-self.işlemler[i][4]
                self.sonuçlar.append(sonuç)
                if sonuç > 0:
                    self.kârlı_işlem_sayısı += 1
                    self.kârlar.append(sonuç)
                else:
                    self.zararlı_işlem_sayısı += 1
                    self.zararlar.append(sonuç)
        # Genel işlemleri yorumlama (Buy)
        self.Buy_sonuçlar = []
        self.Buy_kârlar = []
        self.Buy_zararlar = []
        self.Buy_kârlı_işlem_sayısı = 0
        self.Buy_zararlı_işlem_sayısı = 0
        for i in self.Buy_işlemler:
            Bsonuç = i[4]-i[2]
            self.Buy_sonuçlar.append(Bsonuç)
            if Bsonuç > 0:
                self.Buy_kârlar.append(Bsonuç)
                self.Buy_kârlı_işlem_sayısı += 1
            else:
                self.Buy_zararlar.append(Bsonuç)
                self.Buy_zararlı_işlem_sayısı += 1


        # Genel işlemleri yorumlama (SELL)
        self.Sell_sonuçlar = []
        self.Sell_kârlar = []
        self.Sell_zararlar = []
        self.Sell_kârlı_işlem_sayısı = 0
        self.Sell_zararlı_işlem_sayısı = 0
        for i in self.Sell_işlemler:
            Ssonuç = i[2]-i[4]
            self.Sell_sonuçlar.append(Ssonuç)
            if Ssonuç > 0:
                self.Sell_kârlar.append(Ssonuç)
                self.Sell_kârlı_işlem_sayısı += 1
            else:
                self.Sell_zararlar.append(Ssonuç)
                self.Sell_zararlı_işlem_sayısı += 1



        # winrate,ortalama kâr ve ortalama zarar hesaplama
        if len(self.işlemler) != 0: # işlem sayısı 0 değil ise
            self.winrate = self.kârlı_işlem_sayısı/len(self.işlemler)
        else:
            self.winrate = 0
        
        
        if len(self.kârlar)!=0:  # kârlı işlem sayısı 0 değil ise
            self.ortalama_kâr = sum(self.kârlar)/len(self.kârlar)
        else:
            self.ortalama_kâr = 0
        
        
        if len(self.zararlar)!=0: # Zararlı işlem sayısı 0 değil ise
            self.ortalama_zarar = -1 * sum(self.zararlar)/len(self.zararlar)
        else:
            self.ortalama_zarar = 0



        #Sonuç bakiye hesaplama
        self.sonuç = sum(self.kârlar)+sum(self.zararlar)

        # her işlem sonundaki bakiyeyi gösteren liste
        self.kümülatif = []
        for i in self.sonuçlar:
            if len(self.kümülatif) != 0:
                self.kümülatif.append(self.kümülatif[-1]+i)
            else:
                self.kümülatif.append(self.sonuçlar[0])



        # Ardışık kâr ve zararı bulmak
        self.ardışık_kâr = 1
        self.ardışık_zarar = 1
        self.en_yüksek_ardışık_kârlar = []
        self.en_yüksek_ardışık_zararlar = []

        for i in range(len(self.sonuçlar)-1):
            if self.sonuçlar[i] > 0:
                if self.sonuçlar[i+1] > 0:
                    self.ardışık_kâr += 1
                else:
                    self.en_yüksek_ardışık_kârlar.append(self.ardışık_kâr)
                    self.ardışık_kâr = 1
            if self.sonuçlar[i] <= 0:
                if self.sonuçlar[i+1] <= 0:
                    self.ardışık_zarar += 1
                else:
                    self.en_yüksek_ardışık_zararlar.append(self.ardışık_zarar)
                    self.ardışık_zarar = 1


        # Excel'e yazarken sıkıntı olmasın diye uzunluğunu bir yapıoyum ("1" ekleyerek)
        if len(self.en_yüksek_ardışık_kârlar)==0:
            self.en_yüksek_ardışık_kârlar.append("1")

        if len(self.en_yüksek_ardışık_zararlar)==0:
            self.en_yüksek_ardışık_zararlar.append("1")



        # winrate,ortalama kâr ve ortalama zarar hesaplama(Buy)
        if len(self.Buy_işlemler)!=0:
            self.Buy_winrate = self.Buy_kârlı_işlem_sayısı/len(self.Buy_işlemler)
        else:
            self.Buy_winrate = 0
        
        if len(self.Buy_kârlar)!=0:
            self.Buy_ortalama_kâr = sum(self.Buy_kârlar)/len(self.Buy_kârlar)
        else:
            self.Buy_ortalama_kâr = 0
        
        if len(self.Buy_zararlar)!=0:
            self.Buy_ortalama_zarar = -1 * \
                sum(self.Buy_zararlar)/len(self.Buy_zararlar)
        else:
            self.Buy_ortalama_zarar = 0

        
        # Buy işlemleri sonucunu bulmak
        self.Buy_sonuç = sum(self.Buy_kârlar)+sum(self.Buy_zararlar)


        # Sadece buy işlemleri ile bakiyeyi göstermek
        self.Buy_kümülatif = []
        for i in self.Buy_sonuçlar:
            if len(self.Buy_kümülatif) != 0:
                self.Buy_kümülatif.append(self.Buy_kümülatif[-1]+i)
            else:
                self.Buy_kümülatif.append(self.Buy_sonuçlar[0])

        #Buy işlemleri için ardışık kâr ve zararı bulmak        
        self.Buy_ardışık_kâr = 1
        self.Buy_ardışık_zarar = 1
        self.Buy_en_yüksek_ardışık_kârlar = []
        self.Buy_en_yüksek_ardışık_zararlar = []

        for i in range(len(self.Buy_sonuçlar)-1):
            if self.Buy_sonuçlar[i] > 0:
                if self.Buy_sonuçlar[i+1] > 0:
                    self.Buy_ardışık_kâr += 1
                else:
                    self.Buy_en_yüksek_ardışık_kârlar.append(
                        self.Buy_ardışık_kâr)
                    self.Buy_ardışık_kâr = 1
            if self.Buy_sonuçlar[i] <= 0:
                if self.Buy_sonuçlar[i+1] <= 0:
                    self.Buy_ardışık_zarar += 1
                else:
                    self.Buy_en_yüksek_ardışık_zararlar.append(
                        self.Buy_ardışık_zarar)
                    self.Buy_ardışık_zarar = 1

        #Excel'e yazarken sıkıntı olmasın diye tekrardan uzunluklarını 1 yapıyom
        if len(self.Buy_en_yüksek_ardışık_kârlar)==0:
            self.Buy_en_yüksek_ardışık_kârlar.append(1)
        if len(self.Buy_en_yüksek_ardışık_zararlar)==0:
            self.Buy_en_yüksek_ardışık_zararlar.append(1)



        # Sell yön için winrate.ortalama kâr ve ortalama zarar hesaplama
        if len(self.Sell_işlemler)!=0:
            self.Sell_winrate = self.Sell_kârlı_işlem_sayısı / len(self.Sell_işlemler)
        else:
            self.Sell_winrate = 0

        if len(self.Sell_kârlar)!=0:
            self.Sell_ortalama_kâr = sum(self.Sell_kârlar)/len(self.Sell_kârlar)
        else:
            self.Sell_ortalama_kâr = 0

        if len(self.Sell_zararlar) !=0:
            self.Sell_ortalama_zarar = -1 * sum(self.Sell_zararlar)/len(self.Sell_zararlar)
        else:
            self.Sell_ortalama_zarar = 0

        # Sell işlemleri için sonuç hesaplama
        self.Sell_sonuç = sum(self.Sell_kârlar)+sum(self.Sell_zararlar)

        # Sell işlemleri için bakiyeler
        self.Sell_kümülatif = []
        for i in self.Sell_sonuçlar:
            if len(self.Sell_kümülatif) != 0:
                self.Sell_kümülatif.append(self.Sell_kümülatif[-1]+i)
            else:
                self.Sell_kümülatif.append(self.Sell_sonuçlar[0])
        

        # Sell işlemler için ardışık kâr ve zarar hesaplama
        self.Sell_ardışık_kâr = 1
        self.Sell_ardışık_zarar = 1
        self.Sell_en_yüksek_ardışık_kârlar = []
        self.Sell_en_yüksek_ardışık_zararlar = []

        for i in range(len(self.Sell_sonuçlar)-1):
            if self.Sell_sonuçlar[i] > 0:
                if self.Sell_sonuçlar[i+1] > 0:
                    self.Sell_ardışık_kâr += 1
                else:
                    self.Sell_en_yüksek_ardışık_kârlar.append(
                        self.Sell_ardışık_kâr)
                    self.Sell_ardışık_kâr = 1
            if self.Sell_sonuçlar[i] <= 0:
                if self.Sell_sonuçlar[i+1] <= 0:
                    self.Sell_ardışık_zarar += 1
                else:
                    self.Sell_en_yüksek_ardışık_zararlar.append(
                        self.Sell_ardışık_zarar)
                    self.Sell_ardışık_zarar = 1

        # Excel'e yazarken sıkıntı olmasın diye uzunluk değiştirme
        if len(self.Sell_en_yüksek_ardışık_kârlar)==0:
            self.Sell_en_yüksek_ardışık_kârlar.append(1)
        if len(self.Sell_en_yüksek_ardışık_zararlar)==0:
            self.Sell_en_yüksek_ardışık_zararlar.append(1)


    # df olmadığı için çalışmaz...  
    def mum_grafiği(self,df,color_up="red",color_down="green",EMA1_color="aqua",EMA2_color="red",EMA3_color="white",EMA1=False,EMA2=False,EMA3=False,destekler:list=False):
        plt.figure() 
        minler =[]
        maxlar = []
        for i in range(len(df)):
            minler.append(df.loc[i].low)
            maxlar.append(df.loc[i].high)
        düşük = min(minler)
        yüksek = max(maxlar)
        ax = plt.axes()
        ax.set_facecolor("#262626")

        up = df[df.close >= df.open]
        
        down = df[df.close < df.open]
        
        # When the stock prices have decreased, then it
        # will be represented by blue color candlestick
        col1 = color_down
        
        # When the stock prices have increased, then it 
        # will be represented by green color candlestick
        col2 = color_up
        
        # Setting width of candlestick elements
        width = .8
        width2 = .08
        
        # Plotting up prices of the stock
        plt.bar(up.index, up.close-up.open, width, bottom=up.open, color=col1)
        plt.bar(up.index, up.high-up.close, width2, bottom=up.close, color=col1)
        plt.bar(up.index, up.low-up.open, width2, bottom=up.open, color=col1)
        
        # Plotting down prices of the stock
        plt.bar(down.index, down.close-down.open, width, bottom=down.open, color=col2)
        plt.bar(down.index, down.high-down.open, width2, bottom=down.open, color=col2)
        plt.bar(down.index, down.low-down.close, width2, bottom=down.close, color=col2)
        
        # rotating the x-axis tick labels at 30degree 
        # towards right
        plt.xticks(rotation=30, ha='right')
        
        # displaying candlestick chart of stock data 
        # of a week
        plt.xlabel("Mum numarası",fontweight="bold")
        plt.ylabel("fiyat",fontweight="bold")

        #Şimdi Emaları çizmenin zemanı.
        if EMA1 != False:
            plt.plot(df.index,df[EMA1],color=EMA1_color)
        if EMA2 != False:
            plt.plot(df.index,df[EMA2],color=EMA2_color)
        if EMA3 != False:
            plt.plot(df.index,df[EMA3],color=EMA3_color)
        
        # Desteklerin çizimi
        if destekler != False:
            for i in range(len(destekler)):
                plt.axhline(y=destekler[i][1],xmin=destekler[i][0]/len(df),color = "green",linestyle = "--",linewidth=0.8)
        
        plt.xlim(0,len(df)+1)
        plt.ylim(düşük-5,yüksek+5)
        plt.show()
        

    def excele_yaz(self):
        workbook = xlsxwriter.Workbook(f"{self.name} backtest sonuçları.xlsx")
        # Genel sayfası başlangıç -----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------
        worksheet = workbook.add_worksheet("Genel")

        başlık = workbook.add_format()
        başlık.set_bold()
        başlık.set_italic()
        başlık.set_align("center")
        worksheet.set_column(0, 6, 13.71)
        worksheet.set_column(1, 10, 23.29)
        # BAŞLIKLAR
        worksheet.write("B1", "YÖN", başlık)
        worksheet.write("C1", "İŞLEME GİRİŞ TARİHİ", başlık)
        worksheet.write("D1", "İŞLEMDEN ÇIKIŞ TARİHİ", başlık)
        worksheet.write("E1", "İŞLEME GİRİŞ FİYATI", başlık)
        worksheet.write("F1", "İŞLEMDEN ÇIKIŞ FİYATI", başlık)
        worksheet.write("G1", "KÂR", başlık)
        worksheet.write("H1", "KÜMÜLATİF KÂR", başlık)
        worksheet.write("J1", "WIN RATE", başlık)
        worksheet.write("K1", "KAZANÇ/ZARAR ORANI", başlık)
        worksheet.write("J5", "KÂRLI İŞLEM SAYISI", başlık)
        worksheet.write("K5", "ZARARLI İŞLEM SAYISI", başlık)
        worksheet.write("J9", "ORTALAMA KÂR", başlık)
        worksheet.write("K9", "ORTALAMA ZARAR", başlık)
        worksheet.write("I1", "SONUÇ", başlık)

        # ---------------------------------------------------------------------------------

        # İNDEX
        for i in range(len(self.işlemler)):
            worksheet.write(1+i, 0, i, başlık,)

        # YÖN SÜTUNU BİÇİMİ
        buy_yönü = workbook.add_format()
        buy_yönü.set_bg_color("#6BFA52")
        buy_yönü.set_bold()
        buy_yönü.set_color("black")
        buy_yönü.set_align("center")

        sell_yönü = workbook.add_format()
        sell_yönü.set_bg_color("#F14F33")
        sell_yönü.set_bold()
        sell_yönü.set_color("white")
        sell_yönü.set_align("center")

        # TARİHİ SÜTUNU BİÇİMİ
        tarihformatı = workbook.add_format({'num_format': 'yyyy/mm/dd hh:mm'})

        # KÂR SÜTUNU YAPACAĞIM BİÇİM
        kâr_biçimi = workbook.add_format()
        kâr_biçimi.set_bg_color("#90FB68")
        kâr_biçimi.set_bold()
        kâr_biçimi.set_align("center")
        kâr_biçimi.set_italic()
        kâr_biçimi.set_right(5)
        zarar_biçimi = workbook.add_format()
        zarar_biçimi.set_bg_color("#F77C61")
        zarar_biçimi.set_bold()
        zarar_biçimi.set_align("center")
        zarar_biçimi.set_italic()
        zarar_biçimi.set_right(5)
        worksheet.conditional_format(1, 6, len(self.işlemler), 6, {'type':     'cell',
                                                                   'criteria': '>',
                                                                   'value':    0,
                                                                   'format':   kâr_biçimi})
        worksheet.conditional_format(1, 6, len(self.işlemler), 6, {'type':     'cell',
                                                                   'criteria': '<=',
                                                                   'value':    0,
                                                                   'format':   zarar_biçimi})

        # KÜMÜLATİF KÂR SÜTUNU
        kkâr_biçimi = workbook.add_format()
        kkâr_biçimi.set_bg_color("green")
        kkâr_biçimi.set_bold()
        kkâr_biçimi.set_align("center")
        kkâr_biçimi.set_italic()
        kkâr_biçimi.set_color("white")
        kzarar_biçimi = workbook.add_format()
        kzarar_biçimi.set_bg_color("red")
        kzarar_biçimi.set_bold()
        kzarar_biçimi.set_align("center")
        kzarar_biçimi.set_italic()
        kzarar_biçimi.set_color("white")
        worksheet.conditional_format(1, 7, len(self.işlemler), 7, {'type':     'cell',
                                                                   'criteria': '>',
                                                                   'value':    0,
                                                                   'format':   kkâr_biçimi})
        worksheet.conditional_format(1, 7, len(self.işlemler), 7, {'type':     'cell',
                                                                   'criteria': '<=',
                                                                   'value':    0,
                                                                   'format':   kzarar_biçimi})

        worksheet.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                      'criteria': '>',
                                                      'value':    0,
                                                      'format':   kkâr_biçimi})
        worksheet.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                      'criteria': '<=',
                                                      'value':    0,
                                                      'format':   kzarar_biçimi})

        # ÖNCE İLK HÜCRESİNİ YAPIYORUM YANINDAKİ İLE AYNI
        worksheet.write("H2", "=G2", başlık)
        # ŞİMDİ KALANI
        for i in range(len(self.işlemler)-1):
            worksheet.write(2+i, 7, "=G"+str(3+i)+"+H"+str(2+i), başlık)

        # BURADAN İTİBAREN İŞLEMLERİ İŞLEM İŞLEM YAZIYORUM...
        for i in range(len(self.işlemler)):
            if self.işlemler[i][0] == "Buy":   # BUY İÇİN YÖN VE KÂR
                worksheet.write(i+1, 1, self.işlemler[i][0], buy_yönü)  # YÖN
                worksheet.write(i+1, 6, "=F"+str(i+2)+"-E"+str(i+2))  # KÂR
            else:  # Sell İÇİN YÖN VE KÂR
                worksheet.write(i+1, 1, self.işlemler[i][0], sell_yönü)
                worksheet.write(
                    i+1, 6, "=-1*(F"+str(i+2)+"-E"+str(i+2)+")")  # KÂR
            # GİRİŞ TARİHİ
            worksheet.write(i+1, 2, self.işlemler[i][1], tarihformatı)
            # GİRİŞ TARİHİ
            worksheet.write(i+1, 3, self.işlemler[i][3], tarihformatı)
            worksheet.write(i+1, 4, self.işlemler[i][2])  # ÇIKIŞ FİYATI
            worksheet.write(i+1, 5, self.işlemler[i][4])  # ÇIKIŞ FİYATI

        # WİNRATE YAZIYORUM
        winrate_formatı1 = workbook.add_format()
        winrate_formatı1 = workbook.add_format({'num_format': '%0'})
        winrate_formatı1.set_bold()
        winrate_formatı1.set_bg_color("#6BFA52")
        winrate_formatı1.set_color("green")
        winrate_formatı2 = workbook.add_format()
        winrate_formatı2 = workbook.add_format({'num_format': '%0'})
        winrate_formatı2.set_bold()
        if self.winrate >= 0.45:
            worksheet.write("J2", self.winrate, winrate_formatı1)
        else:
            worksheet.write("J2", self.winrate, winrate_formatı2)

        # KALAN VERİLER
        worksheet.write("J6", self.kârlı_işlem_sayısı)
        worksheet.write("K6", self.zararlı_işlem_sayısı)
        worksheet.write("J10", self.ortalama_kâr)
        worksheet.write("K10", self.ortalama_zarar)
        worksheet.write("K2", "=J10/K10")
        worksheet.write("I2", self.sonuç, başlık)
        worksheet.write("J13", "PORTFÖYÜN MAX DEĞERİ", başlık)
        worksheet.write("J14", max(self.kümülatif), başlık)
        worksheet.write("K13", "PORTFÖYÜN MİN DEĞERİ", başlık)
        worksheet.write("K14", min(self.kümülatif), başlık)
        worksheet.write("J17", "ALINAN EN BÜYÜK KÂR", başlık)
        worksheet.write("J18", max(self.sonuçlar), başlık)
        worksheet.write("K17", "ALINAN EN BÜYÜK ZARAR", başlık)
        worksheet.write("K18", min(self.sonuçlar), başlık)
        worksheet.write("J21", "EN YÜKSEK ARDIŞIK KÂR", başlık)
        worksheet.write("J22", max(self.en_yüksek_ardışık_kârlar), başlık)
        worksheet.write("K21", "EN YÜKSEK ARDIŞIK ZARAR", başlık)
        worksheet.write("K22", max(self.en_yüksek_ardışık_zararlar), başlık)
        worksheet.write("J25", "TOPLAM İŞLEM MALİYETİ", başlık)
        worksheet.write("J26", 0.33*len(self.sonuçlar), başlık)
        worksheet.write("K25", "GERÇEK SONUÇ", başlık)
        worksheet.write(
            "K26", self.kümülatif[-1] - 0.33*len(self.sonuçlar), başlık)
        # Genel sayfası bitti -----------------------------------------------------------------------------------------------
        # Long sayfası başlangıç -----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------
        wb1 = workbook.add_worksheet("Buy")

        wb1.set_column(0, 6, 13.71)
        wb1.set_column(1, 10, 23.29)

        wb1.conditional_format(1, 6, len(self.Buy_işlemler), 6, {'type':     'cell',
                                                                 'criteria': '>',
                                                                 'value':    0,
                                                                 'format':   kâr_biçimi})
        wb1.conditional_format(1, 6, len(self.Buy_işlemler), 6, {'type':     'cell',
                                                                 'criteria': '<=',
                                                                 'value':    0,
                                                                 'format':   zarar_biçimi})

        wb1.conditional_format(1, 7, len(self.Buy_işlemler), 7, {'type':     'cell',
                                                                 'criteria': '>',
                                                                 'value':    0,
                                                                 'format':   kkâr_biçimi})
        wb1.conditional_format(1, 7, len(self.Buy_işlemler), 7, {'type':     'cell',
                                                                 'criteria': '<=',
                                                                 'value':    0,
                                                                 'format':   kzarar_biçimi})

        wb1.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                'criteria': '>',
                                                'value':    0,
                                                'format':   kkâr_biçimi})
        wb1.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                'criteria': '<=',
                                                'value':    0,
                                                'format':   kzarar_biçimi})

        # BAŞLIKLAR
        wb1.write("B1", "YÖN", başlık)
        wb1.write("C1", "İŞLEME GİRİŞ TARİHİ", başlık)
        wb1.write("D1", "İŞLEMDEN ÇIKIŞ TARİHİ", başlık)
        wb1.write("E1", "İŞLEME GİRİŞ FİYATI", başlık)
        wb1.write("F1", "İŞLEMDEN ÇIKIŞ FİYATI", başlık)
        wb1.write("G1", "KÂR", başlık)
        wb1.write("H1", "KÜMÜLATİF KÂR", başlık)
        wb1.write("J1", "WIN RATE", başlık)
        wb1.write("K1", "KAZANÇ/ZARAR ORANI", başlık)
        wb1.write("J5", "KÂRLI İŞLEM SAYISI", başlık)
        wb1.write("K5", "ZARARLI İŞLEM SAYISI", başlık)
        wb1.write("J9", "ORTALAMA KÂR", başlık)
        wb1.write("K9", "ORTALAMA ZARAR", başlık)
        wb1.write("I1", "SONUÇ", başlık)

        wb1.write("H2", "=G2", başlık)

        # ŞİMDİ KALANI
        for i in range(len(self.Buy_işlemler)-1):
            wb1.write(2+i, 7, "=G"+str(3+i)+"+H"+str(2+i), başlık)

        # BURADAN İTİBAREN İŞLEMLERİ İŞLEM İŞLEM YAZIYORUM...
        for i in range(len(self.Buy_işlemler)):
            wb1.write(i+1, 1, self.Buy_işlemler[i][0], buy_yönü)  # YÖN
            wb1.write(i+1, 6, "=F"+str(i+2)+"-E"+str(i+2))  # KÂR
            # GİRİŞ TARİHİ
            wb1.write(i+1, 2, self.Buy_işlemler[i][1], tarihformatı)
            # GİRİŞ TARİHİ
            wb1.write(i+1, 3, self.Buy_işlemler[i][3], tarihformatı)
            wb1.write(i+1, 4, self.Buy_işlemler[i][2])  # ÇIKIŞ FİYATI
            wb1.write(i+1, 5, self.Buy_işlemler[i][4])  # ÇIKIŞ FİYATI

            # WİNRATE YAZIYORUM

        if self.Buy_winrate >= 0.45:
            wb1.write("J2", self.Buy_winrate, winrate_formatı1)
        else:
            wb1.write("J2", self.Buy_winrate, winrate_formatı2)

        # KALAN VERİLER
        wb1.write("J6", self.Buy_kârlı_işlem_sayısı)
        wb1.write("K6", self.Buy_zararlı_işlem_sayısı)
        wb1.write("J10", self.Buy_ortalama_kâr)
        wb1.write("K10", self.Buy_ortalama_zarar)
        wb1.write("K2", "=J10/K10")
        wb1.write("I2", self.Buy_sonuç, başlık)
        wb1.write("J13", "PORTFÖYÜN MAX DEĞERİ", başlık)
        wb1.write("J14", max(self.Buy_kümülatif), başlık)
        wb1.write("K13", "PORTFÖYÜN MİN DEĞERİ", başlık)
        wb1.write("K14", min(self.Buy_kümülatif), başlık)
        wb1.write("J17", "ALINAN EN BÜYÜK KÂR", başlık)
        wb1.write("J18", max(self.Buy_sonuçlar), başlık)
        wb1.write("K17", "ALINAN EN BÜYÜK ZARAR", başlık)
        wb1.write("K18", min(self.Buy_sonuçlar), başlık)
        wb1.write("J21", "EN YÜKSEK ARDIŞIK KÂR", başlık)
        wb1.write("J22", max(self.Buy_en_yüksek_ardışık_kârlar), başlık)
        wb1.write("K21", "EN YÜKSEK ARDIŞIK ZARAR", başlık)
        wb1.write("K22", max(self.Buy_en_yüksek_ardışık_zararlar), başlık)
        wb1.write("J25", "TOPLAM İŞLEM MALİYETİ", başlık)
        wb1.write("J26", 0.33*len(self.Buy_sonuçlar), başlık)
        wb1.write("K25", "GERÇEK SONUÇ", başlık)
        wb1.write("K26", self.Buy_kümülatif[-1] -
                  0.33*len(self.Buy_sonuçlar), başlık)

        # Long sayfası bitti -----------------------------------------------------------------------------------------------
        # Shortsayfası başlangıç -----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------

        wb2 = workbook.add_worksheet("Sell")

        wb2.set_column(0, 6, 13.71)
        wb2.set_column(1, 10, 23.29)

        wb2.conditional_format(1, 6, len(self.Sell_işlemler), 6, {'type':     'cell',
                                                                  'criteria': '>',
                                                                  'value':    0,
                                                                  'format':   kâr_biçimi})
        wb2.conditional_format(1, 6, len(self.Sell_işlemler), 6, {'type':     'cell',
                                                                  'criteria': '<=',
                                                                  'value':    0,
                                                                  'format':   zarar_biçimi})

        wb2.conditional_format(1, 7, len(self.Sell_işlemler), 7, {'type':     'cell',
                                                                  'criteria': '>',
                                                                  'value':    0,
                                                                  'format':   kkâr_biçimi})
        wb2.conditional_format(1, 7, len(self.Sell_işlemler), 7, {'type':     'cell',
                                                                  'criteria': '<=',
                                                                  'value':    0,
                                                                  'format':   kzarar_biçimi})

        wb2.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                'criteria': '>',
                                                'value':    0,
                                                'format':   kkâr_biçimi})
        wb2.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                'criteria': '<=',
                                                'value':    0,
                                                'format':   kzarar_biçimi})

        # BAŞLIKLAR
        wb2.write("B1", "YÖN", başlık)
        wb2.write("C1", "İŞLEME GİRİŞ TARİHİ", başlık)
        wb2.write("D1", "İŞLEMDEN ÇIKIŞ TARİHİ", başlık)
        wb2.write("E1", "İŞLEME GİRİŞ FİYATI", başlık)
        wb2.write("F1", "İŞLEMDEN ÇIKIŞ FİYATI", başlık)
        wb2.write("G1", "KÂR", başlık)
        wb2.write("H1", "KÜMÜLATİF KÂR", başlık)
        wb2.write("J1", "WIN RATE", başlık)
        wb2.write("K1", "KAZANÇ/ZARAR ORANI", başlık)
        wb2.write("J5", "KÂRLI İŞLEM SAYISI", başlık)
        wb2.write("K5", "ZARARLI İŞLEM SAYISI", başlık)
        wb2.write("J9", "ORTALAMA KÂR", başlık)
        wb2.write("K9", "ORTALAMA ZARAR", başlık)
        wb2.write("I1", "SONUÇ", başlık)

        wb2.write("H2", "=G2", başlık)

        # ŞİMDİ KALANI
        for i in range(len(self.Sell_işlemler)-1):
            wb2.write(2+i, 7, "=G"+str(3+i)+"+H"+str(2+i), başlık)

        # BURADAN İTİBAREN İŞLEMLERİ İŞLEM İŞLEM YAZIYORUM...
        for i in range(len(self.Sell_işlemler)):
            wb2.write(i+1, 1, self.Sell_işlemler[i][0], sell_yönü)  # YÖN
            wb2.write(i+1, 6, "=-1*(F"+str(i+2)+"-E"+str(i+2)+")")  # KÂR
            # GİRİŞ TARİHİ
            wb2.write(i+1, 2, self.Sell_işlemler[i][1], tarihformatı)
            # GİRİŞ TARİHİ
            wb2.write(i+1, 3, self.Sell_işlemler[i][3], tarihformatı)
            wb2.write(i+1, 4, self.Sell_işlemler[i][2])  # ÇIKIŞ FİYATI
            wb2.write(i+1, 5, self.Sell_işlemler[i][4])  # ÇIKIŞ FİYATI

            # WİNRATE YAZIYORUM

        if self.Sell_winrate >= 0.45:
            wb2.write("J2", self.Sell_winrate, winrate_formatı1)
        else:
            wb2.write("J2", self.Sell_winrate, winrate_formatı2)

        # KALAN VERİLER
        wb2.write("J6", self.Sell_kârlı_işlem_sayısı)
        wb2.write("K6", self.Sell_zararlı_işlem_sayısı)
        wb2.write("J10", self.Sell_ortalama_kâr)
        wb2.write("K10", self.Sell_ortalama_zarar)
        wb2.write("K2", "=J10/K10")
        wb2.write("I2", self.Sell_sonuç, başlık)
        wb2.write("J13", "PORTFÖYÜN MAX DEĞERİ", başlık)
        if len(self.Sell_kümülatif)!=0:
            wb2.write("J14", max(self.Sell_kümülatif), başlık)
            wb2.write("K14", min(self.Sell_kümülatif), başlık)
            wb2.write("J18", max(self.Sell_sonuçlar), başlık)
            wb2.write("K18", min(self.Sell_sonuçlar), başlık)
            wb2.write(
            "K26", self.Sell_kümülatif[-1] - 0.33*len(self.Sell_sonuçlar), başlık)
        wb2.write("K13", "PORTFÖYÜN MİN DEĞERİ", başlık) 
        wb2.write("J17", "ALINAN EN BÜYÜK KÂR", başlık)
        wb2.write("K17", "ALINAN EN BÜYÜK ZARAR", başlık)
        wb2.write("J21", "EN YÜKSEK ARDIŞIK KÂR", başlık)
        wb2.write("J22", max(self.Sell_en_yüksek_ardışık_kârlar), başlık)
        wb2.write("K21", "EN YÜKSEK ARDIŞIK ZARAR", başlık)
        wb2.write("K22", max(self.Sell_en_yüksek_ardışık_zararlar), başlık)
        wb2.write("J25", "TOPLAM İŞLEM MALİYETİ", başlık)
        wb2.write("J26", 0.33*len(self.Sell_sonuçlar), başlık)
        wb2.write("K25", "GERÇEK SONUÇ", başlık)
        

        # ------------------------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------

        """eklemeli_sonuç = workbook.add_worksheet("eklemeli sonuç")

        başlık = workbook.add_format()
        başlık.set_bold()
        başlık.set_italic()
        başlık.set_align("center")
        eklemeli_sonuç.set_column(0, 6, 13.71)
        eklemeli_sonuç.set_column(1, 10, 23.29)
        # BAŞLIKLAR
        eklemeli_sonuç.write("B1", "YÖN", başlık)
        eklemeli_sonuç.write("C1", "İŞLEME GİRİŞ TARİHİ", başlık)
        eklemeli_sonuç.write("D1", "İŞLEMDEN ÇIKIŞ TARİHİ", başlık)
        eklemeli_sonuç.write("E1", "İŞLEME GİRİŞ FİYATI", başlık)
        eklemeli_sonuç.write("F1", "İŞLEMDEN ÇIKIŞ FİYATI", başlık)
        eklemeli_sonuç.write("G1", "KÂR", başlık)
        eklemeli_sonuç.write("H1", "KÜMÜLATİF KÂR", başlık)
        eklemeli_sonuç.write("J1", "WIN RATE", başlık)
        eklemeli_sonuç.write("K1", "KAZANÇ/ZARAR ORANI", başlık)
        eklemeli_sonuç.write("J5", "KÂRLI İŞLEM SAYISI", başlık)
        eklemeli_sonuç.write("K5", "ZARARLI İŞLEM SAYISI", başlık)
        eklemeli_sonuç.write("J9", "ORTALAMA KÂR", başlık)
        eklemeli_sonuç.write("K9", "ORTALAMA ZARAR", başlık)
        eklemeli_sonuç.write("I1", "SONUÇ", başlık)


        eklemeli_sonuç.conditional_format(1, 6, len(self.işlemler), 6, {'type':     'cell',
                                                                   'criteria': '>',
                                                                   'value':    0,
                                                                   'format':   kâr_biçimi})
        eklemeli_sonuç.conditional_format(1, 6, len(self.işlemler), 6, {'type':     'cell',
                                                                   'criteria': '<=',
                                                                   'value':    0,
                                                                   'format':   zarar_biçimi})








        eklemeli_sonuç.conditional_format(1, 7, len(self.işlemler), 7, {'type':     'cell',
                                                                   'criteria': '>',
                                                                   'value':    0,
                                                                   'format':   kkâr_biçimi})
        eklemeli_sonuç.conditional_format(1, 7, len(self.işlemler), 7, {'type':     'cell',
                                                                   'criteria': '<=',
                                                                   'value':    0,
                                                                   'format':   kzarar_biçimi})


        eklemeli_sonuç.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                                   'criteria': '>',
                                                                   'value':    0,
                                                                   'format':   kkâr_biçimi})
        eklemeli_sonuç.conditional_format(25, 10, 25, 10, {'type':     'cell',
                                                                   'criteria': '<=',
                                                                   'value':    0,
                                                                   'format':   kzarar_biçimi})  

        # İŞLEMLERİ YAZIYORUM
        self.katsayı = 1
        for i in range(len(self.işlemler)):
            if self.işlemler[i][0]=="Buy":   # BUY İÇİN YÖN VE KÂR
                eklemeli_sonuç.write(i+1,1,self.işlemler[i][0],buy_yönü) # YÖN
                eklemeli_sonuç.write(i+1,6,"=(F"+str(i+2)+"-E"+str(i+2)+")*"+str(self.katsayı))  #KÂR
                
            else:  # Sell İÇİN YÖN VE KÂR
                eklemeli_sonuç.write(i+1,1,self.işlemler[i][0],sell_yönü)
                eklemeli_sonuç.write(i+1,6,"=-1*(F"+str(i+2)+"-E"+str(i+2)+")*"+str(self.katsayı))  #KÂR
                
            eklemeli_sonuç.write(i+1,2,self.işlemler[i][1],tarihformatı) #GİRİŞ TARİHİ
            eklemeli_sonuç.write(i+1,3,self.işlemler[i][3],tarihformatı) #GİRİŞ TARİHİ
            eklemeli_sonuç.write(i+1,4,self.işlemler[i][2]) #ÇIKIŞ FİYATI
            eklemeli_sonuç.write(i+1,5,self.işlemler[i][4]) #ÇIKIŞ FİYATI                                                           


        if self.winrate >= 0.45:
            eklemeli_sonuç.write("J2",self.winrate,winrate_formatı1)
        else:
            eklemeli_sonuç.write("J2",self.winrate,winrate_formatı2)

        #KALAN VERİLER
        eklemeli_sonuç.write("J6",self.kârlı_işlem_sayısı)
        eklemeli_sonuç.write("K6",self.zararlı_işlem_sayısı)
        eklemeli_sonuç.write("J10",self.ortalama_kâr)
        eklemeli_sonuç.write("K10",self.ortalama_zarar)
        eklemeli_sonuç.write("K2","=J10/K10")
        eklemeli_sonuç.write("I2",self.sonuç,başlık)
        eklemeli_sonuç.write("J13","PORTFÖYÜN MAX DEĞERİ",başlık)
        eklemeli_sonuç.write("J14",max(self.kümülatif),başlık)
        eklemeli_sonuç.write("K13","PORTFÖYÜN MİN DEĞERİ",başlık)
        eklemeli_sonuç.write("K14",min(self.kümülatif),başlık)      
        eklemeli_sonuç.write("J17","ALINAN EN BÜYÜK KÂR",başlık)
        eklemeli_sonuç.write("J18",max(self.sonuçlar),başlık)
        eklemeli_sonuç.write("K17","ALINAN EN BÜYÜK ZARAR",başlık)
        eklemeli_sonuç.write("K18",min(self.sonuçlar),başlık)
        eklemeli_sonuç.write("J21","EN YÜKSEK ARDIŞIK KÂR",başlık)
        eklemeli_sonuç.write("J22",max(self.en_yüksek_ardışık_kârlar),başlık)        
        eklemeli_sonuç.write("K21","EN YÜKSEK ARDIŞIK ZARAR",başlık)
        eklemeli_sonuç.write("K22",max(self.en_yüksek_ardışık_zararlar),başlık)
        eklemeli_sonuç.write("J25","TOPLAM İŞLEM MALİYETİ",başlık)
        eklemeli_sonuç.write("J26",0.33*len(self.sonuçlar),başlık)
        eklemeli_sonuç.write("K25","GERÇEK SONUÇ",başlık)
        eklemeli_sonuç.write("K26",self.kümülatif[-1] - 0.33*len(self.sonuçlar),başlık)

        # ÖNCE İLK HÜCRESİNİ YAPIYORUM YANINDAKİ İLE AYNI
        eklemeli_sonuç.write("H2", "=G2", başlık)
        # ŞİMDİ KALANI
        for i in range(len(self.işlemler)-1):
            eklemeli_sonuç.write(2+i, 7, "=G"+str(3+i)+"+H"+str(2+i), başlık)"""

        workbook.close()

    def grafiği_çiz(self, color_buy="green", color_sell="red"):
        # FONKSİYON BURDAN BAŞLAR
        plt.figure()  # Çevrenin rengi (grafik arkaplanı değil)

        # Grafikte bazı düzenlemeler
        plt.xlabel("Tarih")
        plt.ylabel("Fiyat")
        ax = plt.axes()
        ax.set_facecolor("#262626")
        """plt.plot(df.time,df.close,color="white")"""  # Normal grafik
        # Şimdi yeşil renkli "Buy" oluşturacağım x=[başlangıç tarihi,2.tarih,3.tarih,....,bitiş tarihi] şeklinde listeler oluşturacağım
        tarih1 = []
        fiyat1 = []
        tarih2 = []
        fiyat2 = []

        # şimdi indekslerin farkını kullanarak işlemde olduğu indeksleri bulacağım örneğin ilk işlem için
        # çıkış_indeksi[0]-giriş_indexi[0]= bir sayı olacak mesela 15... 15 zaman boyunca o aralıkta kaldım demek
        # for döngüsüyle 15tane eklerim ve geçerli tarihi aynı şekilde fiyatları bulmuş olurum

        """for i in işlemler:
            print("yön:",i[0],"    giriş tarihi:",i[1],"    giriş fiyatı:",i[2],"    çıkış tarihi:",i[3],"    çıkış fiyatı:",i[4],"    giriş indexi:",i[5],"    çıkış indexi:",i[6])
        """

        for j in range(len(self.Buy_işlemden_çıkış_fiyatları)-1):
            a = self.Buy_işlemden_çıkış_indexleri[j] - \
                self.Buy_işleme_giriş_indexleri[j]
            for i in range(a):
                tarih1.append(
                    self.df.loc[self.Buy_işleme_giriş_indexleri[j]+i].time)
                fiyat1.append(
                    self.df.loc[self.Buy_işleme_giriş_indexleri[j]+i].close)
            plt.plot(tarih1, fiyat1, color=color_buy)
            tarih1 = []
            fiyat1 = []

        for j in range(len(self.Sell_işlemden_çıkış_fiyatları)-1):
            a = self.Sell_işlemden_çıkış_indexleri[j] - \
                self.Sell_işleme_giriş_indexleri[j]
            for i in range(a):
                tarih2.append(
                    self.df.loc[self.Sell_işleme_giriş_indexleri[j]+i].time)
                fiyat2.append(
                    self.df.loc[self.Sell_işleme_giriş_indexleri[j]+i].close)
            plt.plot(tarih2, fiyat2, color=color_sell)
            tarih2 = []
            fiyat2 = []
        plt.show()

    def portföyü_göster(self):
        plt.figure()
        plt.xlabel("işlem")
        plt.ylabel("Portföyün değeri")
        ax = plt.axes()
        ax.set_facecolor("#262626")
        ax.plot(self.kümülatif, color="white")
        ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
        plt.show()

    def portföy_işlem_göster(self, hız=1.0,color_buy="Green", color_sell="red"):
        Üç_İşlem_indexler = []
        Üç_İşlem_Fiyatlar = []
        fig, ax = plt.subplots(2, 1, figsize=(15, 9))
        ax[0].set_facecolor("#262626")
        ax[1].set_facecolor("#262626")
        ax[0].set_title("Grafik")
        ax[0].set_xlabel("index")
        ax[0].set_ylabel("Fiyat")
        ax[1].set_title("Portföy değişimi")
        ax[1].set_xlabel("işlem")
        ax[1].set_ylabel("Portföy büyümesi")
        ax[1].axhline(y=0, color="red", linestyle="--", linewidth=1)
        ax[1].set_ylim([-10, 10])
        # Şimdi ekleme kısmı... işlem işlem gitsin. grafik çıksın 3 saniye dursun sonra yeni işlem eklenmiş hali gelsin.
        # Bu süreçte baktığımız kısımda değişiyor tabiki
        # Önce ilk işlem kısmı gelsin.
        # Grafik hareketi kuralları
        # 1-)Grafikte toplam 5 işlemlik alan gösterilecek
        # 2-)Önemli alan(üzerinde çalıştığımız alan) renkli olacak kalanlar beyaz
        # 3-)Üzereinde çalıştığımız alan 4 olduğunda 2 olacak şekilde yeni grafik çizilecek.
        # Şimdi önce ilk 5 işlemlik kısım. Tarih ve Fiyat listelerini ayarlayacağım.

        for i in range(self.işlemler[len(self.işlemler)-1][6]):  # 3.işlemin çıkış indexi
            Üç_İşlem_indexler.append(i)
            Üç_İşlem_Fiyatlar.append(self.df.loc[i].close)
        ax[0].plot(Üç_İşlem_indexler, Üç_İşlem_Fiyatlar, color="white")
        # Şimdi ilk 5 işlemi beyaz olarak gösteriyor. Ben ilk işlem kısmını işlem yönüne göre boyamasını istiyorum
        plt.show(block=False)
        plt.pause(4)
        # Önce grafiği kapat
        plt.close()
        fig, ax = plt.subplots(2, 1, figsize=(15, 9))
        ax[0].set_facecolor("#262626")
        ax[1].set_facecolor("#262626")
        ax[0].set_title("Grafik")
        ax[0].set_xlabel("index")
        ax[0].set_ylabel("Fiyat")
        ax[1].set_title("Portföy değişimi")
        ax[1].set_xlabel("işlem")
        ax[1].set_ylabel("Portföy büyüklüğü")
        ax[1].axhline(y=0, color="red", linestyle="--", linewidth=1)
        """ax[1].set_ylim([-40, 100])"""
        # Şimdi yenisini(ilk işlem boyalı) çiz önce tamamını(boyasız)
        ax[0].plot(Üç_İşlem_indexler, Üç_İşlem_Fiyatlar, color="#262626")
        ax[1].plot(self.kümülatif, color="#262626")
        # Yeni grafikler(üzerinde çalıştığım işlem)(bunu boya)
        çalıştığım_işlem = [0]
        çalıştığım_kümülatif = [0]
        for j in range(len(self.işlemler)):
            çalıştığım_index = []
            çalıştığım_fiyat = []
            
            

            for i in range(self.işlemler[j][5], self.işlemler[j][6]+1):
                çalıştığım_index.append(i)
                çalıştığım_fiyat.append(self.df.loc[i].close)
            """line_tp = ax[0].axhline(y=self.işlemler[j+1][7],
                        color="green", linestyle="--", linewidth=1)
            line_sl = ax[0].axhline(y=self.işlemler[j+1][8],
                        color="red", linestyle="--", linewidth=1)"""

            çalıştığım_işlem.append(j)
            çalıştığım_kümülatif.append(self.kümülatif[j])

                    
            if self.işlemler[j][0] == "Buy":
                renk = color_buy
            if self.işlemler[j][0] == "Sell":
                renk = color_sell
            ax[0].plot(çalıştığım_index, çalıştığım_fiyat, color=renk)
            ax[1].plot(çalıştığım_işlem,çalıştığım_kümülatif,color = "aqua")
            plt.pause(hız)
            plt.show(block=False)
            
                
        plt.pause(9)

