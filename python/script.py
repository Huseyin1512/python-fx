# Burda robotu kodlayacağım şartı vereceğim(diğer dosyalardan gelen fonksiyonların döndürdüğüne göre doğru yönde işleme giriyor.)
from veriler import Veri
import grafikler as göster
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import time
mt5.initialize()
account = 5009681664
authorized = mt5.login(account, password="yhpaugj4")


"""

Name     : dneem BEŞDAKKALIK
Type     : Forex Hedged USD
Server   : MetaQuotes-Demo
Login    : 66514137
Password : 1delqueo
Investor : iev8pmei


"""
işleme_giriş_fiyatı = []

Veri_düzen = Veri()

df = Veri_düzen.veri_al(ürün_adı="XAUUSD", periyot="15M", uzaklık=25000)


Veri_düzen.veri_indikatör_ekle_ATR(df=df, periyot=21)

ATR = 2.5
işlem_girmeye_uygun_mu = 0


def longla(symbol, lot):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
    # sembol MarketWatch'te yoksa, ekle
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("symbol_select({}}) failed, exit", symbol)
            mt5.shutdown()
            quit()
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 500
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price-ATR,
        "tp": price + 3*ATR,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # işlem isteği gönder
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
    işleme_giriş_fiyatı.append(price)
    return result


def shortla(symbol, lot):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
    # sembol MarketWatch'te yoksa, ekle
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("symbol_select({}}) failed, exit", symbol)
            mt5.shutdown()
            quit()
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 500
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price+ATR,
        "tp": price-3*ATR,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # işlem isteği gönder
    sonuç = mt5.order_send(request)
    if sonuç.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(sonuç.retcode))
    işleme_giriş_fiyatı.append(price)
    return sonuç


def sl_değiştirme(ticket,yeni_sl,tp):
    request = {
    "action": mt5.TRADE_ACTION_SLTP,
    "position": ticket,
    "sl": yeni_sl,
    "tp": tp,
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK,
    "ENUM_ORDER_STATE": mt5.ORDER_FILLING_RETURN,
}
    #// perform the check and display the result 'as is'
    result = mt5.order_send(request)

    if result is not None and  result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))

        print(" result",result)
    if result is None:
        result = mt5.order_send(request)

pozisyon_sayısı = mt5.positions_total()
son_işlem = "Buy"
iz_süren_buy = 0
iz_süren_sell = 100000000

pozisyon_bilgileri = mt5.positions_get()
print(pozisyon_bilgileri)
tp = pozisyon_bilgileri[0].tp
ticket = pozisyon_bilgileri[0].ticket
iz_süren_sl = pozisyon_bilgileri[0].price_current - ATR
sl_değiştirme(ticket=ticket,yeni_sl=1930,tp=tp)

"""while True:
    if pozisyon_sayısı == 0 and son_işlem == "Sell":
        longla("XAUUSD", 1.0)
        son_işlem = "Buy"
        print("Long işleme girdi1")
        pozisyon_sayısı = mt5.positions_total()
    if pozisyon_sayısı == 0 and son_işlem == "Buy":
        shortla("XAUUSD", 1.0)
        son_işlem = "Sell"
        print("Short işleme girdi")
        pozisyon_sayısı = mt5.positions_total()
    if pozisyon_sayısı == 1: 
        if son_işlem == "Buy":
            # Buy yönlü işlemde isem
            pozisyon_bilgileri = mt5.positions_get()
            ticket = pozisyon_bilgileri[0].ticket
            tp = pozisyon_bilgileri[0].tp
            if pozisyon_bilgileri[0].price_current - pozisyon_bilgileri[0].price_open >= 1.5*ATR:
                iz_süren_sl = pozisyon_bilgileri[0].price_current - ATR
                if iz_süren_sl > iz_süren_buy:
                    iz_süren_buy = iz_süren_sl
                    sl_değiştirme(ticket=ticket,yeni_sl=iz_süren_buy,tp=tp)
                    print(f"Buy iz süren sl değiştirildi. yeni iz süren sl:{iz_süren_buy}")
        else:
            # Sell yönlü işlemde isem
            pozisyon_bilgileri = mt5.positions_get()
            ticket = pozisyon_bilgileri[0].ticket
            tp = pozisyon_bilgileri[0].tp
            if pozisyon_bilgileri[0].price_open - pozisyon_bilgileri[0].price_current >= ATR:
                iz_süren_sl = pozisyon_bilgileri[0].price_current + ATR
                if iz_süren_sl < iz_süren_sell:
                    iz_süren_sell = iz_süren_sl
                    sl_değiştirme(ticket=ticket,yeni_sl=iz_süren_sell,tp=tp)
                    print(f"Sel iz süren sl değiştirildi. yeni iz süren sl:{iz_süren_sell}")

    time.sleep(0.3)
    pozisyon_sayısı = mt5.positions_total()"""




