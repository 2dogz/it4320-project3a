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
            for i in j:
                ticker = i[0]
                msg = '({}, {}),'.format(ticker, ticker)
                print (msg)
                #y = '{} {}'.format(x,x)
            #return y

print(do_this())
