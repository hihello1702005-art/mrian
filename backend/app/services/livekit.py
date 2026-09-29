from ..core.config import settings
class LiveKitService:
 def create_token(self,identity,room):
  if settings.demo_mode:return {'token':f'demo-livekit-token-for-{identity}-{room}','url':'wss://demo.livekit.invalid','room':room,'demo_mode':True}
  if not all([settings.livekit_url,settings.livekit_api_key,settings.livekit_api_secret]):raise RuntimeError('LiveKit is not configured')
  from livekit import api
  token=api.AccessToken(settings.livekit_api_key,settings.livekit_api_secret).with_identity(identity).with_name(identity).with_grants(api.VideoGrants(room_join=True,room=room,can_publish=True,can_subscribe=True)).to_jwt()
  return {'token':token,'url':settings.livekit_url,'room':room,'demo_mode':False}
