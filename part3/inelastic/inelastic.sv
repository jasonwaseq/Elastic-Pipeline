module inelastic
  #(parameter [31:0] width_p = 8
   /* verilator lint_off WIDTHTRUNC */
   ,parameter [0:0] datapath_reset_p = 0
   /* verilator lint_on WIDTHTRUNC */
   )
  (input [0:0] clk_i
  ,input [0:0] reset_i

  ,input [0:0] en_i

  // Fill in the ranges of the busses below
  ,input [width_p-1 : 0] data_i
  ,output [width_p-1 : 0] data_o);

  logic [width_p-1 : 0] data_l;

  always_ff @(posedge clk_i) begin
    if (datapath_reset_p && reset_i) begin
      data_l <= '0;
    end else if (en_i) begin
      data_l <= data_i; 
    end
  end

  assign data_o = data_l;
  
endmodule
