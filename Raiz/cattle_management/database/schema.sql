-- Schema do Banco de Dados - AgroGestor - Sistema de Gestão de Rebanho

-- Tabela de Usuários (para login)
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    nome_completo TEXT,
    email TEXT,
    nivel_acesso TEXT DEFAULT 'Operador', -- Admin, Gerente, Operador
    primeiro_acesso INTEGER DEFAULT 1, -- 1=primeiro acesso (forçar troca senha)
    ultimo_login TIMESTAMP,
    ativo INTEGER DEFAULT 1,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Licenças
CREATE TABLE IF NOT EXISTS licencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave_licenca TEXT NOT NULL UNIQUE,
    data_ativacao TIMESTAMP,
    data_expiracao TIMESTAMP,
    ativo INTEGER DEFAULT 1
);

-- CADASTROS SECUNDÁRIOS (Tabelas de Lookup)

-- Tipo de Animal
CREATE TABLE IF NOT EXISTS tipo_animal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Tipo de Receita
CREATE TABLE IF NOT EXISTS tipo_receita (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Tipo de Despesa
CREATE TABLE IF NOT EXISTS tipo_despesa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Medicamentos
CREATE TABLE IF NOT EXISTS medicamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    tipo TEXT, -- Medicamento, Vacina, Vermífugo
    unidade TEXT,
    descricao TEXT
);

-- Pastos
CREATE TABLE IF NOT EXISTS pastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    area_hectares REAL,
    descricao TEXT
);

-- Causa da Morte
CREATE TABLE IF NOT EXISTS causa_morte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Status do Animal
CREATE TABLE IF NOT EXISTS status_animal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Raça
CREATE TABLE IF NOT EXISTS raca (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Origem
CREATE TABLE IF NOT EXISTS origem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- CADASTROS PRINCIPAIS

-- Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf_cnpj TEXT UNIQUE,
    email TEXT,
    telefone TEXT,
    uf TEXT,
    cidade TEXT,
    endereco TEXT,
    cep TEXT,
    observacoes TEXT,
    ativo INTEGER DEFAULT 1,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fornecedores
CREATE TABLE IF NOT EXISTS fornecedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf_cnpj TEXT UNIQUE,
    email TEXT,
    telefone TEXT,
    uf TEXT,
    cidade TEXT,
    endereco TEXT,
    cep TEXT,
    observacoes TEXT,
    ativo INTEGER DEFAULT 1,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Animais
CREATE TABLE IF NOT EXISTS animais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brinco TEXT NOT NULL UNIQUE,
    lote TEXT,
    status_id INTEGER,
    pasto_id INTEGER,
    tipo_id INTEGER,
    sexo TEXT, -- Macho, Fêmea
    raca_id INTEGER,
    data_desmama DATE,
    origem_id INTEGER,
    data_compra DATE,
    data_nascimento DATE,
    peso_atual REAL,
    descricao TEXT,
    nome TEXT,
    brinco_pai TEXT,
    brinco_mae TEXT,
    data_entrada DATE,
    observacao TEXT,
    causa_morte_id INTEGER,
    data_morte DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (status_id) REFERENCES status_animal(id),
    FOREIGN KEY (pasto_id) REFERENCES pastos(id),
    FOREIGN KEY (tipo_id) REFERENCES tipo_animal(id),
    FOREIGN KEY (raca_id) REFERENCES raca(id),
    FOREIGN KEY (origem_id) REFERENCES origem(id),
    FOREIGN KEY (causa_morte_id) REFERENCES causa_morte(id)
);

-- LANÇAMENTOS E MOVIMENTAÇÕES

-- Despesas
CREATE TABLE IF NOT EXISTS despesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_despesa_id INTEGER,
    fornecedor_id INTEGER,
    descricao TEXT,
    valor REAL NOT NULL,
    quantidade REAL DEFAULT 1,
    valor_unitario REAL,
    desconto REAL DEFAULT 0,
    valor_final REAL, -- Calculado: (quantidade * valor_unitario) - desconto
    data_gasto DATE NOT NULL,
    data_vencimento DATE,
    data_pagamento DATE,
    pago INTEGER DEFAULT 0,
    forma_pagamento TEXT, -- Dinheiro, PIX, Cartão, Boleto, Transferência
    numero_nota TEXT,
    pago_por INTEGER, -- ID do funcionário que efetuou o pagamento
    conta_bancaria_id INTEGER,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_despesa_id) REFERENCES tipo_despesa(id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
    FOREIGN KEY (pago_por) REFERENCES funcionarios(id),
    FOREIGN KEY (conta_bancaria_id) REFERENCES contas_bancarias(id)
);

