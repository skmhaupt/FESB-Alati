import csv
import glob

def weight_generator():
    fpaths = glob.glob('Raspored_scraping/data/timetables/*.csv')
    if(len(fpaths) > 1):
        print('Found', len(fpaths), '.csv files.')
    elif(len(fpaths) == 0):
        print('Error: No .csv file found!')
        return

    Errors=[]
    for fpath in fpaths:
        #open csv file
        try:
            user = fpath.split("\\",1)[1].split("_",1)[0]
            print("User: ", user)
            with open(fpath, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                #skip first line
                next(reader)
                #Every row contains: id, name, shortName, colorId, professor, eventType, groups, classroom, start, end, description, recurring, recurringType, recurringUntil, studyCode
                #                    0   1     2          3        4          5          6       7          8      9    10           11         12             13              14
                for row in reader:
                    print(row[10])
                    #.append(Student(row[0],row[1],row[2],row[3])) 
        except Exception as e:
            print('Error with csv file', e)
            Errors.append(user)
            
    print("Errors with users: ", Errors)