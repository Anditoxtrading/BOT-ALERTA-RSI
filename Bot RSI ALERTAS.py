import time
import pandas as pd
import numpy as np
from binance.client import Client
import telebot

# Claves de API de Binance
API_KEY = 'tu_api_key'
API_SECRET = 'tu_api_secret'

# Conectar al cliente de Binance
client = Client(API_KEY, API_SECRET)

# Configuración de Telegram
bot_token = ""
bot = telebot.TeleBot(bot_token)
chat_id = 

# Función para enviar mensaje a Telegram
def enviar_alerta_telegram(message):
    try:
        bot.send_message(chat_id, message)
    except Exception as e:
        print(f"Error al enviar alerta a Telegram: {e}")

def obtener_datos_klines(simbolo, intervalo, limite=100):
    """
    Obtiene datos históricos de velas (klines) desde Binance.
    """
    klines = client.futures_klines(symbol=simbolo, interval=intervalo, limit=limite)
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df['close'] = pd.to_numeric(df['close'])
    return df[['timestamp', 'close']]

def calcular_rsi(datos, periodos=14):
    """
    Calcula el RSI a partir de datos de cierre.
    """
    delta = datos['close'].diff()
    ganancia = np.where(delta > 0, delta, 0)
    perdida = np.where(delta < 0, -delta, 0)
    
    avg_ganancia = pd.Series(ganancia).rolling(window=periodos).mean()
    avg_perdida = pd.Series(perdida).rolling(window=periodos).mean()
    
    rs = avg_ganancia / avg_perdida
    rsi = 100 - (100 / (1 + rs))
    datos['rsi'] = rsi
    return datos

def obtener_rsi_actual(simbolo, intervalo):
    """
    Obtiene el RSI más reciente para un símbolo en Binance.
    """
    datos = obtener_datos_klines(simbolo, intervalo)
    datos_rsi = calcular_rsi(datos)
    rsi_actual = datos_rsi.iloc[-1]
    return {
        "symbol": simbolo,
        "timestamp": rsi_actual["timestamp"],
        "close": rsi_actual["close"],
        "rsi": rsi_actual["rsi"]
    }

def obtener_todos_los_pares_usdt():
    """
    Obtiene todos los símbolos que terminan en USDT de Binance Futuros.
    """
    info = client.futures_exchange_info()
    pares_usdt = [symbol['symbol'] for symbol in info['symbols'] if symbol['symbol'].endswith('USDT')]
    return pares_usdt

# Configuración del bot
intervalo = "4h"  # Intervalo de tiempo de 4 horas

# Iniciar bucle infinito
while True:
    try:
        # Obtener todos los pares USDT
        pares_usdt = obtener_todos_los_pares_usdt()

        # Calcular el RSI de todos los pares y enviar alertas
        for simbolo in pares_usdt:
            try:
                resultado = obtener_rsi_actual(simbolo, intervalo)
                rsi = resultado['rsi']
                mensaje = None

                # Evaluar RSI para enviar alertas
                if rsi < 20:
                    mensaje = f"🟢 *LONG ALERT* 🟢\n\nSímbolo: {simbolo}\nRSI: {rsi:.2f} (Sobrevendido)\nPrecio: {resultado['close']:.2f} USDT"
                elif rsi > 80:
                    mensaje = f"🔴 *SHORT ALERT* 🔴\n\nSímbolo: {simbolo}\nRSI: {rsi:.2f} (Sobrecomprado)\nPrecio: {resultado['close']:.2f} USDT"

                # Enviar mensaje si hay alerta
                if mensaje:
                    enviar_alerta_telegram(mensaje)
                    print(mensaje)  # Log para verificar en consola
            
            except Exception as e:
                print(f"Error al procesar {simbolo}: {e}")

        # Esperar antes de la siguiente iteración
        print("Esperando 15 minutos para la próxima evaluación...")
        time.sleep(900)  # 15 minutos de espera (900 segundos)

    except Exception as e:
        print(f"Error en el bucle principal: {e}")
        time.sleep(60)  # Esperar un minuto antes de intentar de nuevo
