-- Script para criar a tabela da Série A Italiana
-- Execute este script no banco tabelas_classificacao.db

CREATE TABLE IF NOT EXISTS classificacao_serie_a_italiana (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posicao INTEGER NOT NULL,
    time TEXT NOT NULL,
    pontos INTEGER DEFAULT 0,
    jogos INTEGER DEFAULT 0,
    vitorias INTEGER DEFAULT 0,
    empates INTEGER DEFAULT 0,
    derrotas INTEGER DEFAULT 0,
    gols_pro INTEGER DEFAULT 0,
    gols_contra INTEGER DEFAULT 0,
    saldo_gols INTEGER DEFAULT 0,
    aproveitamento REAL DEFAULT 0.0,
    ultimos_confrontos TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados iniciais da Série A Italiana 2024/2025
INSERT OR REPLACE INTO classificacao_serie_a_italiana (posicao, time, pontos, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_gols, aproveitamento, ultimos_confrontos) VALUES
(1, 'Inter de Milão', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(2, 'Juventus', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(3, 'AC Milan', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(4, 'Atalanta', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(5, 'Roma', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(6, 'Lazio', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(7, 'Napoli', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(8, 'Fiorentina', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(9, 'Bologna', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(10, 'Torino', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(11, 'Genoa', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(12, 'Monza', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(13, 'Lecce', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(14, 'Udinese', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(15, 'Cagliari', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(16, 'Verona', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(17, 'Empoli', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(18, 'Frosinone', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(19, 'Sassuolo', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, ''),
(20, 'Salernitana', 0, 0, 0, 0, 0, 0, 0, 0, 0.0, '');

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_serie_a_italiana_posicao ON classificacao_serie_a_italiana(posicao);
CREATE INDEX IF NOT EXISTS idx_serie_a_italiana_time ON classificacao_serie_a_italiana(time);










