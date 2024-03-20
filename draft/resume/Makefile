
MAIN=main

$(MAIN).pdf: $(MAIN).tex
	rubber --pdf $(MAIN).tex

.PHONY: clean
clean:
	rm -rf $(MAIN).pdf
	rm -rf *.log *.rubbercache
