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
    CONSTRAINT favorite_pk
        PRIMARY KEY (source_product_id, replacement_product_id)
);

CREATE TABLE product_category
(
    product_id      INTEGER      NOT NULL
        CONSTRAINT product_category_product_id_fk
            REFERENCES product,
    category_id INTEGER      NOT NULL
        CONSTRAINT product_category_category_id_fk
            REFERENCES category,
    CONSTRAINT product_category_pk
        PRIMARY KEY (product_id, category_id)
);
