
from typing import Union
import asyncio
import asyncpg
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None


    async def create_pool(self):
        self.pool = await asyncpg.create_pool(dsn=config.POSTGRES_URL)
    @staticmethod
    def formar_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, id: int, name: str):
        sql = " INSERT INTO users (id, name) VALUES ($1, $2)"
        await self.pool.execute(sql, id, name)

    async def get_balance_user(self, **kwargs):
        sql = "SELECT balance FROM users WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        return await self.pool.fetch(sql, *parameters)

    async def select_all_users(self):
        sql = "SELECT id FROM users "
        return await self.pool.fetch(sql)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def count_users(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM users")

    async def delete_users(self):
        await self.pool.execute("DELETE FROM users WHERE True")

    async def get_count_order(self, **kwargs):
        sql = "SELECT COUNT(*) FROM orders WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        return await self.pool.fetchval(sql, *parameters)

    async def get_orders(self, **kwargs):
        sql = "SELECT * FROM orders WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        return await self.pool.fetch(sql, *parameters)

    async def get_count_refill(self, **kwargs):
        sql = "SELECT COUNT(sum) FROM refill WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        return await self.pool.fetchval(sql, *parameters)

