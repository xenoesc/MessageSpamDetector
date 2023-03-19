#this module will handle all low level tests on the message
from ocr import textRead
import re #regex
import requests
from nslookup import Nslookup

def getIP(dns):
    dns_query = Nslookup(dns_servers=["8.8.8.8"], verbose=False, tcp=False)
    ips_record = dns_query.dns_lookup(dns)
    returnVal = ips_record.answer
    returnVal = ''.join(returnVal)
    return returnVal

def get_ip_location(domain):
    ip_address = getIP(domain)
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    city = response.get("city")
    region = response.get("region")
    country =  response.get("country_name")
    returnList = [city,region,country]
    return returnList

#textSelect = str((textRead('tests/testemail1.png', 'eng'))) #convert text to string by default
#emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', textSelect) #find all the email addresses in the string
#print(emails)
print(get_ip_location('gmail.com'))
