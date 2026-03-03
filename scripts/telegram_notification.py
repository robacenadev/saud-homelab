#!/usr/bin/python3
"""
telegram_notification.py
Script de alerta do Zabbix via Telegram.

Uso:
    python3 telegram_notification.py <CHAT_ID> <SUBJECT> <MESSAGE>

Configuração:
    Substitua SEU_BOT_TOKEN_AQUI pelo token gerado pelo @BotFather.
"""

import telebot
import sys

# =============================================
# CONFIGURAÇÃO — substitua pelo seu token real
# ⚠️ Mantenha este token fora do repositório!
# =============================================
BOT_TOKEN = 'SEU_BOT_TOKEN_AQUI'

def main():
    if len(sys.argv) < 4:
        print("Uso: telegram_notification.py <CHAT_ID> <SUBJECT> <MESSAGE>")
        sys.exit(1)

    destination = sys.argv[1]
    subject     = sys.argv[2]
    message     = sys.argv[3]

    # Normalizar quebras de linha
    message = message.replace('\\n', '\n').replace('/n', '\n')

    try:
        tb = telebot.TeleBot(BOT_TOKEN)
        tb.send_message(
            destination,
            subject + '\n' + message,
            disable_web_page_preview=True,
            parse_mode='HTML'
        )
        print(f"Mensagem enviada com sucesso para {destination}")
        sys.exit(0)

    except Exception as e:
        print(f"Erro ao enviar mensagem: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
