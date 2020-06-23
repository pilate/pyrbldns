import sys


def main():
    filename = sys.argv[1]
    with open(filename, 'r')  as f:
        a_record = txt_record = None
        for line_num, line in enumerate(f):
            line = line.rstrip()

            if not line:
                continue

            # comment or  directive
            if line[0] in ('#', '$'):
                continue

            # start of a new list
            elif line[0] == ':':
                if line.count(':') < 2:
                    raise Exception(f'Missing colon on line {line_num}')

                _, a_record, txt_record = line.split(':', 2)
                continue

            # must be an ip or domain line, make sure we know what list its in
            elif not a_record:
                raise Exception(f'Found resources without a record. Line: {repr(line)}')

            # domain name
            elif line[0] == '.':
                print(f'Domain: {line}, A: {a_record}, TXT: {txt_record.replace("$", line[1:])}')


main() if __name__ == '__main__' else None
