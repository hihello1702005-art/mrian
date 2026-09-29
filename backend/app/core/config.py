from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
 model_config=SettingsConfigDict(env_file='.env',extra='ignore')
 app_env:str='development'; demo_mode:bool=True; jwt_secret:str='development-only-secret'; cors_origins:str='http://localhost:5173'
 azuracast_base_url:str=''; azuracast_api_key:str=''; azuracast_station_id:str=''; azuracast_stream_url:str=''
 livekit_url:str=''; livekit_api_key:str=''; livekit_api_secret:str=''
@lru_cache
def get_settings(): return Settings()
settings=get_settings()
