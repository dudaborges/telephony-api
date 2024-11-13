from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "callrecord" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "type" VARCHAR(10) NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL,
    "call_id" INT NOT NULL,
    "source" VARCHAR(15),
    "destination" VARCHAR(15)
);
CREATE TABLE IF NOT EXISTS "phonebill" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "phone_number" VARCHAR(15) NOT NULL,
    "period" DATE NOT NULL,
    "total_cost" DECIMAL(10,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "phonebill_callrecord" (
    "phonebill_id" UUID NOT NULL REFERENCES "phonebill" ("id") ON DELETE CASCADE,
    "callrecord_id" UUID NOT NULL REFERENCES "callrecord" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_phonebill_c_phonebi_97ce20" ON "phonebill_callrecord" ("phonebill_id", "callrecord_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