-- Aplicações (Sanidade)
CREATE TABLE IF NOT EXISTS aplicacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER,
    brinco TEXT,
    medicamento_id INTEGER,
    status TEXT, -- Concluído, Pendente
    classe TEXT, -- Medicamento, Vacina, Vermífugo
    unidade TEXT,
    data_aplicacao DATE NOT NULL,
    quantidade REAL,
    dose TEXT,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animais(id),
    FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id)
);

-- Inseminações
CREATE TABLE IF NOT EXISTS inseminacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER,
    brinco TEXT,
    data_inseminacao DATE NOT NULL,
    status TEXT, -- Em processo, Concluído
    efetivou INTEGER DEFAULT 0, -- 0=Não, 1=Sim
    data_cria DATE,
    quantidade_crias INTEGER,
    touro_reprodutor TEXT,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animais(id)
);

-- Controle de Peso
CREATE TABLE IF NOT EXISTS controle_peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER,
    brinco TEXT,
    data_pesagem DATE NOT NULL,
    peso REAL NOT NULL,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animais(id)
);

-- Receitas (Vendas)
CREATE TABLE IF NOT EXISTS receitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda DATE NOT NULL,
    tipo_receita_id INTEGER,
    cliente_id INTEGER,
    numero_pedido TEXT,
    numero_lote TEXT,
    numero_nota TEXT,
    descricao TEXT,
    quantidade REAL,
    valor_unitario REAL,
    desconto REAL DEFAULT 0,
    valor_total REAL, -- Calculado: (quantidade * valor_unitario) - desconto
    valor_final REAL, -- Mesmo que valor_total (mantido para consistência)
    data_vencimento DATE,
    data_pagamento DATE,
    pago INTEGER DEFAULT 0,
    forma_pagamento TEXT, -- Dinheiro, PIX, Cartão, Boleto, Transferência
    recebido_por INTEGER, -- ID do funcionário que recebeu
    conta_bancaria_id INTEGER,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_receita_id) REFERENCES tipo_receita(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (recebido_por) REFERENCES funcionarios(id),
    FOREIGN KEY (conta_bancaria_id) REFERENCES contas_bancarias(id)
);

-- NOVOS CADASTROS

-- Funcionários
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE,
    rg TEXT,
    data_nascimento DATE,
    telefone TEXT,
    email TEXT,
    cargo TEXT,
    setor TEXT,
    salario REAL,
    data_admissao DATE,
    data_demissao DATE,
    ativo INTEGER DEFAULT 1,
    endereco TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contas Bancárias
CREATE TABLE IF NOT EXISTS contas_bancarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_conta TEXT NOT NULL,
    banco TEXT,
    agencia TEXT,
    numero_conta TEXT,
    tipo_conta TEXT, -- Corrente, Poupança, Investimento
    saldo_inicial REAL DEFAULT 0,
    saldo_atual REAL DEFAULT 0,
    data_abertura DATE,
    ativo INTEGER DEFAULT 1,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transferências Bancárias
CREATE TABLE IF NOT EXISTS transferencias_bancarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_origem_id INTEGER NOT NULL,
    conta_destino_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    data_transferencia DATE NOT NULL,
    descricao TEXT,
    efetuado_por INTEGER, -- ID do funcionário
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conta_origem_id) REFERENCES contas_bancarias(id),
    FOREIGN KEY (conta_destino_id) REFERENCES contas_bancarias(id),
    FOREIGN KEY (efetuado_por) REFERENCES funcionarios(id)
);

-- Inventário - Itens
CREATE TABLE IF NOT EXISTS inventario_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE,
    nome TEXT NOT NULL,
    categoria TEXT, -- Medicamentos, Insumos, Ferramentas, Equipamentos, Alimentos
    unidade TEXT, -- kg, L, unidade, saco, caixa
    estoque_minimo REAL DEFAULT 0,
    estoque_atual REAL DEFAULT 0,
    valor_unitario REAL,
    localizacao TEXT,
    fornecedor_id INTEGER,
    ativo INTEGER DEFAULT 1,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
);

