Database processing service
# The REST API 
 
 The REST API is available at 
    
    127.0.0.1:5000 

Method GET:
  
    127.0.0.1:5000/worker - show all workers
    127.0.0.1:5000/department - show all departments
    127.0.0.1:5000/worker/<id> - show one workers (only curl)
    127.0.0.1:5000/department/<id> - show one department (only curl)

Method POST:
  
    127.0.0.1:5000/worker - add worker
        args:
            department_key - department id
            worker_name - workers name
            birthday - workers birthday
            salary - workers salary
        
    127.0.0.1:5000/department - add department
        args:
            department_name - departments name
    

Method PUT:

    127.0.0.1:5000/worker/<id> - edit worker, whose number is <id>
        args:
            department_key - department id
            worker_name - workers name
            birthday - workers birthday
            salary - workers salary

    127.0.0.1:5000/department/<id> - edit department, whose number is <id>
        args:
            department_name - departments name

Method DELETE:
    
    127.0.0.1:5000/worker/<id> - delete worker, whose number is <id>
    127.0.0.1:5000/department/<id> - delete department, whose number is <id>


# WEB service:

WEB service starts at :

      127.0.0.1:5020

table of workers : 

    127.0.0.1:5020/workers
    
table of departments : 

    127.0.0.1:5020/departments