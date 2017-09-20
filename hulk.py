#!/usr/bin/env python2.7

#!/usr/bin/env python2.7

import functools
import hashlib
import itertools
import multiprocessing
import os
import string
import sys

# Constants

ALPHABET    = string.ascii_lowercase + string.digits
ARGUMENTS   = sys.argv[1:]
CORES       = 1
HASHES      = 'hashes.txt'
LENGTH      = 1
PREFIX      = ''

# Functions
def usage(exit_code=0):
    print '''Usage: {} [-a alphabet -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file'''.format(os.path.basename(sys.argv[0]))
    sys.exit(exit_code)

def md5sum(s):
    ''' Generate MD5 digest for given string.

    >>> md5sum('abc')
    '900150983cd24fb0d6963f7d28e17f72'

    >>> md5sum('wake me up inside')
    '223a947ce000ce88e263a4357cca2b4b'
    '''
    #Implement
    return hashlib.md5(s).hexdigest()

def permutations(length, alphabet=ALPHABET):
    ''' Yield all permutations of alphabet up to provided length.

    >>> list(permutations(1, 'ab'))
    ['a', 'b']

    >>> list(permutations(2, 'ab'))
    ['aa', 'ab', 'ba', 'bb']

    >>> list(permutations(1))       # doctest: +ELLIPSIS
    ['a', 'b', ..., '9']

    >>> list(permutations(2))       # doctest: +ELLIPSIS
    ['aa', 'ab', ..., '99']
    '''
    #Implement as a generator
    if length == 1:
    	for x in alphabet:
    		yield x
    else:
		for x in alphabet:
			for letter in permutations(length - 1, alphabet):
				yield x + letter

def smash(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes

    >>> smash([md5sum('ab')], 2)
    ['ab']

    >>> smash([md5sum('abc')], 2, prefix='a')
    ['abc']

    >>> smash(map(md5sum, 'abc'), 1, 'abc')
    ['a', 'b', 'c']
    '''
    #Implement with list or generator comprehensions

    p = permutations(length)
    hash_list = [(prefix + x) for x in p if md5sum(prefix + x) in hashes]
    
    return hash_list

# Main Execution
if __name__ == '__main__':
    # Parse command line arguments
	args = sys.argv[1:]
	while len(args) and args[0].startswith('-') and len(args[0]) > 1:
	    arg = args.pop(0)
	    if arg == '-a':
	    	ALPHABET = args.pop(0)
	    elif arg == '-c':
	    	CORES = int(args.pop(0))
	    elif arg == '-l':
	    	LENGTH = int(args.pop(0))
	    elif arg == '-p':
	    	PREFIX = args.pop(0)
	    elif arg == '-s':
	    	HASHES = args.pop(0)
	    elif arg == '-h':
	        usage(0)
	    else:
	        usage(1)

    #Load hashes set
	hashset = set(line.strip() for line in open(HASHES))

    #Execute smash function to get passwords
	if CORES == 1 and LENGTH == 1:
		passwords = smash(hashset, LENGTH, ALPHABET, PREFIX)
	else:
		sublength = LENGTH / 2
		subsmash = functools.partial(smash, hashset, LENGTH-sublength, ALPHABET)
		pool = multiprocessing.Pool(CORES)
		passwords = itertools.chain.from_iterable(pool.imap(subsmash, [(PREFIX+x) for x in permutations(sublength, ALPHABET)]))

    #Print passwords
	for x in passwords:
		print x

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: