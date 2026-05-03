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
