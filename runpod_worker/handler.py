"""RunPod Serverless queue worker. Requires a GPU and configured HF model.
Return one JSON object with candidates. Does not retain CV input.
"""
import json, os
import runpod
from transformers import pipeline

MODEL=os.getenv('MODEL_ID','Qwen/Qwen2.5-3B-Instruct')
# Choose compatible GPU type / model size in RunPod before deployment.
generator=pipeline('text-generation',model=MODEL,device_map='auto',dtype='auto')

def handler(job):
    input_data=job.get('input') or {}
    if input_data.get('task')!='extract_skills':return {'error':'Unsupported task'}
    prompt=str(input_data.get('prompt',''))[:25000]
    system=str(input_data.get('system',''))[:2000]
    if not prompt:return {'error':'Empty prompt'}
    messages=[{'role':'system','content':system},{'role':'user','content':prompt}]
    generated=generator(messages,max_new_tokens=1300,do_sample=False)
    output=generated[0]['generated_text']
    if isinstance(output,list):output=output[-1].get('content','')
    # Return text for backend validation; backend rejects ungrounded or unknown skills.
    return {'text':str(output)}

runpod.serverless.start({'handler':handler})
