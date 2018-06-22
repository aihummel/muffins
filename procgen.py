from fractions import Fraction as Fr
import re


# @author: Lexa

# TODO by MON, input easy, email
class Proc:
    def __init__(self, m, s, text, numbers):
        self.m = m
        self.s = s
        self.text = text
        self.numbers = numbers


def main():
    #    text = \
    #        """
    # $f(%s,%s)$
    # $f(%s,%s)=%s$
    # 1. %s muffins divided $(%s, %s)$.
    # 2. %s muffin divided $(%s, %s)$.
    # 3. Give %s students %s shares of size %s.
    # 4. Give %s students %s share of size %s and %s shares of size %s.
    # """
    #
    #    numbers1 = [Fr(5), Fr(4), Fr(5), Fr(4), Fr(3, 8), Fr(4), Fr(3, 8)]
    #    numbers1.extend([Fr(5, 8), Fr(1), Fr(1, 2), Fr(1, 2), Fr(2), Fr(2)])
    #    numbers1.extend([Fr(5, 8), Fr(2), Fr(1), Fr(1, 2), Fr(2), Fr(3, 8)])
    #
    # numbers2 = [Fr(9), Fr(4), Fr(9), Fr(4), Fr(7, 16), Fr(8), Fr(7, 16)]
    # numbers2.extend([Fr(9, 16), Fr(1), Fr(1, 2), Fr(1, 2), Fr(2), Fr(4)])
    # numbers2.extend([Fr(9, 16), Fr(2), Fr(1), Fr(1, 2), Fr(4), Fr(7, 16)])
    #
    # oproc1 = Proc(5, 4, text, numbers1)
    # oproc2 = Proc(9, 4, text, numbers2)

    # proc1 = parse_proc("proc1.tex")
    # proc2 = parse_proc("proc2.tex")
    #
    # # print(mkproc((oproc1, oproc2)))
    # print(mkproc((proc1, proc2)))

    print(get_general("proc1.tex", "proc2.tex"))


# input: file names for example procs
# generates file with and returns general proc
def get_general(file1, file2):
    proc1 = parse_proc(file1)
    proc2 = parse_proc(file2)
    general_proc = mkproc((proc1, proc2))
    filename = "generated_proc.tex"
    f = open(filename, 'w')
    f.write(general_proc)
    f.close()
    return general_proc


# Make proc for f(N*k+M, N) given procs for f(N*A+M, N) and f(N*B+M, N).
# ex_procs is tuple of two example f(N*k+M, N) Proc instances
# determine N, M, and ks
def mkproc(ex_procs):
    assert ex_procs[0].s == ex_procs[1].s
    N = ex_procs[0].s
    assert ex_procs[0].m % N == ex_procs[1].m % N
    M = ex_procs[0].m % N
    k0 = (ex_procs[0].m - M) / N
    k1 = (ex_procs[1].m - M) / N

    # Fit linear equations for each n=mk+b (num. and denom. separate)
    assert ex_procs[0].text == ex_procs[1].text
    formulae = []
    for i in range(len(ex_procs[0].numbers)):
        n0 = ex_procs[0].numbers[i]
        n1 = ex_procs[1].numbers[i]
        m_num = (n1.numerator - n0.numerator) / (k1 - k0)
        b_num = n0.numerator - m_num * k0
        m_denom = (n1.denominator - n0.denominator) / (k1 - k0)
        b_denom = n0.denominator - m_denom * k0

        # Make coefficients integers
        if int(m_num) != m_num:
            m_num_frac = Fr(m_num)
            d = m_num_frac.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d
        if int(b_num) != b_num:
            b_num_frac = Fr(b_num)
            d = b_num_frac.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d
        if int(m_denom) != m_denom:
            m_denom_frac = Fr(m_denom)
            d = m_denom_frac.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d
        if int(b_denom) != b_denom:
            b_denom_frac = Fr(b_denom)
            d = b_denom_frac.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d

        # divide any common multiple
        factor = min(val for val in [m_num, m_denom, b_num, b_denom] if val != 0)
        while factor > 1:
            if m_num % factor == m_denom % factor == b_num % factor == b_denom % factor == 0:
                m_num /= factor
                m_denom /= factor
                b_num /= factor
                b_denom /= factor
                break

        # check if numerator is multiple of denominator
        if m_num == m_denom == 0 or b_num == b_denom == 0 or \
                (m_denom != 0 and b_denom != 0 and m_num / m_denom == b_num / b_denom):
            frac = Fr(b_num / b_denom) if m_denom == 0 else Fr(m_num / m_denom)
            m_num = 0
            m_denom = 0
            b_num = frac.numerator
            b_denom = frac.denominator

        # make sure denominator isn't too negative
        if m_denom < 0 or m_denom == 0 and b_denom < 0:
            m_num *= -1
            m_denom *= -1
            b_num *= -1
            b_denom *= -1

        # insert string for formula accounting for cases of m and b
        formulae.append(formula_string(m_num, m_denom, b_num, b_denom))

    # insert formulae
    return ex_procs[0].text % tuple(formulae)


