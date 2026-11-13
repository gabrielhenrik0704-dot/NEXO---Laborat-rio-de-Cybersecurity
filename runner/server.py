"""NEXO isolated job service. No shell or arbitrary command endpoint."""
import os,json,time,secrets,ipaddress,socket,subprocess,threading,uuid,xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit
TOKEN=os.environ.get('NEXO_RUNNER_TOKEN','')
NETWORKS=[ipaddress.ip_network(v.strip(),strict=False) for v in os.environ.get('NEXO_ALLOWED_CIDRS','').split(',') if v.strip()]
HOSTS={v.strip().lower() for v in os.environ.get('NEXO_ALLOWED_HOSTS','').split(',') if v.strip()}
JOBS={};LOCK=threading.Lock();SLOTS=threading.BoundedSemaphore(2)
def validate_target(target):
 if not isinstance(target,str) or not target or len(target)>253 or any(c in target for c in '/\\\n\r\t @:#?'):raise ValueError('Informe apenas um IPv4 ou nome de host.')
 try: addresses=[ipaddress.ip_address(target)]
 except ValueError:
  if target.lower() not in HOSTS:raise ValueError('Host não incluído no escopo definido pelo administrador.')
  addresses=list({ipaddress.ip_address(v[4][0]) for v in socket.getaddrinfo(target,None,socket.AF_INET,socket.SOCK_STREAM)})
 if not addresses or any(not any(ip in net for net in NETWORKS) for ip in addresses):raise ValueError('Endereço fora das redes autorizadas pelo administrador.')
 if any(ip.version!=4 for ip in addresses):raise ValueError('Este adaptador aceita somente IPv4.')
 return str(sorted(addresses,key=int)[0])
def summarize(xml):
 root=ET.fromstring(xml);hosts=[]
 for h in root.findall('host'):
  hosts.append({'address':h.find('address').attrib.get('addr','') if h.find('address') is not None else '', 'status':h.find('status').attrib.get('state','') if h.find('status') is not None else '', 'ports':[{'port':p.attrib.get('portid'), 'protocol':p.attrib.get('protocol'), 'state':p.find('state').attrib.get('state') if p.find('state') is not None else '', 'service':p.find('service').attrib if p.find('service') is not None else {}} for p in h.findall('ports/port')]})
 return {'hosts':hosts,'summary':root.find('runstats/finished').attrib.get('summary','') if root.find('runstats/finished') is not None else ''}
def execute(job):
 with LOCK:job['status']='running';job['startedAt']=time.time()
 # Fixed argv; the target is a resolved IP already checked against server scope.
 argv=['nmap','-sT','-sV','--version-light','--top-ports','100','--max-retries','1','--host-timeout','60s','-oX','-',job['resolvedTarget']]
 try:
  result=subprocess.run(argv,capture_output=True,text=True,timeout=75,check=False)
  if result.returncode:raise RuntimeError('Nmap retornou erro. Revise o estado do executor e o escopo.')
  data=summarize(result.stdout)
  with LOCK:job['result']=data;job['status']='completed'
 except subprocess.TimeoutExpired:
  with LOCK:job['status']='failed';job['error']='O teste excedeu 75 segundos.'
 except Exception:
  with LOCK:job['status']='failed';job['error']='Não foi possível executar ou interpretar o resultado do Nmap.'
 finally:
  with LOCK:job['finishedAt']=time.time()
  SLOTS.release()
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,status,data):
  raw=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
 def identity(self):
  header=self.headers.get('Authorization','');expected='Bearer '+TOKEN
  if not TOKEN or not secrets.compare_digest(header,expected):self.send(401,{'error':'Acesso não autorizado.'});return None
  owner=self.headers.get('X-Nexo-User','')
  if len(owner)!=64 or any(c not in '0123456789abcdef' for c in owner):self.send(400,{'error':'Identidade do solicitante ausente.'});return None
  return owner
 def do_GET(self):
  owner=self.identity()
  if not owner:return
  path=urlsplit(self.path).path
  if path=='/v1/health':return self.send(200,{'service':'nexo-runner','tool':'nmap_tcp','ready':bool(NETWORKS),'scopeConfigured':bool(NETWORKS),'maxConcurrent':2,'persistentJobs':False})
  if path.startswith('/v1/jobs/'):
   ident=path.rsplit('/',1)[1]
   with LOCK:job=dict(JOBS[ident]) if ident in JOBS else None
   if not job or job['owner']!=owner:return self.send(404,{'error':'Trabalho não encontrado.'})
   return self.send(200,{k:v for k,v in job.items() if k!='owner'})
  self.send(404,{'error':'Rota não encontrada.'})
 def do_POST(self):
  owner=self.identity()
  if not owner:return
  if urlsplit(self.path).path!='/v1/jobs':return self.send(404,{'error':'Rota não encontrada.'})
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n<1 or n>4000:return self.send(413,{'error':'Solicitação acima do limite.'})
   data=json.loads(self.rfile.read(n))
   if data.get('tool')!='nmap_tcp':return self.send(400,{'error':'Ferramenta não habilitada.'})
   target=validate_target(data.get('target',''))
  except (ValueError,socket.gaierror):return self.send(400,{'error':'Alvo inválido ou fora do escopo configurado no servidor.'})
  if not SLOTS.acquire(blocking=False):return self.send(429,{'error':'Executor ocupado. Tente novamente mais tarde.'})
  job={'id':str(uuid.uuid4()),'owner':owner,'tool':'nmap_tcp','target':data['target'],'resolvedTarget':target,'status':'queued','createdAt':time.time()}
  with LOCK:
   expired=[k for k,v in JOBS.items() if v.get('finishedAt',time.time())<time.time()-3600]
   for k in expired:del JOBS[k]
   if len(JOBS)>500:SLOTS.release();return self.send(429,{'error':'Limite de histórico temporário atingido.'})
   JOBS[job['id']]=job
  response={k:v for k,v in job.items() if k!='owner'}
  threading.Thread(target=execute,args=(job,),daemon=True).start();self.send(202,response)
if __name__=='__main__':
 if len(TOKEN)<32:raise SystemExit('Configure NEXO_RUNNER_TOKEN com pelo menos 32 caracteres.')
 ThreadingHTTPServer(('0.0.0.0',8080),Handler).serve_forever()
