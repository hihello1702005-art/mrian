"""Production persistence models; Demo Mode uses the in-memory repository."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime,ForeignKey,Integer,String,Text,UniqueConstraint,func
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
class Base(DeclarativeBase): pass
class ProfileModel(Base):
 __tablename__='profiles'; id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid4())); name:Mapped[str]=mapped_column(String(80));email:Mapped[str]=mapped_column(String(255),unique=True,index=True);avatar_url:Mapped[str|None]=mapped_column(Text);role:Mapped[str]=mapped_column(String(12),default='USER');created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class RadioShowModel(Base):
 __tablename__='radio_shows';id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid4()));title:Mapped[str]=mapped_column(String(120),index=True);description:Mapped[str]=mapped_column(Text,default='');category:Mapped[str]=mapped_column(String(60),index=True);thumbnail_url:Mapped[str|None]=mapped_column(Text);status:Mapped[str]=mapped_column(String(20),default='DRAFT');created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now());recordings:Mapped[list['RecordingModel']]=relationship(back_populates='show')
class RecordingModel(Base):
 __tablename__='recordings';id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid4()));show_id:Mapped[str]=mapped_column(ForeignKey('radio_shows.id'),index=True);storage_path:Mapped[str]=mapped_column(Text);playback_url:Mapped[str|None]=mapped_column(Text);duration:Mapped[int]=mapped_column(Integer);status:Mapped[str]=mapped_column(String(20),default='PROCESSING');created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now());show:Mapped[RadioShowModel]=relationship(back_populates='recordings')
class FavoriteModel(Base):
 __tablename__='favorites';__table_args__=(UniqueConstraint('user_id','show_id'),);id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid4()));user_id:Mapped[str]=mapped_column(ForeignKey('profiles.id'));show_id:Mapped[str]=mapped_column(ForeignKey('radio_shows.id'))
