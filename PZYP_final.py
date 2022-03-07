# Compressor e descompressor -teste
'''
Usage:
    pzip [-c [-l LEVEL] | -d | -h] [-s] [-p PASSWORD] FILE

Operation:
    -c, --encode, --compress            Compress FILE whith PZYP
    -d, --decode, --decompress          Decompress FILE compressed with PZYP

Options:
    -l, --level=LEVEL                   Compression level [default: 2] 
    -s, --summary                       Resume of compressed file      
    -h, --help                          Shows this help message and exits.
    -p PASSWORD, --password=PASSWORD    An optional password to encrypt the file (compress only)

    FILE                                The path to the file to compress / decompress
'''
#imports
import struct
from docopt import docopt
from cryptography.fernet import Fernet
import base64
import sys
import os.path
import lzss_io
import time
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
        if len(check_elements) <= offset:
            # All of the elements in check_elements are in elements
            return i - len(check_elements)
        if check_elements[offset] == element:
            offset += 1
        else:
            offset = 0
        i += 1
    return -1

encoding = "utf-8"

def encode(text, max_sliding_window_size, pwcheck):
    
    if pwcheck is not None:
        text_bytes = text.encode(encoding)
    else:
        text_bytes=text
        
    search_buffer = [] # Array of integers, representing bytes
    check_characters = [] # Array of integers, representing bytes
    output = [] # Output array

    i = 0
    for char in text_bytes:
        index = elements_in_array(check_characters, search_buffer) # The index where the characters appears in our search buffer

        if elements_in_array(check_characters + [char], search_buffer) == -1 or i == len(text_bytes) - 1:
            if i == len(text_bytes) - 1 and elements_in_array(check_characters + [char], search_buffer) != -1:
                # Only if it's the last character then add the next character to the text the token is representing
                check_characters.append(char)
            
            if len(check_characters) > 1:
                index = elements_in_array(check_characters, search_buffer)
                offset = i - index - len(check_characters) # Calculate the relative offset
                length = len(check_characters) # Set the length of the token (how many character it represents)
                token = f"<{offset},{length}>" # Build our token

                if len(token) > length:
                    # Length of token is greater than the length it represents, so output the characters
                    output.extend(check_characters) # Output the characters
                else:
                    output.extend(token.encode(encoding)) # Output our token
                
                search_buffer.extend(check_characters) # Add the characters to our search buffer   
            else:
                output.extend(check_characters) # Output the character  
                search_buffer.extend(check_characters) # Add the characters to our search buffer   

            check_characters = []   
        check_characters.append(char)
        if len(search_buffer) > max_sliding_window_size: # Check to see if it exceeds the max_sliding_window_size
            search_buffer = search_buffer[1:] # Remove the first element from the search_buffer
        i += 1
    if pwcheck is not None:
        _lzs_encode(output[2:]) # [2:] resolução de um bug de casting
    else:
       _lzs_encode(bytes(output))

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
                raise ValueError(f'PZYP Error. Empty offset.')
            if scanning_offset:
                offset.append(char)
            else:
                length.append(char)
        else:
            output.append(char) # Add the character to our output
    return bytes(output)


def compress_file(fich, level, password, summary):
    global compressed_file
    global status_message
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
            encode(text_File.read(), set_level(int(level),summary), password) # Runs encode cicle
            file_name = str(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT)
            status_message = f'The file [{fich}] was sucessfuly compressed!\n\nCompressed File: [{file_name}]'
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
            #encripts data
            key = make_key((password).encode(encoding))
            encrypted_data = encrypt(text_File.read(), key)
            #end of data encryption
            compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "wb") #opens in overwrite mode
            create_header(int(level),fich) #writes header to file
            if summary == True:
                compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "rb") #opens file in read mode to read header
                show_header(compressed_file.read())
                compressed_file.close()
            compressed_file = open(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "ab") #opens in append mode to write data
            encode(str(encrypted_data), set_level(int(level),summary),password) # Runs encode cicle
            compressed_file.close()
            text_File.close()
            file_name = str(fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT)
            status_message = f'The file [{fich}] was sucessfuly compressed and encrypted!\n\nCompressed File: [{file_name}]'
            print("The compressed file with password encription", fich.rsplit('.', 1)[0]+"."+DEFAULT_EXT, "has been sucessfuly created !\n")
        else:
            print("The specified file", fich, "does not exists!")

def make_key(password):
    salt = b'FW\x01]\x02\xce\xc5Y\x01}Xi\x1e>\x890'
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=0,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt(file_data , key):
    f = Fernet(key)
    encrypted = f.encrypt(file_data)
    return encrypted

def decrypt(file, key):
    global error_exp
    error_exp = ''
    try:
        f = Fernet(key)
        with open(file, "rb") as file_read:
            encrypted_data = file_read.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(file, "wb") as file_write:
            file_write.write(decrypted_data)
    except:
        error_exp = "erro"

def decrypt_status():
    global status_message
    if error_exp == 'erro':
        print('An error as ocurred decrypting the file, possible cause: incorrect password')
        status_message='An error as ocurred decrypting the file, possible cause: incorrect password'
    else:
        print("The file was decompressed and decrypted!\n")

