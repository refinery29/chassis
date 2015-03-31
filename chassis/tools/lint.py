'''Calls pylint with a special set of parameters.'''

import sys
import os


# check if pylint is installed and import it
try:
    from pylint import lint
except ImportError:
    print "Can't import module pylint. Did you install it?"
    sys.exit(-1)


# either use the files given on the command line or all '*.py' files
# located in and beyond the working directory
FILES = []
for dirpath, dirnames, filenames in os.walk(os.getcwd()):
    FILES.extend(
        os.path.join(dirpath, filename)
        for filename in filenames
        if ".py" == filename[-3:]
    )


# A list of messages that should not be printed by pylint.
SUPRESSED_MESSAGES = [
    # 'I0011',  # Inline option disables a message or a messages category.
    # 'too-few-public-methods',
    # 'too-many-public-methods',
    'fixme',
    # 'file-ignored'
]


PARAMS = [
    '--reports=n',
    '--disable=%s' % ",".join(SUPRESSED_MESSAGES),
    '--dummy-variables-rgx=%s' % "_$|dummy|unused"
]
PARAMS.extend(FILES)


for file_ in FILES:
    os.system('pep8 %s' % (file_,))


lint.Run(PARAMS)
