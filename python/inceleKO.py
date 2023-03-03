import xlsxwriter
import numpy as np

# ÖNCELİKLE ALİ PERŞEMBE'NİN STRATEJİSİ İLE UYGUN OLSUN
# Buy sell yönde de işlemler olmalı (işlemler 1 buy 1 sell şeklinde gitmeli)
# BİTİŞTE DEVAM EDEN İŞLEM OLMAMALI


class analizKO:
    def __init__(self,name, işlemler):
        self.name = name
        self.işlemler = işlemler
        self.Buy_işleme_giriş_tarihleri = []
        self.Buy_işleme_giriş_fiyatları = []
        self.Buy_işlemden_çıkış_tarihleri = []
        self.Buy_işlemden_çıkış_fiyatları = []
        self.Sell_işleme_giriş_tarihleri = []
        self.Sell_işleme_giriş_fiyatları = []
        self.Sell_işlemden_çıkış_tarihleri = []
        self.Sell_işlemden_çıkış_fiyatları = []
        self.Buy_işlemler = []
        self.Sell_işlemler = []

        for i in self.işlemler:
            if i[0]=="Buy":
                self.Buy_işlemler.append(i)
                self.Buy_işleme_giriş_tarihleri.append(i[1])
                self.Buy_işleme_giriş_fiyatları.append(i[2])
                self.Buy_işlemden_çıkış_tarihleri.append(i[3])
                self.Buy_işlemden_çıkış_fiyatları.append(i[4])
            else:
                self.Sell_işlemler.append(i)
                self.Sell_işleme_giriş_tarihleri.append(i[1])
                self.Sell_işleme_giriş_fiyatları.append(i[2])
                self.Sell_işlemden_çıkış_tarihleri.append(i[3])
                self.Sell_işlemden_çıkış_fiyatları.append(i[4])
        
        self.kârlı_işlem_sayısı=0
        self.zararlı_işlem_sayısı=0
        self.sonuçlar=[]
        self.kârlar=[]
        self.zararlar = []
        for i in range(len(self.işlemler)):
            if self.işlemler[i][0]=="Buy":
                sonuç = self.işlemler[i][4]-self.işlemler[i][2]
                self.sonuçlar.append(sonuç)
                if sonuç>0:
                    self.kârlı_işlem_sayısı += 1
                    self.kârlar.append(sonuç)
                else:
                    self.zararlı_işlem_sayısı += 1
                    self.zararlar.append(sonuç)
            if self.işlemler[i][0]=="Sell":
                sonuç = self.işlemler[i][2]-self.işlemler[i][4]
                self.sonuçlar.append(sonuç)
                if sonuç>0:
                    self.kârlı_işlem_sayısı += 1
                    self.kârlar.append(sonuç)
                else:
                    self.zararlı_işlem_sayısı +=1
                    self.zararlar.append(sonuç)
        

        self.Buy_sonuçlar=[]
        self.Buy_kârlar=[]
        self.Buy_zararlar=[]
        self.Buy_kârlı_işlem_sayısı = 0
        self.Buy_zararlı_işlem_sayısı = 0
        for i in self.Buy_işlemler:
            Bsonuç=i[4]-i[2]
            self.Buy_sonuçlar.append(Bsonuç)
            if Bsonuç>0:
                self.Buy_kârlar.append(Bsonuç)
                self.Buy_kârlı_işlem_sayısı += 1
            else:
                self.Buy_zararlar.append(Bsonuç)
                self.Buy_zararlı_işlem_sayısı +=1
        

        self.Sell_sonuçlar=[]
        self.Sell_kârlar=[]
        self.Sell_zararlar=[]
        self.Sell_kârlı_işlem_sayısı = 0
        self.Sell_zararlı_işlem_sayısı = 0
        for i in self.Sell_işlemler:
            Bsonuç=i[2]-i[4]
            self.Sell_sonuçlar.append(Bsonuç)
            if Bsonuç>0:
                self.Sell_kârlar.append(Bsonuç)
                self.Sell_kârlı_işlem_sayısı += 1
            else:
                self.Sell_zararlar.append(Bsonuç)
                self.Sell_zararlı_işlem_sayısı +=1



        self.winrate=self.kârlı_işlem_sayısı/len(self.işlemler)
        self.ortalama_kâr = sum(self.kârlar)/len(self.kârlar)
        self.ortalama_zarar = -1 * sum(self.zararlar)/len(self.zararlar)
        self.sonuç = sum(self.kârlar)+sum(self.zararlar)
        self.kümülatif = []
        for i in self.sonuçlar:
            if len(self.kümülatif)!=0:
                self.kümülatif.append(self.kümülatif[-1]+i)
            else:
                self.kümülatif.append(self.sonuçlar[0])
        self.ardışık_kâr = 1
        self.ardışık_zarar = 1
        self.en_yüksek_ardışık_kârlar = []        
        self.en_yüksek_ardışık_zararlar = []

        for i in range(len(self.sonuçlar)-1):
            if self.sonuçlar[i]>0: 
                if self.sonuçlar[i+1]>0:
                    self.ardışık_kâr +=1
                else:
                    self.en_yüksek_ardışık_kârlar.append(self.ardışık_kâr)
                    self.ardışık_kâr = 1
            if self.sonuçlar[i]<=0:
                if self.sonuçlar[i+1]<=0:
                    self.ardışık_zarar += 1
                else:
                    self.en_yüksek_ardışık_zararlar.append(self.ardışık_zarar)
                    self.ardışık_zarar = 1
            






        
        self.Buy_winrate=self.Buy_kârlı_işlem_sayısı/len(self.Buy_işlemler)
        self.Buy_ortalama_kâr = sum(self.Buy_kârlar)/len(self.Buy_kârlar)
        self.Buy_ortalama_zarar = -1 * sum(self.Buy_zararlar)/len(self.Buy_zararlar)
        self.Buy_sonuç = sum(self.Buy_kârlar)+sum(self.Buy_zararlar)
        self.Buy_kümülatif = []
        for i in self.Buy_sonuçlar:
            if len(self.Buy_kümülatif)!=0:
                self.Buy_kümülatif.append(self.Buy_kümülatif[-1]+i)
            else:
                self.Buy_kümülatif.append(self.Buy_sonuçlar[0])
        self.Buy_ardışık_kâr = 1
        self.Buy_ardışık_zarar = 1
        self.Buy_en_yüksek_ardışık_kârlar = []        
        self.Buy_en_yüksek_ardışık_zararlar = []

        for i in range(len(self.Buy_sonuçlar)-1):
            if self.Buy_sonuçlar[i]>0: 
                if self.Buy_sonuçlar[i+1]>0:
                    self.Buy_ardışık_kâr +=1
                else:
                    self.Buy_en_yüksek_ardışık_kârlar.append(self.Buy_ardışık_kâr)
                    self.Buy_ardışık_kâr = 1
            if self.Buy_sonuçlar[i]<=0:
                if self.Buy_sonuçlar[i+1]<=0:
                    self.Buy_ardışık_zarar += 1
                else:
                    self.Buy_en_yüksek_ardışık_zararlar.append(self.Buy_ardışık_zarar)
                    self.Buy_ardışık_zarar = 1

        

        self.Sell_winrate=self.Sell_kârlı_işlem_sayısı/len(self.Sell_işlemler)
        self.Sell_ortalama_kâr = sum(self.Sell_kârlar)/len(self.Sell_kârlar)
        self.Sell_ortalama_zarar = -1 * sum(self.Sell_zararlar)/len(self.Sell_zararlar)
        self.Sell_sonuç = sum(self.Sell_kârlar)+sum(self.Sell_zararlar)
        self.Sell_kümülatif = []
        for i in self.Sell_sonuçlar:
            if len(self.Sell_kümülatif)!=0:
                self.Sell_kümülatif.append(self.Sell_kümülatif[-1]+i)
            else:
                self.Sell_kümülatif.append(self.Sell_sonuçlar[0])
        self.Sell_ardışık_kâr = 1
        self.Sell_ardışık_zarar = 1
        self.Sell_en_yüksek_ardışık_kârlar = []        
        self.Sell_en_yüksek_ardışık_zararlar = []

        for i in range(len(self.Sell_sonuçlar)-1):
            if self.Sell_sonuçlar[i]>0: 
                if self.Sell_sonuçlar[i+1]>0:
                    self.Sell_ardışık_kâr +=1
                else:
                    self.Sell_en_yüksek_ardışık_kârlar.append(self.Sell_ardışık_kâr)
                    self.Sell_ardışık_kâr = 1
            if self.Sell_sonuçlar[i]<=0:
                if self.Sell_sonuçlar[i+1]<=0:
                    self.Sell_ardışık_zarar += 1
                else:
                    self.Sell_en_yüksek_ardışık_zararlar.append(self.Sell_ardışık_zarar)
                    self.Sell_ardışık_zarar = 1
            

    def excele_yaz(self):
        workbook = xlsxwriter.Workbook(f"{self.name} 방법 분석.xlsx")
        #Genel sayfası başlangıç -----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------
        worksheet = workbook.add_worksheet("일반")

        başlık = workbook.add_format()
        başlık.set_bold()
        başlık.set_italic()
        başlık.set_align("center")
        worksheet.set_column(0, 6, 13.71)
        worksheet.set_column(1, 10, 23.29)
        # BAŞLIKLAR
        worksheet.write("B1", "방향", başlık)
        worksheet.write("C1", "처리 시작 날짜", başlık)
        worksheet.write("D1", "종료 날짜", başlık)
        worksheet.write("E1", "처리 시작 가격", başlık)
        worksheet.write("F1", "종료 가격", başlık)
        worksheet.write("G1", "이익", başlık)
        worksheet.write("H1", "총 이익", başlık)
        worksheet.write("J1", "WIN RATE", başlık)
        worksheet.write("K1", "이익/손해", başlık)
        worksheet.write("J5", "이익이 된 처리 수", başlık)
        worksheet.write("K5", "손해가 된 처리 수", başlık)
        worksheet.write("J9", "평귝 이익", başlık)
        worksheet.write("K9", "평귝 손해", başlık)
        worksheet.write("I1", "결과", başlık)

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

        # 총 이익 SÜTUNU
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
            if self.işlemler[i][0]=="Buy":   # BUY İÇİN YÖN VE KÂR
                worksheet.write(i+1,1,self.işlemler[i][0],buy_yönü) # YÖN
                worksheet.write(i+1,6,"=F"+str(i+2)+"-E"+str(i+2))  #KÂR
            else:  # Sell İÇİN YÖN VE KÂR
                worksheet.write(i+1,1,self.işlemler[i][0],sell_yönü)
                worksheet.write(i+1,6,"=-1*(F"+str(i+2)+"-E"+str(i+2)+")")  #KÂR
            worksheet.write(i+1,2,self.işlemler[i][1],tarihformatı) #GİRİŞ TARİHİ
            worksheet.write(i+1,3,self.işlemler[i][3],tarihformatı) #GİRİŞ TARİHİ
            worksheet.write(i+1,4,self.işlemler[i][2]) #ÇIKIŞ FİYATI
            worksheet.write(i+1,5,self.işlemler[i][4]) #ÇIKIŞ FİYATI

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
            worksheet.write("J2",self.winrate,winrate_formatı1)
        else:
            worksheet.write("J2",self.winrate,winrate_formatı2)

        #KALAN VERİLER
        worksheet.write("J6",self.kârlı_işlem_sayısı)
        worksheet.write("K6",self.zararlı_işlem_sayısı)
        worksheet.write("J10",self.ortalama_kâr)
        worksheet.write("K10",self.ortalama_zarar)
        worksheet.write("K2","=J10/K10")
        worksheet.write("I2",self.sonuç,başlık)
        worksheet.write("J13","포트폴리오의 최대 가치",başlık)
        worksheet.write("J14",max(self.kümülatif),başlık)
        worksheet.write("K13","포트폴리오의 최소 가치",başlık)
        worksheet.write("K14",min(self.kümülatif),başlık)      
        worksheet.write("J17","받은 제일 큰 이익",başlık)
        worksheet.write("J18",max(self.sonuçlar),başlık)
        worksheet.write("K17","받은 제일 큰 손해",başlık)
        worksheet.write("K18",min(self.sonuçlar),başlık)
        worksheet.write("J21","제일 높은 연속 이익 수",başlık)
        worksheet.write("J22",max(self.en_yüksek_ardışık_kârlar),başlık)        
        worksheet.write("K21","제일 높은 연속 손해 수",başlık)
        worksheet.write("K22",max(self.en_yüksek_ardışık_zararlar),başlık)
        worksheet.write("J25","총 처리 비용",başlık)
        worksheet.write("J26",0.33*len(self.sonuçlar),başlık)
        worksheet.write("K25","사실 결과",başlık)
        worksheet.write("K26",self.kümülatif[-1] - 0.33*len(self.sonuçlar),başlık)
        #Genel sayfası bitti -----------------------------------------------------------------------------------------------
        #Long sayfası başlangıç -----------------------------------------------------------------------------------------------
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
        wb1.write("C1", "처리 시작 날짜", başlık)
        wb1.write("D1", "종료 날짜", başlık)
        wb1.write("E1", "처리 시작 가격", başlık)
        wb1.write("F1", "종료 가격", başlık)
        wb1.write("G1", "이익", başlık)
        wb1.write("H1", "총 이익", başlık)
        wb1.write("J1", "WIN RATE", başlık)
        wb1.write("K1", "이익/손해", başlık)
        wb1.write("J5", "이익이 된 처리 수", başlık)
        wb1.write("K5", "손해가 된 처리 수", başlık)
        wb1.write("J9", "평귝 이익", başlık)
        wb1.write("K9", "평귝 손해", başlık)
        wb1.write("I1", "결과", başlık)

        wb1.write("H2", "=G2", başlık)

        # ŞİMDİ KALANI
        for i in range(len(self.Buy_işlemler)-1):
            wb1.write(2+i, 7, "=G"+str(3+i)+"+H"+str(2+i), başlık)

        # BURADAN İTİBAREN İŞLEMLERİ İŞLEM İŞLEM YAZIYORUM...
        for i in range(len(self.Buy_işlemler)):
            wb1.write(i+1,1,self.Buy_işlemler[i][0],buy_yönü) # YÖN
            wb1.write(i+1,6,"=F"+str(i+2)+"-E"+str(i+2))  #KÂR
            wb1.write(i+1,2,self.Buy_işlemler[i][1],tarihformatı) #GİRİŞ TARİHİ
            wb1.write(i+1,3,self.Buy_işlemler[i][3],tarihformatı) #GİRİŞ TARİHİ
            wb1.write(i+1,4,self.Buy_işlemler[i][2]) #ÇIKIŞ FİYATI
            wb1.write(i+1,5,self.Buy_işlemler[i][4]) #ÇIKIŞ FİYATI

            # WİNRATE YAZIYORUM
        
        if self.Buy_winrate >= 0.45:
            wb1.write("J2",self.Buy_winrate,winrate_formatı1)
        else:
            wb1.write("J2",self.Buy_winrate,winrate_formatı2)

        #KALAN VERİLER
        wb1.write("J6",self.Buy_kârlı_işlem_sayısı)
        wb1.write("K6",self.Buy_zararlı_işlem_sayısı)
        wb1.write("J10",self.Buy_ortalama_kâr)
        wb1.write("K10",self.Buy_ortalama_zarar)
        wb1.write("K2","=J10/K10")
        wb1.write("I2",self.Buy_sonuç,başlık)
        wb1.write("J13","포트폴리오의 최대 가치",başlık)
        wb1.write("J14",max(self.Buy_kümülatif),başlık)
        wb1.write("K13","포트폴리오의 최소 가치",başlık)
        wb1.write("K14",min(self.Buy_kümülatif),başlık)      
        wb1.write("J17","받은 제일 큰 이익",başlık)
        wb1.write("J18",max(self.Buy_sonuçlar),başlık)
        wb1.write("K17","받은 제일 큰 손해",başlık)
        wb1.write("K18",min(self.Buy_sonuçlar),başlık)
        wb1.write("J21","제일 높은 연속 이익 수",başlık)
        wb1.write("J22",max(self.Buy_en_yüksek_ardışık_kârlar),başlık)        
        wb1.write("K21","제일 높은 연속 손해 수",başlık)
        wb1.write("K22",max(self.Buy_en_yüksek_ardışık_zararlar),başlık)
        wb1.write("J25","총 처리 비용",başlık)
        wb1.write("J26",0.33*len(self.Buy_sonuçlar),başlık)
        wb1.write("K25","사실 결과",başlık)
        wb1.write("K26",self.Buy_kümülatif[-1] - 0.33*len(self.Buy_sonuçlar),başlık)

        #Long sayfası bitti -----------------------------------------------------------------------------------------------
        #Shortsayfası başlangıç -----------------------------------------------------------------------------------------------
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
        wb2.write("C1", "처리 시작 날짜", başlık)
        wb2.write("D1", "종료 날짜", başlık)
        wb2.write("E1", "처리 시작 가격", başlık)
        wb2.write("F1", "종료 가격", başlık)
        wb2.write("G1", "이익", başlık)
        wb2.write("H1", "총 이익", başlık)
        wb2.write("J1", "WIN RATE", başlık)
        wb2.write("K1", "이익/손해", başlık)
        wb2.write("J5", "이익이 된 처리 수", başlık)
        wb2.write("K5", "손해가 된 처리 수", başlık)
        wb2.write("J9", "평귝 이익", başlık)
        wb2.write("K9", "평귝 손해", başlık)
        wb2.write("I1", "결과", başlık)

        wb2.write("H2", "=G2", başlık)

        # ŞİMDİ KALANI
        for i in range(len(self.Sell_işlemler)-1):
            wb2.write(2+i, 7, "=G"+str(3+i)+"+H"+str(2+i), başlık)

        # BURADAN İTİBAREN İŞLEMLERİ İŞLEM İŞLEM YAZIYORUM...
        for i in range(len(self.Sell_işlemler)):
            wb2.write(i+1,1,self.Sell_işlemler[i][0],sell_yönü) # YÖN
            wb2.write(i+1,6,"=-1*(F"+str(i+2)+"-E"+str(i+2)+")")  #KÂR
            wb2.write(i+1,2,self.Sell_işlemler[i][1],tarihformatı) #GİRİŞ TARİHİ
            wb2.write(i+1,3,self.Sell_işlemler[i][3],tarihformatı) #GİRİŞ TARİHİ
            wb2.write(i+1,4,self.Sell_işlemler[i][2]) #ÇIKIŞ FİYATI
            wb2.write(i+1,5,self.Sell_işlemler[i][4]) #ÇIKIŞ FİYATI

            # WİNRATE YAZIYORUM
        
        if self.Sell_winrate >= 0.45:
            wb2.write("J2",self.Sell_winrate,winrate_formatı1)
        else:
            wb2.write("J2",self.Sell_winrate,winrate_formatı2)

        #KALAN VERİLER
        wb2.write("J6",self.Sell_kârlı_işlem_sayısı)
        wb2.write("K6",self.Sell_zararlı_işlem_sayısı)
        wb2.write("J10",self.Sell_ortalama_kâr)
        wb2.write("K10",self.Sell_ortalama_zarar)
        wb2.write("K2","=J10/K10")
        wb2.write("I2",self.Sell_sonuç,başlık)
        wb2.write("J13","포트폴리오의 최대 가치",başlık)
        wb2.write("J14",max(self.Sell_kümülatif),başlık)
        wb2.write("K13","포트폴리오의 최소 가치",başlık)
        wb2.write("K14",min(self.Sell_kümülatif),başlık)      
        wb2.write("J17","받은 제일 큰 이익",başlık)
        wb2.write("J18",max(self.Sell_sonuçlar),başlık)
        wb2.write("K17","받은 제일 큰 손해",başlık)
        wb2.write("K18",min(self.Sell_sonuçlar),başlık)
        wb2.write("J21","제일 높은 연속 이익 수",başlık)
        wb2.write("J22",max(self.Sell_en_yüksek_ardışık_kârlar),başlık)        
        wb2.write("K21","제일 높은 연속 손해 수",başlık)
        wb2.write("K22",max(self.Sell_en_yüksek_ardışık_zararlar),başlık)
        wb2.write("J25","총 처리 비용",başlık)
        wb2.write("J26",0.33*len(self.Sell_sonuçlar),başlık)
        wb2.write("K25","사실 결과",başlık)
        wb2.write("K26",self.Sell_kümülatif[-1] - 0.33*len(self.Sell_sonuçlar),başlık)

        workbook.close()


