#from githube (delet all images before run)
up_:
	docker-compose up -d

#localy (build before run)
local:clear b up_ log
up:
	docker-compose up
b:
	docker build -t aboglion/flask_tdc flask_app


# delet all images 
clear:
	docker-compose stop flask_io 
	docker-compose down flask_io -v 
	docker-compose kill flask_io 
	docker-compose rm flask_io 
	docker-compose down --rmi all -v 

stop:
	docker-compose down

log:
	docker-compose logs -f flask_io

log_2:
	docker-compose logs -f watchtower

#enter tnside the docker
in:
	docker-compose exec flask_io sh
push:
	git add . && git commit -m "teat" &&git push

	
