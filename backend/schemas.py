"""The shared request formats used by multiple route modules."""
from pydantic import BaseModel, Field
class ProfilePayload(BaseModel):
    user_type:str='student'
    country:str='Malaysia'
    interests:list[str]=Field(default_factory=list)
    skills:dict[str,int]=Field(default_factory=dict)
    mode:str='discover'
    # Start flow fields. None of these are scoring inputs except skills and the quiz-derived interest profile.
    name:str=Field('',max_length=80)
    headline:str=Field('',max_length=160)
    current_role:str=Field('',max_length=160)
    qualification:str=Field('',max_length=160)
    languages:list[str]=Field(default_factory=list,max_length=10)
    goals:str=Field('',max_length=1000)
    years_experience:int=Field(0,ge=0,le=60)
    study_hours:int=Field(6,ge=1,le=60)
    quiz_answers:dict[int,int]|None=None  # RIASEC item id -> 1..5; omitted when the quiz is skipped
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
