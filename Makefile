create_env:
	python -m venv ./.venv/switch-discord-rpc && \
	. ./.venv/switch-discord-rpc/bin/activate && \
	pip install -r requirements.txt

remove_env:
	rm -rf ./.venv/switch-discord-rpc
