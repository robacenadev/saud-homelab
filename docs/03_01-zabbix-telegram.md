# Configuração de Notificações Telegram no Zabbix

> Guia prático para configurar notificações via Telegram no Zabbix 6.0/7.0 com suporte a múltiplos usuários, Telegrams diferentes e host groups específicos.

---

## 📋 Índice

1. [Parte 1: Preparação Inicial](#parte-1-preparação-inicial)
2. [Parte 2: Configuração no Zabbix](#parte-2-configuração-no-zabbix-interface-web)
3. [Parte 3: Criar Ações](#parte-3-criar-ações-uma-por-host-group)
4. [Parte 4: Testes](#parte-4-testes)

---

## PARTE 1: PREPARAÇÃO INICIAL

### 1️⃣ Criar um Bot no Telegram

**Descrição:** O bot é um programa no Telegram que irá enviar as mensagens de alerta.

**Passos:**

1. Abra o Telegram
2. Procure por **@BotFather**
3. Clique em "Iniciar"
4. Envie `/newbot`
5. Escolha um nome para o bot (ex: "ZabbixNotificador")
6. Escolha um username (ex: "zabbix_notificador_bot")
7. **Guarde o TOKEN gerado**
   - Exemplo: `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`
   - ⚠️ **Nunca compartilhe ou suba este token para o GitHub!**

---

### 2️⃣ Obter IDs do Telegram de Cada Pessoa

**Descrição:** Cada pessoa que vai receber alertas precisa de um ID único no Telegram.

**Passos para cada pessoa:**

1. Procure por **@myidbot** no Telegram
2. Clique em "Iniciar"
3. Envie uma mensagem qualquer
4. O bot responderá com seu ID
5. **Guarde este número**

**Exemplo — Tabela de IDs:**

| Nome  | ID Telegram  | Ambiente     |
|-------|--------------|--------------|
| João  | 1111111111   | Produção     |
| Maria | 2222222222   | Produção     |
| Pedro | 3333333333   | Homologação  |
| Ana   | 4444444444   | Cliente_A    |

> 💾 **Dica:** Salve esta tabela em um local seguro (fora do repositório). Você precisará destes dados depois.

---

### 3️⃣ Instalar Dependências no Servidor Zabbix

**Descrição:** Instalar as ferramentas necessárias para o script Python funcionar.

**Comandos:**

```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install pyTelegramBotAPI
```

**Verificar instalação:**

```bash
python3 --version
python3 -c "import telebot; print('OK')"
```

> ✅ Se aparecer "OK", a instalação foi bem-sucedida!

---

### 4️⃣ Criar o Script Python

**Descrição:** Este script irá enviar as mensagens de alerta para o Telegram.

O script está disponível em [`scripts/telegram_notification.py`](../scripts/telegram_notification.py).

**Passo 1 — Copiar o script:**

```bash
sudo cp telegram_notification.py /usr/lib/zabbix/alertscripts/
```

**Passo 2 — Editar e inserir seu TOKEN:**

```bash
sudo nano /usr/lib/zabbix/alertscripts/telegram_notification.py
```

- Procure por `SEU_BOT_TOKEN_AQUI`
- Substitua pelo TOKEN obtido no passo 1

> ⚠️ **Nunca salve o TOKEN diretamente no arquivo que vai para o GitHub!**

---

### 5️⃣ Configurar Permissões do Script

```bash
sudo chmod +x /usr/lib/zabbix/alertscripts/telegram_notification.py
sudo chown zabbix:zabbix /usr/lib/zabbix/alertscripts/telegram_notification.py
```

**Verificar:**

```bash
ls -la /usr/lib/zabbix/alertscripts/telegram_notification.py
```

> ✅ Deve aparecer: `-rwxr-xr-x 1 zabbix zabbix ...`

---

### 6️⃣ Testar o Script Manualmente

```bash
sudo -u zabbix python3 /usr/lib/zabbix/alertscripts/telegram_notification.py "SEU_ID_AQUI" "Teste" "Se recebeu, funciona!"
```

> ✅ Se recebeu a mensagem no Telegram, tudo certo! Prossiga para a Parte 2.

> ❌ Se não recebeu, verifique:
> - O ID do Telegram está correto?
> - O TOKEN está correto no script?
> - Você iniciou conversa com o bot? (envie `/start`)

---

## PARTE 2: CONFIGURAÇÃO NO ZABBIX (Interface Web)

### 7️⃣ Criar Host Groups

1. Vá em **Monitoring** → **Hosts**
2. Clique em **"Create host group"**
3. Crie os grupos necessários:

| Nome do Group   | Ambiente     |
|-----------------|--------------|
| Producao        | Produção     |
| Homologacao     | Homologação  |
| Cliente_A       | Cliente A    |

> 💡 Use nomes sem espaços. Use underscore (`_`) se precisar separar palavras.

---

### 8️⃣ Criar o Media Type

1. Vá em **Administration** → **Media types**
2. Clique em **"Create media type"**

| Campo            | Valor                         |
|------------------|-------------------------------|
| Name             | `Telegram`                    |
| Type             | `Script`                      |
| Script name      | `telegram_notification.py`    |
| Enabled          | ✓                             |

**Script Parameters (adicionar nesta ordem):**

1. `{ALERT.SENDTO}`
2. `{ALERT.SUBJECT}`
3. `{ALERT.MESSAGE}`

---

### 9️⃣ Criar Usuários (Um por Pessoa)

1. Vá em **Administration** → **Users** → **"Create user"**

| Campo      | Valor exemplo      |
|------------|--------------------|
| Username   | `usuario_joao`     |
| Name       | `João`             |
| User type  | `User`             |

**Aba "Permissions":** Adicione o host group do usuário com permissão `Read`.

**Aba "Media":**

| Campo   | Valor                  |
|---------|------------------------|
| Type    | `Telegram`             |
| Send to | ID do Telegram do usuário |

---

### 🔟 Criar User Groups

1. Vá em **Administration** → **User groups** → **"Create user group"**

| User Group         | Membros                  |
|--------------------|--------------------------|
| Grupo_Producao     | usuario_joao, usuario_maria |
| Grupo_Homologacao  | usuario_pedro            |
| Grupo_Cliente_A    | usuario_ana              |

---

## PARTE 3: CRIAR AÇÕES (Uma por Host Group)

> ⚠️ **Este é o passo mais importante!** Uma ação separada por host group garante que alertas não se misturem.

### 1️⃣1️⃣ Criar Ação para Produção

1. Vá em **Alerts** → **Actions** → **Trigger actions** → **"Create action"**

**Aba "Action":**

| Campo   | Valor            |
|---------|------------------|
| Name    | `Alerta_Producao`|
| Enabled | ✓                |

**Aba "Conditions":**

| Type             | Operator                    | Value       |
|------------------|-----------------------------|-------------|
| Host group       | `=`                         | `Producao`  |
| Trigger severity | `is greater than or equals` | `High`      |

**Aba "Operations" — Mensagem:**

```
Subject: 🚨 ALERTA PRODUÇÃO: {TRIGGER.NAME}

AMBIENTE: PRODUÇÃO
Host: {HOST.NAME}
Problema: {TRIGGER.NAME}
Severidade: {TRIGGER.SEVERITY}
Data/Hora: {EVENT.DATE} {EVENT.TIME}
```

---

### 1️⃣2️⃣ Criar Ação para Homologação

Repita o processo acima alterando:

| Campo             | Valor                              |
|-------------------|------------------------------------|
| Name              | `Alerta_Homologacao`               |
| Condition         | Host group = `Homologacao`         |
| Send to           | `Grupo_Homologacao`                |
| Subject           | `⚠️ ALERTA HOMOLOGAÇÃO: {TRIGGER.NAME}` |

---

### 1️⃣3️⃣ Criar Ação para Cliente A

| Campo             | Valor                              |
|-------------------|------------------------------------|
| Name              | `Alerta_Cliente_A`                 |
| Condition         | Host group = `Cliente_A`           |
| Send to           | `Grupo_Cliente_A`                  |
| Subject           | `📢 ALERTA CLIENTE A: {TRIGGER.NAME}` |

---

## PARTE 4: TESTES

### 1️⃣4️⃣ Testar a Configuração Completa

**Teste 1 — Alerta de Produção:**
1. Force um problema em um host do grupo `Producao`
2. Aguarde 2-3 minutos
3. ✅ Esperado: João e Maria recebem | Pedro e Ana **não** recebem

**Teste 2 — Alerta de Homologação:**
1. Force um problema em host do grupo `Homologacao`
2. ✅ Esperado: Apenas Pedro recebe

**Teste 3 — Alerta de Cliente A:**
1. Force um problema em host do grupo `Cliente_A`
2. ✅ Esperado: Apenas Ana recebe

---

## 🔧 TROUBLESHOOTING

### ❌ Mensagem não é recebida

```bash
# Teste manual do script
sudo -u zabbix python3 /usr/lib/zabbix/alertscripts/telegram_notification.py "SEU_ID" "Test" "Test"
```

- Verifique se o ID do Telegram está correto
- Envie `/start` para o bot no Telegram
- Aguarde 2-3 minutos (o Zabbix processa em intervalos)

### ❌ Alerta de um grupo dispara para outro

- Verifique a **condition de Host group** na ação
- Verifique em qual grupo o host realmente está: **Monitoring → Hosts → clique no host**

### ❌ Usuário não vê os hosts no Zabbix

- Verifique as **Permissions** do usuário
- O host group foi adicionado com permissão `Read`?

### ❌ Script não executa

```bash
python3 --version
python3 -c "import telebot; print('OK')"
```

---

## 📊 CHECKLIST FINAL

- [ ] Bot criado no Telegram
- [ ] IDs do Telegram obtidos e salvos em local seguro
- [ ] Dependências instaladas (`python3-pip`, `pyTelegramBotAPI`)
- [ ] Script Python criado com TOKEN configurado
- [ ] Script testado manualmente
- [ ] Permissões do script configuradas
- [ ] Media Type "Telegram" criado no Zabbix
- [ ] Host Groups criados
- [ ] Usuários criados com ID do Telegram
- [ ] User Groups criados
- [ ] Ações criadas por Host Group
- [ ] Todos os testes passaram ✅

---

## 📝 Como Escalar

### Adicionar novo cliente

1. Criar Host Group `Cliente_B`
2. Criar usuário com acesso ao grupo
3. Criar User Group `Grupo_Cliente_B`
4. Criar Ação `Alerta_Cliente_B`
5. Testar

### Adicionar novo usuário a ambiente existente

1. Criar usuário com acesso ao host group desejado
2. Editar o User Group correspondente e adicionar o usuário
3. Pronto! O usuário receberá os alertas no seu Telegram

---

## 📚 Referências

- [Documentação Zabbix - Media Types](https://www.zabbix.com/documentation)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

---

**Última atualização:** 2025-12-05  
**Status:** ✅ Completo e Testado
