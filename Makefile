.PHONY: test install lint

install:
	./install_dependencies.sh

test:
	@cd chassis; nosetests

lint:
	@cd chassis; python tools/lint.py
