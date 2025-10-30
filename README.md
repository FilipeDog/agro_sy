# 🌾 AgroGestor - Sistema de Gestão Agropecuária

Sistema completo de gestão para propriedades rurais, integrando gerenciamento de gado, cultivos agrícolas (banana), controle financeiro, recursos humanos e inventário.

## 📋 Sobre o Projeto

AgroGestor é um sistema ERP (Enterprise Resource Planning) desenvolvido em Python com interface desktop, projetado especificamente para atender as necessidades de gestão de propriedades rurais.

### Principais Funcionalidades

- **🐄 Gestão de Gado**
  - Cadastro completo de animais com genealogia
  - Controle de peso e vacinações
  - Gestão de inseminações e reprodução
  - Rastreamento sanitário

- **🍌 Gestão Agrícola (Banana)**
  - Gerenciamento de talhões/campos
  - Controle de tratos culturais
  - Registro de colheitas
  - Controle de pragas e doenças

- **💰 Gestão Financeira**
  - Controle de receitas e despesas
  - Gestão de contas bancárias
  - Projeção de fluxo de caixa
  - Dashboards financeiros

- **👥 Gestão de Pessoas**
  - Cadastro de funcionários
  - Gerenciamento de usuários com níveis de acesso
  - Cadastro de clientes e fornecedores

- **📦 Gestão de Inventário**
  - Controle de estoque
  - Movimentações de entrada/saída
  - Alertas de estoque mínimo

### Recursos Avançados

- Importação/exportação de dados Excel
- Sistema de backup e restauração
- Temas claro e escuro
- Busca global (Ctrl+F)
- Geração de relatórios
- Log de atividades
- Múltiplos métodos de pagamento

## 🏗️ Estrutura do Projeto

```
agro_sy/
│
├── agrogestor/              # Aplicação principal
│   ├── core/                # Núcleo do sistema
│   │   ├── database/        # Banco de dados e migrações
│   │   └── config/          # Configurações
│   │
│   ├── modules/             # Módulos de negócio
│   │   ├── cattle/          # Gestão de gado
│   │   ├── agriculture/     # Gestão agrícola
│   │   ├── financial/       # Gestão financeira
│   │   ├── people/          # Gestão de pessoas
│   │   └── inventory/       # Gestão de inventário
│   │
│   ├── ui/                  # Interface gráfica
│   │   ├── dashboards/      # Dashboards
│   │   ├── reports/         # Relatórios
│   │   └── shared/          # Componentes compartilhados
│   │
│   ├── utils/               # Utilitários
│   └── main.py              # Ponto de entrada
│
├── data/                    # Dados da aplicação
│   ├── backups/             # Backups do banco
│   └── exports/             # Relatórios exportados
│
├── docs/                    # Documentação
├── scripts/                 # Scripts de manutenção
├── tests/                   # Testes
└── requirements.txt         # Dependências
```

## 🚀 Como Usar

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd agro_sy
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando o Sistema

Execute o arquivo principal:

```bash
python agrogestor/main.py
```

ou

```bash
python3 agrogestor/main.py
```

### Credenciais Padrão

- **Usuário**: admin
- **Senha**: admin123
- **Licença**: DEMO-2024-GADO-CTRL

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia |
|------------|------------|
| Linguagem | Python 3.7+ |
| Interface | Tkinter + ttkbootstrap |
| Banco de Dados | SQLite3 |
| Excel | openpyxl |
| Relatórios | reportlab |
| Gráficos | matplotlib |
| Imagens | Pillow |

## 📚 Documentação

A documentação completa está disponível no diretório `docs/`:

- [Guia de Importação Excel](docs/GUIA_IMPORTACAO_EXCEL.md)
- [Novas Funcionalidades](docs/NOVAS_FUNCIONALIDADES.md)
- [Melhorias Implementadas](docs/MELHORIAS_IMPLEMENTADAS.md)
- [Proposta de Melhorias](docs/PROPOSTA_MELHORIAS.md)

## 🔧 Scripts de Manutenção

Scripts úteis disponíveis em `scripts/`:

- `check_imports.py` - Verificar imports
- `check_syntax.py` - Verificar sintaxe
- `check_code_quality.py` - Análise de qualidade
- `check_database.py` - Verificar integridade do banco
- `fix_all_encoding.py` - Corrigir encoding UTF-8

## 📊 Banco de Dados

O sistema utiliza SQLite com 29 tabelas organizadas em categorias:

- **Autenticação**: usuários, licenças
- **Cadastros**: animais, clientes, fornecedores, funcionários
- **Gestão de Gado**: aplicações, inseminações, controle de peso
- **Gestão Agrícola**: talhões, colheitas, tratos culturais, pragas
- **Financeiro**: despesas, receitas, contas bancárias, transferências
- **Inventário**: itens, movimentações

## 🎨 Temas

O sistema suporta dois temas:

- **Claro** (Flatly) - interface clara e moderna
- **Escuro** (Darkly) - interface escura para reduzir fadiga visual

## 📝 Licença

Sistema desenvolvido para gestão agropecuária.

## 👥 Níveis de Acesso

O sistema possui 3 níveis de acesso:

1. **Administrador** - Acesso completo ao sistema
2. **Gerente** - Acesso a maioria das funcionalidades
3. **Operador** - Acesso limitado a operações básicas

## 🔄 Backup e Restauração

O sistema oferece funcionalidades completas de backup:

- Backup manual ou automático
- Backups compactados
- Informações detalhadas de cada backup
- Restauração point-in-time

## 📈 Relatórios

Relatórios disponíveis:

- Relatórios de gado por status/raça/pasto
- Relatórios financeiros (despesas vs receitas)
- Relatórios de produção agrícola
- Relatórios de movimentações por período

## 🌐 Idioma

Interface em Português (Brasil)

---

**AgroGestor v1.0.0** - Sistema de Gestão Agropecuária
