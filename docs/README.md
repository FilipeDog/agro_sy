# 🐄🍌 Sistema de Gestão Agropecuária - Gado e Bananal

Sistema completo para gestão integrada de fazendas com produção de gado bovino e bananal.

## 📋 Visão Geral

Sistema ERP completo desenvolvido em Python com interface gráfica moderna, permitindo controle total de:
- 🐄 **Rebanho Bovino**: Cadastro, sanidade, reprodução, pesagem e vendas
- 🍌 **Bananal**: Talhões, tratos culturais, colheitas e comercialização
- 💰 **Financeiro**: Despesas, receitas e contas bancárias integradas
- 👥 **RH**: Funcionários e usuários com níveis de acesso
- 📦 **Inventário**: Controle de estoque com alertas
- 📊 **Relatórios**: Diversos relatórios e dashboards

## ✨ Principais Funcionalidades

### Módulo de Gado
- ✅ Cadastro completo de animais (brinco, raça, genealogia)
- ✅ Controle sanitário (vacinas, medicamentos, vermífugos)
- ✅ Reprodução (inseminações, nascimentos)
- ✅ Controle de peso e ganho
- ✅ Movimentações e vendas

### Módulo de Bananal
- ✅ Gestão de talhões (área, variedade, plantio)
- ✅ Tratos culturais (adubação, irrigação, desbaste)
- ✅ Controle de pragas e doenças
- ✅ Colheitas com classificação (A, B, C)
- ✅ Previsão de colheitas

### Financeiro
- ✅ Despesas e receitas detalhadas
- ✅ Múltiplas formas de pagamento
- ✅ Contas bancárias e transferências
- ✅ Relatórios financeiros

### Gestão de Pessoas
- ✅ Cadastro de funcionários
- ✅ Controle de usuários com 3 níveis (Admin, Gerente, Operador)
- ✅ Log de atividades
- ✅ Primeiro acesso força troca de senha

### Utilitários
- ✅ **Importar de Excel**: Importe suas planilhas existentes!
- ✅ **Backup/Restore**: Exportar e importar backups completos
- ✅ **Calculadora integrada**
- ✅ **Validações automáticas** (CPF, CNPJ, email)
- ✅ **Sistema de logs**
- ✅ **Temas claro/escuro**

## 🚀 Como Usar

### Instalação

1. **Requisitos**:
   - Python 3.7 ou superior
   - Sistema operacional: Windows, Linux ou macOS

2. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

3. **Executar**:
```bash
python main.py
```

### Primeiro Acesso

**Credenciais padrão**:
- Usuário: `admin`
- Senha: `admin123`
- Licença: `DEMO-2024-GADO-CTRL`

⚠️ **Importante**: Troque a senha após o primeiro login!

## 📊 Importar Dados do Excel

Tem planilhas existentes? **Importe tudo de uma vez!**

1. Menu → **Utilitários** → **Importar de Excel**
2. Selecione seu arquivo Excel
3. Escolha o tipo de dados (Clientes, Animais, etc)
4. Confira o preview
5. Clique em **Importar**

**Não tem planilha pronta?**
- Clique em "Baixar Modelo Excel"
- Preencha com seus dados
- Importe!

📖 Ver [GUIA_IMPORTACAO_EXCEL.md](GUIA_IMPORTACAO_EXCEL.md) para detalhes.

## 🔧 Estrutura do Projeto

```
cattle_management/
├── database/
│   ├── schema.sql (29 tabelas!)
│   ├── db_manager.py
│   └── gado.db (criado automaticamente)
├── ui/
│   ├── Gado: animals_register.py, expenses.py, revenues.py, etc
│   ├── Bananal: talhoes_register.py, tratos_culturais.py, colheitas_banana.py
│   ├── RH: employees_register.py, users_management.py
│   ├── Financeiro: bank_accounts.py
│   ├── Inventário: inventory.py
│   └── main_window.py
├── utils/
│   ├── theme_manager.py (temas claro/escuro)
│   ├── validators.py (CPF, CNPJ, etc)
│   ├── logger.py (sistema de logs)
│   ├── calculator.py (calculadora integrada)
│   ├── backup_manager.py (backup/restore)
│   └── excel_importer.py (importação Excel)
└── backups/ (backups automáticos)
```

## 🗄️ Banco de Dados

**SQLite** com 29 tabelas principais:

### Gado (10 tabelas)
- animais, clientes, fornecedores
- despesas, receitas, aplicacoes
- inseminacoes, controle_peso

### Bananal (10 tabelas)
- talhoes, variedades_banana
- tratos_culturais, pragas_doencas
- colheitas_banana, vendas_banana
- previsao_colheita, estoque_banana

### Gestão (9 tabelas)
- funcionarios, usuarios
- contas_bancarias, inventario_itens
- log_atividades

## 📈 Relatórios Disponíveis

### Gado
- Animais por status, raça, pasto
- Movimentações por período
- Resultado financeiro

### Bananal
- Produção por talhão
- Custos por hectare
- Classificação de colheitas

### Financeiro
- Despesas vs Receitas
- Fluxo de caixa
- Contas a pagar/receber

## 🔒 Segurança

- ✅ Senhas criptografadas (SHA256)
- ✅ 3 níveis de acesso de usuários
- ✅ Log de todas as atividades
- ✅ Backup automático antes de restaurar
- ✅ Soft delete (registros não são excluídos permanentemente)

## 🆘 Suporte e Problemas

### Problemas Comuns

**"CÃdigo" ao invés de "Código"**
✅ RESOLVIDO! Todos os arquivos convertidos para UTF-8

**Erro ao importar Excel**
- Verifique se o arquivo está fechado
- Confirme o formato (DD/MM/AAAA para datas)

**Banco corrompido**
- Menu → Utilitários → Importar Backup
- Escolha um backup anterior

## 📝 Licença

Sistema desenvolvido para uso em fazendas e propriedades rurais.

## 🤝 Contribuindo

Encontrou um bug? Tem uma sugestão?
- Abra uma issue
- Descreva o problema ou sugestão
- Inclua prints se possível

## 📞 Contato

Para suporte técnico, consulte a documentação ou abra uma issue.

---

## 🎯 Próximas Funcionalidades

- [ ] Exportação de relatórios em PDF
- [ ] Gráficos nos dashboards
- [ ] App mobile
- [ ] Integração com balanças eletrônicas
- [ ] Alertas automáticos via WhatsApp

---

**Desenvolvido com ❤️ usando Python e Claude Code**

🤖 Generated with [Claude Code](https://claude.com/claude-code)
