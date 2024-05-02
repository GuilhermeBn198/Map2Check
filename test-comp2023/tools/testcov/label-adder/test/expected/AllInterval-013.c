// This file is part of the SV-Benchmarks collection of verification tasks:
// https://github.com/sosy-lab/sv-benchmarks
//
// SPDX-FileCopyrightText: 2016 Gilles Audemard
// SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
// SPDX-FileCopyrightText: 2020 The SV-Benchmarks Community
//
// SPDX-License-Identifier: MIT

extern void abort(void) __attribute__((__nothrow__, __leaf__))
__attribute__((__noreturn__));
extern void __assert_fail(const char *, const char *, unsigned int,
                          const char *) __attribute__((__nothrow__, __leaf__))
__attribute__((__noreturn__));
int __VERIFIER_nondet_int();
void reach_error() {
Goal_1:;

  __assert_fail("0", "AllInterval-013.c", 5, "reach_error");
  Goal_2:;
  
}
void assume(int cond) {
Goal_3:;

  if (!cond)
    {
    Goal_5:;
    abort();
    }
    
    Goal_4:;
    
}
int main() {
Goal_6:;

  int cond0;
  int dummy = 0;
  int N;
  int var0;
  var0 = __VERIFIER_nondet_int();
  assume(var0 >= 0);
  assume(var0 <= 12);
  int var1;
  var1 = __VERIFIER_nondet_int();
  assume(var1 >= 0);
  assume(var1 <= 12);
  int var2;
  var2 = __VERIFIER_nondet_int();
  assume(var2 >= 0);
  assume(var2 <= 12);
  int var3;
  var3 = __VERIFIER_nondet_int();
  assume(var3 >= 0);
  assume(var3 <= 12);
  int var4;
  var4 = __VERIFIER_nondet_int();
  assume(var4 >= 0);
  assume(var4 <= 12);
  int var5;
  var5 = __VERIFIER_nondet_int();
  assume(var5 >= 0);
  assume(var5 <= 12);
  int var6;
  var6 = __VERIFIER_nondet_int();
  assume(var6 >= 0);
  assume(var6 <= 12);
  int var7;
  var7 = __VERIFIER_nondet_int();
  assume(var7 >= 0);
  assume(var7 <= 12);
  int var8;
  var8 = __VERIFIER_nondet_int();
  assume(var8 >= 0);
  assume(var8 <= 12);
  int var9;
  var9 = __VERIFIER_nondet_int();
  assume(var9 >= 0);
  assume(var9 <= 12);
  int var10;
  var10 = __VERIFIER_nondet_int();
  assume(var10 >= 0);
  assume(var10 <= 12);
  int var11;
  var11 = __VERIFIER_nondet_int();
  assume(var11 >= 0);
  assume(var11 <= 12);
  int var12;
  var12 = __VERIFIER_nondet_int();
  assume(var12 >= 0);
  assume(var12 <= 12);
  int var13;
  var13 = __VERIFIER_nondet_int();
  assume(var13 >= 1);
  assume(var13 <= 12);
  int var14;
  var14 = __VERIFIER_nondet_int();
  assume(var14 >= 1);
  assume(var14 <= 12);
  int var15;
  var15 = __VERIFIER_nondet_int();
  assume(var15 >= 1);
  assume(var15 <= 12);
  int var16;
  var16 = __VERIFIER_nondet_int();
  assume(var16 >= 1);
  assume(var16 <= 12);
  int var17;
  var17 = __VERIFIER_nondet_int();
  assume(var17 >= 1);
  assume(var17 <= 12);
  int var18;
  var18 = __VERIFIER_nondet_int();
  assume(var18 >= 1);
  assume(var18 <= 12);
  int var19;
  var19 = __VERIFIER_nondet_int();
  assume(var19 >= 1);
  assume(var19 <= 12);
  int var20;
  var20 = __VERIFIER_nondet_int();
  assume(var20 >= 1);
  assume(var20 <= 12);
  int var21;
  var21 = __VERIFIER_nondet_int();
  assume(var21 >= 1);
  assume(var21 <= 12);
  int var22;
  var22 = __VERIFIER_nondet_int();
  assume(var22 >= 1);
  assume(var22 <= 12);
  int var23;
  var23 = __VERIFIER_nondet_int();
  assume(var23 >= 1);
  assume(var23 <= 12);
  int var24;
  var24 = __VERIFIER_nondet_int();
  assume(var24 >= 1);
  assume(var24 <= 12);
  int myvar0 = 1;
  assume(var0 != var1);
  assume(var0 != var2);
  assume(var0 != var3);
  assume(var0 != var4);
  assume(var0 != var5);
  assume(var0 != var6);
  assume(var0 != var7);
  assume(var0 != var8);
  assume(var0 != var9);
  assume(var0 != var10);
  assume(var0 != var11);
  assume(var0 != var12);
  assume(var1 != var2);
  assume(var1 != var3);
  assume(var1 != var4);
  assume(var1 != var5);
  assume(var1 != var6);
  assume(var1 != var7);
  assume(var1 != var8);
  assume(var1 != var9);
  assume(var1 != var10);
  assume(var1 != var11);
  assume(var1 != var12);
  assume(var2 != var3);
  assume(var2 != var4);
  assume(var2 != var5);
  assume(var2 != var6);
  assume(var2 != var7);
  assume(var2 != var8);
  assume(var2 != var9);
  assume(var2 != var10);
  assume(var2 != var11);
  assume(var2 != var12);
  assume(var3 != var4);
  assume(var3 != var5);
  assume(var3 != var6);
  assume(var3 != var7);
  assume(var3 != var8);
  assume(var3 != var9);
  assume(var3 != var10);
  assume(var3 != var11);
  assume(var3 != var12);
  assume(var4 != var5);
  assume(var4 != var6);
  assume(var4 != var7);
  assume(var4 != var8);
  assume(var4 != var9);
  assume(var4 != var10);
  assume(var4 != var11);
  assume(var4 != var12);
  assume(var5 != var6);
  assume(var5 != var7);
  assume(var5 != var8);
  assume(var5 != var9);
  assume(var5 != var10);
  assume(var5 != var11);
  assume(var5 != var12);
  assume(var6 != var7);
  assume(var6 != var8);
  assume(var6 != var9);
  assume(var6 != var10);
  assume(var6 != var11);
  assume(var6 != var12);
  assume(var7 != var8);
  assume(var7 != var9);
  assume(var7 != var10);
  assume(var7 != var11);
  assume(var7 != var12);
  assume(var8 != var9);
  assume(var8 != var10);
  assume(var8 != var11);
  assume(var8 != var12);
  assume(var9 != var10);
  assume(var9 != var11);
  assume(var9 != var12);
  assume(var10 != var11);
  assume(var10 != var12);
  assume(var11 != var12);
  assume(var13 != var14);
  assume(var13 != var15);
  assume(var13 != var16);
  assume(var13 != var17);
  assume(var13 != var18);
  assume(var13 != var19);
  assume(var13 != var20);
  assume(var13 != var21);
  assume(var13 != var22);
  assume(var13 != var23);
  assume(var13 != var24);
  assume(var14 != var15);
  assume(var14 != var16);
  assume(var14 != var17);
  assume(var14 != var18);
  assume(var14 != var19);
  assume(var14 != var20);
  assume(var14 != var21);
  assume(var14 != var22);
  assume(var14 != var23);
  assume(var14 != var24);
  assume(var15 != var16);
  assume(var15 != var17);
  assume(var15 != var18);
  assume(var15 != var19);
  assume(var15 != var20);
  assume(var15 != var21);
  assume(var15 != var22);
  assume(var15 != var23);
  assume(var15 != var24);
  assume(var16 != var17);
  assume(var16 != var18);
  assume(var16 != var19);
  assume(var16 != var20);
  assume(var16 != var21);
  assume(var16 != var22);
  assume(var16 != var23);
  assume(var16 != var24);
  assume(var17 != var18);
  assume(var17 != var19);
  assume(var17 != var20);
  assume(var17 != var21);
  assume(var17 != var22);
  assume(var17 != var23);
  assume(var17 != var24);
  assume(var18 != var19);
  assume(var18 != var20);
  assume(var18 != var21);
  assume(var18 != var22);
  assume(var18 != var23);
  assume(var18 != var24);
  assume(var19 != var20);
  assume(var19 != var21);
  assume(var19 != var22);
  assume(var19 != var23);
  assume(var19 != var24);
  assume(var20 != var21);
  assume(var20 != var22);
  assume(var20 != var23);
  assume(var20 != var24);
  assume(var21 != var22);
  assume(var21 != var23);
  assume(var21 != var24);
  assume(var22 != var23);
  assume(var22 != var24);
  assume(var23 != var24);
  int var_for_abs;
  var_for_abs = var0 - var1;
   if((var_for_abs >= 0) ){
  Goal_8:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_9:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var13 == var_for_abs);
  var_for_abs = var1 - var2;
   if((var_for_abs >= 0) ){
  Goal_10:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_11:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var14 == var_for_abs);
  var_for_abs = var2 - var3;
   if((var_for_abs >= 0) ){
  Goal_12:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_13:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var15 == var_for_abs);
  var_for_abs = var3 - var4;
   if((var_for_abs >= 0) ){
  Goal_14:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_15:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var16 == var_for_abs);
  var_for_abs = var4 - var5;
   if((var_for_abs >= 0) ){
  Goal_16:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_17:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var17 == var_for_abs);
  var_for_abs = var5 - var6;
   if((var_for_abs >= 0) ){
  Goal_18:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_19:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var18 == var_for_abs);
  var_for_abs = var6 - var7;
   if((var_for_abs >= 0) ){
  Goal_20:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_21:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var19 == var_for_abs);
  var_for_abs = var7 - var8;
   if((var_for_abs >= 0) ){
  Goal_22:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_23:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var20 == var_for_abs);
  var_for_abs = var8 - var9;
   if((var_for_abs >= 0) ){
  Goal_24:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_25:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var21 == var_for_abs);
  var_for_abs = var9 - var10;
   if((var_for_abs >= 0) ){
  Goal_26:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_27:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var22 == var_for_abs);
  var_for_abs = var10 - var11;
   if((var_for_abs >= 0) ){
  Goal_28:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_29:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var23 == var_for_abs);
  var_for_abs = var11 - var12;
   if((var_for_abs >= 0) ){
  Goal_30:;
  var_for_abs = var_for_abs ;
  }else{
  Goal_31:;
  var_for_abs = var_for_abs * (-1);
  }
  assume(var24 == var_for_abs);
  reach_error();
  return 0; /* 0 x[0]1 x[1]2 x[2]3 x[3]4 x[4]5 x[5]6 x[6]7 x[7]8 x[8]9 x[9]10
               x[10]11 x[11]12 x[12]13 y[0]14 y[1]15 y[2]16 y[3]17 y[4]18 y[5]19
               y[6]20 y[7]21 y[8]22 y[9]23 y[10]24 y[11] */
               Goal_7:;
               
}