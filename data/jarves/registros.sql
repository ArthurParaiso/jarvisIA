create table if not exists registros
(
    registro     varchar(255)         not null,
    tipo         varchar(255)         null,
    ingles       tinyint(1) default 0 null,
    espanhol     tinyint(1) default 0 null,
    portugues    tinyint(1) default 0 null,
    processado   tinyint(1) default 0 null,
    processVezes int        default 0 not null,
    morf         varchar(255)         null,
    id           int auto_increment
        primary key,
    constraint registros_pk
        unique (registro)
)
    auto_increment = 27412;

