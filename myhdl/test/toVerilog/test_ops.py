import os
path = os.path
import unittest
from unittest import TestCase
import random
from random import randrange
random.seed(2)

from myhdl import *


def binaryOps(
              Bitand,
              Bitor,
              Bitxor,
              FloorDiv,
              LeftShift,
              Mod,
              Mul,
              RightShift,
              Sub,
              Sum,
              EQ,
              NE,
              LT,
              GT,
              LE,
              GE,
              And,
              Or,
              left, right):
    while 1:
        yield left, right
        Bitand.next = left & right
        Bitor.next = left | right
        Bitxor.next = left ^ right
        if right != 0:
            FloorDiv.next = left // right
        if left < 256 and right < 40:
            LeftShift.next = left << right
        if right != 0:
            Mod.next = left % right
        Mul.next = left * right
        RightShift.next = left >> right
        if left >= right:
            Sub.next = left - right
        Sum.next = left + right
        EQ.next = left == right
        NE.next = left != right
        LT.next = left < right
        GT.next = left > right
        LE.next = left <= right
        GE.next = left >= right
        And.next = bool(left and right)
        Or.next = bool(left or right)



def binaryOps_v(
                Bitand,
                Bitor,
                Bitxor,
                FloorDiv,
                LeftShift,
                Mod,
                Mul,
                RightShift,
                Sub,
                Sum,
                EQ,
                NE,
                LT,
                GT,
                LE,
                GE,
                And,
                Or,
                left, right):
    objfile = "binops.o"
    analyze_cmd = "iverilog -o %s binops.v tb_binops.v" % objfile
    simulate_cmd = "vvp -m ../../../cosimulation/icarus/myhdl.vpi %s" % objfile
    if path.exists(objfile):
        os.remove(objfile)
        os.system(analyze_cmd)
    return Cosimulation(simulate_cmd, **locals())

class TestBinaryOps(TestCase):

    def binaryBench(self, m, n):

        M = 2**m
        N = 2**n

        left = Signal(intbv(0)[m:])
        right = Signal(intbv(0)[n:])
        print max(m, n)
        Bitand = Signal(intbv(0)[max(m, n):])
        Bitand_v = Signal(intbv(0)[max(m, n):])
        Bitor = Signal(intbv(0)[max(m, n):])
        Bitor_v = Signal(intbv(0)[max(m, n):])
        Bitxor = Signal(intbv(0)[max(m, n):])
        Bitxor_v = Signal(intbv(0)[max(m, n):])
        FloorDiv = Signal(intbv(0)[m:])
        FloorDiv_v = Signal(intbv(0)[m:])
        LeftShift = Signal(intbv(0)[64:])
        LeftShift_v = Signal(intbv(0)[64:])
        Mod = Signal(intbv(0)[m:])
        Mod_v = Signal(intbv(0)[m:])
        Mul = Signal(intbv(0)[m+n:])
        Mul_v = Signal(intbv(0)[m+n:])
        RightShift = Signal(intbv(0)[m:])
        RightShift_v = Signal(intbv(0)[m:])
        Sub = Signal(intbv(0)[max(m, n):])
        Sub_v = Signal(intbv(0)[max(m, n):])
        Sum = Signal(intbv(0)[max(m, n)+1:])
        Sum_v = Signal(intbv(0)[max(m, n)+1:])
        EQ, NE, LT, GT, LE, GE = [Signal(bool()) for i in range(6)]
        EQ_v, NE_v, LT_v, GT_v, LE_v, GE_v = [Signal(bool()) for i in range(6)]
        And, Or = [Signal(bool()) for i in range(2)]
        And_v, Or_v, = [Signal(bool()) for i in range(2)]

        binops = toVerilog(binaryOps,
                           Bitand,
                           Bitor,
                           Bitxor,
                           FloorDiv,
                           LeftShift,
                           Mod,
                           Mul,
                           RightShift,
                           Sub,
                           Sum,
                           EQ,
                           NE,
                           LT,
                           GT,
                           LE,
                           GE,
                           And,
                           Or,
                           left, right)
        binops_v = binaryOps_v(
                               Bitand_v,
                               Bitor_v,
                               Bitxor_v,
                               FloorDiv_v,
                               LeftShift_v,
                               Mod_v,
                               Mul_v,
                               RightShift_v,
                               Sub_v,
                               Sum_v,
                               EQ_v,
                               NE_v,
                               LT_v,
                               GT_v,
                               LE_v,
                               GE_v,
                               And_v,
                               Or_v,
                               left, right)

        def stimulus():
            for i in range(min(M, N)):
                # print i
                left.next = intbv(i)
                right.next = intbv(i)
                yield delay(10)
            for i in range(100):
                left.next = randrange(M)
                right.next = randrange(N)
                yield delay(10)
            for j, k in ((0, 0), (0, N-1), (M-1, 0), (M-1, N-1)):
                left.next = j
                right.next = k
                yield delay(10)

        def check():
            while 1:
                yield left, right
                yield delay(1)
                # print "%s %s %s %s" % (left, right, Or, Or_v)
                self.assertEqual(Bitand, Bitand_v)
                self.assertEqual(Bitor, Bitor_v)
                self.assertEqual(Bitxor, Bitxor_v)
                self.assertEqual(FloorDiv, FloorDiv_v)
                self.assertEqual(LeftShift, LeftShift_v)
                self.assertEqual(Mod, Mod_v)
                self.assertEqual(Mul, Mul_v)
                self.assertEqual(RightShift, RightShift_v)
                self.assertEqual(Sub, Sub_v)
                self.assertEqual(Sum, Sum_v)
                self.assertEqual(EQ, EQ_v)
                self.assertEqual(NE, NE_v)
                self.assertEqual(LT, LT_v)
                self.assertEqual(GT, GT_v)
                self.assertEqual(LE, LE_v)
                self.assertEqual(GE, GE_v)
                self.assertEqual(And, And_v)
                self.assertEqual(Or, Or_v)

        return binops, binops_v, stimulus(), check()

        def testBinaryOps(self):
            for m, n in ((4, 4,), (5, 3), (2, 6), (8, 7)):
                sim = self.binaryBench(m, n)
                Simulation(sim).run()



