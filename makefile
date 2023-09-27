#from githube (delet all images before run)
debugit: clear log up
update: clear up_
up_:
	docker-compose up -d

#localy (build before run)
local:clear b log up
up:
	docker-compose up
b:
	docker build -t aboglion/flask_tdc flask_app


# delet all images 
clear:
	docker-compose down --rmi all -v 
stop:
	docker-compose down

log:
	docker-compose logs flask_io

#enter tnside the docker
in:
	docker exec -it flask_io sh
	
