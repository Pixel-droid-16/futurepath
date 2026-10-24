"""Transparent, hypothetical AI adoption scenarios. Not empirical labour-market forecasts."""
TASKS = {
 'data-analyst':[('Routine data preparation',80,45),('Explain analytical findings',25,85),('Validate AI-generated analysis',30,95)],
 'cybersecurity-analyst':[('Triage routine alerts',75,65),('Investigate novel threats',20,95),('Oversee AI security systems',25,90)],
 'financial-analyst':[('Prepare standard financial reports',85,45),('Interpret unusual financial risk',25,90),('Validate automated models',35,95)],
 'bi-analyst':[('Refresh recurring dashboards',80,40),('Translate stakeholder needs',20,90),('Audit AI-generated BI metrics',30,95)],
 'health-informatics':[('Clean routine records',70,45),('Ensure clinical data safety',20,95),('Review AI-driven health insights',30,95)],
 'clinical-research':[('Compile trial documentation',70,45),('Manage participant ethics',15,95),('Validate AI research summaries',35,90)],
 'sustainability-analyst':[('Aggregate emissions records',80,35),('Interpret reporting standards',25,95),('Audit automated ESG claims',35,95)],
 'renewable-engineer':[('Run standard simulations',70,45),('Verify engineering safety',15,95),('Supervise AI optimisation',25,95)],
 'automation-engineer':[('Generate routine control scripts',70,45),('Commission safety-critical systems',15,95),('Evaluate AI-driven automation',35,95)],
 'quality-engineer':[('Classify common defects',85,40),('Investigate root causes',25,95),('Audit AI quality inspection',30,95)],
 'instructional-designer':[('Draft standard learning materials',85,35),('Design inclusive instruction',25,95),('Review AI-created assessments',30,95)],
 'ux-designer':[('Produce UI variants',80,40),('Conduct contextual user research',25,95),('Evaluate AI-generated experiences',35,95)],
}

def scenario_details(role_id, scenario):
    """Exposure and human oversight are subjective DEMO assumptions, not probabilities."""
    rapid=scenario=='rapid'
    rows=[]
    for name, exposure, oversight in TASKS.get(role_id,[]):
        change='Major workflow redesign' if rapid and exposure>=65 else ('AI co-pilot likely' if exposure>=65 else 'Human-led with AI support')
        rows.append({'task':name,'automation_exposure':exposure,'human_oversight':oversight,
                     'adoption_impact': change if rapid else ('Selective AI assistance' if exposure>=65 else 'Predominantly human-led')})
    return {'scenario':scenario,'label':'Rapid AI adoption' if rapid else 'Moderate AI adoption',
            'assumption':'Rapid rollout: AI tools become widely embedded across workflows, so AI-related trend signals count double in demand.' if rapid else 'Measured rollout: AI tools support selected workflows with staged adoption; every trend signal counts once.',
            'uncertainty':'Illustrative what-if model; no empirical job-loss or employment probabilities.',
            'tasks':rows,
            'strategic_skills':(['AI output validation','AI governance','workflow redesign','human oversight'] if rapid else ['domain fundamentals','critical thinking','AI literacy','communication']),
            'recommended_action':('Prioritise AI validation and oversight now; adapt workflows and build an AI-assisted portfolio.' if rapid else 'Strengthen core domain skills; practice selected AI-assisted workflows before expanding adoption.')}
