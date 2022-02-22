

import docopt
import os
import sys
from textwrap import dedent


DEFAULT_EXT= 'LZS'

def _main():
    """
    Interactive script.
    """
    # If it wasn't for dependency determination done by 3rd party
    # tools (code analysers, build tools, ), the following 
    # modules should be imported right here, since they are irrelevant
    # for the main purpose of this module (RLE encoding) and only useful
    # when the module is used as a shell/GUI tool
    #   import os
    #   import sys
    #   from textwrap import dedent
    #   from docopt import docopt

    doc = """
    Run-Lenth enconding and decoding.
    Usage:
        pzip [-c [-l LEVEL] | -d | -s | -h] [-p PASSWORD] FILE
    Options:
        -c, --encode, --compress            Compress FILE whith PZYP
        -d, --decode, --decompress          Decompress FILE compressed with PZYP
        -l, LEVEL                           Compression level [default: 2] ------------> Sugere uso no Cabeçalho que é sempre gerado
        -s, --summary                       Resume of compressed file      ------------> Sugere uso no Cabeçalho que é sempre gerado
        -h, --help                          This help 
        -p PASSWORD, --password=PASSWORD    An optional password to encrypt the file
    """
    args = docopt(dedent(doc))

    def exists_or_exit(fich, error_code=3):
        if not os.path.exists(fich):
            print(f"File {fich} doesn't exist", file=sys.stderr)
            sys.exit(error_code)
        #:
    #:

    if args['--compress']:

        fich = args['File']
        exists_or_exit(fich)       
        text_File = open(fich,"r")
        compressed_file = open(fich.rsplit('.', 1)[0]+".LZS", "w")
        print("O ficheiro comprimido", fich.rsplit('.', 1)[0]+".LZS", "foi criado !")
        text_File.close()
        compressed_file.close()    
    elif args['--decompress']:

        fich = args['File']     
        fich_ext = '.' + DEFAULT_EXT

        if not fich.endswith(fich_ext):
            print(f"File must end in {fich_ext}", file=sys.stderr)
            sys.exit(2)

        exists_or_exit(fich)
        compressed_file = open(fich,"r")
        text_File = open(fich.rsplit('.', 1)[0]+"_descomprimido.txt", "w")
        text_File.write(str(decode(compressed_file.read() ).decode('utf-8') ))
        print("O ficheiro foi descomprimido!")
    #:
#:

if __name__ == '__main__':
    _main()
#: