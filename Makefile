all: twoactors.pdf

%.pdf: %.tex
	pdflatex $< -o $@
clean:
	\rm *.pdf
#mie.dvi: mie.tex
#	latex mie.tex && bibtex mie && latex mie.tex  && latex mie.tex