# make string for formula accounting for cases of m and b
def formula_string(m_num, m_denom, b_num, b_denom):
    if m_num == m_denom == 0 and b_denom == 1:  # b
        return "%d" % b_num
    elif m_num == m_denom == 0 and b_denom > 0:  # b0/b1
        return "\\frac{%d}{%d}" % (b_num, b_denom)
    elif m_num != 0 and m_denom == 1 and b_num == b_denom == 0:  # m
        return "%d" % m_num
    elif m_num != 0 and m_denom != 0 and b_num == b_denom == 0:  # m0/m1
        return "\\frac{%d}{%d}" % (m_num, m_denom)
    elif m_num == b_denom == 1 and m_denom == b_num == 0:  # k
        return "k"
    elif m_num == -b_denom == -1 and m_denom == b_num == 0:  # -k
        return "-k"
    elif m_num == b_denom == 1 and m_denom == 0 and b_num > 0:  # k + b
        return "k + %d" % b_num
    elif m_num == b_denom == 1 and m_denom == 0 and b_num < 0:  # k - b
        return "k - %d" % -b_num
    elif m_num == -b_denom == -1 and m_denom == 0 and b_num > 0:  # -k + b
        return "-k + %d" % b_num
    elif m_num == -b_denom == -1 and m_denom == 0 and b_num < 0:  # -k - b
        return "-k - %d" % -b_num
    elif m_num not in (0, 1, -1) and m_denom == b_num == 0 and b_denom == 1:  # mk
        return "%dk" % m_num
    elif m_num not in (0, 1, -1) and m_denom == 0 and b_num > 0 and b_denom == 1:  # mk + b
        return "%dk + %d" % (m_num, b_num)
    elif m_num not in (0, 1, -1) and m_denom == 0 and b_num < 0 and b_denom == 1:  # mk - b
        return "%dk - %d" % (m_num, -b_num)
    elif m_num == b_denom == 0 and m_denom == 1 and b_num != 0:  # b/k
        return "\\frac{%d}{k}" % b_num
    elif m_num == b_denom == 0 and m_denom > 0 and b_num != 0:  # b/mk
        return "\\frac{%d}{%dk}" % (b_num, m_denom)
    elif m_num == 1 and m_denom == 0 and b_num > 0 and b_denom > 0:  # (k + b0)/b1
        return "\\frac{k + %d}{%d}" % (b_num, b_denom)
    elif m_num == 1 and m_denom == 0 and b_num < 0 < b_denom:  # (k - b0)/b1
        return "\\frac{k - %d}{%d}" % (-b_num, b_denom)
    elif m_num == -1 and m_denom == 0 and b_num > 0 and b_denom > 0:  # (-k + b0)/b1
        return "\\frac{-k + %d}{%d}" % (b_num, b_denom)
    elif m_num == -1 and m_denom == 0 and b_num < 0 < b_denom:  # (-k - b0)/b1
        return "\\frac{-k - %d}{%d}" % (-b_num, b_denom)
    elif m_num not in (0, -1, 1) and m_denom == 0 and b_num > 0 and b_denom > 0:  # (mk + b0)/b1
        return "\\frac{%dk + %d}{%d}" % (m_num, b_num, b_denom)
    elif m_num not in (0, -1, 1) and m_denom == 0 and b_num < 0 < b_denom:  # (mk - b0)/b1
        return "\\frac{%dk - %d}{%d}" % (m_num, -b_num, b_denom)
    elif m_num != 0 and m_denom == 1 and b_num > 0 and b_denom == 0:  # m + b/k
        return "%d + \\frac{%d}{k}" % (m_num, b_num)
    elif m_num != 0 and m_denom == 1 and b_num < 0 and b_denom == 0:  # m - b/k
        return "%d - \\frac{%d}{k}" % (m_num, -b_num)
    elif m_num != 0 and m_denom > 1 and b_num > 0 and b_denom == 0:  # (m0k + b)/m1k
        return "\\frac{%dk + %d}{%dk}" % (m_num, b_num, m_denom)
    elif m_num != 0 and m_denom > 1 and b_num < 0 and b_denom == 0:  # (m0k - b)/m1k
        return "\\frac{%dk - %d}{%dk}" % (m_num, -b_num, m_denom)
    elif m_num == 0 and m_denom == 1 and b_num != 0 and b_denom > 0:  # b0/(k + b1)
        return "\\frac{%d}{k + %d}" % (b_num, b_denom)
    elif m_num == 0 and m_denom == 1 and b_num != 0 and b_denom < 0:  # b0/(k - b1)
        return "\\frac{%d}{k - %d}" % (b_num, -b_denom)
    elif m_num == 0 and m_denom > 1 and b_num != 0 and b_denom > 0:  # b0/(mk + b1)
        return "\\frac{%d}{%dk + %d}" % (b_num, m_denom, b_denom)
    elif m_num == 0 and m_denom > 1 and b_num != 0 and b_denom < 0:  # b0/(mk - b1)
        return "\\frac{%d}{%dk - %d}" % (b_num, m_denom, -b_denom)
    elif m_num == m_denom == 1 and b_num == 0 and b_denom > 0:  # k/(k + b)
        return "\\frac{k}{k + %d}" % b_denom
    elif m_num == m_denom == 1 and b_num == 0 and b_denom < 0:  # k/(k - b)
        return "\\frac{k}{k - %d}" % -b_denom
    elif m_num == -m_denom == -1 and b_num == 0 and b_denom > 0:  # -k/(k + b)
        return "\\frac{-k}{k + %d}" % b_denom
    elif m_num == -m_denom == -1 and b_num == 0 and b_denom < 0:  # -k/(k - b)
        return "\\frac{-k}{k - %d}" % -b_denom
    elif m_num == 1 and m_denom > 1 and b_num == 0 and b_denom > 0:  # k/(mk + b)
        return "\\frac{k}{%dk + %d}" % (m_denom, b_denom)
    elif m_num == 1 and m_denom > 1 and b_num == 0 and b_denom < 0:  # k/(mk - b)
        return "\\frac{k}{%dk - %d}" % (m_denom, -b_denom)
    elif m_num == -1 and m_denom > 1 and b_num == 0 and b_denom > 0:  # -k/(mk + b)
        return "\\frac{-k}{%dk + %d}" % (m_denom, b_denom)
    elif m_num == -1 and m_denom > 1 and b_num == 0 and b_denom < 0:  # -k/(mk - b)
        return "\\frac{-k}{%dk - %d}" % (m_denom, -b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num == 0 and b_denom > 0:  # m0k/(m1k + b)
        return "\\frac{%dk}{%dk + %d}" % (m_num, m_denom, b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num == 0 and b_denom < 0:  # m0k/(m1k - b)
        return "\\frac{%dk}{%dk - %d}" % (m_num, m_denom, -b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num > 0 and b_denom > 0:  # (m0k + b0)/(m1k + b1)
        return "\\frac{%dk + %d}{%dk + %d}" % (m_num, b_num, m_denom, b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num < 0 < b_denom:  # (m0k - b0)/(m1k + b1)
        return "\\frac{%dk - %d}{%dk + %d}" % (m_num, -b_num, m_denom, b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_denom < 0 < b_num:  # (m0k + b0)/(m1k - b1)
        return "\\frac{%dk + %d}{%dk - %d}" % (m_num, b_num, m_denom, -b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num < 0 and b_denom < 0:  # (m0k - b0)/(m1k - b1)
        return "\\frac{%dk - %d}{%dk - %d}" % (m_num, -b_num, m_denom, -b_denom)


# Returns the index of the last character of s.
def my_index(text, s):
    return text.index(s) + len(s) - 1


# input: file w/ LaTeX source code of proc w/ numerical values (e.g. 5, 4/5)
# instead of formulae
# output: Proc object
def parse_proc(proc_file):
    infile = open(proc_file)

    text = infile.read()
    orig = text

    # # Removes enumerating numbers.
    # to_remove = [str(s) for s in re.findall(r'\d+\.', text)]
    #
    # for s in to_remove:
    #     text = text.replace(s, "")

    # Captures isolated numbers  and fractions
    # str_nums = re.findall(r'\d+', text)
    str_nums = re.findall(r'\d+[^\w}.\]]|\\frac{\d+}{\d+}', text)
    # str_nums = [''.join(tup) for tup in str_nums]

    # Finds numbers in original text and determines what the fractions are.
    nums = []
    for s in str_nums:
        # if text[my_index(text, s) + 2] == '{':
        if '\\frac' in s:
            # num = text[my_index(text, s) + 3: my_index(text, s) + len(s) + 4]
            # num = num.replace("}", "")
            (num, denom) = tuple(re.findall(r'{(\d+)}', s))
            # to_add = Fr(int(s), int(num))
            to_add = Fr(int(num), int(denom))
            nums.append(to_add)
            text = text.replace(s, "", 1)
            # elif text[my_index(text, s) + 1] == '}':
            #     text = text.replace(s, "", 1)
        else:
            # text = text.replace(s, "", 1)
            # nums.append(Fr(int(s)))
            text = text.replace(s, s[-1], 1)
            nums.append(Fr(int(s[:-1])))

    # Replaces numbers in original with placeholders.
    for s in str_nums:
        # orig = orig.replace(s, "%s")
        orig = orig.replace(s, "%s") if '\\frac' in s else orig.replace(s, "%s"+s[-1])

    # for s in to_remove:
    #     orig = orig.replace(s, "%s.")

    # i = 1
    # while "%s." in orig:
    #     orig = orig.replace("%s.", str(i) + ".", 1)
    #     i = i + 1

    # orig = orig.replace("\\frac{%s}{%s}", "%s")

    # Creates Proc object.
    proc = Proc(nums[0].numerator, nums[1].numerator, orig, nums)

    return proc


#    # read m and s
#    function_start = text.find("f")
#    open_paren = text[function_start:].find("(") + function_start
#    comma = text[open_paren:].find(",") + open_paren
#    close_paren = text[comma:].find(")") + comma
#    m = text[open_paren+1:comma].strip()
#    assert m.isdigit()
#    m = int(m)
#    s = text[comma+1:close_paren].strip()
#    assert s.isdigit()
#    s = int(s)
#
#    # isolate number values and format text
#    # assumes fractions are formatted \frac{a}{b} with no space
#    i = 0
#    numbers = []
#    while i < len(text):
#        if text[i].isdigit():
#            j = i + 1
#            while text[j].isdigit():
#                j += 1
#            if i > 0 and text[i-7:i-1] == r"\frac{" and text[j:j+2] == "}{" and text[j+2].isdigit():
#                k = text[j+3:].find("}") + j+3
#
#        else:
#            i += 1

if __name__ == "__main__":
    main()
