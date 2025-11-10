module top
  (input [0:0] clk_12mhz_i
  ,input [0:0] reset_n_async_unsafe_i
  ,input [3:1] button_async_unsafe_i
  ,output [0:0] spi_cs_o
  ,output [0:0] spi_sd_o
  ,input [0:0] spi_sd_i
  ,output [0:0] spi_sck_o
  ,output [5:1] led_o
  ,output [7:0] ssd_o);

   wire [39:0] data_o;
   wire [39:0] data_i;
   wire [9:0]  position_x;
   wire [9:0]  position_y;

   wire [23:0] color_rgb;
   
   wire [0:0] reset_sync_r;
   wire [0:0] reset_r; // Use this as your reset_signal

   wire [3:1] button_sync_r;
   wire [3:1] button_r;


   dff
     #()
   sync_a
     (.clk_i(clk_12mhz_i)
     ,.reset_i(1'b0)
     ,.en_i(1'b1)
     ,.d_i(reset_n_async_unsafe_i)
     ,.q_o(reset_n_sync_r));

   inv
     #()
   inv
     (.a_i(reset_n_sync_r)
     ,.b_o(reset_sync_r));

   dff
     #()
   sync_b
     (.clk_i(clk_12mhz_i)
     ,.reset_i(1'b0)
     ,.en_i(1'b1)
     ,.d_i(reset_sync_r)
     ,.q_o(reset_r));
       
   generate
     for(genvar idx = 1; idx <= 3; idx++) begin
         dff
           #()
         sync_a
           (.clk_i(clk_12mhz_i)
           ,.reset_i(1'b0)
           ,.en_i(1'b1)
           ,.d_i(button_async_unsafe_i[idx])
           ,.q_o(button_sync_r[idx]));

         dff
           #()
         sync_b
           (.clk_i(clk_12mhz_i)
           ,.reset_i(1'b0)
           ,.en_i(1'b1)
           ,.d_i(button_sync_r[idx])
           ,.q_o(button_r[idx]));
     end
   endgenerate

   PmodJSTK
     #()
   jstk_i
     (.clk_12mhz_i(clk_12mhz_i)
     ,.reset_i(reset_r)
     ,.data_i(data_i)
     ,.spi_sd_i(spi_sd_i)
     ,.spi_cs_o(spi_cs_o)
     ,.spi_sck_o(spi_sck_o)
     ,.spi_sd_o(spi_sd_o)
     ,.data_o(data_o));

   assign position_y = {data_o[25:24], data_o[39:32]};
   assign position_x = {data_o[9:8], data_o[23:16]};
   logic [9:0] position_x_r;
   always_ff @(posedge clk_12mhz_i)
     if (reset_r)
       position_x_r <= 1'b0;
     else
       position_x_r <= position_x;

   assign data_i = {8'b10000100, color_rgb, 8'b00000000};

   assign color_rgb[23:16] = 8'hff;
   assign color_rgb[15:8] = 8'h00;
   assign color_rgb[7:0] = 8'h00;

   // Your code here

  wire [7:0] sig_o;
  sigmoid
  sigmoid_inst (
    .clk_i(clk_12mhz_i),
    .reset_i(reset_r),
    .x_i(position_x_r[9:2]),
    .f_o(sig_o)
  );

  wire [6:0] ssd_top_w;
  wire [6:0] ssd_bottom_w;

  hex2ssd
    #()
  hex2ssd_top_inst (
    .hex_i(sig_o[7:4]),
    .ssd_o(ssd_top_w)
  );

  hex2ssd
    #()
  hex2ssd_bottom_inst (
    .hex_i(sig_o[3:0]),
    .ssd_o(ssd_bottom_w)
  );

  logic digit_select;
  logic [15:0] mux_counter;
  always_ff @(posedge clk_12mhz_i) begin
    if (reset_r) begin
      mux_counter <= 16'd0;
      digit_select <= 1'b0;
    end else begin
      if (mux_counter == 16'd60000) begin
        digit_select <= ~digit_select;
        mux_counter <= 16'd0;
      end else begin
        mux_counter <= mux_counter + 16'd1;
      end
    end
  end

  assign ssd_o = digit_select ? {digit_select, ssd_top_w} : {digit_select, ssd_bottom_w};
  
  assign led_o = position_x_r[9:5];

endmodule

