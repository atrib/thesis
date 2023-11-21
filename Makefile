DOC := thesis

TEX = $(wildcard *.sty *.cls)
# INC = $(wildcard papers/*.tex)
# FIG = $(call rglob,media,*)
DEP = $(TEX) $(FIG) $(INC) $(CHAPTERS)
CHAPTERS = chapters/seccell-core.tex chapters/Midas-core.tex

# override define rglob
# $(foreach d,$(wildcard $(1:=/*)),\
# 	$(call rglob,$d,$2)	$(filter $(subst *,%,$2),$d)\
# )
# endef

# .PHONY: clean partial

$(DOC).pdf: $(DOC).tex $(DOC).bib $(DEP) Resume.pdf
	make -C papers/seccell-paper
	make -C papers/midas-paper midas
	rubber --unsafe --pdf $(DOC).tex 

# resume.pdf: resume.tex
# 	$(call pdflatex,resume)

# partial: $(DOC).tex $(DEP)
# 	pdflatex \
# 		-interaction=nonstopmode -halt-on-error -shell-escape $<

clean:
	rm -rf $(DOC).pdf *-blx.bib *.log *.run.xml *.toc *.rubbercache *.aux _minted-*
# clean:
# 	@rm -rf *.pdf $(call artifacts,*)

# define pdflatex
# pdflatex \
# 	-interaction=nonstopmode -halt-on-error -shell-escape $(1).tex
# bibtex $(1) || true # in case .bib is missing
# pdflatex \
# 	-interaction=nonstopmode -halt-on-error -shell-escape $(1).tex
# pdflatex \
# 	-interaction=nonstopmode -halt-on-error -shell-escape $(1).tex
# # rm -rf $(call artifacts,$1)
# endef

# define artifacts
# $$(cat $(1).aux 2>/dev/null | grep -oP '(?<=\\@input\{).*?(?=\})') \
# 	$(1).aux $(1).log $(1).out \
# 	$(1).toc $(1).bbl $(1).blg $(1).synctex.gz \
# 	$(1).run.xml $(1).bcf $(1)-blx.bib _minted-$(1) \
# 	$(1).pyg $(1).out.pyg
# endef