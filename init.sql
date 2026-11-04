CREATE TABLE IF NOT EXISTS problema (
    id SERIAL PRIMARY KEY,
    problema VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS bairros (
    id SERIAL PRIMARY KEY,
    bairro VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS categoria_problema (
    id SERIAL PRIMARY KEY,
    id_problema INTEGER NOT NULL,
    gravidade INTEGER NOT NULL,
    FOREIGN KEY (id_problema) REFERENCES problema(id)
);

CREATE TABLE IF NOT EXISTS ocorrencias (
    id SERIAL PRIMARY KEY,
    id_categoria_p INTEGER NOT NULL,
    id_bairros INTEGER NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_categoria_p) REFERENCES categoria_problema(id),
    FOREIGN KEY (id_bairros) REFERENCES bairros(id)
);
