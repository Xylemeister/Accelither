module top (
	input  		MAX10_CLK1_50,
	
	input [2:1]	GSENSOR_INT,
	inout  		GSENSOR_SDI,
	inout 		GSENSOR_SDO,
	output 		GSENSOR_CS_N,
	output 		GSENSOR_SCLK,
	
	output [9:0] LEDR,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
);

wire [15:0] filter_val;

filter filter0 (
	.clk  (MAX10_CLK1_50),
	.sdi  (GSENSOR_SDO),
	.sdo  (GSENSOR_SDI),
	.cs_n (GSENSOR_CS_N),
	.sclk (GSENSOR_SCLK),
	.out  (filter_val),
	.t1   (LEDR)
);

hex_to_7seg seg_0 (
	.in(filter_val[3:0]),
	.out(HEX0)
);
hex_to_7seg seg_1 (
	.in(filter_val[7:4]),
	.out(HEX1)
);
hex_to_7seg seg_2 (
	.in(filter_val[11:8]),
	.out(HEX2)
);
hex_to_7seg seg_3 (
	.in(filter_val[15:12]),
	.out(HEX3)
);

platform platform0 (
	.clk_clk          (MAX10_CLK1_50),
	.reset_reset_n    (1'b1),
	.filter_in_export (filter_val)
);

endmodule
