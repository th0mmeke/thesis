Rscript -e "library(knitr); knit('mythesis.Rnw')"
Rscript -e "library(knitr); knit('toyworld.Rnw')"
Rscript -e "library(knitr); knit('model.Rnw')"
Rscript -e "library(knitr); knit('toyworld2.Rnw')"
Rscript -e "library(knitr); knit('appendices.Rnw')"

latexmk -pdf mythesis

