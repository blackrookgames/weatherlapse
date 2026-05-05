__all__ = [ 'StrUtil' ]

from io import StringIO as _StringIO

class StrUtil:
    """ Utility for string-related operations """

    @classmethod
    def to_argv(cls, s:str):
        """
        Parses the string as if the content is command-line arguments.\n
        Supported escape sequences:
        - \\n
        - \\\\\\
        - \\\\\"
        - \\\\'
        - \\b
        - \\r
        - \\a
        - \\0
        - \\x?? (?? indicates an 8-bit hexadecimal number)
        - \\u???? (???? indicates a 16-bit hexadecimal number)

        :param s: String to parse
        """
        argv:list[str] = []
        strio = _StringIO()
        pos = 0
        def flush():
            nonlocal argv, strio
            argv.append(strio.getvalue())
            strio.close()
            strio = _StringIO()
        def read():
            nonlocal pos
            def readchar():
                nonlocal pos
                c = s[pos]
                pos += 1
                return c
            # Is this an escape sequence?
            c = readchar()
            if c != '\\': return False, c
            # Yes! Is this a simple escape sequence?
            if pos == len(s): return True, chr(0)
            c = readchar()
            match c:
                case 'n': return True, '\n'
                case 't': return True, '\t'
                case '\\': return True, '\\'
                case '\"': return True, '\"'
                case '\'': return True, '\''
                case 'b': return True, '\b'
                case 'r': return True, '\r'
                case 'a': return True, '\a'
                case '0': return True, '\0'
            # No! It must be a character code.
            match c:
                case 'x': count = 2
                case 'u': count = 4
                case _: count = 0
            code = 0
            while count > 0:
                if pos == len(s): break
                code <<= 4
                c = ord(readchar())
                if c >= 0x30 and c <= 0x39: code |= c - 0x30
                elif c >= 0x41 and c <= 0x46: code |= (c - 0x41) + 10
                elif c >= 0x61 and c <= 0x66: code |= (c - 0x61) + 10
                count -= 1
            return True, chr(code)
        between = True
        inquotes = False
        try:
            while pos < len(s):
                e, c = read()
                # Is this the start of an argument?
                if between:
                    if ord(c) <= 0x20: continue
                    between = False
                # Is this a quotation mark
                if (not e) and c == '\"':
                    if inquotes:
                        flush()
                        between = True
                        inquotes = False
                    else:
                        inquotes = True
                    continue
                # Is this whitespace?
                if (not inquotes) and ord(c) <= 0x20:
                    flush()
                    between = True
                    continue
                # Anything else
                strio.write(c)
            # Last argument?
            if not between: flush()
        finally: strio.close()
        return argv
