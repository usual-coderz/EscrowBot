from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)

db = client["escrowbot"]

# Collections
admins = db["admins"]
deals = db["deals"]
users = db["users"]
trades = db["trades"]
payments = db["payments"]
warnings = db["warnings"]