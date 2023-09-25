update: clear up

up:
	docker-compose up -d
down:
	docker-compose down

clear:
	docker-compose down --rmi all -v 

	
