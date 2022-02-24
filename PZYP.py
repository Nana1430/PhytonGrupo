# Compressor e descompressor -teste
'''
Usage:
    pzip [-c [-l LEVEL] | -d | -h] [-s] [-p PASSWORD] FILE

Operation:
    -c, --encode, --compress            Compress FILE whith PZYP
    -d, --decode, --decompress          Decompress FILE compressed with PZYP

Options:
    -l, LEVEL                           Compression level [default: 2] ------------> Sugere uso no Cabeçalho que é sempre gerado
    -s, --summary                       Resume of compressed file      ------------> Sugere uso no Cabeçalho que é sempre gerado
    -h, --help                          Shows this help message and exits.
    -p PASSWORD, --password=PASSWORD    An optional password to encrypt the file (compress only)

    FILE                                The path to the file to compress / decompress
'''
#imports
import struct
from docopt import docopt
import sys
import os.path
import lzss_io
import time

# da referencia lzss_io
UNENCODED_STRING_SIZE = 8   # in bits
ENCODED_OFFSET_SIZE = 12    # in bits
ENCODED_LEN_SIZE = 4        # in bits
ENCODED_STRING_SIZE = ENCODED_OFFSET_SIZE + ENCODED_LEN_SIZE  # in bits

WINDOW_SIZE = 2 ** ENCODED_OFFSET_SIZE        # in bytes
BREAK_EVEN_POINT = ENCODED_STRING_SIZE // 8   # in bytes
MIN_STRING_SIZE = BREAK_EVEN_POINT + 1        # in bytes
MAX_STRING_SIZE = 2 ** ENCODED_LEN_SIZE - 1  + MIN_STRING_SIZE  # in bytes

ctx = lzss_io.PZYPContext(
        encoded_offset_size=4,   # janela terá 16 bytes
        encoded_len_size=3       # comprimentos de 8 + 1 - 1 = 8 bytes
    )

DEFAULT_EXT= 'LZS'    

# Compressor
def elements_in_array(check_elements, elements):
    i = 0
    offset = 0
    for element in elements:
        if len(check_elements) <= offset:    # All of the elements in check_elements are in elements
            return i - len(check_elements)
        #:
        if check_elements[offset] == element:
            offset += 1
        else:
            offset = 0
	#:
        i += 1
    #:
    return -1
#:
encoding = "utf-8"

def encode(text_bytes, max_sliding_window_size=4096): #"4096 is default if argument is omited"

    search_buffer = [] # Array of integers, representing bytes
    check_characters = [] # Array of integers, representing bytes
    output = [] # Output array

    i = 0
    for char in text_bytes:
        index = elements_in_array(check_characters, search_buffer) # The index where the characters appears in our search buffer

        if elements_in_array(check_characters + [char], search_buffer) == -1 or i == len(text_bytes) - 1:
            if i == len(text_bytes) - 1 and elements_in_array(check_characters + [char], search_buffer) != -1:
                
                check_characters.append(char)
		# Only if it's the last character then add the next character to the text the token is representing
            #:
            if len(check_characters) > 1:
                index = elements_in_array(check_characters, search_buffer)
                offset = i - index - len(check_characters) 	# Calculate the relative offset
                length = len(check_characters)	 		# Set the length of the token (how many character it represents)

                token = f"<{offset},{length}>" 			# Build our token

                if len(token) > length:  			# Length of token is greater than the length it represents, so output the characters                   
                    output.extend(check_characters) 		# Output the characters
                else:
                    output.extend(token.encode(encoding)) 	# Output our token

                #:
                search_buffer.extend(check_characters) 		# Add the characters to our search buffer   
            else:
                output.extend(check_characters) 		# Output the character
                search_buffer.extend(check_characters) 		# Add the characters to our search buffer   
	    #:
            check_characters = []   
        #:
        check_characters.append(char)

        if len(search_buffer) > max_sliding_window_size: 	# Check to see if it exceeds the max_sliding_window_size
            search_buffer = search_buffer[1:] 			# Remove the first element from the search_buffer
	#:
        i += 1
    #:
    _lzs_encode(bytes(output))
    #return bytes(output) 
#:
encoding = "utf-8"

#Descompressor
def decode(text):
	
    text_bytes = text  				# The text encoded as bytes
    output = [] 						# The output characters

    inside_token = False
    scanning_offset = True

    length = [] 						# Length number encoded as bytes
    offset = [] 						# Offset number encoded as bytes

    for char in text_bytes:
        if char == "<".encode(encoding)[0]:
            inside_token = True 				# We're now inside a token
            scanning_offset = True 				# We're now looking for the length number
        elif char == ",".encode(encoding)[0] and inside_token:
            scanning_offset = False
        elif char == ">".encode(encoding)[0]:
            inside_token = False 				# We're no longer inside a token

            # Convert length and offsets to an integer
            length_num = int(bytes(length).decode(encoding))
            offset_num = int(bytes(offset).decode(encoding))

            # Get text that the token represents
            referenced_text = output[-offset_num:][:length_num]

            output.extend(referenced_text) 			# referenced_text is a list of bytes so we use extend to add each one to output

            # Reset length and offset
            length, offset = [], []
	
        elif inside_token:
            if offset == "":
                raise ValueError(f'PZYPError.')
	    #:
            if scanning_offset:
                offset.append(char)
            else:
                length.append(char)
	    #:
        else:
            output.append(char) # Add the character to our output
	#:
    return bytes(output)
#:

def compress_file(fich, level, password, summary):
    global compressed_file
    if password is None:
        print("\nCompression without password")
        print(f'Level: [{level}] |'f' Summary: [{summary}]'f' File: [{fich}]\n')
        if os.path.exists(fich):
            text_File = open(fich,"rb")
            compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "wb") #opens in overwrite mode
            create_header(int(level),fich) #writes header to file
            if summary == True:
                compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "rb") #opens file in read mode to read header
                show_header(compressed_file.read())
                compressed_file.close()
            compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "ab") #opens in append mode to write data
            encode(text_File.read(), set_level(int(level))) # Runs encode cicle
            print("The compressed file", fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "has been sucessfuly created !\n")
            text_File.close()
            compressed_file.close()
        else:
            print("The specified file", fich, "does not exists!")
    else:
        print("\nCompression with password")
        print(f'Level: [{level}] |'f' Summary: [{summary}]'f' File: [{fich}]\n')
        if os.path.exists(fich):
            text_File = open(fich,"rb")
            compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "wb") #opens in overwrite mode
            create_header(int(level),fich) #writes header to file
            if summary == True:
                compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "rb") #opens file in read mode to read header
                show_header(compressed_file.read())
                compressed_file.close()
            compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "ab") #opens in append mode to write data
            encode(text_File.read(), set_level(int(level))) # Runs encode cicle
            print("The compressed file", fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "has been sucessfuly created !\n")
            text_File.close()
            compressed_file.close()
        else:
            print("The specified file", fich, "does not exists!")


def set_level(level):

    if level not in range(1,5):
        print(f' The specified compression level {level} it is outside possible interval [1-4]')
        print("Exiting...")
        sys.exit(2)
    else:
        match level:
            case 1:
                print("Compression level 1 settings | window 1kb")
                comp_lvl = 1024
            case 2:
                print("Compression level 2 settings | window 4kb")
                comp_lvl = 4096
            case 3:
                print("Compression level 3 settings | window 16kb")
                comp_lvl = 16384
            case 4:
                print("Compression level 4 settings | windows 32kb")
                comp_lvl = 32768
    return comp_lvl
                    
def decompress_file(fich, password, summary):
    global compressed_file
    if password is None:
        print("\nDecompress without password")
        print(f' Summary: [{summary}]'f' File: [{fich}]\n')
        if os.path.exists(fich):
            compressed_file = open(fich,"rb")
            if summary == True:
                show_header(compressed_file.read(262))
            text_File = open(fich.rsplit('.', 1)[0]+"_descomprimido.txt", "wb")
            compressed_file.seek(0,0) #reset the file position
            compressed_file.seek(262,1) # set it to byte 262
            dados=compressed_file.read()
            #print(decode(read_lzs_file(dados)))
            text_File.write(decode(read_lzs_file(dados)))
            print("The file was decompressed!\n")
        else:
            print("The specified file", fich, "does not exists!")
    else:
        print("\nDecompress with password")
        print(f' Summary: [{summary}]'f' File: [{fich}]\n')
        if os.path.exists(fich):
            compressed_file = open(fich,"rb")
            if summary == True:
                show_header(compressed_file.read(262))
            text_File = open(fich.rsplit('.', 1)[0]+"_descomprimido.txt", "wb")
            compressed_file.seek(0,0) #reset the file position
            compressed_file.seek(262,1) # set it to byte 262
            dados=compressed_file.read()
            #print(decode(read_lzs_file(dados)))
            text_File.write(decode(read_lzs_file(dados)))
            print("The file was decompressed!\n")
        else:
            print("The specified file", fich, "does not exists!")

def _lzs_encode(window):
    with lzss_io.io.BytesIO() as out:
        with lzss_io.LZSSWriter(out, ctx=ctx) as writer:
            for byte_int in window:
                writer.write(bytes((byte_int,)))
        #print('O ficheiro de saída tem os seguintes dados: ')
        out.seek(0)
        dados_comp = out.read()
        compressed_file.write(dados_comp)

def read_lzs_file(comp_file):
    dados = []
    #print('Vamos descodificar os dados anteriores')
    with lzss_io.io.BytesIO(bytes(comp_file)) as in_:
        with lzss_io.LZSSReader(in_, ctx=ctx) as reader:
            for encoded_flag, elemento in reader:
                dados.extend(elemento)
    return(dados)

def create_header(level,fich):
    #reverse power
    match level:
            case 1:
                reverse = 10 #(1024)
            case 2:
                reverse = 12 #(4096)
            case 3:
                reverse = 14 #(16384) 
            case 4:
                reverse = 15 #(32768)
    #timestamp (in seconds) - Double was used / could not set it to 32b integer/big-endian, but total header still uses 262 bytes
    ts = time.time()
    file = bytes(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, 'utf-8')
    compressed_file.write(struct.pack('bbd246p',reverse,reverse,ts,file))
    compressed_file.close()

def show_header(data):
    #print(data)
    #print(struct.calcsize("bbd246p"))
    tup_data = struct.unpack('bbd246p',data)
    comp_time = (time.strftime('%m/%d/%Y %H:%M:%S'))
    print("\nHeader data summary:\n")
    print(f'Name of compressed file : [{tup_data[3].decode("utf-8")}]')
    print(f'Timestamp : [{tup_data[2]}]')
    print(f'Window size : [{2 ** tup_data[0]} KB] {tup_data[0]} Bits | length size : [Default]') #lenght size WIP
    print(f'Compression date / time : [{comp_time}]\n') 

def main():
    # docopt saves arguments and options as key:value pairs in a dictionary
    args = docopt(__doc__, version='0.1')
    file = args['FILE']

    # run args
    if args['--compress']:
        compress_file(file, args['-l'], args["--password"],args["--summary"])
    if args['--decompress']:
        decompress_file(file, args["--password"],args["--summary"])
        
if __name__=='__main__':
    main()

   
