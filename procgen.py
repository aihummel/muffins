from fractions import Fraction as Fr
import itertools as it
import re
import time

class Proc:
    def __init__(self, m, s, text, numbers):
        self.m = m
        self.s = s
        self.text = text
        self.numbers = numbers


def main():
#    print(get_general_give_only("proc1.tex", "proc2.tex"))
    
    # [Fr(5), Fr(4), Fr(5), Fr(4), Fr(3, 8), Fr(4), Fr(3, 8), Fr(5, 8), 
    # Fr(1), Fr(1, 2), Fr(1, 2), Fr(2), Fr(2), Fr(5, 8), Fr(2), Fr(1), 
    # Fr(1, 2), Fr(2), Fr(3, 8)] 
    t = time.time()
#    print(find_proc(5, 4, Fr(3,8), 2)) 
#    print(find_proc(9, 4, Fr(7,16), 2))
#    print(find_proc(11, 6, Fr(7,18), 2))
#    print(find_proc(7, 3, Fr(5,12), 1))
#    print(find_proc(8, 3, Fr(4,9), 1))
#    print(find_proc(13, 10, Fr(7,20), 4))
    print(find_proc(31, 13, Fr(21,52), 3)) #466 seconds to <1 second!!
#    print(find_proc(21, 5, Fr(7,15), 2))
#    print(find_proc(34, 15, Fr(13,30), 7))
#    print(find_proc(32, 13, Fr(5,13), 6))
#    print(find_proc(59, 33, Fr(40,99), 16))
    
    print(time.time() - t)
    
    # instructions = r"1. $4k$ muffins divided $(\frac{4k-1}{8k},\frac{4k+1}{8k})$", \
    #                r"2. $1$ muffin divided $(\frac{1}{2},\frac{1}{2})$", \
    #                r"3. Give 2 students $2k$ shares of size $\frac{4k+1}{8k}$", \
    #                r"4. Give 2 students 1 share of size $\frac{1}{2}$ and $2k$ shares of size $\frac{4k-1}{8k}$"
    # print(format_tex("f(4k+1,4)", r"$f(4k+1,4) = \frac{4k-1}{8k}$ for $k > 0$:", instructions))

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

# input: file names for give-only example procs
# generates file with and returns general proc
def get_general_give_only(file1, file2):
    text1 = part_input(file1)
    text2 = part_input(file2)
    proc1 = parse_proc(text=text1)
    proc2 = parse_proc(text=text2)
    general_proc = mkproc((proc1, proc2))
    filename = "generated_proc.tex"
    f = open(filename, 'w')
    f.write(general_proc)
    f.close()
    return general_proc

def symmetric_pairs(size, pairs, pairwise):
    if size == 2:
        return pairs
    
    new_pairs = []
    
    for pair in pairs:
        i = len(pair)//2 - 1
        sub_pair = pair[i: i+2]
        j = pairwise.index(sub_pair)
        
        new_pairwise = pairwise[j: len(pairwise)]
        
        for p in new_pairwise:
            to_add = []
            to_add += pair
            to_add += p
            to_add.sort()
            new_pairs.append(to_add)
            
    return symmetric_pairs(size - 2, new_pairs, pairwise)

def one_is_in(combos, i):
    for c in combos:
        if set(c).issubset(set(i)):
            return True
    
    return False

def combos_helper(s, method, vals, methods):
    for i in vals:
        if s < i:
            continue
        
        j = method[i]
        method[i] = j + 1
        
        if s > i:
            combos_helper(s - i, method, vals, methods)
        else:
            new_m = []
            new_m += method
            methods.append(new_m)
            
        k = method[i]
        method[i] = k - 1

# Helper function that returns linear combinations that sum to the value.   
def combo(arr, val):
    combos = []
    method = [0]*(arr[len(arr) - 1] + 1)
    
    methods = []
    combos_helper(val, method, arr, methods)
    
    new_methods = []
    good_coeffs = []
    
    for m in methods:
        if not m in new_methods:
            new_methods.append(m)
    
    for m in new_methods:
        good_coeffs.append(m[arr[0]: arr[len(arr) - 1] + 1])
        
    for i in good_coeffs:
        to_add = []
        
        for j in range(len(arr)):
            to_add += list(it.repeat(arr[j], i[j]))
            
        combos.append(to_add)
        
    return combos

