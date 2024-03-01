DOC := thesis

TEMPLATE = $(wildcard *.sty *.cls)
MAINTEX = $(wildcard ./*.tex)
CHAPTERS = $(wildcard chapters/*.tex)
RESUME = resume/main.pdf

MEDIA = $(wildcard media/midas/*.pdf) $(wildcard media/seccells/*.pdf)
GEN = data/seccells/32ksim/mycached_full.pdf data/seccells/network_1ktlb_sim/nfv_full.pdf
GEN += data/compsok/scoring_security.pdf data/compsok/scoring_practicality.pdf
GEN += data/compsok/table_security.tex data/compsok/table_practicality.tex
# $(wildcard data/compsok/*.tex)

DEP = $(TEMPLATE) $(MEDIA) $(GEN) $(MAINTEX) $(CHAPTERS) $(RESUME)

# override define rglob
# $(foreach d,$(wildcard $(1:=/*)),\
# 	$(call rglob,$d,$2)	$(filter $(subst *,%,$2),$d)\
# )
# endef

# .PHONY: clean partial

$(DOC).pdf: $(DOC).tex $(DOC).bib $(DEP)
	echo $(GEN)
	$(call pdflatex,$(DOC))

resume/%:
	make -C resume $(@F)

data/compsok/%.pdf: data/compsok/*.json data/compsok/*.csv data/compsok/process.py
	cd data/compsok && python3 process.py

.SECONDEXPANSION:
data/%.pdf: $$(@D)/data.csv
	make -C $(@D)/ $@

clean:
	rm -rf $(DOC).pdf 
	rm -rf *-blx.bib *.log *.run.xml *.toc *.rubbercache
	rm -rf *.aux _minted-* *.blg *.bbl *.lot *.lof *.bcf
	rm -rf chapters/*.aux 
	rm -rf $(GEN)
	make -C resume clean

define pdflatex
pdflatex -interaction=nonstopmode -halt-on-error -shell-escape $(1).tex 
bibtex $(1)  
pdflatex -interaction=nonstopmode -halt-on-error -shell-escape $(1).tex 
pdflatex -interaction=nonstopmode -halt-on-error -shell-escape $(1).tex 
endef

# define artifacts
# $$(cat $(1).aux 2>/dev/null | grep -oP '(?<=\\@input\{).*?(?=\})') \
# 	$(1).aux $(1).log $(1).out \
# 	$(1).toc $(1).bbl $(1).blg $(1).synctex.gz \
# 	$(1).run.xml $(1).bcf $(1)-blx.bib _minted-$(1) \
# 	$(1).pyg $(1).out.pyg
# endef