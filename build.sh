Rscript -e "library(knitr); knit('mythesis.Rnw')"
Rscript -e "library(knitr); knit('toyworld.Rnw')"
Rscript -e "library(knitr); knit('model.Rnw')"
Rscript -e "library(knitr); knit('multiplication.Rnw')"
Rscript -e "library(knitr); knit('variability.Rnw')"
Rscript -e "library(knitr); knit('appendices.Rnw')"

latexmk -pdf mythesis

