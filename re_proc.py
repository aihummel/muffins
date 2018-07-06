from fractions import Fraction as Fr
import re


# @author: Lexa


# for checking general procs
# input: general proc filename, desired k-value
# output: makes file with specific proc
def re_parse(proc_file, k):
    infile = open(proc_file)
    text = infile.read()
    infile.close()

    # selects formulae involving k
    exps = re.findall(r"\d*k[^+\-\w]|\d*k *[+\-] *\d+.", text)

    # loops through formulae
    vals = []
    for exp in exps:
        # mark insertion point
        text = text.replace(exp, "@" + exp[-1], 1)

        # tokenize formula
        exp = exp[:-1]
        seq = re.findall(r"(\d*)(k) *([+-]) *(\d+)", exp) if "+" in exp or "-" in exp else re.findall(r"(\d*)(k)", exp)
        seq = list(seq[0])
        if "" in seq:
            seq.remove("")

        # multiply k by coefficient if any
        my_k = k
        if len(seq) > 1 and seq[1] == "k":
            my_k *= int(seq[0])
            del seq[0]

        # determine formula value
        val = 0
        if seq[0] == "k":
            if len(seq) == 1:
                val = my_k
            elif seq[1] == "+":
                val = my_k + int(seq[2])
            else:
                val = my_k - int(seq[2])
        elif len(seq) == 1:
            val = int(seq[0])
        # print(exp, "\t", val)
        vals.append(val)

    # replace formulae with values
    for val in vals:
        text = text.replace("@", str(val), 1)

    # reduce fractions to integers when possible
    fractions = re.findall(r'\\frac{\d+}{\d+}', text)
    replace = []
    for frac in fractions:
        (num, denom) = tuple(re.findall(r'\d+', frac))
        num = int(num)
        denom = int(denom)
        if num % denom == 0:
            replace.append(str(int(num / denom)))
        else:
            replace.append(frac)
        text = text.replace(frac, "@", 1)
    for s in replace:
        text = text.replace("@", s, 1)

    # write outfile
    outfile = open("specific_"+proc_file, "w")
    outfile.write(text)
    outfile.close()


if __name__ == "__main__":
    re_parse("generated_proc.tex", 9)
    re_parse("compare.tex", 9)
