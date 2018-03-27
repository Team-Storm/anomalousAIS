import zerorpc
import csv
import sys
class HelloRPC(object):
    def hello(self, name):
    	lines  = name.split('\n')
    	with open('irisWrite.csv','w') as file:
    		for line in lines:
        		file.write(line)
        		file.write('\n')
    	#with open("irisWrite.cv", "wb") as csv_file:
       		#writer = csv.writer(csv_file, delimiter=',')
        	#for line in lines:
        		#writer.writerow(line)   ##2
    	#for line in lines:
    		#print(line)
    		#myFile = open('example2.csv', 'w')
			#with myFile:
    			#writer = csv.writer(myFile)
    			#writer.writerows(myData) ##1
    	return "Hogya"

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
