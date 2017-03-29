.DEFAULT_GOAL := test

FILES :=                \
    app/__init__.py     \
    app/models.py       \
    app/tests.py        \
    app/tests.out       \
    IDB1.log            \
    IDB1.html           \
    
ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
endif

.pylintrc:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

app/tests.out: .pylintrc
	-$(PYLINT) app/tests.py
	-$(COVERAGE) run    --branch --include=app/tests.py app/tests.py >  app/tests.out 2>&1
	-$(COVERAGE) report -m                      >> app/tests.out
	cat app/tests.out

IDB1.html: 
	pydoc3 -w app/models.py
	mv models.html IDB1.html

IDB1.log:
	git log > IDB1.log

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__
	rm -f .pylintrc
	rm -f  IDB1.html
	rm -f  IDB1.log

config:
	git config -l

format:
	$(AUTOPEP8) -i app/__init__.py
	$(AUTOPEP8) -i app/models.py
	$(AUTOPEP8) -i app/ScrapeAPI.py
	$(AUTOPEP8) -i app/populateDb.py
	$(AUTOPEP8) -i app/tests.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: IDB1.html IDB1.log app/tests.out
	ls -al
	make check

versions:
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	-which $(PYDOC)
	-$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	which flask
	flask --version
	@echo
	$(PIP) list