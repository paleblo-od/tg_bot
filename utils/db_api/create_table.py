from loader import db


async def create_table_users():
    sql = """ 
    CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL,
    Name VARCHAR(255) NOT NULL,
    balance DECIMAL DEFAULT 0,
    PRIMARY KEY (id))
    """
    await db.pool.execute(sql)



async def create_table_orders():
    sql = """ 
    CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    data VARCHAR(255),
    sum DECIMAL)
    """
    await db.pool.execute(sql)


async def create_table_payments():
    sql = """ 
    CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255),
    user_id INTEGER REFERENCES users(id),
    sum DECIMAL,
    payment VARCHAR(255))
    """
    await db.pool.execute(sql)


async def run():
    await create_table_users()
    await create_table_orders()
    await create_table_payments()

