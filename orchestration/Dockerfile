FROM esblng/base/python

RUN echo '#!/bin/bash' > /usr/local/bin/runtests && \
    echo 'if [ -z "$1" ];' >> /usr/local/bin/runtests && \
    echo '  then' >> /usr/local/bin/runtests && \
    echo '      python3 -m unittest -v tests/*.py' >> /usr/local/bin/runtests && \
    echo '  else' >> /usr/local/bin/runtests && \
    echo '      python3 -m unittest -v tests/$1.py' >> /usr/local/bin/runtests && \
    echo 'fi' >> /usr/local/bin/runtests && \
    chmod a+x /usr/local/bin/runtests

COPY . /var/www/
CMD ["ping", "127.0.0.1"]