-- Inventário - Movimentações
CREATE TABLE IF NOT EXISTS inventario_movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    tipo_movimento TEXT NOT NULL, -- Entrada, Saída, Ajuste
    quantidade REAL NOT NULL,
    valor_unitario REAL,
    valor_total REAL,
    data_movimento DATE NOT NULL,
    motivo TEXT, -- Compra, Venda, Uso, Perda, Ajuste de Estoque
    documento TEXT, -- Número da nota/pedido
    responsavel_id INTEGER,
    despesa_id INTEGER, -- Link com despesa (se for entrada por compra)
    aplicacao_id INTEGER, -- Link com aplicação (se for saída por uso)
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES inventario_itens(id),
    FOREIGN KEY (responsavel_id) REFERENCES funcionarios(id),
    FOREIGN KEY (despesa_id) REFERENCES despesas(id),
    FOREIGN KEY (aplicacao_id) REFERENCES aplicacoes(id)
);

-- Log de Atividades
CREATE TABLE IF NOT EXISTS log_atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    usuario_nome TEXT,
    acao TEXT NOT NULL, -- Login, Logout, Cadastro, Edição, Exclusão
    modulo TEXT, -- Animais, Clientes, Despesas, etc
    descricao TEXT,
    ip_address TEXT,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- ============================================
-- MÓDULO DE BANANAL
-- ============================================

-- Variedades de Banana
CREATE TABLE IF NOT EXISTS variedades_banana (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    ciclo_medio_dias INTEGER, -- Dias até a colheita
    producao_media_ton_ha REAL, -- Produção média em toneladas por hectare
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Talhões/Lotes de Bananal
CREATE TABLE IF NOT EXISTS talhoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    localizacao TEXT,
    area_hectares REAL NOT NULL,
    variedade_id INTEGER,
    data_plantio DATE,
    espacamento TEXT, -- Ex: 3m x 2m
    densidade_plantas_ha INTEGER,
    situacao TEXT DEFAULT 'Ativo', -- Ativo, Colhido, Replantio, Inativo
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variedade_id) REFERENCES variedades_banana(id)
);

-- Tratos Culturais
CREATE TABLE IF NOT EXISTS tratos_culturais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talhao_id INTEGER NOT NULL,
    tipo_trato TEXT NOT NULL, -- Adubação, Irrigação, Desbaste, Desfolha, Controle de Pragas, Controle de Doenças
    data_execucao DATE NOT NULL,
    produto_utilizado TEXT,
    quantidade REAL,
    unidade TEXT,
    custo REAL,
    responsavel_id INTEGER,
    observacoes TEXT,
    proxima_aplicacao DATE, -- Para criar alertas
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talhao_id) REFERENCES talhoes(id),
    FOREIGN KEY (responsavel_id) REFERENCES funcionarios(id)
);

-- Controle de Pragas e Doenças
CREATE TABLE IF NOT EXISTS pragas_doencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    tipo TEXT, -- Praga, Doença, Fungo, Bactéria
    sintomas TEXT,
    tratamento_recomendado TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ocorrências de Pragas/Doenças
CREATE TABLE IF NOT EXISTS ocorrencias_pragas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talhao_id INTEGER NOT NULL,
    praga_doenca_id INTEGER NOT NULL,
    data_identificacao DATE NOT NULL,
    severidade TEXT, -- Leve, Moderada, Grave
    area_afetada_percentual REAL,
    tratamento_aplicado TEXT,
    data_tratamento DATE,
    custo_tratamento REAL,
    resolvido INTEGER DEFAULT 0,
    data_resolucao DATE,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talhao_id) REFERENCES talhoes(id),
    FOREIGN KEY (praga_doenca_id) REFERENCES pragas_doencas(id)
);

-- Colheitas de Banana
CREATE TABLE IF NOT EXISTS colheitas_banana (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talhao_id INTEGER NOT NULL,
    data_colheita DATE NOT NULL,
    quantidade_kg REAL NOT NULL,
    quantidade_caixas INTEGER,
    peso_medio_cacho REAL,
    classificacao_a_kg REAL DEFAULT 0, -- Qualidade A
    classificacao_b_kg REAL DEFAULT 0, -- Qualidade B
    classificacao_c_kg REAL DEFAULT 0, -- Qualidade C (descarte)
    custo_colheita REAL,
    responsavel_id INTEGER,
    destino TEXT, -- Venda, Consumo Próprio, Doação
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talhao_id) REFERENCES talhoes(id),
    FOREIGN KEY (responsavel_id) REFERENCES funcionarios(id)
);