def multiOps(
              Bitand,
              Bitor,
              Bitxor,
              And,
              Or,
              argm, argn, argp):
    while 1:
        yield argm, argn, argp
        Bitand.next = argm & argn & argp
        Bitor.next = argm | argn | argp
        Bitxor.next = argm ^ argn ^ argp
        And.next = bool(argm and argn and argp)
        Or.next = bool(argm and argn and argp)


def multiOps_v(
                Bitand,
                Bitor,
                Bitxor,
                And,
                Or,
                argm, argn, argp):

    objfile = "multiops.o"
    analyze_cmd = "iverilog -o %s multiops.v tb_multiops.v" % objfile
    simulate_cmd = "vvp -m ../../../cosimulation/icarus/myhdl.vpi %s" % objfile
    if path.exists(objfile):
        os.remove(objfile)
    os.system(analyze_cmd)
    return Cosimulation(simulate_cmd, **locals())

class TestMultiOps(TestCase):

    def multiBench(self, m, n, p):

        M = 2**m
        N = 2**n
        P = 2**p

        argm = Signal(intbv(0)[m:])
        argn = Signal(intbv(0)[n:])
        argp = Signal(intbv(0)[p:])
        Bitand = Signal(intbv(0)[max(m, n, p):])
        Bitand_v = Signal(intbv(0)[max(m, n, p):])
        Bitor = Signal(intbv(0)[max(m, n, p):])
        Bitor_v = Signal(intbv(0)[max(m, n, p):])
        Bitxor = Signal(intbv(0)[max(m, n, p):])
        Bitxor_v = Signal(intbv(0)[max(m, n, p):])
        And, Or = [Signal(bool()) for i in range(2)]
        And_v, Or_v, = [Signal(bool()) for i in range(2)]

        multiops = toVerilog(multiOps,
                           Bitand,
                           Bitor,
                           Bitxor,
                           And,
                           Or,
                           argm, argn, argp)
        multiops_v = multiOps_v(
                               Bitand_v,
                               Bitor_v,
                               Bitxor_v,
                               And_v,
                               Or_v,
                               argm, argn, argp)

        def stimulus():
            for i in range(min(M, N, P)):
                # print i
                argm.next = intbv(i)
                argn.next = intbv(i)
                argp.next = intbv(i)
                yield delay(10)
            for i in range(100):
                argm.next = randrange(M)
                argn.next = randrange(N)
                argp.next = randrange(P)
                yield delay(10)
            for j, k, l in ((0, 0, 0),   (0, 0, P-1), (0, N-1, P-1),
                            (M-1, 0, 0),  (M-1, 0, P-1), (M-1, N-1, 0),
                            (0, N-1, 0), (M-1, N-1, P-1)):
                argm.next = j
                argn.next = k
                argp.next = l
                yield delay(10)

        def check():
            while 1:
                yield argm, argn, argp
                yield delay(1)
                # print "%s %s %s %s %s" % (argm, argn, argp, Bitxor, Bitxor_v)
                self.assertEqual(Bitand, Bitand_v)
                self.assertEqual(Bitor, Bitor_v)
                self.assertEqual(Bitxor, Bitxor_v)
                self.assertEqual(And, And_v)
                self.assertEqual(Or, Or_v)

        return multiops, multiops_v, stimulus(), check()

    def testMultiOps(self):
        for m, n, p in ((4, 4, 4,), (5, 3, 2), (3, 4, 6), (3, 7, 4)):
            sim = self.multiBench(m, n, p)
            Simulation(sim).run()



def unaryOps(
             Not,
             Invert,
             arg):
    while 1:
        yield arg
        Not.next = not arg
        Invert.next = ~arg

def unaryOps_v(
               Not,
               Invert,
               arg):
    objfile = "unaryops.o"
    analyze_cmd = "iverilog -o %s unaryops.v tb_unaryops.v" % objfile
    simulate_cmd = "vvp -m ../../../cosimulation/icarus/myhdl.vpi %s" % objfile
    if path.exists(objfile):
        os.remove(objfile)
    os.system(analyze_cmd)
    return Cosimulation(simulate_cmd, **locals())



class TestUnaryOps(TestCase):

    def unaryBench(self, m):

        M = 2**m

        arg = Signal(intbv(0)[m:])
        Not = Signal(bool(0))
        Not_v = Signal(bool(0))
        Invert = Signal(intbv(0)[m:])
        Invert_v = Signal(intbv(0)[m:])

        unaryops = toVerilog(unaryOps,
                             Not,
                             Invert,
                             arg)
        unaryops_v = unaryOps_v(
                                Not_v,
                                Invert_v,
                                arg)

        def stimulus():
            for i in range(M):
                arg.next = intbv(i)
                yield delay(10)
            for i in range(100):
                arg.next = randrange(M)
                yield delay(10)
            raise StopSimulation

        def check():
            while 1:
                yield arg
                self.assertEqual(Not, Not_v)
                self.assertEqual(Invert, Invert_v)

        return unaryops, unaryops_v, stimulus(), check()

    def testUnaryOps(self):
        for m in (4, 7):
            sim = self.unaryBench(m)
            Simulation(sim).run()


if __name__ == '__main__':
    unittest.main()


