'''Calls pylint with a special set of parameters.'''

import sys
import os
import six

if sys.version_info[0] == 2:
    if sys.version_info[1] < 7:
        six.print_("pylint not supported for Python < 2.7. Skipping.")
        sys.exit(0)

if sys.version_info[0] == 3:
    if sys.version_info[1] == 2:
        six.print_("pylint not supported for Python 3.2. Skipping.")
        sys.exit(0)

# check if pylint is installed and import it
try:
    from pylint import lint
except ImportError:
    six.print_("Can't import module pylint. Did you install it?")
    sys.exit(-1)

# either use the files given on the command line or all '*.py' files
# located in and beyond the working directory
FILES = []

# pylint: disable=invalid-name
argc = len(sys.argv)
if argc > 1:
    FILES = sys.argv[1:argc]
else:
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
    'locally-disabled',
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
