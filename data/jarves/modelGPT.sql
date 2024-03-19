create table if not exists modelGPT
(
    nome       varchar(255)  null,
    tpm        int           null,
    rpm        int           null,
    rpd        int           null,
    usado      int default 0 not null,
    dataInicio date          not null,
    dataFim    date          null
);

