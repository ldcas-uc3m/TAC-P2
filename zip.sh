#!/bin/bash
# Bash script to zip the whole project in order to make it deriverable
# please make sure zip and texlive are installed

set -e  # exit on error

OUTFILE="../Grafos3_3_Arnaiz_Casais.zip"
REPORT_FILENAME="memoria.pdf"

[ -e $OUTFILE ] && rm $OUTFILE  # remove if exists already

# generate data
echo "Building simulator..."
cd build
make --silent
cd ..

echo "Performing tests..."
source .venv/bin/activate
python3 src/test.py || exit


# compile the report (and save it to root folder)
echo "Compiling the report..."
latexmk -cd -shell-escape -silent -pdf report/report.tex 
cp report/report.pdf $REPORT_FILENAME


# zip it (excluding useless stuff)
echo "Zipping..."
zip -q -r "$OUTFILE" . -x zip.sh report/\* \*.git\* img/\* *__pycache__/\* .venv/\* *.xml *.jar build/\* .vscode/\*

# cleanup
echo "Cleaning up..."
rm $REPORT_FILENAME