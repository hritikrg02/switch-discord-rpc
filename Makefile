create_env:
	python -m venv ./.venv/switch-discord-rpc && \
	. ./.virtualenvs/switch-discord-rpc/bin/activate && \
	pip install -r requirements.txt

remove_env:
	rm -rf ./.venv/switch-discord-rpc

run:
	. ./.virtualenvs/switch-discord-rpc/bin/activate && \
	source .env.local && \
	python main.py