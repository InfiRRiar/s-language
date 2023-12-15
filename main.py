from sly import Lexer, Parser
import re


class Lex(Lexer):
    tokens = {STRING, INT, S_INFO, TYPE}

    ignore = "\n "
    literals = {"(", ")", "groups", "students"}

    @_(r';.*\n')
    def ignore_comment(self, t):
        self.lineno += 1

    @_(r'\d+')
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'groups|students')
    def TYPE(self, t):
        return t

    @_(r'name|group|age')
    def S_INFO(self, t):
        return t

    STRING = r'[\w\-]+'


class Parse(Parser):
    debugfile = "output/log.out"
    tokens = Lex.tokens

    @_('"(" content content ")"')
    def contents(self, p):
        for i in p.content1.keys():
            p.content0[i] = p.content1[i]
        return p.content0

    @_('"(" s_key s_key s_key ")"')
    def student(self, p):
        a = dict()
        a[p.s_key0[0]] = p.s_key0[1][1]
        a[p.s_key1[0]] = p.s_key1[1][1]
        a[p.s_key2[0]] = p.s_key2[1][1]
        return a

    @_("student")
    def students(self, p):
        return [p.student]

    @_("students student")
    def students(self, p):
        p.students.append(p.student)
        return p.students

    @_('S_INFO "(" line ")"')
    def s_key(self, p):
        return [p.S_INFO, p.line]

    @_('lines line')
    def lines(self, p):
        p.lines.append(p.line[1])
        return p.lines

    @_('line')
    def lines(self, p):
        return [p.line[0]]

    @_('STRING',
       'INT')
    def line(self, p):
        return p

    @_('TYPE "(" students ")"')
    def content(self, p):
        a = dict()
        a[p.TYPE] = p.students
        return a

    @_('TYPE "(" lines ")"')
    def content(self, p):
        a = dict()
        a[p.TYPE] = p.lines
        return a


if __name__ == '__main__':
    name = "1"
    data = open(f"input/tests/{name}.txt", 'r').read()
    lexer = Lex()
    parser = Parse()
    result = str(parser.parse(lexer.tokenize(data)))
    result = result.replace("'", '"')
    file = open(f"output/tests/{name}.json", "w")
    file.write(str(result))
    print(result)
