// -----------------------------------------------------------------------------
// Copyright (c) 2024-2026 All rights reserved
// -----------------------------------------------------------------------------
// Author : Yunwei Mao (230238275@seu.edu.cn)
// File   : Comp_Tree
// Create : 2024/05/27
// Revise : ----
// Func   : Comparison Tree with Hybrid Precision
// -----------------------------------------------------------------------------


`timescale 1ns / 1ps
module CT_F (
    op_in
    , clk
    , arst_n
    , en
    , gval_out
    , gpos_out
);

//======== Input Ports ========//
input [16-1:0] op_in;
input clk;
input arst_n;
input en;

//======== Output Ports ========//
output [8-1:0] gval_out;
output [1+4-1:0] gpos_out;

wire [16-1:0] op_l0;
assign op_l0 = op_in;
//======== Comparison Tree Layer 1 ========//
wire [8-1:0] gval_l1;
wire [1-1:0] gpos_l1;
// INST
Comp_l1#(
  .dwt_in_1(8),
  .frac_in_1(4),
  .sign_in_1(0),
  .dwt_in_2(8),
  .frac_in_2(4),
  .sign_in_2(0),
  .dwt_out_g(8),
  .frac_out_g(4))
 Comp_l1u0 (
  .op_in_1(op_l0[1*8-1:0*8]),
  .op_in_2(op_l0[2*8-1:1*8]),
  .clk(clk),
  .arst_n(arst_n),
  .en(en),
  .gval_out(gval_l1[1*8-1:0*8]),
  .gpos_out(gpos_l1[1*1-1:0*1])
);
// END of INST

// ready to precess new inputs
reg rdy_in;

// FSM
localparam IDLE     = 2'b00;
localparam ASSIGN   = 2'b01;
localparam COMP     = 2'b10;

reg  [2:0] CS, NS; // Current State, Next State
reg  [2-1:0] turn_cnt; // counter


// Sequential State Transition
always @(posedge clk, negedge arst_n) begin
    if (~arst_n) begin
        CS <= IDLE;
    end
    else if (en) begin
        CS <= NS;
    end
end

// Combinational Condition Judgement
always @(*) begin
    case (CS)
        IDLE: begin
            if (en) begin
                NS = ASSIGN;
            end
            else begin
                NS = IDLE;
            end
        end
        ASSIGN: begin
            if (turn_cnt == 2'b0) begin
                NS = ASSIGN;
            end
            else begin
                NS = COMP;
            end
        end
        COMP: begin
            if (turn_cnt != 0) begin
                NS = COMP;
            end
            else begin
                NS = ASSIGN;
            end
        end
        default: NS = IDLE;
    endcase
end

// Sequential FSM Output
reg  [8-1:0]    gval_FSM; // greater value of Comp in FSM
reg  [4-1:0]  gpos_FSM; // the position of greater value in FSM
reg  [1-1:0]   gpos_tmp; // the origin position of greater value
wire                    gpos_FSM_w;
wire [8-1:0]    gval_FSM_w;
// Counter
always @(posedge clk, negedge arst_n) begin
    if (~arst_n) begin
        turn_cnt <= 2'b0;
    end
    else begin
        case (NS)
            IDLE: begin
                turn_cnt <= 2'b0;
            end
            ASSIGN: begin
                if (4 == 2'b0) begin
                    turn_cnt <= 2'b0;
                end
                else begin
                    turn_cnt <= 2'b1;
                end
            end
            COMP: begin
                if (turn_cnt >= 4) begin
                    turn_cnt <= 2'b0;
                end
                else begin
                    turn_cnt <= turn_cnt + 1;
                end
            end
            default: turn_cnt <= 2'b0;
        endcase
    end
end
// Comp
always @(posedge clk, negedge arst_n) begin
    if (~arst_n) begin
        gval_FSM <= 8'b0;
        gpos_FSM <= 4'b0;
        gpos_tmp <= 1'b0;
        rdy_in   <= 1'b0;
    end
    else begin
        case (NS)
            IDLE: begin
                gval_FSM <= 8'b0;
                gpos_FSM <= 4'b0;
                gpos_tmp <= 1'b0;
                rdy_in   <= 1'b0;
            end
            ASSIGN: begin
                rdy_in   <= 1'b0;
                gval_FSM <= gval_l1;
                gpos_tmp <= gpos_l1;
            end
            COMP: begin
                if (turn_cnt == 1'b0) begin
                    gval_FSM <= gval_l1;
                    gpos_tmp <= gpos_l1;
                end else if (turn_cnt < 4) begin

                    gval_FSM <= gval_FSM_w;
                    gpos_FSM <= {gpos_FSM_w, gpos_FSM[4-1:1]};
                end
                if (turn_cnt == 4) begin
                    rdy_in   <= 1'b1;
                end
            end
            default: begin
                gval_FSM <= 8'b0;
                gpos_FSM <= 4'b0;
                gpos_tmp <= 1'b0;
                rdy_in   <= 1'b0;
            end
        endcase
    end
end
assign gval_out = (rdy_in == 1'b1)? gval_FSM:8'b0;
assign gpos_out = (rdy_in == 1'b1)? {gpos_FSM, gpos_tmp}:1+4'b0;
// INST
Comp_pos_FSM#(
  .dwt_in_1(8),
  .frac_in_1(4),
  .sign_in_1(0),
  .dwt_in_2(8),
  .frac_in_2(4),
  .sign_in_2(0),
  .dwt_out_g(8),
  .frac_out_g(4),
  .dwt_pos_in(1))
 Comp_pos_FSM_u0 (
  .op_in_1(gval_FSM),
  .op_in_2(gval_l1),
  .gpos_in_1(gpos_tmp),
  .gpos_in_2(gpos_l1),
  .clk(clk),
  .arst_n(arst_n),
  .en(en),
  .gval_out(gval_FSM_w),
  .gpos_out(gpos_FSM_w)
);
// END of INST
endmodule
