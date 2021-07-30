import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  # "w" 의미는 write!! 즉 정보를 쓰기만 하고 file에 저장해준다는 말~!
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  #가로로 각각 이름 뭐로할거니??
  # []로 묶어주지 않으면 t,i,t,l,e,",", ,c,o,m,p,a,n,y,",", ,l,o,c,a,t,i,o,n,",", ,l,i,n,k 이렇게 됨;;;
  for job in jobs:
    writer.writerow(list(job.values()))
    #우리는 type = list를 원하는데 그냥 job.values() 하면 dict_values거든~
  return
