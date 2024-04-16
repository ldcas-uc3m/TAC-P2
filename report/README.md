# Lab report template

## Usage

The report consists of a main file [`report.tex`](report.tex), which includes a cover ([`parts/0-cover.tex`](parts/0-cover.tex)), a Table of Contents (if you uncomment it), and all the Markdown and LaTeX files inside the [`parts/`](parts/) folder that you want to include.


## Compilation

**NOTE:** Some of the images included are generated through the [`test.py`](../src/test.py) script, so make sure to execute that before compiling.

First you must install LaTeX.

- For Linux, install `texlive-full`.
- For Windows, install [MiKTeX](https://miktex.org/download#win), make sure you add it to your `PATH`, and install [Perl](https://strawberryperl.com/). If it’s not installed already, open the MikTeX Package Manager and install the `latexmk` package.
- For MacOS, install [MacTeX](https://www.tug.org/mactex/mactex-download.html) and then install `latexmk` with:
    ```
    sudo tlmgr install latexmk
    ```

To compile the report, use the command:
```
latexmk -cd -shell-escape -pdf report.tex
```

## VS Code
Some useful extensions:
- [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
    - If you are using the extension, please set `-shell-escape` (see [LaTeX Workshop FAQ](https://github.com/James-Yu/LaTeX-Workshop/wiki/FAQ#how-to-pass--shell-escape-to-latexmk))
- [LTeX](https://marketplace.visualstudio.com/items?itemName=valentjn.vscode-ltex): Grammar checker.
    - You can change the language through the `ltex.language` setting in VS Code settings.