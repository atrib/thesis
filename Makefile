DOC := thesis

TEX = $(wildcard *.sty *.cls)
# INC = $(wildcard papers/*.tex)
# FIG = $(call rglob,media,*)
MEDIA = data/seccells/32ksim/mycached_full.pdf data/seccells/network_1ktlb_sim/nfv_full.pdf
DEP = $(TEX) $(FIG) $(INC) $(CHAPTERS) $(MEDIA)
CHAPTERS = $(wildcard chapters/*.tex) 

# override define rglob
# $(foreach d,$(wildcard $(1:=/*)),\
# 	$(call rglob,$d,$2)	$(filter $(subst *,%,$2),$d)\
# )
# endef

# .PHONY: clean partial

$(DOC).pdf: $(DOC).tex $(DOC).bib $(DEP) Resume.pdf 
	$(call pdflatex,$(DOC))

.SECONDEXPANSION:
data/%.pdf: $$(@D)/data.csv
	make -C $(@D)/ $@

# resume.pdf: resume.tex
# 	$(call pdflatex,resume)

# partial: $(DOC).tex $(DEP)
# 	pdflatex \
# 		-interaction=nonstopmode -halt-on-error -shell-escape $<

clean:
	rm -rf $(DOC).pdf $(MEDIA) *-blx.bib *.log *.run.xml *.toc *.rubbercache
	rm -rf *.aux _minted-* *.blg *.bbl
	rm -rf chapters/*.aux 
# clean:
# 	@rm -rf *.pdf $(call artifacts,*)

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