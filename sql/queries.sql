CREATE TABLE users (
    id SERIAL PRIMARY KEY,                     
    username VARCHAR(500) UNIQUE NOT NULL,       
    email VARCHAR(500) UNIQUE NOT NULL,          
    password VARCHAR(500) NOT NULL,              
    first_name VARCHAR(500) NOT NULL,            
    last_name VARCHAR(500) NOT NULL,            
    contact VARCHAR(500) NOT NULL,              
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
