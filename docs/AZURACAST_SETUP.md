# AzuraCast setup
Create the Meradio'N station in AzuraCast, configure its managed playlists, schedule and automation, and create a scoped API key. Set `AZURACAST_BASE_URL`, `AZURACAST_API_KEY`, `AZURACAST_STATION_ID`, and the public `AZURACAST_STREAM_URL` in backend environment only. The backend calls `/api/nowplaying/{station}` and translates outages to 503; clients never see the key.
