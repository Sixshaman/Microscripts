import sys
import re

if __name__ == "__main__":
    non_aligned_lines = []
    with open(sys.argv[1], "r", encoding="utf8") as f:
        for line in f:
            non_aligned_lines.append(line.replace("\n", "\r\n"))
        f.close()

    max_len = 0
    for non_aligned_line in non_aligned_lines:
        if re.match("\[.+\] .*\.\.\.[0-9]{2}\:[0-9]{2}.*", non_aligned_line):
            max_len = max(max_len, len(non_aligned_line))

    with open(sys.argv[1], "w", encoding="utf8") as f:
        for line in non_aligned_lines:
            groups = re.findall("(\[.+\] .*)(\.\.\.[0-9]{2}\:[0-9]{2}.*)", line)
            if len(groups) > 0:
                if len(groups[0]) == 2:
                    dot_len = max_len - len(line)
                    f.write(groups[0][0] + "." * dot_len + groups[0][1])
                else:
                    f.write(line[:-1])
            else:
                f.write(line[:-1])
                
        f.close()