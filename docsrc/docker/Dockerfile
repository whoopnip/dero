FROM python:3.6

RUN mkdir -p /usr/share/man/man1 \
 && export DEBIAN_FRONTEND=noninteractive \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
        gosu sudo \
        curl make \
        dvipng graphviz \
        latexmk texlive-fonts-recommended texlive-latex-extra texlive-latex-recommended \
        git \
    \
&& pip install 'Sphinx                        == 2.1.2'    \
                'alabaster                     == 0.7.12'   \
                'gitpython                     == 2.1.11'   \
                'sphinx-autobuild              == 0.7.1'    \
    \
 && apt-get autoremove -y \
 && rm -rf /var/cache/* \
 && rm -rf /var/lib/apt/lists/*

RUN chown root:root /usr/local/bin/* \
 && chmod 755 /usr/local/bin/*

COPY requirements.txt /home

RUN pip install -r /home/requirements.txt

ENV DATA_DIR=/dero/docsrc

WORKDIR $DATA_DIR

CMD ["make", "github"]
