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
