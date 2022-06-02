from multiprocessing.sharedctypes import Value


id = "192.168.2.1:8080/1.0"
Value = 2

tmp, tmp2 = id.split("/", 1)
tmp = tmp + "/" + tmp2.split(".")[0] + "." + Value.__str__()
id2 = tmp 
print (id2)