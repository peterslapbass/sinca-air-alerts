# SINCA Air Alerts 🇨🇱

Sistema automático de alertas de calidad del aire basado en datos del SINCA (Chile).

## 🚀 Qué hace

- Consume datos en tiempo real desde SINCA
- Evalúa niveles de PM2.5
- Detecta cambios de estado (normal → alerta)
- Envía notificaciones (opcional vía Telegram)

## ⚙️ Configuración

1. Clonar repo
2. Instalar dependencias:
# SINCA Air Alerts 🇨🇱

Sistema automático de alertas de calidad del aire basado en datos del SINCA (Chile).

## 🚀 Qué hace

- Consume datos en tiempo real desde SINCA
- Evalúa niveles de PM2.5
- Detecta cambios de estado (normal → alerta)
- Envía notificaciones (opcional vía Telegram)

## ⚙️ Configuración

1. Clonar repo
2. Instalar dependencias:
pip install -r requirements.txt

3. Configurar variables de entorno:
- TELEGRAM_TOKEN
- CHAT_ID

4. Ejecutar:
python src/main.py

## ⏱ Automatización

El proyecto incluye GitHub Actions para ejecución cada 10 minutos.

## 📊 Variables evaluadas

- PM2.5
- >50 → warning
- >100 → crítico

## 🧠 Futuras mejoras

- Soporte multi-contaminante
- Panel web de alertas
- Predicción de tendencias

## Bot interactivo (experimental)

El proyecto incluye un bot.py opcional para interacción mediante comandos de Telegram.

Ejemplo:

/top_pm25  
/top_pm10

El bot requiere ejecución persistente (run_polling()), por lo que no está habilitado en GitHub Actions por defecto.

Puede desplegarse en:
- Render
- Railway
- VPS
- Raspberry Pi

Mientras tanto, main.py mantiene el sistema automático de alertas y rankings mediante GitHub Actions.
