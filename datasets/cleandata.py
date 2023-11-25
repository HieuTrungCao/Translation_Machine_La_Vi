import os
import io
import re

def check_double(src, trg):
    srcs = src.strip().split()
    trgs = trg.strip().split()

    length = min(len(srcs), len(trgs))

    sum = 0

    for i in range(length):
        if srcs[i] == trgs[i]:
            sum += 1
    return (sum / length) > 0.7

def clean_link(src, trg):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    
    src = re.sub(regex, "http", src)
    trg = re.sub(regex, "http", trg)

    return src, trg

def split_num(text):
    s = ""
    for i in range(len(text)):
        c = text[i]
        if c.isdigit():
            if i < len(text) - 1 and text[i + 1] != " ": 
                c = c + " "
            if i > 0 and s[-1] != " ":
                c = " " + c
        s = s + c
    return s

def split_nums(src, trg):
    src = split_num(src)
    trg = split_num(trg)
    
    return src, trg

def rm_unicode(src, trg):
    src = re.sub("&quot;", "\"", src)
    trg = re.sub("&quot;", "\"", trg)

    return src, trg

def split_char(text, ch):
    s = ""
    for i in range(len(text)):
        c = text[i]
        if c == ch:
            if i < len(text) - 1 and text[i + 1] == ch: 
                c = c + " "
        s = s + c
    return s

def split_chars(src, trg, char):
    src = split_char(src, char)
    trg = split_char(trg, char)

    return src, trg

def clean(path):

    sources = []
    targets = []

    max_len_src = 0
    max_len_trg = 0

    with io.open(path + ".lo", mode='r', encoding='utf-8') as src:
        with io.open(path + ".vi", mode='r', encoding='utf-8') as trg:
            for s, t in zip(src.readlines(), trg.readlines()):
                if not check_double(s, t):
                    s, t = clean_link(s, t)
                    s, t = split_nums(s, t)
                    s, t = rm_unicode(s, t)
                    s, t = split_chars(s, t, ".")
                    s, t = split_chars(s, t, "-")
                    s, t = split_chars(s, t, "_")
                    s, t = split_chars(s, t, "*")
                    s, t = split_chars(s, t, "!")
                    s, t = split_chars(s, t, "$")
                    s, t = split_chars(s, t, "%")
                    s, t = split_chars(s, t, "^")                 
                    s, t = split_chars(s, t, "(")
                    s, t = split_chars(s, t, ")")                 
                    s, t = split_chars(s, t, "{")
                    s, t = split_chars(s, t, "}")                 
                    s, t = split_chars(s, t, "[")                 
                    s, t = split_chars(s, t, "]")                 
                    s, t = split_chars(s, t, "\"")
                    s, t = split_chars(s, t, "\\")                 
                    s, t = split_chars(s, t, "/")                 
                    s, t = split_chars(s, t, ":")
                    s, t = split_chars(s, t, ",")                 
                    s, t = split_chars(s, t, "★")
                    max_len_src = max(max_len_src, len(s.split()))
                    max_len_trg = max(max_len_trg, len(t.split()))
                sources.append(s)
                targets.append(t)
    
    with io.open(path + ".lo", mode='w', encoding='utf-8') as src:
        src.writelines(sources)
    
    with io.open(path + ".vi", mode='w', encoding='utf-8') as trg:
        trg.writelines(targets)

    print("max src: ", max_len_src)
    print("max trg: ", max_len_trg)

# &quot;

# paths = ["data/la_vi/Dev/dev2023", "data/la_vi/Train/train2023", "data/la_vi/Test/test"]

# clean(paths[0])
# clean(paths[1])
# clean(paths[2])