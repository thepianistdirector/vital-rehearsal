import urllib.request,json,hashlib,datetime
from pathlib import Path
out=Path(__file__).resolve().parent/'sources';out.mkdir(exist_ok=True)
base='https://models.physiomeproject.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml'
items=[]
for name,url in [('view.html',base+'/view'),('metadata.html',base+'/cmeta'),('model.cellml',base),('documentation.html',base+'/documentation')]:
    item={'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'browser_prior_attempt':'view and cmeta returned HTTP 403 through web tool'}
    try:
        with urllib.request.urlopen(url,timeout=30) as response:data=response.read();item['status']=response.status;item['resolved_url']=response.url
        (out/name).write_bytes(data);item.update(file=name,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
    except Exception as e:item['error']=str(e)
    items.append(item)
(out/'retrieval.json').write_text(json.dumps(items,indent=2)+'\n')
print(json.dumps(items,indent=2))
