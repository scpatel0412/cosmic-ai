CREATE TABLE users (
    id SERIAL PRIMARY KEY,                     
    username VARCHAR(500) UNIQUE NOT NULL,       
    email VARCHAR(500) UNIQUE NOT NULL,          
    password VARCHAR(500) NOT NULL,              
    first_name VARCHAR(500) NOT NULL,            
    last_name VARCHAR(500) NOT NULL,            
    contact VARCHAR(500) NOT NULL,
    stripe_customer_id VARCHAR NOT NULL,            
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,  
    deleted_at TIMESTAMP,                       
    CONSTRAINT valid_deleted_at CHECK (
        deleted_at IS NULL OR deleted_at >= created_at
    ) 
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY, 
    summary VARCHAR NOT NULL,  
    user_id INTEGER NOT NULL, 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    deleted_at TIMESTAMP, 
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    questions TEXT NOT NULL,
    answer TEXT,
    conversations_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (conversations_id) REFERENCES conversations(id) ON DELETE CASCADE
);

ALTER TABLE users
ADD COLUMN stripe_customer_id VARCHAR NOT NULL;

CREATE TABLE user_subscriptions (
    id SERIAL PRIMARY KEY,
    checkout_id VARCHAR NOT NULL,
    amount VARCHAR NOT NULL,
    create_time VARCHAR NOT NULL,
    expire_time VARCHAR NOT NULL,
    payment_status VARCHAR NOT NULL,
    user_id INTEGER NOT NULL,
    invoice_id VARCHAR NOT NULL;
    subscription_id VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

ALTER TABLE user_subscriptions
ADD COLUMN invoice_id VARCHAR NOT NULL;

ALTER TABLE user_subscriptions
ADD COLUMN subscription_id VARCHAR NOT NULL;