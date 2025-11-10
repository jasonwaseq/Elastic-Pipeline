module elastic
  #(parameter width_p = 8,
    parameter datapath_gate_p = 0,
    parameter datapath_reset_p = 0)
  (input  logic              clk_i,
   input  logic              reset_i,

   input  logic [width_p-1:0] data_i,
   input  logic              valid_i,
   output logic              ready_o,

   output logic              valid_o,
   output logic [width_p-1:0] data_o,
   input  logic              ready_i);

  logic [width_p-1:0] data_l;
  logic valid_l;

  assign ready_o = ~valid_l || ready_i;

  always_ff @(posedge clk_i) begin
    if (reset_i) begin
      valid_l <= 1'b0;
      if (datapath_reset_p != 0)
        data_l <= '0;
    end
    else if (ready_o) begin
      valid_l <= valid_i;
      if (datapath_gate_p != 0) begin
        if (valid_i)
          data_l <= data_i;
      end else begin
        data_l <= data_i;
      end
    end
  end

  assign valid_o = valid_l;
  assign data_o  = data_l;

endmodule
