#!/usr/bin/env python3
import json,sys
if '--version' in sys.argv:
 print('codex-cli 0.153.4'); raise SystemExit
for line in sys.stdin:
 try: m=json.loads(line)
 except: continue
 if 'id' not in m: continue
 method=m.get('method'); rid=m['id']
 if method=='initialize': result={}
 elif method=='model/list': result={'data':[{'id':'gpt-5.6-luna','supportedReasoningEfforts':['low','medium']},{'id':'gpt-5.6-terra','supportedReasoningEfforts':['low','medium','high']},{'id':'gpt-5.6','supportedReasoningEfforts':['medium','high','xhigh']},{'id':'gpt-5.6-sol','supportedReasoningEfforts':['medium','high']},{'id':'gpt-6-astra','supportedReasoningEfforts':['low','medium','high']} ]}
 elif method=='account/rateLimits/read': result={'planType':'prolite','rateLimits':{'primary':{'usedPercent':75},'ordinaryUsageAllowed':True}}
 else: result={}
 print(json.dumps({'jsonrpc':'2.0','id':rid,'result':result}),flush=True)