-- Previsão de Colheita
CREATE TABLE IF NOT EXISTS previsao_colheita (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talhao_id INTEGER NOT NULL,
    data_prevista DATE NOT NULL,
    quantidade_estimada_kg REAL,
    status TEXT DEFAULT 'Prevista', -- Prevista, Realizada, Cancelada
    colheita_realizada_id INTEGER,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talhao_id) REFERENCES talhoes(id),
    FOREIGN KEY (colheita_realizada_id) REFERENCES colheitas_banana(id)
);

-- Estoque de Banana
CREATE TABLE IF NOT EXISTS estoque_banana (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colheita_id INTEGER NOT NULL,
    classificacao TEXT NOT NULL, -- A, B, C
    quantidade_entrada_kg REAL NOT NULL,
    quantidade_atual_kg REAL NOT NULL,
    data_entrada DATE NOT NULL,
    local_armazenamento TEXT,
    temperatura REAL,
    umidade REAL,
    data_validade DATE,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (colheita_id) REFERENCES colheitas_banana(id)
);

-- Vendas de Banana (complementa a tabela receitas)
CREATE TABLE IF NOT EXISTS vendas_banana (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receita_id INTEGER, -- Link com tabela receitas
    estoque_banana_id INTEGER,
    colheita_id INTEGER,
    cliente_id INTEGER,
    data_venda DATE NOT NULL,
    classificacao TEXT NOT NULL,
    quantidade_kg REAL NOT NULL,
    valor_kg REAL NOT NULL,
    valor_total REAL NOT NULL,
    forma_pagamento TEXT,
    nota_fiscal TEXT,
    destino TEXT, -- Mercado, Atacado, Varejo, Exportação
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (receita_id) REFERENCES receitas(id),
    FOREIGN KEY (estoque_banana_id) REFERENCES estoque_banana(id),
    FOREIGN KEY (colheita_id) REFERENCES colheitas_banana(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Custos de Produção por Talhão
CREATE TABLE IF NOT EXISTS custos_producao_talhao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talhao_id INTEGER NOT NULL,
    mes_referencia TEXT NOT NULL, -- YYYY-MM
    custo_insumos REAL DEFAULT 0,
    custo_mao_obra REAL DEFAULT 0,
    custo_energia REAL DEFAULT 0,
    custo_agua REAL DEFAULT 0,
    custo_combustivel REAL DEFAULT 0,
    custo_manutencao REAL DEFAULT 0,
    outros_custos REAL DEFAULT 0,
    custo_total REAL DEFAULT 0,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talhao_id) REFERENCES talhoes(id)
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_animais_brinco ON animais(brinco);
CREATE INDEX IF NOT EXISTS idx_animais_status ON animais(status_id);
CREATE INDEX IF NOT EXISTS idx_despesas_data ON despesas(data_gasto);
CREATE INDEX IF NOT EXISTS idx_receitas_data ON receitas(data_venda);
CREATE INDEX IF NOT EXISTS idx_aplicacoes_data ON aplicacoes(data_aplicacao);
CREATE INDEX IF NOT EXISTS idx_controle_peso_data ON controle_peso(data_pesagem);
CREATE INDEX IF NOT EXISTS idx_funcionarios_cpf ON funcionarios(cpf);
CREATE INDEX IF NOT EXISTS idx_inventario_codigo ON inventario_itens(codigo);
CREATE INDEX IF NOT EXISTS idx_log_usuario ON log_atividades(usuario_id);
CREATE INDEX IF NOT EXISTS idx_log_data ON log_atividades(data_hora);
CREATE INDEX IF NOT EXISTS idx_talhoes_codigo ON talhoes(codigo);
CREATE INDEX IF NOT EXISTS idx_colheitas_data ON colheitas_banana(data_colheita);
CREATE INDEX IF NOT EXISTS idx_tratos_data ON tratos_culturais(data_execucao);
CREATE INDEX IF NOT EXISTS idx_vendas_banana_data ON vendas_banana(data_venda);

-- Tabela de Movimentações de Inventário
CREATE TABLE IF NOT EXISTS movimentacoes_inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    quantidade REAL NOT NULL,
    valor_unitario REAL,
    data DATE NOT NULL,
    motivo TEXT,
    saldo_anterior REAL,
    saldo_novo REAL,
    FOREIGN KEY (item_id) REFERENCES inventario_itens(id)
);
