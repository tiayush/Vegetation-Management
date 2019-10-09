
from db import Trial
sqlA = Trial()
f = open('file.txt', "r")
lines = list(f)
f.close()

command = sqlA.maketable()
for i in lines:
    i = i.replace("\n", "")
    l = i.split(' ')
    l = list(map(int, l))
    command = sqlA.makeinsert("TREES",l[0],l[1],l[2],l[3],l[4])
    sqlA.put_record(command)
    # command = sqlA.makeinsert("TREES",5,2)
    # sqlA.put_record(command)
    # query=sqlA.make_query("TREES","2")
    # sqlA.read_record(query)]

command = sqlA.make_query("TREES", "1400")
sqlA.read_record(command)



