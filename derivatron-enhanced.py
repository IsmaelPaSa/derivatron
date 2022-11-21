# -*- coding: utf-8 -*-

class Derivatron:
    def __init__(self):
        import math
        import random
        self.__math = math
        self.__random = random
        self.sym_var = ['x', 'y', 'z']
        self.sym_fun = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w']
        self.sym_xcp = ['!', '@', '#', '$', '%', '&', '[', ']', '{', '}', '|', ':', ';', ',', '<', '>', '=', '_', '~', "=", "/", "*"]
        self.sym_opt = {
            "constant": {
                "euler":"e"
            },
            "symbols": {
                "o_parenthese":"(",
                "c_parenthese":")",
                "equal":"=",
                "division":"/",
                "multiply":"*",
            },
            "logarithmic": {
            },
            "inv_trigonometric": {
            },
            "algebraic": {
                "plus":"+",
                "minus":"-"
            },
            "trigonometric": {
                "tan":"tan(",
                "sin":"sin(",
                "cos":"cos(",
                "sec":"sec(",
                "csc":"csc(",
                "cot":"cot("
            },
            "exponential": {
                "caret":"^",
            }
        }
        self.mode = "dot"
        self.dot_val = 1.0
        self.ran_val = [1.0, 1.0, 1.0]
        self.h_val = 0.001
        self.var = []
        self.der_var = ""
        self.fun = ""
        self.der = ""
        self._fun_det = []
        self._fun_bits = []
        self._fun_alg = []
        self._der_bits = []
        self._der_alg = []
        self.der_file = ""
        self.aprox_file = ""
        self._der_file_prefix = "_der"
        self._aprox_file_prefix = "_aprox"
        self._file_extension = ".dat"
    # - # - # - # - #
    def _getter(self, bit, opt="", der_var=""):
        c = "1"
        u = "0"
        n = "1"
        if not der_var:
            der_var = self.der_var
        try:
            caret = self.sym_opt["exponential"]["caret"]
            __caret = len(caret)
            __bit = len(bit)
            # c*v^n
            if opt == "":
                _var = bit.find(der_var)
                __var = len(der_var)
                if _var != -1:
                    u = der_var
                    # cv^n
                    if _var > 0:
                        c = bit[0:_var]
                    # v^n
                    else:
                        c = "1"
                    # v^n
                    if caret in bit:
                        n = bit[bit.find(caret)+__caret:__bit]
                    # v
                    else:
                        n = "1"
                # c
                else:
                    c = bit
            # c*e^u
            elif opt == self.sym_opt["constant"]["euler"]:
                euler = self.sym_opt["constant"]["euler"]
                _euler = bit.find(euler)
                __euler = len(euler)
                if _euler != -1:
                    # ce^u
                    if _euler > 0:
                        c = bit[0:_euler]
                    # e^u
                    else:
                        c = "1"
                    # e^u
                    if caret in bit:
                        u = bit[bit.find(caret)+__caret:__bit]
                    # e
                    else:
                        u = "1"
            # c*opt(u)^n
            elif opt in bit:
                c_parenthese = self.sym_opt["symbols"]["c_parenthese"]
                __c_parenthese = len(c_parenthese)
                _opt = bit.find(opt)
                __opt = len(opt)
                # copt(u)^n
                if _opt > 0:
                    c = bit[0:_opt]
                # opt(u)^n
                else:
                    c = "1"
                # opt(u)^n
                if caret in bit:
                    u = bit[_opt+__opt:bit.find(caret)-__c_parenthese]
                    n = bit[bit.find(caret)+__caret:__bit]
                # opt(u)
                else:
                    u = bit[_opt+__opt:__bit-__c_parenthese]
                    n = "1"
        except:
            pass
        try:
            c = str(float(c))
        except:
            pass
        try:
            u = str(float(u))
        except:
            pass
        try:
            n = str(float(n))
        except:
            pass
        return c, u, n
    def _extractor(self, fun=""):
        if not fun:
            fun = self.fun
        fun_bits = []
        fun_alg = []
        try:
            sym = []
            if fun.find(self.sym_opt["algebraic"]["plus"]) != 0 and fun.find(self.sym_opt["algebraic"]["minus"]) != 0:
                sym.append(self.sym_opt["algebraic"]["plus"])
            for i in range(len(fun)):
                if fun[i:i+1] == self.sym_opt["algebraic"]["plus"]:
                    sym.append(self.sym_opt["algebraic"]["plus"])
                if fun[i:i+1] == self.sym_opt["algebraic"]["minus"]:
                    sym.append(self.sym_opt["algebraic"]["minus"])
            fun_alg = sym
            _fun = fun
            for i in self.sym_opt["algebraic"]:
                _fun = _fun.replace(self.sym_opt["algebraic"][i], " ")
            fun_bits = _fun.split()
        except Exception as e:
            pass
        return fun_bits, fun_alg
    def _determinator(self, fun="", var=[]):
        if not fun:
            fun = self.fun
        if not var:
            var = self.var
        is_derivable = False
        has_logarithmic = False
        has_inv_trigonometric = False
        has_algebraic = False
        has_trigonometric = False
        has_exponential = False
        has_constant = False
        logarithmic = []
        inv_trigonometric = []
        algebraic = []
        trigonometric = []
        exponential = []
        constant = []
        try:
            # Check for constants
            for i in self.sym_opt["constant"]:
                if self.sym_opt["constant"][i] in fun:
                    constant.append(self.sym_opt["constant"][i])
                    has_constant = True
            # Check for algebraic
            for i in self.sym_opt["algebraic"]:
                if self.sym_opt["algebraic"][i] in fun:
                    algebraic.append(self.sym_opt["algebraic"][i])
                    has_algebraic = True
            # Check for exponential
            for i in self.sym_opt["exponential"]:
                if self.sym_opt["exponential"][i] in fun:
                    exponential.append(self.sym_opt["exponential"][i])
                    has_exponential = True
            # Check for trigonometric
            for i in self.sym_opt["trigonometric"]:
                if self.sym_opt["trigonometric"][i] in fun:
                    trigonometric.append(self.sym_opt["trigonometric"][i])
                    has_trigonometric = True
            # Has 2 variables
            if len(var) != 1:
                is_derivable = False
            else:
                self.der_var = self.var[0]
                is_derivable = True
        except:
            pass
        return {
            "is_derivable":is_derivable,
            "has_logarithmic":has_logarithmic,
            "has_inv_trigonometric":has_inv_trigonometric,
            "has_algebraic":has_algebraic,
            "has_trigonometric":has_trigonometric,
            "has_exponential":has_exponential,
            "has_constant":has_constant,
            "logarithmic":logarithmic,
            "inv_trigonometric":inv_trigonometric,
            "algebraic":algebraic,
            "trigonometric":trigonometric,
            "exponential":exponential,
            "constant":constant,
        }
    # - # - # - # - #
    def _evaluator(self, fun, var, delta):
        eva_fun = 0
        try:
            fun_bits, fun_alg = self._extractor(fun)
            fun_det = self._determinator(fun)
            sel = 0
            eva_bits = []
            for i in fun_bits:
                if fun_det["has_trigonometric"]:
                    for j in self.sym_opt["trigonometric"]:
                        if self.sym_opt["trigonometric"][j] in i:
                            c, u, n = self._getter(i, self.sym_opt["trigonometric"][j])
                            eva_u = self._evaluator(u, var, delta)
                            # var in u
                            _u = float(eva_u)
                            # sin(u)
                            if self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["sin"]:
                                _opt = self.__math.sin(_u)
                            # cos(u)
                            elif self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["cos"]:
                                _opt = self.__math.cos(_u)
                            # tan(u)
                            elif self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["tan"]:
                                _opt = self.__math.tan(_u)
                            # sec(u)
                            elif self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["sec"]:
                                _opt = 1 / self.__math.cos(_u)
                            # csc(u)
                            elif self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["csc"]:
                                _opt = 1 / self.__math.sin(_u)
                            # cot(u)
                            elif self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["cot"]:
                                _opt = 1 / self.__math.tan(_u)
                            else:
                                _opt = float(0)
                elif fun_det["has_constant"] and self.sym_opt["constant"]["euler"] in i:
                    c, u, n = self._getter(i, self.sym_opt["constant"]["euler"])
                    eva_u = self._evaluator(u, var, delta)
                    _u = float(eva_u)
                    _opt = self.__math.exp(_u)
                else:
                    c, u, n = self._getter(i)
                    if u == var:
                        _opt = float(delta)
                    else:
                        _opt = float(1)
                _c = float(c)
                _n = float(n)
                eva_bits.append(_c * (_opt ** _n))
                sel = sel + 1
            eva_fun = 0
            for i in range(len(fun_bits)):
                if fun_alg[i] == self.sym_opt["algebraic"]["plus"]:
                    eva_fun = eva_fun + eva_bits[i]
                elif fun_alg[i] == self.sym_opt["algebraic"]["minus"]:
                    eva_fun = eva_fun - eva_bits[i]
        except Exception as e:
            print("error", e)
            fun_det["is_derivable"] = False
            pass
        return eva_fun
    def _sym_match(self, op_one, op_two):
        if op_one == op_two:
            return self.sym_opt["algebraic"]["plus"]
        else:
            return self.sym_opt["algebraic"]["minus"]
    def _derivator(self, fun_bits=[], fun_alg=[], fun_det={}):
        if not fun_bits:
            fun_bits = self._fun_bits
        if not fun_det:
            fun_det = self._fun_det
        if not fun_alg:
            fun_alg = self._fun_alg
        der_bits = []
        der_alg = []
        try:
            sel = 0
            for i in fun_bits:
                if fun_det["has_trigonometric"]:
                    for j in self.sym_opt["trigonometric"]:
                        if self.sym_opt["trigonometric"][j] in i:
                            c, u, n = self._getter(i, self.sym_opt["trigonometric"][j])
                            u_bits, u_alg = self._extractor(u)
                            u_det = self._determinator(u)
                            du_bits, du_alg = self._derivator(u_bits, u_alg, u_det)
                            # c*opt(u)^n
                            if float(n) > float(1):
                                raise Exception("Aun no podemos resolver esto")
                            # c*opt(u)
                            else:
                                if len(du_bits) == 1 and du_bits[0] != str(float(0)):
                                    _c = float(c) * float(du_bits[0])
                                    _u = u
                                    _n = float(1)
                                    # csin(u)
                                    if self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["sin"]:
                                        _opt = self.sym_opt["trigonometric"]["cos"]
                                        _sym = self._sym_match(fun_alg[sel], self.sym_opt["algebraic"]["plus"])
                                    # ccos(u)
                                    elif self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["cos"]:
                                        _opt = self.sym_opt["trigonometric"]["sin"]
                                        _sym = self._sym_match(fun_alg[sel], self.sym_opt["algebraic"]["minus"])
                                    # ctan(u)
                                    elif self.sym_opt["trigonometric"][j] == self.sym_opt["trigonometric"]["tan"]:
                                        _opt = self.sym_opt["trigonometric"]["sec"]
                                        _sym = self._sym_match(fun_alg[sel], self.sym_opt["algebraic"]["plus"])
                                        _n = float(2)
                                    der_bits.append(str(_c) + _opt + _u + self.sym_opt["symbols"]["c_parenthese"] + self.sym_opt["exponential"]["caret"] + str(_n))
                                    der_alg.append(_sym)
                                else:
                                    der_bits.append("0")
                                    der_alg.append(fun_alg[sel])
                elif fun_det["has_constant"] and self.sym_opt["constant"]["euler"] in i:
                    c, u, n = self._getter(i, self.sym_opt["constant"]["euler"])
                    u_bits, u_alg = self._extractor(u)
                    u_det = self._determinator(u)
                    du_bits, du_alg = self._derivator(u_bits, u_alg, u_det)
                    # c*e^u
                    if len(du_bits) == 1 and du_bits[0] != str(float(0)):
                        _c = float(c) * float(du_bits[0])
                        _u = u
                        der_bits.append(str(_c) + self.sym_opt["constant"]["euler"] + self.sym_opt["exponential"]["caret"] + _u)
                        der_alg.append(fun_alg[sel])
                    else:
                        der_bits.append("0")
                        der_alg.append(fun_alg[sel])
                else:
                    c, u, n = self._getter(i)
                    u_bits, u_alg = self._extractor(u)
                    # c*u^n
                    if u != str(float(0)):
                        _c = float(c) * float(n)
                        _n = float(n) - float(1)
                        # c
                        if _n == float(0):
                            der_bits.append(_c)
                            der_alg.append(fun_alg[sel])
                        # c*u^n
                        else:
                            der_bits.append(str(_c) + u + self.sym_opt["exponential"]["caret"] + str(_n))
                            der_alg.append(fun_alg[sel])
                    else:
                        der_bits.append("0")
                        der_alg.append(fun_alg[sel])
                sel = sel + 1
        except Exception as e:
            fun_det["is_derivable"] = False
            pass
        return der_bits, der_alg
    # - # - # - # - #
    def set_fun(self, fun):
        try:
            fun = fun.replace(" ", "")
            for i in self.sym_var:
                if i in fun and i not in self.var:
                    self.var.append(i)
            for i in self.sym_xcp:
                fun = fun.replace(i, "")
            self.fun = fun
            self._fun_det = self._determinator()
            self._fun_bits, self._fun_alg = self._extractor()
            self.aprox_file = ""
            self.der_file = ""
            return 0
        except Exception as e:
            print(e)
            return 1
    def set_ran_val(self, r_min, r_max, steps):
        try:
            r_max = float(r_max)
            r_min = float(r_min)
            steps = float(steps)
            if steps <= 0:
                steps = 1.0
            if r_max == r_min:
                self.mode = "dot"
                self.dot_val = r_max
            else:
                self.mode = "ran"
                if r_min > r_max:
                    self.ran_val = [r_max, r_min, steps]
                else:
                    self.ran_val = [r_min, r_max, steps]
            self.aprox_file = ""
            self.der_file = ""
            return 0
        except:
            return 1
    def set_dot_val(self, dot):
        try:
            dot = float(dot)
            self.mode = "dot"
            self.dot_val = dot
            self.aprox_file = ""
            self.der_file = ""
            return 0
        except:
            return 1
    def set_h_val(self, h):
        try:
            self.h_val = float(h)
            self.aprox_file = ""
            self.der_file = ""
            return 0
        except:
            return 1
    # - # - # - # - #
    def aproximate(self, name=""):
        try:
            if name == "":
                name = str(self.__random.randint(1000, 9999))
            if self._fun_det["is_derivable"]:
                if not self.der:
                    self.derivate()
                # Filename
                der_file_name = name + self._der_file_prefix + self._file_extension
                aprox_file_name = name + self._aprox_file_prefix + self._file_extension
                # Range
                if self.mode == "dot":
                    ran = [self.dot_val, self.dot_val, float(1)]
                elif self.mode == "ran":
                    ran = self.ran_val
                else:
                    raise Exception("Modo aun no implementado")
                # Aprox
                if not self.h_val == float(0):
                    # Open file
                    f = open(aprox_file_name, "w")
                    i = ran[0]
                    stop = ran[1]
                    step = ran[2]
                    # loop
                    while i <= stop:
                        val = (self._evaluator(self.fun, self.der_var, self.h_val + float(i)) - self._evaluator(self.fun, self.der_var, float(i))) / self.h_val
                        f.write(str(i) + "\t" + str(val) + "\n")
                        i = i + step
                    self.aprox_file = aprox_file_name
                # Der
                else:
                    # Open file
                    f = open(der_file_name, "w")
                    i = ran[0]
                    stop = ran[1]
                    step = ran[2]
                    # loop
                    while i <= stop:
                        val = self._evaluator(self.der, self.der_var, float(i))
                        f.write(str(i) + "\t" + str(val) + "\n")
                        i = i + step
                    self.der_file = der_file_name
            else:
                raise Exception("Aun no podemos resolver esto")
            return 0
        except Exception as e:
            return 1
    def derivate(self):
        try:
            if not self.der:
                if self._fun_det["is_derivable"]:
                    self._der_bits, self._der_alg = self._derivator()
                    der = ""
                    for i in range(len(self._der_alg)):
                        der = der + self._der_alg[i] + str(self._der_bits[i])
                    self.der = der
                else:
                    raise Exception("Aun no podemos resolver esto")
            return 0
        except Exception as e:
            return 1


