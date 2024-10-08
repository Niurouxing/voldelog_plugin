from utils import *
from py2v import py2v
from ModuleLoader import *

@py2v
def ModuleBasic(p1, p2):
    #/ module BASIC #(vparamB1, vparamB2, vparamBN)( // vparams are declared with verilog lines
    if p1 > 0:
       #/ portBA1,
       pass
    if p2 > 0:
       #/ portBA2,
       pass
    #/ );

    #/ endmodule
    continue 
    


@py2v
def ModuleMUL(param1, param2, paramN):  # Params (called by the python script) are placed in the python function definition.
    #/ module MUL #(vparam1, vparam2, vparamN)(
    if param1 > 0:
       #/ port1,
       pass
    if param2 > 0:
       #/ port2,
       pass
    if paramN > 0:
       #/ portN
       pass
    #/ );

    #/ localparam IDLE     = 2'b00;
    #/ localparam ASSIGN   = 2'b01;
    #/  localparam COMP     = 2'b10;
    #/  always @(posedge clk, negedge arst_n) begin
    #/      if (~arst_n) begin
    #/          CS <= IDLE;
    #/      end
    #/      else if (en) begin
    #/          CS <= NS;
    #/      end
    #/  end


    #/ INST:
    ModuleBasic(p1 = 10, p2 = 10)
    #/ VPARAMS:
    #/ vparamB1 : 19
    #/ vparamB2 : 6
    #/ vparamBN : 5
    #/ PORTS:
    #/ portBA1 : xxx
    #/ portBA2 : yyy
    #/ MODULE_NAME: BASIC
    #/ INST_NAME: BASIC1
    #/ ENDINST

    # vparams and ports are declared with verilog lines
    #/ start of module MUL
    #/ middle of module MUL
    #/ end of module MUL
    #/ endmodule

@py2v
def ModuleTOP(param_top1,param_top2):
    rst1 = 1
    rst2 = 2
    rstn = 3
    inst_ports_list = []
    #/ module TOP #(vparam_top1, vparam_top2, vparam_top3)(
    if param_top1 > 0:
       #/ port_top1,
       inst_ports_list.append('A_IN')
       pass

    if param_top2 > 0:
       #/ port_top2,
       inst_ports_list.append('B_IN')
       pass
    #/ );
    if param_top1 > 0:
        #/ INST:
        ModuleMUL(param1= rst1, param2 = rst2, paramN = rstn)
        #/ VPARAMS:
        #/ vparam1 : 3
        #/ vparam2 : 6
        #/ vparamN : 5
        #/ PORTS:
        #/ PORT1 : aaa
        #/ PORT2 : bbb
        #/ PORT3 : ccc
        #/ MODULE_NAME: MUL
        #/ INST_NAME: MUL1
        #/ ENDINST

\
    #/ endmodule

ModuleTOP(param_top1 = 2,param_top2 = 4)
#print(v_declaration)
# inst_code =   ['        #/ INST: \n\n', '        #/ PARAMS: \n\n', '        #/ param1 : 1\n\n', '        #/ param2 : 2', '#/ param3 : 3\n\n', '        #/ VPARAMS: \n\n', '        #/ vparam1 : 3\n\n', '        #/ vparam2 : 4\n\n','        #/ vparam3 : 5\n\n', '        #/ INST_NAME: MUL1\n\n', '        #/ MODULE_NAME: MUL\n\n']
# [X,Y,Z,W,P] = parseVerilog_inst_block(inst_code, ())locals
#/ wire A_IN, B_IN, A_OUT, B_OUT, C_OUT;