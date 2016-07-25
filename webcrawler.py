from bs4 import BeautifulSoup
import urllib2
import json

def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False

    return True


url = "http://www.airfleets.net/crash/stat_country.htm"
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")
accidents = soup.findAll('tr', class_='texten')
accidentlist = dict()

with open('country_placemark.json','r') as f:
    data = f.read()

d = json.loads(data)

place = [[None]*2 for x in xrange(0, 4)]
for i in range(0, 4):
    place[i][0] = i

s1 = []
s2 = []
s3 = []
s4 = []

for a in accidents:
    if a.contents[1].style == '30%' and a.contents[2].style == '40%':
        country_name = a.contents[0].strings
        print country_name
        acc_count = int(a.contents[1].strings[:2])
        if country_name == 'USA':
            s4.append(float(38.883333))
            s4.append(float(-77.000000))
            s4.append(1)
                    
        for name in d:
            if is_number(name['CapitalLatitude']) and is_number(name['CapitalLongitude']):
                if name['CountryName'] == country_name:
                    if acc_count < 8:
                        s1.append(float(name['CapitalLatitude']))
                        s1.append(float(name['CapitalLongitude']))
                        s1.append(0.2)
                    elif acc_count < 15:
                        s2.append(float(name['CapitalLatitude']))
                        s2.append(float(name['CapitalLongitude']))
                        s2.append(0.5)
                    elif acc_count >= 15 and acc_count < 20:
                        s3.append(float(name['CapitalLatitude']))
                        s3.append(float(name['CapitalLongitude']))
                        s3.append(0.8)
                    elif acc_count > 20:
                        s4.append(float(name['CapitalLatitude']))
                        s4.append(float(name['CapitalLongitude']))
                        s4.append(1)

            
place[0][1] = s1
place[1][1] = s2
place[2][1] = s3
place[3][1] = s4

accidentdata = json.dumps(place)
try:
    fd = open('accidents.json', 'w')
    fd.write(accidentdata)
    fd.close()
    print "Finished operation"
except:
    print "Cannot open json file for writing"





