
def get_data():
    import csv 
    # csv file name 
    filename = "data.csv"

    # initializing the titles and rows list 
    fields = [] 
    rows = [] 

    # reading csv file 
    with open(filename, 'r') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        
        # extracting field names through first row 
        fields = next(csvreader)

        # extracting each data row one by one 
        for row in csvreader: 
            rows.append(row) 
    return fields,rows
    #  printing first 5 rows 
    print('\nFirst 5 rows are:\n') 
    for row in rows[:5]: 
        # parsing each column of a row 
        for col in row: 
            print("%10s"%col), 
        print('\n') 