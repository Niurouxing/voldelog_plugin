
#/ while True:
#/     print("hello world")

#/ `timescale 1ns / 1ps
#/ module ADD_TRN_TCPL_WRP_TCPL_d1_rst_n #(
#/     parameter dwt_in_1   = 1,
#/     parameter signed frac_in_1  = 0,
#/     parameter sign_in_1  = 1,
#/     parameter dwt_in_2   = 3,
#/     parameter signed frac_in_2  = 0,
#/     parameter sign_in_2  = 1,
#/     parameter dwt_out    = 3,
#/     parameter signed frac_out   = 0
#/     // sign_out = (sign_in_1 || sign_in_2)
#/ )(
#/     op_in_1, op_in_2
#/     , clk
#/     , rst_n
#/     , op_out
#/ );
#/ 
#/ //======== Input Ports ========//
#/ input [dwt_in_1-1:0] op_in_1;
#/ input [dwt_in_2-1:0] op_in_2;
#/ input clk;
#/ input rst_n;
#/ 
#/ //======== Output Ports ========//
#/ output [dwt_out-1:0] op_out;
#/ 
#/ //======== Pre-Add Fixed Point Match ========//
#/ localparam signed LSB_FIX = (frac_in_1 > frac_in_2)?-frac_in_1:-frac_in_2;
#/ localparam signed MSB_FIX = (dwt_in_1-frac_in_1 > dwt_in_2-frac_in_2)?(dwt_in_1-frac_in_1-1+1):(dwt_in_2-frac_in_2-1+1); // +1 is in case of sign bit
#/ 
#/ localparam dwt_fix = MSB_FIX - LSB_FIX + 1;
#/ localparam signed frac_fix = -LSB_FIX;
#/ localparam sign_out = sign_in_1 || sign_in_2;
#/ 
#/ wire [dwt_fix-1:0] op_in_1_fix, op_in_2_fix;
#/ 
#/ // INST
#/ FxP_Match_TRN_TCPL_WRP_TCPL#(
#/   .dwt_in(dwt_in_1),
#/   .frac_in(frac_in_1),
#/   .sign_in(sign_in_1),
#/   .dwt_out(dwt_fix),
#/   .frac_out(frac_fix),
#/   .sign_out(sign_out))
#/  FxP_Match_TRN_TCPL_WRP_TCPL_u1 (
#/   .op_in(op_in_1),
#/   .op_out(op_in_1_fix)
#/ );
#/ // END of INST
#/ 
#/ // INST
#/ FxP_Match_TRN_TCPL_WRP_TCPL#(
#/   .dwt_in(dwt_in_2),
#/   .frac_in(frac_in_2),
#/   .sign_in(sign_in_2),
#/   .dwt_out(dwt_fix),
#/   .frac_out(frac_fix),
#/   .sign_out(sign_out))
#/  FxP_Match_TRN_TCPL_WRP_TCPL_u2 (
#/   .op_in(op_in_2),
#/   .op_out(op_in_2_fix)
#/ );
#/ // END of INST
#/ 
#/ //======== Adder ========//
#/ wire [dwt_fix-1:0] op_result;
#/ assign op_result = op_in_1_fix + op_in_2_fix;
#/ 
#/ //======== Post-Add Fixed Point Match ========//
#/ wire [dwt_out-1:0] op_fixed;
#/ // INST
#/ FxP_Match_TRN_TCPL_WRP_TCPL#(
#/   .dwt_in(dwt_fix),
#/   .frac_in(frac_fix),
#/   .sign_in(sign_out),
#/   .dwt_out(dwt_out),
#/   .frac_out(frac_out),
#/   .sign_out(sign_out))
#/  FxP_Match_TRN_TCPL_WRP_TCPL_u3 (
#/   .op_in(op_result),
#/   .op_out(op_fixed)
#/ );
#/ // END of INST
#/ 
#/ //======== Output Assign ========//
#/ // INST
#/ Delay_rst_n#(
#/   .dwt(dwt_out),
#/   .n(1))
#/  Delay_rst_n_u1 (
#/   .op_in(op_fixed),
#/   .op_out(op_out),
#/   .clk(clk),
#/   .rst_n(rst_n)
#/ );
#/ // END of INST
#/ 
#/ endmodule
