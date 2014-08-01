import csv
import sys

ifile = open(sys.argv[1], 'rb')
ofile  = open(sys.argv[2], 'wb')
nominals = []
if 3 < len(sys.argv):
    nominals = sys.argv[3:len(sys.argv)]

try:
    reader = csv.reader(ifile)
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    count = 0    
    titles = []
    for row in reader:
        if count == 0: 
            titles = row
            writer.writerow(row)
        else:
            crow = []
            for i in range(0, len(row)):
                x = row[i]
                if titles[i] in nominals:
                    crow.append('0' if x == '1' else ('1' if x == '2' else x))
                else:
                    crow.append(x);
            writer.writerow(crow)
        count = count + 1
        
finally:
    ifile.close()
    ofile.close()