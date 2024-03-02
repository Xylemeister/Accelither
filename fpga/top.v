module top (
	input  		 MAX10_CLK1_50,
	
	// Switches
	input  [9:0] SW,
	
	// LEDS
	output [9:0] LEDR,
	
	// 7 segs
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3,
	output [6:0] HEX4,
	output [6:0] HEX5,
	
	// Buttons
	input [1:0] KEY,
	
	// Accelerometer
	inout  		 GSENSOR_SDI,
	inout 		 GSENSOR_SDO,
	output 		 GSENSOR_CS_N,
	output 		 GSENSOR_SCLK
);

wire [15:0] filter_val_x;
wire [15:0] filter_val_y;
wire [15:0] filter_val_z;

filter filter0 (
	.clk   (MAX10_CLK1_50),
	.sdi   (GSENSOR_SDO),
	.sdo   (GSENSOR_SDI),
	.cs_n  (GSENSOR_CS_N),
	.sclk  (GSENSOR_SCLK),
	.out_x (filter_val_x),
	.out_y (filter_val_y),
	.out_z (filter_val_z)
);

platform platform0 (
	.buttons_export  (KEY),
	.clk_clk         (MAX10_CLK1_50),
	.filter_x_export (filter_val_x),
	.filter_y_export (filter_val_y),
	.filter_z_export (filter_val_z),
	.hex0_export     (HEX0),
	.hex1_export     (HEX1),
	.hex2_export     (HEX2),
	.hex3_export     (HEX3),
	.hex4_export     (HEX4),
	.hex5_export     (HEX5),
	.leds_export     (LEDR),
	.reset_reset_n   (1'b1),
	.switches_export (SW)
);

endmodule
