"""Holland RIASEC interest quiz (18 items, 3 per type, Likert 1-5), ported from LaluanKu.

Interest fit is guidance, never a gate: it never hides careers and the quiz can be skipped.
Career profiles come from O*NET career interest types (see riasec_source in data/roles.json).
"""
import math

TYPES=('R','I','A','S','E','C')
TYPE_NAMES={'R':'Realistic','I':'Investigative','A':'Artistic','S':'Social','E':'Enterprising','C':'Conventional'}
TYPE_BLURBS={'R':'hands-on work with tools, machines or the outdoors','I':'solving problems, analysing and researching',
             'A':'creating, designing and expressing ideas','S':'helping, teaching and caring for people',
             'E':'leading, persuading and starting things','C':'organising information, records and procedures'}
# Interleaved R, I, A, S, E, C so similar items aren't answered back to back.
QUESTIONS=[
    (1,'R','Fix or assemble machines, devices or equipment'),(2,'I',"Work out why something isn't working by testing ideas"),
    (3,'A','Design posters, videos, layouts or websites'),(4,'S','Teach or explain things to other people'),
    (5,'E','Persuade people to try an idea or a product'),(6,'C','Keep records, files or schedules well organised'),
    (7,'R','Work outdoors or with my hands, on a farm, site or workshop'),(8,'I','Analyse numbers or data to find patterns'),
    (9,'A','Write stories, captions or articles'),(10,'S','Help people with their problems or look after them'),
    (11,'E','Lead a project or a group and make the decisions'),(12,'C','Check details carefully so there are no mistakes'),
    (13,'R','Operate tools, vehicles or machinery'),(14,'I','Learn how things work in science or technology'),
    (15,'A','Come up with original ideas instead of following a set method'),(16,'S','Work in a team where people support each other'),
    (17,'E','Start or grow a small business'),(18,'C','Follow clear procedures and work with spreadsheets'),
]
LIKERT=[(1,'Strongly dislike'),(2,'Dislike'),(3,'Not sure'),(4,'Like'),(5,'Strongly like')]

def clamp_likert(v):
    try:return min(5,max(1,round(float(v))))
    except (TypeError,ValueError):return 3

def score_quiz(answers):
    """Average of each type's three answers (1-5), rescaled to 0..1. Unanswered items count as neutral (3)."""
    answers={int(k):v for k,v in (answers or {}).items()}
    scores={}
    for t in TYPES:
        items=[q for q in QUESTIONS if q[1]==t]
        scores[t]=round((sum(clamp_likert(answers.get(q[0])) for q in items)/len(items)-1)/4,2)
    return scores

def riasec_code(scores,length=3):
    """Top types by score (ties keep R-I-A-S-E-C order), e.g. 'ICR'."""
    return ''.join(sorted(TYPES,key=lambda t:(-scores[t],TYPES.index(t)))[:length])

def interest_fit(user,role):
    """Cosine similarity of the two mean-centred profiles, mapped from [-1, 1] to [0, 1]; a flat profile gives 0.5."""
    def centre(p):
        mean=sum(p[t] for t in TYPES)/len(TYPES)
        return [p[t]-mean for t in TYPES]
    u,r=centre(user),centre(role)
    norm=math.hypot(*u)*math.hypot(*r)
    return 0.5 if norm<1e-9 else (sum(a*b for a,b in zip(u,r))/norm+1)/2

def shared_top_types(user,role):
    """Types both profiles rank in their top three, for a plain-language 'why'."""
    top=set(riasec_code(role))
    return [t for t in riasec_code(user) if t in top]
