import aiosqlite
import asyncio


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    # USERS
    async def add_user(self, user_id):
        cursor = await self.connection.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
        await self.connection.commit()
        return cursor.lastrowid

    async def get_valorant_nickname(self, user_id) -> int:
        rows = await self.connection.execute(
            "SELECT valorant_nickname FROM users WHERE id=?",
            (user_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result[0] else None

    async def get_user_id_by_nickname(self, nickname) -> int:
        rows = await self.connection.execute(
            "SELECT id FROM users WHERE valorant_nickname=?",
            (nickname,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result[0] else None

    async def updata_nick_name(self, user_id, valorant_nickname):
        await self.connection.execute(
            "UPDATE users SET valorant_nickname=? WHERE id=?",
            (valorant_nickname, user_id),
        )
        await self.connection.commit()

    async def get_user_by_id(self, user_id):
        cursor = await self.connection.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return await cursor.fetchone()
    
    async def get_user_activity(self, user_id):
        rows = await self.connection.execute(
            "SELECT activity FROM users WHERE id=?",
            (user_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result[0] else 0

    async def is_already_exists(self, user_id):
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM users WHERE id=?",
            (user_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] > 0
    async def get_all_user_ids(self):
        cursor = await self.connection.execute("SELECT id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]  
    
    async def update_user_activity(self, user_id, add_activity):
        cursor = await self.connection.execute(
            "UPDATE users SET activity = activity + ? WHERE id = ?", (add_activity, user_id)
        )
        await self.connection.commit()
        return cursor.rowcount  #

    async def change_room_owner(self, room_id, user_id):
        await self.connection.execute(
            "UPDATE user_rooms SET user_id=? WHERE room_id=?",
            (user_id, room_id),
        )
        await self.connection.commit()

    async def delete_user(self, user_id):
        cursor = await self.connection.execute("DELETE FROM users WHERE id=?", (user_id,))
        await self.connection.commit()

    # USER ROOMS
    async def add_user_room(self, user_id, room_id, room_name):
        await self.connection.execute(
            "INSERT INTO user_rooms (user_id, room_id, room_name) VALUES (?, ?, ?)",
            (user_id, room_id, room_name),
        )
        await self.connection.commit()

    async def get_user_room_id(self, user_id) -> int | None:
        rows = await self.connection.execute(
            "SELECT room_id FROM user_rooms WHERE user_id=?",
            (user_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else None
    async def update_is_close_user_room(self,room_id, is_close: bool):
        await self.connection.execute(
            "UPDATE user_rooms SET is_closed=? WHERE room_id=?",
            (is_close, room_id),
        )
        await self.connection.commit()

    async def rename_user_room(self, room_id, new_room_name):
        await self.connection.execute(
            "UPDATE user_rooms SET room_name=? WHERE room_id=?",
            (new_room_name, room_id),
        )
        await self.connection.commit()

    async def change_room_owner(self, room_id, user_id):
        await self.connection.execute(
            "UPDATE user_rooms SET user_id=? WHERE room_id=?",
            (user_id, room_id),
        )
        await self.connection.commit()

    async def delete_user_room(self, user_id=-1, room_id=-1):
        await self.connection.execute(
            "DELETE FROM user_rooms WHERE user_id=? OR room_id=?",
            (
                user_id,
                room_id,
            ),
        )
        await self.connection.commit()

    async def is_owner(self, user_id):
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM user_rooms WHERE user_id=?",
            (user_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] > 0

    async def get_room_owner(self, room_id) -> int:
        rows = await self.connection.execute(
            "SELECT user_id FROM user_rooms WHERE room_id=?",
            (room_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0]

    async def get_is_closed_room(self, room_id=-1, user_id=-1) -> bool:
        rows = await self.connection.execute(
            "SELECT is_closed FROM user_rooms WHERE room_id=? OR user_id=?",
            (room_id, user_id),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] == 1

    async def is_user_channel(self, room_id) -> bool:
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM user_rooms WHERE room_id=?",
            (room_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] > 0

    # USER WARNS
    async def add_warn(self, user_id: int, server_id: int, moderator_id: int, reason: str) -> int:
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_warnings(self, user_id: int, server_id: int) -> list:
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list
