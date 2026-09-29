import logging
from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.security import hash_password,verify_password,token,user,allow
from .schemas.contracts import *
from .services.demo_data import USERS,SHOWS,RECORDINGS,SCHEDULE
from .services.azuracast import AzuraCastService
from .services.livekit import LiveKitService
logging.basicConfig(level=logging.INFO); app=FastAPI(title="Meradio'N API",version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins.split(','),allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
def serialize(s): return {k:v for k,v in s.__dict__.items() if k!='password_hash'}
@app.get('/api/health')
def health(): return {'status':'healthy','application':'meradion','demo_mode':settings.demo_mode}
@app.post('/api/auth/register',status_code=201)
def register(payload:Register):
 if payload.email in USERS: raise HTTPException(409,'Email already registered')
 if payload.role not in {'USER','RJ'}: raise HTTPException(422,'Invalid self-service role')
 from .models.entities import Profile
 p=Profile(name=payload.name,email=str(payload.email),password_hash=hash_password(payload.password),role=payload.role);USERS[p.email]=p
 return {'access_token':token(p.id,p.role),'token_type':'bearer','profile':serialize(p)}
@app.post('/api/auth/login')
def login(payload:Login):
 p=USERS.get(str(payload.email))
 if not p or not verify_password(payload.password,p.password_hash):raise HTTPException(401,'Invalid email or password')
 return {'access_token':token(p.id,p.role),'token_type':'bearer','profile':serialize(p)}
@app.get('/api/auth/me')
def me(c=Depends(user)): return next((serialize(p) for p in USERS.values() if p.id==c['sub']),c)
@app.get('/api/radio/now-playing')
async def now_playing():
 try:return await AzuraCastService().now_playing()
 except Exception as exc: raise HTTPException(503,'Unable to connect to the station') from exc
@app.get('/api/radio/live')
async def live(): return await now_playing()
@app.get('/api/radio/station')
async def station(): return await AzuraCastService().station()
@app.get('/api/shows')
def shows(q:str|None=None,category:str|None=None):
 result=[serialize(x) for x in SHOWS.values()]
 if q: result=[x for x in result if q.lower() in (x['title']+x['description']).lower()]
 if category: result=[x for x in result if x['category'].lower()==category.lower()]
 return result
@app.post('/api/shows',status_code=201)
def create_show(payload:ShowIn,c=Depends(allow('ADMIN'))):
 from .models.entities import Show
 s=Show(**payload.model_dump());SHOWS[s.id]=s;return serialize(s)
@app.get('/api/shows/{show_id}')
def show(show_id:str):
 if show_id not in SHOWS:raise HTTPException(404,'Show not found')
 return serialize(SHOWS[show_id])
@app.put('/api/shows/{show_id}')
def update_show(show_id:str,payload:ShowIn,c=Depends(allow('ADMIN'))):
 s=SHOWS.get(show_id)
 if not s:raise HTTPException(404,'Show not found')
 for k,v in payload.model_dump().items():setattr(s,k,v)
 return serialize(s)
@app.delete('/api/shows/{show_id}',status_code=204)
def delete_show(show_id:str,c=Depends(allow('ADMIN'))):
 if not SHOWS.pop(show_id,None):raise HTTPException(404,'Show not found')
@app.post('/api/shows/{show_id}/start')
def start_show(show_id:str,c=Depends(allow('RJ','ADMIN'))):
 if show_id not in SHOWS:raise HTTPException(404,'Show not found')
 return {'show_id':show_id,'status':'LIVE','recording':'RECORDING'}
@app.post('/api/shows/{show_id}/end')
def end_show(show_id:str,c=Depends(allow('RJ','ADMIN'))): return {'show_id':show_id,'status':'ENDED','recording':'PROCESSING'}
@app.get('/api/schedule')
def schedule():return SCHEDULE
@app.post('/api/schedule',status_code=201)
def create_schedule(p:ScheduleIn,c=Depends(allow('ADMIN'))):
 if p.show_id not in SHOWS:raise HTTPException(404,'Show not found')
 d=p.model_dump(mode='json');d['id']=str(len(SCHEDULE)+1);SCHEDULE.append(d);return d
@app.put('/api/schedule/{schedule_id}')
def update_schedule(schedule_id:str,p:ScheduleIn,c=Depends(allow('ADMIN'))):
 for i,x in enumerate(SCHEDULE):
  if x['id']==schedule_id:SCHEDULE[i]={**x,**p.model_dump(mode='json')};return SCHEDULE[i]
 raise HTTPException(404,'Schedule item not found')
@app.delete('/api/schedule/{schedule_id}',status_code=204)
def remove_schedule(schedule_id:str,c=Depends(allow('ADMIN'))):
 for x in SCHEDULE:
  if x['id']==schedule_id:SCHEDULE.remove(x);return
 raise HTTPException(404,'Schedule item not found')
@app.get('/api/recordings')
def recordings():return RECORDINGS
@app.get('/api/recordings/{recording_id}')
def recording(recording_id:str):
 return next((x for x in RECORDINGS if x['id']==recording_id),None) or (_ for _ in ()).throw(HTTPException(404,'Recording not found'))
@app.post('/api/recordings',status_code=201)
def create_recording(p:RecordingIn,c=Depends(allow('RJ','ADMIN'))):
 d=p.model_dump();d['id']=str(len(RECORDINGS)+1);RECORDINGS.append(d);return d
FAVORITES:dict[str,list[str]]={}
@app.get('/api/favorites')
def favorites(c=Depends(user)):return [serialize(SHOWS[s]) for s in FAVORITES.get(c['sub'],[]) if s in SHOWS]
@app.post('/api/favorites',status_code=201)
def favorite(p:FavoriteIn,c=Depends(user)):
 if p.show_id not in SHOWS:raise HTTPException(404,'Show not found')
 FAVORITES.setdefault(c['sub'],[]).append(p.show_id);return {'show_id':p.show_id}
@app.delete('/api/favorites/{show_id}',status_code=204)
def unfavorite(show_id:str,c=Depends(user)): FAVORITES[c['sub']]=[x for x in FAVORITES.get(c['sub'],[]) if x!=show_id]
@app.post('/api/notifications',status_code=202)
def notify(p:NotificationIn,c=Depends(allow('ADMIN'))):return {'status':'queued','notification':p.model_dump()}
@app.get('/api/analytics')
def analytics(c=Depends(allow('ADMIN'))):return {'current_listeners':284,'listening_hours':1248,'total_shows':len(SHOWS),'total_recordings':len(RECORDINGS),'listener_trend':[120,145,132,210,195,248,284],'popular_shows':[{'title':'Morning Vibes','listeners':820},{'title':'Campus Beats','listeners':610}]}
@app.post('/api/livekit/token')
def livekit_token(p:LiveKitTokenIn,c=Depends(allow('RJ','ADMIN'))):return LiveKitService().create_token(c['sub'],p.room_name or f'show-{p.show_id}')
