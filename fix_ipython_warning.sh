#!/bin/bash

# A script to fix that annoying ipython deprecation warning for
# "DeprecationWarning: With-statements now directly support multiple context managers"
# via https://github.com/matematikaadit/matematikaadit.github.io/issues/29

FILENAME=`ipython locate`/profile_default/startup/00-disable-deprecation-warning.py

if [ ! -f $FILENAME ]
then
    FILE=$( cat <<EOF
# hide deprecation warning
# IPython/terminal/interactiveshell.py:432:
# DeprecationWarning: With-statements now directly ...

import warnings
import exceptions
warnings.filterwarnings("ignore",
    category=exceptions.DeprecationWarning,
    module='IPython.terminal.interactiveshell',
    lineno=432) # change lineno to your line number warning
EOF
)
    echo "$FILE" > $FILENAME
    echo "Created $FILENAME"
fi