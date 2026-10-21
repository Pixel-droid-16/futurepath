"""The shared request formats used by multiple route modules."""
from pydantic import BaseModel, Field
class ProfilePayload(BaseModel):
    user_type:str='student'
    country:str='Malaysia'
    interests:list[str]=Field(default_factory=list)
    skills:dict[str,int]=Field(default_factory=dict)
    mode:str='discover'
class SavePayload(BaseModel):
    scenario:str='moderate'
    role_id:str='data-analyst'
    snapshot_id:str|None=None
class ComparePayload(BaseModel):
    history_id:int
    scenario:str='moderate'
class AIExtractRequest(BaseModel):
    text:str=Field(min_length=3,max_length=12000)
    provider:str='auto'
