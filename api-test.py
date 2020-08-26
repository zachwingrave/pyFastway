import xml, logging
#from SOAPpy import WSDL
from suds.client import Client

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
url = "http://localhost/shipping-services-api-wsdl.wsdl"

live_url = "http://ws.aramex.net/shippingapi/tracking/service_1_0.svc"
test_url = "http://ws.dev.aramex.net/shippingapi/shipping/service_1_0.svc"

client = Client(url)

client.sd[0].service.setlocation(test_url)

clientobj = client.factory.create('ClientInfo')
clientobj.UserName = 'testingapi@aramex.com'
clientobj.Password = 'R123456789$r'
clientobj.Version = 'v1.0'
clientobj.AccountNumber = '20016'
clientobj.AccountPin = '331421'
clientobj.AccountEntity = 'AMM'
clientobj.AccountCountryCode = 'JO'

transactionobj = client.factory.create('Transaction')
transactionobj.Reference1 = 'PRINT_LABEL_1441457996'
transactionobj.Reference2 = ''
transactionobj.Reference3 = ''
transactionobj.Reference4 = ''
transactionobj.Reference5 = ''

labelinfoobj = client.factory.create('LabelInfo')
labelinfoobj.ReportID = '9201'
labelinfoobj.ReportType = 'url'

print(client.service.PrintLabel(clientobj,transactionobj,"001","EXP","",labelinfoobj))