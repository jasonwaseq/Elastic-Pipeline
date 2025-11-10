`ifndef HEXPATH
`define HEXPATH "/workspaces/lab-3-behavioral-verilog-jasonwaseq/part2/hex2ssd/"
`endif
module hex2ssd
  (input [3:0] hex_i
  ,output [6:0] ssd_o
  );

   // For Lab 3, please use your RAM to implement this module.
   // You may use assign statments to connect wires, but not
   // to perform logic. 

  wire dummy_clk;
  assign dummy_clk = 1'b0;

  ram_1r1w_async
    #(.width_p(7),
      .depth_p(16),
      .filename_p("hex2ssd.hex")
    )
  ram_1r1w_async_inst (
    .clk_i(dummy_clk),
    .reset_i(1'b0),
    .wr_valid_i(1'b0),
    .wr_data_i(7'b0),
    .wr_addr_i(4'b0),
    .rd_addr_i(hex_i),
    .rd_data_o(ssd_o)
  );

endmodule

/*
module hex2ssd
  (input [3:0] hex_i
  ,output [6:0] ssd_o
  );

logic [6:0] ssd_l;
                  //GFEDCBA
always_comb begin
  case (hex_i)
  4'h0 : ssd_l = 7'b1000000; // 0
  4'h1 : ssd_l = 7'b1111001; // 1
  4'h2 : ssd_l = 7'b0100100; // 2
  4'h3 : ssd_l = 7'b0110000; // 3
  4'h4 : ssd_l = 7'b0011001; // 4
  4'h5 : ssd_l = 7'b0010010; // 5
  4'h6 : ssd_l = 7'b0000010; // 6
  4'h7 : ssd_l = 7'b1111000; // 7
  4'h8 : ssd_l = 7'b0000000; // 8
  4'h9 : ssd_l = 7'b0011000; // 9
  4'hA : ssd_l = 7'b0001000; // A
  4'hB : ssd_l = 7'b0000011; // b
  4'hC : ssd_l = 7'b1000110; // C
  4'hD : ssd_l = 7'b0100001; // d
  4'hE : ssd_l = 7'b0000110; // E
  4'hF : ssd_l = 7'b0001110; // F
  default: ssd_l = 7'b1111111; 
  endcase
end

assign ssd_o = ssd_l;

endmodule
*/
