"""Repository seam: replace this demo store with SQLAlchemy repositories when DEMO_MODE=false."""
class DemoRepository:
 def __init__(self,store): self.store=store
 def all(self): return list(self.store.values()) if isinstance(self.store,dict) else list(self.store)
 def get(self,key): return self.store.get(key) if isinstance(self.store,dict) else next((item for item in self.store if item['id']==key),None)
