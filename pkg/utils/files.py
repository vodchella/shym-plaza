def read_file_lines(file_name: str):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_file(file_name: str):
    f = open(file_name, 'r')
    lines = f.read()
    f.close()
    return lines


def write_file(file_name: str, data: str):
    f = open(file_name, 'w')
    f.write(data)
    f.close()


def write_file_binary(file_name: str, data: str):
    f = open(file_name, 'wb')
    f.write(data.encode('utf-8'))
    f.close()
