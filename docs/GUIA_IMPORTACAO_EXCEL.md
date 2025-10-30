# 📊 Guia de Importação de Dados via Excel

## Como Importar Suas Planilhas

### 1️⃣ Preparar Planilha Excel

#### Formato Necessário:
- **Primeira linha**: Nomes das colunas (cabeçalhos)
- **Segunda linha em diante**: Seus dados

#### Exemplo para Clientes:
```
| nome          | cpf_cnpj      | email           | telefone      | cidade    | uf |
|---------------|---------------|-----------------|---------------|-----------|-------|
| João Silva    | 123.456.789-00| joao@email.com  | (11)99999-9999| São Paulo | SP |
| Maria Santos  | 987.654.321-00| maria@email.com | (11)88888-8888| Campinas  | SP |
```

### 2️⃣ Colunas Por Tipo de Dado

#### **Clientes / Fornecedores**
- `nome` (obrigatório)
- `cpf_cnpj`
- `email`
- `telefone`
- `cidade`
- `uf`
- `endereco`
- `cep`
- `observacoes`

#### **Funcionários**
- `nome` (obrigatório)
- `cpf`
- `rg`
- `telefone`
- `email`
- `cargo`
- `setor`
- `salario`
- `data_nascimento` (formato: DD/MM/AAAA)
- `data_admissao` (formato: DD/MM/AAAA)

#### **Animais**
- `brinco` (obrigatório)
- `lote`
- `sexo` (Macho ou Fêmea)
- `data_nascimento` (formato: DD/MM/AAAA)
- `peso_atual`
- `nome`
- `observacao`

#### **Talhões (Bananal)**
- `codigo` (obrigatório)
- `nome` (obrigatório)
- `area_hectares` (obrigatório)
- `localizacao`
- `data_plantio` (formato: DD/MM/AAAA)
- `espacamento` (ex: 3m x 2m)
- `densidade_plantas_ha`

#### **Despesas**
- `data_gasto` (formato: DD/MM/AAAA)
- `descricao`
- `valor`
- `tipo_despesa` (ex: Ração, Medicamento)
- `fornecedor`
- `quantidade`

#### **Receitas**
- `data_venda` (formato: DD/MM/AAAA)
- `descricao`
- `valor_total`
- `quantidade`
- `cliente`

### 3️⃣ Como Importar no Sistema

1. **Menu** → Utilitários → **Importar de Excel**

2. **Selecionar Arquivo**
   - Clique em "Selecionar Excel"
   - Escolha seu arquivo .xlsx ou .xls

3. **Configurar Importação**
   - **Tipo de Dados**: Escolha o que está importando (Clientes, Animais, etc)
   - **Planilha**: Se tiver múltiplas abas, escolha qual
   - **Linha inicial**: Geralmente linha 2 (primeira com dados)

4. **Verificar Preview**
   - O sistema mostra as primeiras 20 linhas
   - Confira se os dados estão corretos

5. **Importar**
   - Clique em "Importar Dados"
   - Confirme a ação
   - Aguarde o resultado

### 4️⃣ Baixar Modelos Prontos

**Não sabe como fazer a planilha?**

1. No importador, selecione o **Tipo de Dados**
2. Clique em **"Baixar Modelo Excel"**
3. Salve o arquivo
4. Preencha com seus dados
5. Importe de volta!

### 5️⃣ Dicas Importantes

✅ **Datas**: Use formato DD/MM/AAAA (ex: 25/10/2024)
✅ **Números**: Use vírgula ou ponto (ex: 1250.50 ou 1250,50)
✅ **Telefones**: Com ou sem formatação (aceita ambos)
✅ **CPF/CNPJ**: Com ou sem pontos/traços

❌ **Evite**:
- Células mescladas
- Linhas ou colunas vazias no meio dos dados
- Caracteres especiais estranhos nos nomes das colunas
- Datas em formato texto

### 6️⃣ Tratamento de Erros

Se houver erros:
- O sistema mostra quais linhas falharam
- As linhas corretas SÃO importadas
- Você pode corrigir o Excel e reimportar só as que falharam

### 7️⃣ Exemplo Completo

**Arquivo: clientes.xlsx**

Planilha "Clientes":
```
nome          | cpf_cnpj       | telefone       | cidade    | uf
João da Silva | 123.456.789-00 | (11)99999-9999 | São Paulo | SP
Maria Oliveira| 987.654.321-00 | (21)88888-8888 | Rio       | RJ
```

**No sistema**:
1. Utilitários → Importar de Excel
2. Selecionar arquivo: clientes.xlsx
3. Tipo: Clientes
4. Planilha: Clientes
5. Linha inicial: 2
6. Importar Dados

**Resultado**: 2 clientes cadastrados! ✅

---

## 🆘 Problemas Comuns

### "Erro ao abrir arquivo"
- Verifique se o arquivo está fechado (não aberto no Excel)
- Confirme se é .xlsx ou .xls

### "Linha X: erro"
- Verifique se todos os campos obrigatórios estão preenchidos
- Confira o formato das datas
- Verifique se números estão sem texto

### "Nenhum dado importado"
- Confira se a "Linha inicial" está correta
- Verifique se a planilha selecionada tem dados

---

## 💡 Você Sabia?

- Pode importar **milhares de registros** de uma vez
- O sistema **valida automaticamente** CPF, datas, etc
- **Não duplica** registros (verifica antes de inserir)
- Funciona com Excel antigo (.xls) e novo (.xlsx)

---

**Dúvidas?** Menu → Utilitários → Sobre
