#from githube (delet all images before run)
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
log_w:
	docker-compose logs watchtower

#enter tnside the docker
in:
	docker-compose exec flask_io sh
git_push:
	git add . && git commit -m "teat" &&git push

	
