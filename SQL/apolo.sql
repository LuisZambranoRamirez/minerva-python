CREATE DATABASE apolo;

-- 1. CREACIÓN DE TIPOS ENUM (PostgreSQL requiere crearlos primero)
CREATE TYPE gain_strategy_enum AS ENUM ('PORCENTAJE', 'INCREMENTAL');

CREATE TYPE sale_type_enum AS ENUM ('UNIDAD', 'GRANEL');

CREATE TYPE category_enum AS ENUM (
    'BEBIDAS',
    'ABARROTES_SECOS',
    'CAFE_INFUSIONES',
    'LACTEOS',
    'CARNES',
    'SNACKS_GOLOSINAS',
    'CUIDADO_PERSONAL',
    'LIMPIEZA_HOGAR',
    'BEBES', -- Sin tilde para evitar conflictos de encoding
    'MASCOTAS',
    'OTROS'
);

CREATE TYPE loss_reason_enum AS ENUM ('DAÑADO', 'VENCIMIENTO', 'PERDIDO', 'COMSUMO', 'DRAKO', 'ROBO', 'OTROS');

CREATE TYPE payment_method_enum AS ENUM ('EFECTIVO', 'DIGITAL');

CREATE TYPE return_reason_enum AS ENUM ('DAÑADO', 'VENCIDO', 'EQUIVOCACION', 'OTROS');


-- 2. CREACIÓN DE TABLAS
CREATE TABLE supplier (
    supplierNameId VARCHAR(100) PRIMARY KEY,
    ruc CHAR(11) UNIQUE,
    phoneNumber CHAR(9) UNIQUE,
    registrationDate TIMESTAMP NOT NULL 
);

CREATE TABLE customer (
    customerNameId VARCHAR(100) PRIMARY KEY,
    phoneNumber CHAR(9) UNIQUE,
    registrationDate TIMESTAMP NOT NULL
);

CREATE TABLE product (
    productNameId VARCHAR(100) PRIMARY KEY,
    gainStrategy gain_strategy_enum NOT NULL,
    gainAmount DECIMAL(10,2) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock DECIMAL(10,3) NOT NULL, 
    reorderLevel DECIMAL(10,3),
    barCode CHAR(13) UNIQUE,
    SaleType sale_type_enum NOT NULL,
    category category_enum NOT NULL,    
    registrationDate TIMESTAMP NOT NULL
);

CREATE TABLE unitToBulk (    
    unitProductNameId VARCHAR(100) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL,
    bulkProductNameId VARCHAR(100) NOT NULL UNIQUE,  
    registrationDate TIMESTAMP NOT NULL,

    PRIMARY KEY (bulkProductNameId, unitProductNameId),

    CONSTRAINT fk_bulk_product FOREIGN KEY (bulkProductNameId)
        REFERENCES product(productNameId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_unit_product FOREIGN KEY (unitProductNameId)
        REFERENCES product(productNameId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE stockEntry (
    stockEntryId CHAR(36) PRIMARY KEY,
    productNameId VARCHAR(100) NOT NULL,
    supplierNameId VARCHAR(100) NOT NULL,
    unitPrice DECIMAL(10,2) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL,
    expirationDate TIMESTAMP,
    registrationDate TIMESTAMP NOT NULL,
 
    CONSTRAINT fk_stockEntry_product FOREIGN KEY (productNameId)
        REFERENCES product(productNameId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_stockEntry_supplier FOREIGN KEY (supplierNameId)
        REFERENCES supplier(supplierNameId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE    
);

CREATE TABLE sale (
    saleId CHAR(36) PRIMARY KEY,
    customerNameId VARCHAR(100) NOT NULL,
    registrationDate TIMESTAMP NOT NULL,

    CONSTRAINT fk_sale_customerNameId FOREIGN KEY (customerNameId)
        REFERENCES customer(customerNameId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE saleDetail (
    saleDetailId CHAR(36) PRIMARY KEY,
    saleId CHAR(36) NOT NULL,
    productNameId VARCHAR(100) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL,
    unitPrice DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_sd_sale FOREIGN KEY (saleId)
        REFERENCES sale(saleId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_sd_product FOREIGN KEY (productNameId)
        REFERENCES product(productNameId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE inventoryLoss (
    inventoryLossId CHAR(36) PRIMARY KEY,
    productNameId VARCHAR(100) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL,
    reason loss_reason_enum NOT NULL,
    observation VARCHAR(255),
    registrationDate TIMESTAMP NOT NULL,

    CONSTRAINT fk_inventoryLoss_product FOREIGN KEY (productNameId)
        REFERENCES product(productNameId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE pay (
    payId CHAR(36) PRIMARY KEY,
    saleId CHAR(36) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    paymentMethod payment_method_enum NOT NULL,
    registrationDate TIMESTAMP NOT NULL,

    CONSTRAINT fk_pay_sale FOREIGN KEY (saleId)
        REFERENCES sale(saleId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE productReturn (
    productReturnId CHAR(36) PRIMARY KEY,
    saleDetailId CHAR(36) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL,
    reason return_reason_enum NOT NULL,
    registrationDate TIMESTAMP NOT NULL,

    CONSTRAINT fk_return_sale FOREIGN KEY (saleDetailId)
        REFERENCES saleDetail(saleDetailId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 3. DATOS INICIALES
INSERT INTO supplier (supplierNameId, registrationDate) VALUES ('anonimo', CURRENT_TIMESTAMP);
INSERT INTO customer (customerNameId, registrationDate) VALUES ('anonimo', CURRENT_TIMESTAMP);