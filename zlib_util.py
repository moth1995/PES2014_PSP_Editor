import zlib
import os

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

def is_inflate(data):
    '''
    We read the offset 32 and check if we have a file number or a zlib magic number
    '''
    offset_32 = data[:2]
    return offset_32 == b'\x78\xDA' or offset_32 == b'\x78\x01' or offset_32 == b'\x78\x5E' or offset_32 == b'\x78\x9C'

def get_zlib_comp_level(data):
    pass

def pad_with_zeros(data):
    '''
    Fill with zeros at the end of the inflate file, needed to create the compress pes file
    '''
    size = len(data)
    if size % 16 != 0:
        pad_number = 16 - (size % 16)
    else:
        return data
    padding = bytearray([0x0 for _ in range(pad_number)])  # Create bytearray
    data = data + padding  # Append bytes to the end
    return data

def decrypt_kit(header,data):
    raise NotImplementedError

def pestext_to_png(data):
    raise NotImplementedError

def get_name_from_path(file_path):
    return os.path.basename(file_path)

def get_filenames(header,data,num_of_files,name):
    '''
    Returns a list within the filenames for the subbins inside the compressed file, if its a pes texture, then it will also
    return those names separate with a middle dash
    '''
    filenames = []
    if is_comp_pes_text(header):
        filenames_index_offset = bytes_to_int(data[4:8])
        for i in range(num_of_files):
            offset = bytes_to_int(data[filenames_index_offset + i * 4 : filenames_index_offset + i * 4 + 4])
            filename = data[offset : offset + 16].partition(b"\0")[0].decode()
            # Instead of using underscore we use middle dash for the file name when its a pes texture 
            # mainly because those store the names of files
            filenames.append(f'{name}_{i:03}-{filename}')
        return filenames
    else:
        for i in range(num_of_files):
            filenames.append(f'{name}_{i:03}')
        return filenames

def get_uncompress_files(header,data,num_of_files,data_size):
    '''
    Does all the logic needed and returns a list with all the files
    '''
    files_index_offset = bytes_to_int(data[4:8])
    if is_comp_pes_text(header):
        files_index_offset = bytes_to_int(data[8:12])
    files_data = []
    for i in range(num_of_files):
        offset = bytes_to_int(data[files_index_offset + i * 4 : files_index_offset + i * 4 + 4])
        end_offset = bytes_to_int(data[files_index_offset + i * 4 +4 : files_index_offset + i * 4 + 8])
        if i == num_of_files-1:
            '''
            Si estamos en la ultima iteracion, o sea leyendo el ultimo archivo, 
            seleccionamos desde el offset inicial del ultimo archivo hasta el final del archivo total
            O sea el valor que sacamos del encabezado mucho antes
            '''
            end_offset = data_size
        file_data = unzlib_it(data[offset : end_offset][32:])
        files_data.append(file_data)
    return files_data

def decompress(file):
    name = get_name_from_path(file)
    content = file_read(file)
    header = content[:32]
    data = content[32:]
    data_size = bytes_to_int(header[4:8])
    if is_audio(header):
        raise NotImplementedError 
    elif is_ovl(header):
        raise NotImplementedError
    elif is_pes_kit(header):
        return pestext_to_png(decrypt_kit(header,data))
    elif is_inflate(data[:2]):
        '''
        IF we fall here then it's a pes .str file the ones that contains text for the game
        '''
        with open(f'{name}_{0:03}','wb') as s: s.write(unzlib_it(data))
    else:
        '''
        If we get here then we got a compress pes file, it could be one with textures for the game 
        or with binary data to modify for ie. the database of players
        '''
        num_of_files = bytes_to_int(data[:4])
        filenames = get_filenames(header,data,num_of_files,name)
        files_data = get_uncompress_files(header,data,num_of_files,data_size)
        for filenumber,file in enumerate(files_data):
            with open(filenames[filenumber],'wb') as s: s.write(file)

decompress('./input/0TEXT/ID00051.bin')