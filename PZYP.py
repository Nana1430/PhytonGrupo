# Compressor e descompressor -teste

#imports
import sys
import os.path

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

def encode(text, max_sliding_window_size=4096):
    text_bytes = text.encode(encoding)

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
    return bytes(output)
#:
encoding = "utf-8"

#Descompressor
def decode(text):
	
    text_bytes = text.encode(encoding) 				# The text encoded as bytes
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

def compress_file(fich):
    if os.path.exists(fich):
        text_file = open(fich,"r")
        compressed_file = open(fich.rsplit('.', 1)[0]+".LZS", "w")
        compressed_file.write(str(encode(text_file.read(), 1024)))
        print("O ficheiro comprimido", fich.rsplit('.', 1)[0]+".LZS", "foi criado !")
    else:
        print("O ficheiro especificado", fich, "não existe!")

def sys_argv_func(*args):
    if len(sys.argv) <= 1 or len(sys.argv) >= 4:
        print("Utilização: PYZP", "[-d](para descomprimir - opcional)", 
            "ficheiro", file=sys.stderr)
        sys.exit(2)
    #:
    if len(sys.argv) == 2: 					# only the file argument (compress)
        compress_file(sys.argv[1])
    #:
    if len(sys.argv) == 3: 					# 2 arguments, testing if is -d
        if sys.argv[1].lower() != "-d":
            print("Argumento desconhecido",sys.argv[1], " Utilização: PYZP", "[-d](para descomprimir - opcional)", 
            "ficheiro", file=sys.stderr)
            sys.exit(2)
        else:
            print(decode(sys.argv[2]).decode(encoding))
	#:
    #:

if __name__ == "__main__":
    sys_argv_func(sys.argv)
    
    
#:


   
