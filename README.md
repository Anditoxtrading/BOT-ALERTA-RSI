# Bot de RSI para Binance Futuros y Alertas en Telegram

Este proyecto implementa un bot en Python que calcula el RSI (Índice de Fuerza Relativa) de todos los pares de criptomonedas con el par USDT en Binance Futuros. Si el RSI de alguna moneda está por debajo de 20 (condición de sobreventa) o por encima de 80 (condición de sobrecompra), el bot envía una alerta a un chat de Telegram indicando si es un momento potencial para "Long" o "Short".

---

## Funcionalidades
- Obtiene todos los pares USDT de Binance Futuros.
- Calcula el RSI en un intervalo de tiempo de 4 horas para cada par.
- Envía alertas a Telegram si el RSI está en condiciones extremas:
  - RSI <= 20: Indica "Long".
  - RSI >= 80: Indica "Short".
- Funciona en un bucle infinito, actualizando los datos periódicamente.

---

## Requisitos

### Lenguaje
- **Python 3.7 o superior**

### Librerías necesarias
Debes instalar las siguientes librerías antes de ejecutar el proyecto:

 **`Librerias`**    
   ```bash
   pip install pandas
   pip install numpy
   pip install python-binance
   pip install pyTelegramBotAPI

   
### No es necesario colocar las apis de binance para que el bot funcione correctamente
