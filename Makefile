REDIS=redis-server
REDIS_CLI=redis-cli
PY=python3

run: 
	$(REDIS) &
	$(PY) run.py

clean:
	$(REDIS_CLI) shutdown
