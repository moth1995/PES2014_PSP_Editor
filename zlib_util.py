import zlib

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='little')

def unzlib_it(data):
    return zlib.decompress(data)

def zlib_it(data,compression):
    return zlib.compress(data,compression)

def file_read(file):
    '''
    Gets a file and return a byte array with his content
    '''
    with open(file, 'rb') as f:
        file_contents  = bytearray(f.read())
    return file_contents

def is_comp_pes_text(header):
    '''
    Search for the magic number for compressed pes texture in the header of the file
    The difference between this and another zlib pes file is that within this we have the filename
    '''
    return header[:4] == b'\x00\x02\x00\x00'

def is_audio(header):
    return header[:4] == b'RIFF'

def is_ovl(header):
    return header[:4] == b'MWo3'

def is_pes_kit(header):
    return header[:4] == b'\x00\x06\x01\x00' and header[8:12] == b'\xe0,\x02\x00'

def decrypt_kit(header,data):
    raise NotImplementedError

def pestext_to_png(data):
    raise NotImplementedError

def decompress(file):
    content = file_read(file)
    header = content[:32]
    #print(header)
    data = content[32:]
    #print(data[:8])
    data_size = bytes_to_int(header[4:8])
    #print(data_size)
    if is_audio(header):
        pass
    elif is_ovl(header):
        pass
    elif is_pes_kit(header):
        data = decrypt_kit(header,data)
        return pestext_to_png(data)
    else:
        num_of_files = bytes_to_int(data[:4])
        #print(num_of_files)
        files_index_offset = bytes_to_int(data[4:8])
        print(files_index_offset)
        filenames = []
        if is_comp_pes_text(header):
            # es necesario sacar los nombres si vamos a leerlo en memoria?
            filenames_index_offset = bytes_to_int(data[4:8])
            files_index_offset = bytes_to_int(data[8:12])
            for i in range(num_of_files):
                offset = filenames_index_offset + i * 4
                filename = str(data[offset : offset + 16])
                print(filename)
                filenames.append(filename)
            print(filenames)
        for i in range(num_of_files):
            print(i)
            offset = bytes_to_int(data[files_index_offset + i * 4 : files_index_offset + i * 4 + 4])
            print(offset)
            end_offset = bytes_to_int(data[files_index_offset + i * 4 +4 : files_index_offset + i * 4 + 8])
            print(end_offset)
            if i == num_of_files-1:
                '''
                Si estamos en la ultima iteracion, o sea leyendo el ultimo archivo, 
                seleccionamos desde el offset inicial del ultimo archivo hasta el final del archivo total
                O sea el valor que sacamos del encabezado mucho antes
                '''
                end_offset = data_size
            file_data = data[offset : end_offset]
            # Se pasa lo que seleccionamos sin el encabezado
            with open(f'subbin {i}.bin','wb') as s: s.write(unzlib_it(file_data[32:]))

decompress('./input/0TEXT/ID00051.bin')