def set_level(level, summary):
    if level not in range(1,5):
        print(f' The specified compression level {level} it is outside possible interval [1-4]')
        print("Exiting...")
        sys.exit(2)
    else:
        match level:
            case 1:
                if summary == True:
                    comp_lvl = 1024
                else:
                    print("Compression level 1 settings | window 1kb")
                    comp_lvl = 1024
            case 2:
                if summary == True:
                    comp_lvl = 4096
                else:
                    print("Compression level 2 settings | window 1kb")
                    comp_lvl = 4096
            case 3:
                if summary == True:
                    comp_lvl = 16384
                else:
                    print("Compression level 3 settings | window 1kb")
                    comp_lvl = 16384
            case 4:
                if summary == True:
                    comp_lvl = 32769
                else:
                    print("Compression level 4 settings | window 1kb")
                    comp_lvl = 32769
    return comp_lvl
                    
def decompress_file(fich, password, summary):
    global compressed_file
    global status_message
    if password is None:
        print("\nDecompress without password")
        print(f'Summary: [{summary}]'f' File: [{fich}]\n')
        if os.path.exists(fich):
            compressed_file = open(fich,"rb")
            if summary == True:
                show_header(compressed_file.read(262))
            compressed_file.seek(0,0) #reset the file position
            file_name_ext =  get_original_file_name(compressed_file.read(262))            
            file_extension = os.path.splitext(file_name_ext)[1]
            file_names = os.path.splitext(file_name_ext)[0]
            text_File = open(file_names+"_descomprimido"+file_extension, "wb")
            compressed_file.seek(0,0) #reset the file position
            compressed_file.seek(262,1) # set it to byte 262
            dados=compressed_file.read()
            text_File.write(decode(read_lzs_file(dados)))
            file_name = str(file_names+"_descomprimido"+file_extension)
            status_message = f'The file was decompressed!\n\nSummary: [{summary}]'f'File: [{file_name}]'
            print("The file was decompressed!\n")
        else:
            print("The specified file", fich, "does not exists!")
    else:
        print("\nDecompress with password")
        print(f'Summary: [{summary}]'f' File: [{fich}]\n')
        if os.path.exists(fich):
            compressed_file = open(fich,"rb")
            if summary == True:
                show_header(compressed_file.read(262))
            compressed_file.seek(0,0) #reset the file position
            file_name_ext =  get_original_file_name(compressed_file.read(262))            
            file_extension = os.path.splitext(file_name_ext)[1]
            file_names = os.path.splitext(file_name_ext)[0]
            text_File = open(file_names+"_descomprimido"+file_extension, "wb")
            compressed_file.seek(0,0) #reset the file position
            compressed_file.seek(262,1) # set it to byte 262
            dados=compressed_file.read()
            text_File.write(decode(read_lzs_file(dados)))
            text_File.close()
            file_name = str(file_names+"_descomprimido"+file_extension)
            key = make_key((password).encode(encoding))
            decrypt(file_name, key)
            status_message = f'The file was decompressed and decrypted!\n\nSummary: [{summary}]'f'File: [{file_name}]'
            decrypt_status()
        else:
            print("The specified file", fich, "does not exists!")

def _lzs_encode(window):
    with lzss_io.io.BytesIO() as out:
        with lzss_io.LZSSWriter(out, ctx=ctx) as writer:
            for byte_int in window:
                writer.write(bytes((byte_int,)))
        out.seek(0)
        dados_comp = out.read()
        compressed_file.write(dados_comp)

def read_lzs_file(comp_file):
    dados = []
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
    file = bytes(fich, 'utf-8')
    compressed_file.write(struct.pack('bbd246p',reverse,reverse,ts,file))
    compressed_file.close()

def show_header(data):
    tup_data = struct.unpack('bbd246p',data)
    comp_time = (time.strftime('%m/%d/%Y %H:%M:%S'))
    print("\nHeader data summary:\n")
    print(f'Name of compressed file : [{tup_data[3].decode("utf-8")}]')
    print(f'Timestamp : [{tup_data[2]}]')
    print(f'Window size : [{2 ** tup_data[0]} KB] {tup_data[0]} Bits | length size : [Default]') #lenght size WIP
    print(f'Compression date / time : [{comp_time}]') 
    print(f'Author(s): Ana Graça, Nuno Guerra, Sónia Jardim\n')

def get_original_file_name(data):
    tup_data = struct.unpack('bbd246p',data)
    comp_time = (time.strftime('%m/%d/%Y %H:%M:%S'))
    return tup_data[3].decode("utf-8")

def status():
    global status_message
    return str(status_message)

def main():
    # docopt saves arguments and options as key:value pairs in a dictionary
    args = docopt(__doc__, version='0.1')
    file = args['FILE']

    # run args
    if args['--compress']:
        compress_file(file, args["--level"], args["--password"],args["--summary"])
    if args['--decompress']:
        decompress_file(file, args["--password"],args["--summary"])

    # function to compress / decompress from Gui_module
def ui_main(operation, level, password, summary, file):
    if operation == "compress":
        compress_file(file, level, password, summary)
    if operation == "uncompress":
        decompress_file(file, password, summary)
        
if __name__=='__main__':
    main()
    sys.exit(0)



   
