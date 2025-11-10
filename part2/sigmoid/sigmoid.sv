`ifndef HEXPATH
`define HEXPATH "/workspaces/lab-3-behavioral-verilog-jasonwaseq/part2/sigmoid/"
`endif
module sigmoid
  (input [0:0] clk_i
  ,input [0:0] reset_i
  ,input [7:0] x_i
  ,output [7:0] f_o
   );

   // For Lab 3, please use your RAM to implement this module.
   // You may use assign statments to connect wires, but not
   // to perform logic.
  
  ram_1r1w_async
    #(.width_p(8),
      .depth_p(256),
      .filename_p("sigmoid.hex")
    )
  ram_1r1w_async_inst (
    .clk_i(clk_i),
    .reset_i(reset_i),
    .wr_valid_i(1'd0),
    .wr_data_i(8'd0),
    .wr_addr_i(8'd0),
    .rd_addr_i(x_i+8'd128),
    .rd_data_o(f_o)
  );

endmodule
