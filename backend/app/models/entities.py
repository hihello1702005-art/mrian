"""SQLAlchemy-ready domain map; database/schema.sql is the deployment source of truth."""
from dataclasses import dataclass,field
from datetime import datetime,timezone
from uuid import uuid4
def now(): return datetime.now(timezone.utc).isoformat()
def uid(): return str(uuid4())
@dataclass
class Profile: id:str=field(default_factory=uid); name:str=''; email:str=''; password_hash:str=''; role:str='USER'; avatar_url:str=''; created_at:str=field(default_factory=now)
@dataclass
class Show: id:str=field(default_factory=uid); title:str=''; description:str=''; category:str='Music'; thumbnail_url:str=''; status:str='DRAFT'; hosts:list[str]=field(default_factory=list); created_at:str=field(default_factory=now)
