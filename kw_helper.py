from datapackage import Package

package = Package('https://datahub.io/core/nyse-other-listings/datapackage.json')

def do_this():
    # print list of all resources:
    print(package.resource_names[1])

    # print processed tabular data (if exists any)
    c = 0
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            c+=1
            j = resource.read()
            choicesList = []
            for i in j:
                ticker = i[0]
                msg = (ticker, ticker)
                if '$' not in ticker:
                    if '.' not in ticker:
                        choicesList.append(msg)
                #y = '{} {}'.format(x,x)
            return choicesList
            #return y
#x = do_this()

#print(x)

choices=[("IBM", "IBM"),("GOOGL", "GOOGL"),]

#print(type(choices))
#print(type(x))
import requests

def do_this_2():
    c = 0
    choicesList = []
    data = requests.get('https://pkgstore.datahub.io/core/nyse-other-listings/nyse-listed_json/data/e8ad01974d4110e790b227dc1541b193/nyse-listed_json.json').json()
    for d in data:
        ticker = d['ACT Symbol']
        msg = (ticker, ticker)
        if '$' not in ticker:
            if '.' not in ticker:
                choicesList.append(msg)
    return choicesList
print(do_this_2())