def subtract(a, b):
    for i in a:
        if i in b:
            b.remove(i)

# input: muffins, students, fc fraction, number of "fixed" students
def find_proc(m, s, fc, fixed):
    whole = fc.denominator
    total = m*(whole//s)
    
    interval = []
    for i in range(fc.numerator, whole - fc.numerator + 1):
        interval.append(i)
        
    combos = combo(interval, total)
    
    del interval[0]
    del interval[len(interval) - 1]
    
    fixed_shares = []
    
    for j in combos:
        if sum(j) % j[0] == 0:
            fixed_shares = j
            break
        
    all_fixed = list(it.repeat(fixed_shares, fixed))
    flat_fixed = []
    opp_flat_fixed = []
    
    for l in all_fixed:
        flat_fixed += l
        
    for i in flat_fixed:
        opp_flat_fixed.append(whole - i)
        
    length = 2*(m - len(flat_fixed))
    pairs = []
    
    for i in range(len(interval)//2 + 1):
        pair = []
        
        pair.append(interval[i])
        pair.append(interval[len(interval) - i - 1])
        pairs.append(pair)
        
    poss = symmetric_pairs(length, pairs, pairs)
    
    for i in poss:
        i += opp_flat_fixed
        i.sort()
        
    proc = []
    
    for i in poss:
        proc = []
        
        while one_is_in(combos, i):
            for j in range(len(combos)):
                if set(combos[j]).issubset(set(i)):
                    subtract(combos[j], i)
                    proc.append(combos[j])
        
        if len(i) == 0:
            proc += all_fixed
            return proc
        
    return None
        
# Make proc for f(N*k+M, N) given procs for f(N*A+M, N) and f(N*B+M, N).
# ex_procs is tuple of two example f(N*k+M, N) Proc instances
# determine N, M, and ks
def mkproc(ex_procs):
    assert ex_procs[0].s == ex_procs[1].s
    N = ex_procs[0].s
    assert ex_procs[0].m % N == ex_procs[1].m % N
    M = ex_procs[0].m % N
    k0 = int((ex_procs[0].m - M) / N)
    k1 = int((ex_procs[1].m - M) / N)

    # Fit linear equations for each n=mk+b (num. and denom. separate)
    assert ex_procs[0].text == ex_procs[1].text
    formulae = []
    for i in range(len(ex_procs[0].numbers)):
        n0 = ex_procs[0].numbers[i]
        n1 = ex_procs[1].numbers[i]
        m_num = Fr(n1.numerator - n0.numerator, k1 - k0)
        b_num = Fr(n0.numerator * m_num.denominator - m_num.numerator * k0, m_num.denominator)
        m_denom = Fr(n1.denominator - n0.denominator, k1 - k0)
        b_denom = Fr(n0.denominator * m_denom.denominator - m_denom.numerator * k0, m_denom.denominator)

        # print("n", n0, n1)
        # print("k", k0, k1)
        # print(m_num, b_num)
        # print(m_denom, b_denom)
        # print()

        # Make coefficients integers
        if m_num.denominator != 1:
            d = m_num.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d
        if b_num.denominator != 1:
            d = b_num.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d
        if m_denom.denominator != 1:
            d = m_denom.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d
        if b_denom.denominator != 1:
            d = b_denom.denominator
            m_num *= d
            b_num *= d
            m_denom *= d
            b_denom *= d
        m_num = int(m_num)
        b_num = int(b_num)
        m_denom = int(m_denom)
        b_denom = int(b_denom)

        # divide any common multiple
        factor = min(val for val in [m_num, m_denom, b_num, b_denom] if val != 0)
        while factor > 1:
            if m_num % factor == m_denom % factor == b_num % factor == b_denom % factor == 0:
                m_num /= factor
                m_denom /= factor
                b_num /= factor
                b_denom /= factor
                break
            factor = min(val for val in [m_num, m_denom, b_num, b_denom, factor-1] if val != 0)

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
        return "k+%d" % b_num
    elif m_num == b_denom == 1 and m_denom == 0 and b_num < 0:  # k - b
        return "k-%d" % -b_num
    elif m_num == -b_denom == -1 and m_denom == 0 and b_num > 0:  # -k + b
        return "-k+%d" % b_num
    elif m_num == -b_denom == -1 and m_denom == 0 and b_num < 0:  # -k - b
        return "-k-%d" % -b_num
    elif m_num not in (0, 1, -1) and m_denom == b_num == 0 and b_denom == 1:  # mk
        return "%dk" % m_num
    elif m_num not in (0, 1, -1) and m_denom == 0 and b_num > 0 and b_denom == 1:  # mk + b
        return "%dk+%d" % (m_num, b_num)
    elif m_num not in (0, 1, -1) and m_denom == 0 and b_num < 0 and b_denom == 1:  # mk - b
        return "%dk-%d" % (m_num, -b_num)
    elif m_num == b_denom == 0 and m_denom == 1 and b_num != 0:  # b/k
        return "\\frac{%d}{k}" % b_num
    elif m_num == b_denom == 0 and m_denom > 0 and b_num != 0:  # b/mk
        return "\\frac{%d}{%dk}" % (b_num, m_denom)
    elif m_num == 1 and m_denom == 0 and b_num > 0 and b_denom > 0:  # (k + b0)/b1
        return "\\frac{k+%d}{%d}" % (b_num, b_denom)
    elif m_num == 1 and m_denom == 0 and b_num < 0 < b_denom:  # (k - b0)/b1
        return "\\frac{k-%d}{%d}" % (-b_num, b_denom)
    elif m_num == -1 and m_denom == 0 and b_num > 0 and b_denom > 0:  # (-k + b0)/b1
        return "\\frac{-k+%d}{%d}" % (b_num, b_denom)
    elif m_num == -1 and m_denom == 0 and b_num < 0 < b_denom:  # (-k - b0)/b1
        return "\\frac{-k-%d}{%d}" % (-b_num, b_denom)
    elif m_num not in (0, -1, 1) and m_denom == 0 and b_num > 0 and b_denom > 0:  # (mk + b0)/b1
        return "\\frac{%dk+%d}{%d}" % (m_num, b_num, b_denom)
    elif m_num not in (0, -1, 1) and m_denom == 0 and b_num < 0 < b_denom:  # (mk - b0)/b1
        return "\\frac{%dk-%d}{%d}" % (m_num, -b_num, b_denom)
    elif m_num != 0 and m_denom == 1 and b_num > 0 and b_denom == 0:  # m + b/k
        return "%d+\\frac{%d}{k}" % (m_num, b_num)
    elif m_num != 0 and m_denom == 1 and b_num < 0 and b_denom == 0:  # m - b/k
        return "%d-\\frac{%d}{k}" % (m_num, -b_num)
    elif m_num != 0 and m_denom > 1 and b_num > 0 and b_denom == 0:  # (m0k + b)/m1k
        return "\\frac{%dk+%d}{%dk}" % (m_num, b_num, m_denom)
    elif m_num != 0 and m_denom > 1 and b_num < 0 and b_denom == 0:  # (m0k - b)/m1k
        return "\\frac{%dk-%d}{%dk}" % (m_num, -b_num, m_denom)
    elif m_num == 0 and m_denom == 1 and b_num != 0 and b_denom > 0:  # b0/(k + b1)
        return "\\frac{%d}{k+%d}" % (b_num, b_denom)
    elif m_num == 0 and m_denom == 1 and b_num != 0 and b_denom < 0:  # b0/(k - b1)
        return "\\frac{%d}{k-%d}" % (b_num, -b_denom)
    elif m_num == 0 and m_denom > 1 and b_num != 0 and b_denom > 0:  # b0/(mk + b1)
        return "\\frac{%d}{%dk+%d}" % (b_num, m_denom, b_denom)
    elif m_num == 0 and m_denom > 1 and b_num != 0 and b_denom < 0:  # b0/(mk - b1)
        return "\\frac{%d}{%dk-%d}" % (b_num, m_denom, -b_denom)
    elif m_num == m_denom == 1 and b_num == 0 and b_denom > 0:  # k/(k + b)
        return "\\frac{k}{k+%d}" % b_denom
    elif m_num == m_denom == 1 and b_num == 0 and b_denom < 0:  # k/(k - b)
        return "\\frac{k}{k-%d}" % -b_denom
    elif m_num == -m_denom == -1 and b_num == 0 and b_denom > 0:  # -k/(k+b)
        return "\\frac{-k}{k+%d}" % b_denom
    elif m_num == -m_denom == -1 and b_num == 0 and b_denom < 0:  # -k/(k - b)
        return "\\frac{-k}{k-%d}" % -b_denom
    elif m_num == 1 and m_denom > 1 and b_num == 0 and b_denom > 0:  # k/(mk + b)
        return "\\frac{k}{%dk+%d}" % (m_denom, b_denom)
    elif m_num == 1 and m_denom > 1 and b_num == 0 and b_denom < 0:  # k/(mk - b)
        return "\\frac{k}{%dk-%d}" % (m_denom, -b_denom)
    elif m_num == -1 and m_denom > 1 and b_num == 0 and b_denom > 0:  # -k/(mk + b)
        return "\\frac{-k}{%dk+%d}" % (m_denom, b_denom)
    elif m_num == -1 and m_denom > 1 and b_num == 0 and b_denom < 0:  # -k/(mk - b)
        return "\\frac{-k}{%dk-%d}" % (m_denom, -b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num == 0 and b_denom > 0:  # m0k/(m1k + b)
        return "\\frac{%dk}{%dk+%d}" % (m_num, m_denom, b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num == 0 and b_denom < 0:  # m0k/(m1k - b)
        return "\\frac{%dk}{%dk-%d}" % (m_num, m_denom, -b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num > 0 and b_denom > 0:  # (m0k + b0)/(m1k + b1)
        return "\\frac{%dk+%d}{%dk+%d}" % (m_num, b_num, m_denom, b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num < 0 < b_denom:  # (m0k - b0)/(m1k + b1)
        return "\\frac{%dk-%d}{%dk+%d}" % (m_num, -b_num, m_denom, b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_denom < 0 < b_num:  # (m0k + b0)/(m1k - b1)
        return "\\frac{%dk+%d}{%dk-%d}" % (m_num, b_num, m_denom, -b_denom)
    elif m_num not in (0, 1, -1) and m_denom > 1 and b_num < 0 and b_denom < 0:  # (m0k - b0)/(m1k - b1)
        return "\\frac{%dk-%d}{%dk-%d}" % (m_num, -b_num, m_denom, -b_denom)


# input: file w/ LaTeX source code of proc w/ numerical values (e.g. 5, 4/5) OR string of source code
# instead of formulae
# output: Proc object
def parse_proc(proc_file=None, text=None):
    if proc_file is not None:
        infile = open(proc_file)
        text = infile.read()
    orig = text

    # Captures isolated numbers  and fractions.
    str_nums = re.findall(r'\d+[^\w}.\]]|\\frac{\d+}{\d+}', text)

    # Finds numbers in original text and determines what the fractions are.
    nums = []
    for s in str_nums:
        if '\\frac' in s:
            (num, denom) = tuple(re.findall(r'{(\d+)}', s))
            to_add = Fr(int(num), int(denom))
            nums.append(to_add)
            text = text.replace(s, "", 1)
        else:
            text = text.replace(s, s[-1], 1)
            nums.append(Fr(int(s[:-1])))

    # Replaces numbers in original with placeholders.
    for s in str_nums:
        orig = orig.replace(s, "%s") if '\\frac' in s else orig.replace(s, "%s"+s[-1])

    # Creates Proc object.
    proc = Proc(nums[0].numerator, nums[1].numerator, orig, nums)

    return proc

# takes changing components of a procedure and outputs full LaTeX
# idk may be useful at some point
def format_tex(subsection_heading, result_line, instructions):
    header = "\\documentclass[a4paper]{article}\n\n%% Language and font encodings\n" \
        "\\usepackage[english]{babel}\n\\usepackage[utf8x]{inputenc}\n\\usepackage[T1]{fontenc}\n\n" \
        "\\setlength{\\parindent}{4em}\n\\setlength{\\parskip}{1em}\n" \
        "\\renewcommand{\\baselinestretch}{1}\n\n%% Sets page size and margins\n" \
        "\\usepackage[a4paper,top=3cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}\n\n" \
        "\\begin{document}"
    footer = "\\end{document}"
    subsection_prefix = "\n\\subsection{%s}\n\\hspace{4ex}" % subsection_heading
    instruction_prefix = "\n\\noindent\n\\hspace{4ex}"

    body = "\n".join("%s\n%s" % (instruction_prefix, instruction) for instruction in instructions)
    text = "%s\n%s\n%s\n%s\n\n%s" % (header, subsection_prefix, result_line, body, footer)
    return text


# input: file with only "give students" lines
# output: text of full file
# use to prepare "give"-only files for use with the normal proc generation methods
def part_input(proc_file):
    infile = open(proc_file)
    text = infile.read()
    infile.close()

    # find:
    # no muffins for each piece size pair
    # min share size
    # m, s, f(m, s)

    divisions = {}  # str for size pair : number of muffins divided
    solution = float("inf")
    m = 0
    s = 0

    # record values for each "give" instruction
    give_strs = re.findall(r" ((\d+)(.*\[\d+:(\\frac{\d+}{\d+}|\d+)\])+)", text)
    for give in give_strs:
        no_recipients = int(give[1])
        s += no_recipients

        muffin_dists = re.findall(r"(\[\d+:(\\frac{\d+}{\d+}|\d+)\])", give[0])
        for dist in muffin_dists:
            no_shares = int(dist[0][1:dist[0].find(":")])
            share_size = Fr(*(int(x) for x in re.findall(r"\d+", dist[1]))) if dist[1][0] == "\\" else int(dist[1])

            # update divisions
            size_pair = "("
            if dist[1] == "1":
                size_pair += dist[1]
            else:
                num1 = share_size.numerator
                denom = share_size.denominator
                num2 = denom - num1
                size_pair += "\\frac{" + str(min(num1, num2)) + "}{" + str(denom) + "}," \
                             "\\frac{" + str(max(num1, num2)) + "}{" + str(denom) + "}"
            size_pair += ")"
            if size_pair in divisions:
                divisions[size_pair] += no_recipients * no_shares
            else:
                divisions[size_pair] = no_recipients * no_shares

            # update solution
            solution = min(solution, share_size)

    # find m
    give = give_strs[0]
    muffin_dists = re.findall(r"(\[\d+:(\\frac{\d+}{\d+}|\d+)\])", give[0])
    no_shares_list = [int(dist[0][1:dist[0].find(":")]) for dist in muffin_dists]
    share_size_list = [Fr(*(int(x) for x in re.findall(r"\d+", dist[1]))) if dist[1][0] == "\\" else int(dist[1])
                       for dist in muffin_dists]
    m_over_s = sum(no_shares_list[i] * share_size_list[i] for i in range(len(no_shares_list)))
    m = m_over_s * s

    # write header
    subsection_heading = "f(" + str(m) + "," + str(s) + ")"
    result_line = "$" + str(subsection_heading) + r" = \frac{" + str(solution.numerator)\
                  + "}{" + str(solution.denominator) + "}$"

    # make "divide" instruction for each division in dictionary
    instructions = []
    i = 1
    keys = list(divisions.keys())
    keys.sort()
    while keys[0] == "(1)":
        keys.append(keys[0])
        del keys[0]
    for key in keys:
        value = divisions[key]
        if key != "(1)":
            value = int(value/2)
        instructions.append(str(i) + ". $" + str(value) + "$ muffins divided $" + key + "$")
        i += 1

    # append "gives"
    for give in give_strs:
        instructions.append(str(i) + ". Give " + give[0] + "$")
        i += 1

    return format_tex(subsection_heading, result_line, instructions)


if __name__ == "__main__":
    main()
