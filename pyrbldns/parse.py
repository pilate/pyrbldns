import re
import sys



ENTRY_RE = re.compile(r'^(?P<prefix>[\w\/\.\*-]+)\s*(?P<value>.*)$')


def parse_value(value_str):
    if value_str.count(':') < 2:
        raise Exception(f'Two colons expected: {value_str}')

    _, a_record, txt_record = value_str.split(':', 2)
    return a_record, txt_record


def parse(fileobj):
    a_default = txt_default = None
    for line_num, line in enumerate(fileobj):
        line = line.strip()

        if not line:
            continue

        # comment or directive
        if line[0] in ('#', '$'):
            continue

        # exclusion
        if line[0] == '!':
            continue

        # new default value
        elif line[0] == ':':
            a_default, txt_default = parse_value(line)
            continue

        # must be an ip or domain line, make sure we know what list its in
        elif not a_default:
            raise Exception(f'Found resources without a record. Line: {repr(line)}')

        # All other entries... hopefully
        else:
            a_record, txt_record = a_default, txt_default

            match = ENTRY_RE.match(line)
            if not match:
                raise Exception(f'Unknown line format: {line}')

            prefix, value = match.groups()
            if value:
                if value.startswith(':'):
                    a_record, txt_record = parse_value(value)
                else:
                    txt_record = value

            print(f'prefix: {prefix}, a:{a_record}, txt:{txt_record}')


def main():
    filename = sys.argv[1]
    with open(filename, 'r')  as f:
        parse(f)


main() if __name__ == '__main__' else None
