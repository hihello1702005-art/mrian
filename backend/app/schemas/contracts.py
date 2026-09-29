from datetime import datetime
from pydantic import BaseModel,EmailStr,Field
class Register(BaseModel): name:str=Field(min_length=2,max_length=80); email:EmailStr; password:str=Field(min_length=8,max_length=128); role:str='USER'
class Login(BaseModel): email:EmailStr; password:str
class ShowIn(BaseModel): title:str=Field(min_length=2,max_length=120); description:str=''; category:str='Music'; thumbnail_url:str=''; status:str='DRAFT'; hosts:list[str]=[]
class ScheduleIn(BaseModel): show_id:str; start_time:datetime; end_time:datetime; recurrence:str='ONCE'
class RecordingIn(BaseModel): show_id:str; storage_path:str; playback_url:str; duration:int=Field(ge=1); status:str='PROCESSING'
class FavoriteIn(BaseModel): show_id:str
class NotificationIn(BaseModel): title:str=Field(min_length=2,max_length=120); message:str=Field(min_length=2,max_length=500); type:str='ANNOUNCEMENT'
class LiveKitTokenIn(BaseModel): show_id:str; room_name:str|None=None
