DOC := thesis

TEMPLATE = $(wildcard *.sty *.cls)
FIG = $(wildcard media/midas/*.pdf) $(wildcard media/seccells/*.pdf)
MEDIA = data/seccells/32ksim/mycached_full.pdf data/seccells/network_1ktlb_sim/nfv_full.pdf
MAINTEX = $(wildcard ./*.tex)
CHAPTERS = $(wildcard chapters/*.tex)
RESUME = resume/main.pdf
DEP = $(TEMPLATE) $(FIG) $(MEDIA) $(MAINTEX) $(CHAPTERS) $(RESUME)

# override define rglob
# $(foreach d,$(wildcard $(1:=/*)),\
# 	$(call rglob,$d,$2)	$(filter $(subst *,%,$2),$d)\
# )
# endef

# .PHONY: clean partial

$(DOC).pdf: $(DOC).tex $(DOC).bib $(DEP)
	$(call pdflatex,$(DOC))

resume/%:
	make -C resume $(@F)

.SECONDEXPANSION:
data/%.pdf: $$(@D)/data.csv
	make -C $(@D)/ $@

clean:
	rm -rf $(DOC).pdf $(MEDIA) 
	rm -rf *-blx.bib *.log *.run.xml *.toc *.rubbercache
	rm -rf *.aux _minted-* *.blg *.bbl *.lot *.lof *.bcf
	rm -rf chapters/*.aux 
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