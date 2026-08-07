from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["escrowbot"]

admins = db["admins"]
deals = db["deals"]
users = db["users"]
trades = db["trades"]
payments = db["payments"]
warnings = db["warnings"]
settings = db["settings"]