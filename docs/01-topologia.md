# 🖥️ Topologia do Ambiente

Visualização da infraestrutura do ambiente Saud Homelab.

---

## 🗺️ Diagrama de Topologia

```mermaid
graph TB
    subgraph PC_Principal["💻 PC Principal (Host Hyper-V)"]
        Windows[Windows OS]
        HyperV[Hyper-V Manager]
    end

    subgraph VM_Ubuntu["🐧 VM Ubuntu 22.04 LTS"]
        Ubuntu[Ubuntu 22.04]

        subgraph Servicos["Serviços"]
            Zabbix[🔍 Zabbix Server<br/>Porta: 10051]
            MySQL[🗄️ MySQL Database<br/>Porta: 3306]
        end
    end

    Windows --> HyperV
    HyperV --> Ubuntu
    Ubuntu --> Zabbix
    Ubuntu --> MySQL
    Zabbix --> MySQL

    style PC_Principal fill:#e1f5ff
    style VM_Ubuntu fill:#fff4e1
    style Zabbix fill:#90EE90
    style MySQL fill:#FFD700
    style Servicos fill:#ffe0b2
```

---

## 🌐 Endereços de Acesso

| Serviço       | IP (exemplo)   | Porta |
|---------------|----------------|-------|
| Zabbix Web    | 192.168.x.110  | 80    |
| Zabbix Server | 192.168.x.110  | 10051 |
| MySQL         | 192.168.x.110  | 3306  |

> 💡 Substitua `192.168.x.110` pelo IP real da sua VM na sua rede local.

---

## 💻 Componentes

### PC Principal (Host)
- **OS:** Windows com Hyper-V habilitado
- **Função:** Hospedar a VM do Zabbix
- **Ferramenta de doc:** Obsidian

### VM Linux
- **OS:** Ubuntu Server 22.04 LTS
- **Serviços:**
  - **Zabbix Server** — Coleta e processa os dados de monitoramento
  - **MySQL** — Armazena o histórico e configurações do Zabbix

---

## 🔗 Fluxo de Comunicação

```
Hosts monitorados → Zabbix Agent (10050)
                  → Zabbix Server (10051)
                  → MySQL (3306)
```

---

**Versão:** 2.0  
**Última atualização:** 2025-11-15
