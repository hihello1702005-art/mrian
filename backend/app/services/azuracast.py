import httpx
from ..core.config import settings
class AzuraCastService:
 async def now_playing(self):
  if settings.demo_mode:return {'is_live':True,'station':{'name':"Meradio'N",'stream_url':'https://example.invalid/live','listeners':284},'now_playing':{'song':'Golden Hour','artist':'Ananya Rao','artwork_url':''},'show':{'title':'Morning Vibes','hosts':['RJ Sai','RJ Rahul'],'category':'Music'}}
  if not all([settings.azuracast_base_url,settings.azuracast_station_id]): raise RuntimeError('AzuraCast is not configured')
  headers={'X-API-Key':settings.azuracast_api_key} if settings.azuracast_api_key else {}
  async with httpx.AsyncClient(timeout=8) as client:
   r=await client.get(f'{settings.azuracast_base_url.rstrip("/")}/api/nowplaying/{settings.azuracast_station_id}',headers=headers);r.raise_for_status();return r.json()
 async def station(self):
  data=await self.now_playing();return data['station']
