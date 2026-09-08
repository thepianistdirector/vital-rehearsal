"""Deterministic, nonpreemptive FCFS synthetic process model; no physiology coupling."""
import csv
import heapq

def solve(spec,directory):
    available=[(0.,i) for i in range(spec['servers'])];heapq.heapify(available)
    rows=[]
    for job in sorted(spec['jobs'],key=lambda j:(j['arrival_s'],j['id'])):
        free,server=heapq.heappop(available)
        start=max(free,job['arrival_s'])
        finish=start+job['service_s']+spec['service_delay_s']
        rows.append({'id':job['id'],'server':server,'arrival_s':job['arrival_s'],'start_s':start,'finish_s':finish,'wait_s':start-job['arrival_s']})
        heapq.heappush(available,(finish,server))
    with (directory/'schedule.csv').open('x',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return {'execution_state':'COMPLETED','conclusion':'SYNTHETIC_SCHEDULE_ONLY','limitation':'Wholly synthetic jobs and service times; no real care data, patient outcomes or physiology coupling.',
            'metrics':{'jobs':len(rows),'mean_wait_s':sum(r['wait_s'] for r in rows)/len(rows),'max_wait_s':max(r['wait_s'] for r in rows),'makespan_s':max(r['finish_s'] for r in rows)},
            'event_type':'synthetic.service_completed.v1','coupling':'NONE'}
