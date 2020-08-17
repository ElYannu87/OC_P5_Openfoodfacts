CREATE TABLE category
(
    id   SERIAL NOT NULL
        CONSTRAINT category_pk
            PRIMARY KEY,
    tag  TEXT,
    name TEXT   NOT NULL,
    url  TEXT   NOT NULL
);

CREATE TABLE product
(
    id              SERIAL NOT NULL
        CONSTRAINT product_pk
            PRIMARY KEY,
    name            TEXT   NOT NULL,
    store           TEXT,
    nutrition_grade CHAR   NOT NULL,
    url             TEXT   NOT NULL,
    category        INTEGER
        CONSTRAINT product_category_id_fk
            REFERENCES category
);

CREATE TABLE favorite
(
    source_product_id      INTEGER      NOT NULL
        CONSTRAINT favorite_source_product_id_fk
            REFERENCES product,
    replacement_product_id INTEGER      NOT NULL
        CONSTRAINT favorite_replacement_product_id_fk
            REFERENCES product,
    name                   VARCHAR(300) NOT NULL,
    store                  VARCHAR(300) NOT NULL,
    nutrition_grade        CHAR         NOT NULL,
    url                    VARCHAR(255) NOT NULL,
    category               VARCHAR(300) NOT NULL,
    CONSTRAINT favorite_pk
        PRIMARY KEY (source_product_id, replacement_product_id)
);
