import yaml
from collections import Counter

def parseLine(input):
    """
    Parse a line of input.

    Keyword arguments:
    input -- The data to parse
    """

    return [x.strip() for x in input.split(':', 1)]

def parseDate(input):
    """
    Parse a date and return in the format YYYY-mm-dd
    Dates that are missing the month or date will have those parts omitted

    Keyword arguments:
    input -- The data to parse
    """

    elements = input.replace(' ', '').split('/')
    
    if len(elements) == 1 and not elements[0]:
        return None
    
    else:
        date = elements[2] # year

        if elements[0]: # month
            date += f"-{elements[0]:>02}"

            if elements[1]: # day
                date += f"-{elements[1]:>02}"

        return date
    
def splitValues(input, isDate=False, isAddr=False):
    """
    Split ;-delimited sets of values.
    
    Keyword arguments:
    isDate -- The values to be split should be parsed as dates (default False)
    isAddr -- The values to be split are addresses (default False)
    """

    values = input.rstrip(';').split(';') # remove any trailing delimiters and split

    if len(values) == 1 and not values[0]:
        return None

    if isDate:
        values = [ parseDate(value) for value in values ]

    if isAddr:
        values = [ ', '.join(e for e in element if e and e != ' ') for element in (value.split('/') for value in values) ]
    
    return values

def getTopValues(fields):
    """
    Find the most frequently occurring values in the reports

    Keyword arguments:
    fields -- The keys to find the top values of
    """

    topValues = {}

    for field in fields:
        # Get all unique values for this field and count them
        allValues = Counter([ item for sublist in (report[field] for report in reports) if sublist is not None for item in sublist])
        
        # Record the top values for that field and their rank
        topValues[field] = {k:v for k, v in zip((value[0] for value in allValues.most_common(7)),range(7,0,-1)) }
    
    return topValues

reports = [] # list to hold parsed reports

with open("AtlanticStorm.txt") as data:
    
    # strip lines that do not contain data
    lines = [ l for l in (line.strip() for line in data) if l and l != "REPORT" ]

    # parse each report
    for line in range(0, len(lines)-1, 9):
        id = parseLine(lines[line])
        reportDate = parseLine(lines[line+1])
        referenceID = parseLine(lines[line+2])
        reportSource = parseLine(lines[line+3])
        reportDesc = parseLine(lines[line+4])

        persons = parseLine(lines[line+5])
        persons[1] = splitValues(persons[1]) # split multiple values

        dates = parseLine(lines[line+6])
        dates[1] = splitValues(dates[1], isDate=True) # split multiple values

        places = parseLine(lines[line+7])
        places[1] = splitValues(places[1], isAddr=True) # split multiple values

        orgs = parseLine(lines[line+8])
        orgs[1] = splitValues(orgs[1]) # split multiple values
     
        # add report to list of reports
        reports.append({
            id[0]:id[1], 
            reportDate[0]:parseDate(reportDate[1]), 
            referenceID[0]:referenceID[1], 
            reportSource[0]:reportSource[1], 
            reportDesc[0]:reportDesc[1], 
            persons[0]:persons[1], 
            dates[0]:dates[1], 
            places[0]:places[1], 
            orgs[0]:orgs[1],
            'WEIGHT':0
            })

    topValues = getTopValues(['PERSONS', 'PLACES', 'DATES'])

    # add the weights for each field to the record
    for report in reports:
        for type in topValues:
            data = report[type]
            
            if data is not None:
              for value in data:
                if value in topValues[type]:
                    report['WEIGHT'] += topValues[type][value]

    # sort the reports by weight (desc)
    reports.sort(key=lambda x: x['WEIGHT'], reverse=True)

# save as yaml    
with open("./_data/reports.yaml", 'w', encoding='utf-8') as fout:
    yaml.dump(reports, fout, indent=4)