try:
    if __name__ == "__main__":
        # - # - # - # - #
        import sys
        usr_console = ""
        match sys.argv:
            case ['--console']:
                if sys.argv.find('--console') + 1 == 'internal':
                    usr_console = "internal"
                elif sys.argv.find('--console') + 1 == 'rich':
                    usr_console = "rich"
        # - # - # - # - #
        class Console:
            def __init__(self, console=""):
                if console == "":
                    console = "rich"
                try:
                    import readline
                    self.__readline = readline
                except:
                    pass
                import sys
                self.__sys = sys
                import os
                self.__os = os
                try:
                    if console == 'rich':
                        from rich.console import Console
                        self.console = Console()
                        self.name = "rich"
                    else:
                        raise Exception('Not rich')
                except:
                    class Console:
                        def __init__(self):
                            import datetime
                            self._datetime = datetime
                        def print(self, *args, **kargs):
                            print(*args)
                        def log(self, *args, **kargs):
                            print(self._datetime.datetime.now(), "|", *args)
                        def rule(self, *args, **kargs):
                            print(">>>", *args, "<<<")
                        def input(self, *args, **kargs):
                            return input(*args)
                    self.console = Console()
                    self.name = "internal"
            # - # - # - # - #
            def _exception(self, e):
                if str(e):
                    self.error()
                    self.error("):")
                    self.error("Algo ha salido mal")
                    self.error("Error:", e)
                    self.error()
                else:
                    self.console.print()
                self.__sys.exit(0)
            # - # - # - # - #
            def _print(self, *args, **kargs):
                style = ""
                justify = ""
                overflow = ""
                if "style" in kargs:
                    style = kargs["style"]
                if "justify" in kargs:
                    justify = kargs["justify"]
                if "overflow" in kargs:
                    overflow = kargs["overflow"]
                if "separator" in kargs:
                    separator = kargs["separator"]
                    fp = ""
                    for i in args:
                        fp = fp + separator + i
                    args = [fp[len(separator):len(fp)]]
                self.console.print(*args, style=style, justify=justify, overflow=overflow)
            def _log(self, *args, **kargs):
                style = ""
                justify = ""
                if "style" in kargs:
                    style = kargs["style"]
                if "justify" in kargs:
                    justify = kargs["justify"]
                if "separator" in kargs:
                    separator = kargs["separator"]
                    fp = ""
                    for i in args:
                        fp = fp + separator + i
                    args = [fp[len(separator):len(fp)]]
                self.console.log(*args, style=style, justify=justify)
            def _rule(self, *args, **kargs):
                style = ""
                separator = " "
                if "style" in kargs:
                    style = kargs["style"]
                if "separator" in kargs:
                    separator = kargs["separator"]
                fp = ""
                for i in args:
                    fp = fp + separator + i
                fp = fp[len(separator):len(fp)]
                self.console.rule(fp, style=style)
            def _input(self, *args, **kargs):
                separator = " "
                if "separator" in kargs:
                    separator = kargs["separator"]
                fp = ""
                for i in args:
                    fp = fp + separator + i
                fp = fp[len(separator):len(fp)]
                # return self.console.input(fp)
                result = input(fp).split(separator)
                while '' in result:
                    result.remove('')
                return result
            def _clear(self, *args, **kargs):
                match self.__os.name:
                    case "nt":
                        self.__os.system("cls")
                    case "posix":
                        self.__os.system("clear")
                    case _:
                        pass
            # - # - # - # - #
            def print(self, *args, **kargs):
                if not "style" in kargs:
                    kargs["style"] = "italic white"
                self._print(*args, **kargs)
            def log(self, *args, **kargs):
                if not "style" in kargs:
                    kargs["style"] = "italic cyan revese"
                self._log(*args, **kargs)
            def rule(self, *args, **kargs):
                if not "style" in kargs:
                    kargs["style"] = "bold italic white"
                self._rule(*args, **kargs)
            def error(self, *args, **kargs):
                if not "style" in kargs:
                    kargs["style"] = "italic red reverse"
                self._print(*args, **kargs)
            def warn(self, *args, **kargs):
                if not "style" in kargs:
                    kargs["style"] = "italic yellow reverse"
                self._print(*args, **kargs)
            def success(self, *args, **kargs):
                if not "style" in kargs:
                    kargs["style"] = "italic green reverse"
                self._print(*args, **kargs)
            def input(self, *args, **kargs):
                try:
                    if not "style" in kargs:
                        kargs["style"] = "italic"
                    return self._input(*args, **kargs)
                except KeyboardInterrupt as e:
                    self.console.print()
                    # self.__sys.exit(0)
                    return ""
                except Exception as e:
                    self._exception(e)
            def clear(self, *args, **kargs):
                self._clear(*args, **kargs)
        # - # - # - # - #
        import sys
        import random
        # - # - # - # - #
        console = Console(usr_console)
        # - # - # - # - #
        def _exception(e):
            console.error()
            console.error("):")
            console.error("Uh oh. Parece que ha ocurrido un error")
            console.error("Error en:", e)
            console.error()
            sys.exit(0)
        # - # - # - # - #
        app_splash = '\n ▓█████▄ ▓█████  ██▀███   ██▓ ██▒   █▓ ▄▄▄     ▄▄▄█████▓ ██▀███   ▒█████   ███▄    █ \n ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒▓██▒▓██░   █▒▒████▄   ▓  ██▒ ▓▒▓██ ▒ ██▒▒██▒  ██▒ ██ ▀█   █ \n ░██   █▌▒███   ▓██ ░▄█ ▒▒██▒ ▓██  █▒░▒██  ▀█▄ ▒ ▓██░ ▒░▓██ ░▄█ ▒▒██░  ██▒▓██  ▀█ ██▒\n ░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  ░██░  ▒██ █░░░██▄▄▄▄██░ ▓██▓ ░ ▒██▀▀█▄  ▒██   ██░▓██▒  ▐▌██▒\n ░▒████▓ ░▒████▒░██▓ ▒██▒░██░   ▒▀█░   ▓█   ▓██▒ ▒██▒ ░ ░██▓ ▒██▒░ ████▓▒░▒██░   ▓██░\n  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░░▓     ░ ▐░   ▒▒   ▓▒█░ ▒ ░░   ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ \n  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░ ▒ ░   ░ ░░    ▒   ▒▒ ░   ░      ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░\n  ░ ░  ░    ░     ░░   ░  ▒ ░     ░░    ░   ▒    ░        ░░   ░ ░ ░ ░ ▒     ░   ░ ░ \n    ░       ░  ░   ░      ░        ░        ░  ░           ░         ░ ░           ░ \n  ░                               ░                                                  \n'
        app_name = "Derivatron"
        app_edition = "Enhanced Edition"
        app_author = "Pasa-san"
        app_version = "2.4.1"
        app_codename = "Spice"
        app_copyright = "(c) 2022"
        # - # - # - # - #
        def _splash(mode=0, usr_color="white", usr_justify="left"):
            if mode < 0:
                mode = 10
                usr_justify = "center"
            if console.name == "rich":
                usr_style = "" + usr_color
                console.print("", app_splash, justify=usr_justify, style=usr_style)
                if mode >= 1:
                    console.print("", "[bold]" + app_name + "[/bold]", app_version, "[reverse]" + app_codename + "[/reverse]", justify=usr_justify, style=usr_style)
                    console.print("", "[italic]" + app_edition + "[/italic]", justify=usr_justify, style=usr_style)
                if mode >= 2:
                    console.print("", app_author + ",", "[italic]" + app_copyright + "[/italic]", justify=usr_justify, style=usr_style)
                if mode >= 1:
                    console.print()
            else:
                console.print("", app_splash, justify=usr_justify, style=usr_color)
                if mode >= 1:
                    console.print("", app_name, app_version, app_codename, justify=usr_justify, style=usr_color)
                if mode >= 2:
                    console.print("", app_edition, justify=usr_justify, style=usr_color)
                    console.print("", app_author, app_copyright, justify=usr_justify, style=usr_color)
                if mode >= 1:
                    console.print()
        # - # - # - # - #
        cli_name = "derivatron"
        cli_separator = ">"
        # - # - # - # - #
        loop = True
        idkwiad = 0
        # - # - # - # - #
        input_affirmative = ["s", "y"]
        input_negative = ["n"]
        # - # - # - # - #
        fun_dict = {}
        # - # - # - # - #
        _splash()
        # - # - # - # - #
        while loop:
            _input = console.input(cli_name + cli_separator + " ")
            if _input:
                # console.log(_input)
                match _input:
                    # - # - # - # - #
                    case ["exit", *any]:
                        sys.exit(0)
                    case ["clear", *any]:
                        console.clear()
                    case ["version", *any]:
                        _splash(-1, "red")
                    # - # - # - # - #
                    case ["help", *any]:
                        hs0 = "\t"
                        hs2 = "\t>"
                        hs3 = "\t -"
                        hs1 = " " + "--->" + "  "
                        console.print(hs2, "Opciones")
                        console.print(hs0, "help", hs1, "Muestra este menu de ayuda")
                        console.print(hs0, "version", hs1, "Muestra informacion sobre", cli_name)
                        console.print(hs0, "exit", hs1, "Salir de", cli_name)
                        console.print(hs0, "fun <id> <function>", hs1, "Establece una funcion")
                        console.print(hs0, "range <id> <min> <max> <steps>", hs1, "Establece un rango para evaluar la funcion")
                        console.print(hs0, "dot <id> <value>", hs1, "Establece un valor de x para evaluar la funcion")
                        console.print(hs0, "h <id> <value>", hs1, "Establece un valor de h para aproximar la funcion")
                        console.print(hs0, "der <id>", hs1, "Deriva la funcion")
                        console.print(hs0, "aprox <id>", hs1, "Deriva y evalua la funcion")
                        console.print(hs0, "list <id>", hs1, "Muestra informacion de la funcion")
                        console.print(hs0, "drop <id>", hs1, "Elimina una funcion")
                        console.print()
                        console.print(hs2, "Notas")
                        console.print(hs3, "'range' y 'dot' son incompatibles")
                        console.print(hs3, "'dot', 'range' y 'h' se establecen de manera global si no se establece <id>")
                        console.print(hs3, "'der', 'aprox' y 'list' se ejecutan de manera global si no se establece <id>")
                        console.print(hs3, "'der' solo deriva la funcion sin evaluar y con el valor 0 para 'h'")
                        console.print(hs3, "Si se establece el valor 0 para 'h', al ejecutar 'aprox' se evaluara la funcion con la derivada exacta")
                    # - # - # - # - #
                    case ["fun", *usr_input]:
                        try:
                            usr_fun_id = usr_input[0]
                            usr_fun = _input[2]
                            d_dummy = Derivatron()
                            status = d_dummy.set_fun(usr_fun)
                            if status != 0:
                                console.error(cli_name, "no logro agregar la funcion", usr_fun_id)
                            else:
                                if not usr_fun_id in fun_dict and usr_fun_id in d_dummy.sym_fun:
                                    fun_dict[usr_fun_id] = d_dummy
                                else:
                                    added = False
                                    for i in range(len(d_dummy.sym_fun)):
                                        fun_id = random.choice(d_dummy.sym_fun)
                                        if not fun_id == usr_fun_id and not fun_id in fun_dict:
                                            console.warn(usr_fun_id, "no se encuentra disponible, se utilizara", fun_id, "en su lugar")
                                            fun_dict[fun_id] = d_dummy
                                            added = True
                                            break
                                    if not added:
                                        console.error(usr_fun_id, "no se encuentra disponible y", cli_name, "no logro agregar la funcion")
                        except Exception as e:
                            console.warn("Uso: fun <id> <function>")
                    # - # - # - # - #
                    case ["range", *usr_input]:
                        try:
                            if fun_dict == {}: 
                                console.print("No hay funciones establecidas")
                            else:
                                _list = []
                                usr_steps = _input[-1]
                                usr_max = _input[-2]
                                usr_min = _input[-3]
                                if not len(usr_input) > 3:
                                    _list = fun_dict
                                else:
                                    usr_input.pop(-1)
                                    usr_input.pop(-1)
                                    usr_input.pop(-1)
                                    _list = usr_input
                                for key in _list:
                                    try:
                                        obj = fun_dict[key]
                                        status = obj.set_ran_val(usr_min, usr_max, usr_steps)
                                        if status != 0:
                                            console.error("El rango no puedo ser establecido a", key)
                                    except Exception as e:
                                        console.warn(key, "no existe en la lista")
                        except Exception as e:
                            console.warn("Uso: range <id> <min> <max> <steps>")
                    case ["dot", *usr_input]:
                        try:
                            if fun_dict == {}: 
                                console.print("No hay funciones establecidas")
                            else:
                                _list = []
                                usr_dot = _input[-1]
                                if not len(usr_input) > 1:
                                    _list = fun_dict
                                else:
                                    usr_input.pop(-1)
                                    _list = usr_input
                                for key in _list:
                                    try:
                                        obj = fun_dict[key]
                                        status = obj.set_dot_val(usr_dot)
                                        if status != 0:
                                            console.error(usr_dot, "no puedo ser establecido a", key)
                                    except Exception as e:
                                        console.warn(key, "no existe en la lista")
                        except Exception as e:
                            console.warn("Uso: dot <id> <value>")
                    case ["h", *usr_input]:
                        try:
                            if fun_dict == {}: 
                                console.print("No hay funciones establecidas")
                            else:
                                _list = []
                                usr_h = _input[-1]
                                if not len(usr_input) > 1:
                                    _list = fun_dict
                                else:
                                    usr_input.pop(-1)
                                    _list = usr_input
                                for key in _list:
                                    try:
                                        obj = fun_dict[key]
                                        status = obj.set_h_val(usr_h)
                                        if status != 0:
                                            console.error(usr_h, "no puedo ser establecido a", key)
                                    except Exception as e:
                                        console.warn(key, "no existe en la lista")
                        except Exception as e:
                            console.warn("Uso: h <id> <value>")
                    # - # - # - # - #
                    case ["der", *usr_input]:
                        try:
                            if fun_dict == {}: 
                                console.print("No hay funciones establecidas")
                            else:
                                _list = []
                                if not usr_input:
                                    _list = fun_dict
                                else:
                                    _list = usr_input
                                for key in _list:
                                    try:
                                        obj = fun_dict[key]
                                        status = obj.derivate()
                                        if status == 0:
                                            console.print("d" + key + "/" + "d" + obj.der_var, obj.sym_opt["symbols"]["equal"], obj.der)
                                        else:
                                            console.error(cli_name, "no logro derivar a", key)
                                    except Exception as e:
                                        console.warn(key, "no existe en la lista")    
                        except Exception as e:
                            console.warn("Uso: der <id>")
                    case ["aprox", *usr_input]:
                        try:
                            if fun_dict == {}: 
                                console.print("No hay funciones establecidas")
                            else:
                                _list = []
                                if not usr_input:
                                    _list = fun_dict
                                else:
                                    _list = usr_input
                                for key in _list:
                                    try:
                                        obj = fun_dict[key]
                                        status = obj.aproximate(key)
                                        if status == 0:
                                            if obj.der_file != "":
                                                console.success(cli_name, "logro derivar y evaluar a", key, "vease el archivo", obj.der_file)
                                            if obj.aprox_file != "":
                                                console.success(cli_name, "logro aproximar a", key, "vease el archivo", obj.aprox_file)
                                        else:
                                            console.error(cli_name, "no logro aproximar a", key)
                                    except Exception as e:
                                        console.warn(key, "no existe en la lista")    
                        except Exception as e:
                            console.warn("Uso: aprox <id>")
                    # - # - # - # - #
                    case ["list", *usr_input]:
                        try:
                            if fun_dict == {}: 
                                console.print("No hay funciones establecidas")
                            else:
                                _list = []
                                console.print("id\tfun\t\t\tvar\t\th\tmode\tran")
                                if not usr_input:
                                    _list = fun_dict
                                else:
                                    _list = usr_input
                                for key in _list:
                                    try:
                                        obj = fun_dict[key]
                                        var = ""
                                        fun = obj.fun
                                        for i in obj.var:
                                            var = var + " " + i
                                        h = obj.h_val
                                        mode = obj.mode
                                        eva = ""
                                        if obj.mode == "ran":
                                            eva = str(obj.ran_val[0]) + ", " + str(obj.ran_val[1]) + ", " + str(obj.ran_val[2]) 
                                        elif obj.mode == "dot":
                                            eva = obj.dot_val
                                        if len(fun) <= 5:
                                            _list_fun_t = 3
                                        elif len(fun) < 15:
                                            _list_fun_t = 2
                                        else:
                                            _list_fun_t = 1
                                        if len(var) < 3:
                                            _list_var_t = 2
                                        else:
                                            _list_var_t = 1
                                        console.print(key, "\t", fun, "\t" * _list_fun_t, var, "\t" * _list_var_t, h, "\t", mode, "\t", eva)
                                    except Exception as e:
                                        console.warn(key, "no existe en la lista")    
                        except Exception as e:
                            console.warn("Uso: list <id>")
                    # - # - # - # - #
                    case ["drop", *usr_input]:
                        try:
                            for key in usr_input:
                                if not key in fun_dict:
                                    console.warn(i, "No existe en la lista")
                                else:
                                    drop_input = console.input("Esta a punto de eliminar", key + ", ¿Continuar?", "[" + input_affirmative[0] + "/" + input_negative[0] + "]", "")
                                    if drop_input[0] in input_affirmative:
                                        fun_dict.pop(key)
                                    else:
                                        pass
                        except Exception as e:
                            console.warn("Uso: drop <id>")
                    # - # - # - # - #
                    case _:
                        console.warn(_input[0], "no es un comando valido o esta incompleto")   
            else:
                idkwiad = idkwiad + 1
                if idkwiad > 25:
                    console.print("Intenta escribir 'help' para obtener algo de ayuda!")
                    idkwiad = 0
except Exception as e:
    print()
    print("     ", "):")
    print("     ", "Ha ocurrido un error fatal")
    print("     ", e)
    print()
