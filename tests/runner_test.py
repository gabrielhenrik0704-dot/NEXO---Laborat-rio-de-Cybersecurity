import unittest,sys,ipaddress
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runner'))
import server
class RunnerTests(unittest.TestCase):
 def setUp(self):self.networks=server.NETWORKS;self.hosts=server.HOSTS;server.NETWORKS=[ipaddress.ip_network('192.0.2.0/24')];server.HOSTS={'lab.authorized.invalid'}
 def tearDown(self):server.NETWORKS=self.networks;server.HOSTS=self.hosts
 def test_target_scope(self):
  self.assertEqual(server.validate_target('192.0.2.5'),'192.0.2.5')
  for target in ['8.8.8.8','127.0.0.1','192.0.2.0/24','192.0.2.1;id','-oA /tmp/x','example.org','http://192.0.2.5']:
   with self.assertRaises(ValueError):server.validate_target(target)
 def test_resolution_pinned_and_all_addresses_checked(self):
  with patch('server.socket.getaddrinfo',return_value=[(2,1,6,'',('192.0.2.7',0))]):self.assertEqual(server.validate_target('lab.authorized.invalid'),'192.0.2.7')
  with patch('server.socket.getaddrinfo',return_value=[(2,1,6,'',('192.0.2.7',0)),(2,1,6,'',('8.8.8.8',0))]):
   with self.assertRaises(ValueError):server.validate_target('lab.authorized.invalid')
 def test_empty_scope_denies(self):
  server.NETWORKS=[]
  with self.assertRaises(ValueError):server.validate_target('192.0.2.5')
 def test_parse_output(self):
  xml='<nmaprun><host><status state="up"/><address addr="192.0.2.5"/><ports><port portid="443" protocol="tcp"><state state="open"/><service name="https"/></port></ports></host><runstats><finished summary="1 host"/></runstats></nmaprun>'
  data=server.summarize(xml);self.assertEqual(data['hosts'][0]['ports'][0]['port'],'443');self.assertEqual(data['summary'],'1 host')
if __name__=='__main__':unittest.main()
