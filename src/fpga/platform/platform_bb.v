
module platform (
	buttons_export,
	clk_clk,
	filter_x_export,
	filter_y_export,
	filter_z_export,
	hex0_export,
	hex1_export,
	hex2_export,
	hex3_export,
	hex4_export,
	hex5_export,
	leds_export,
	reset_reset_n,
	switches_export);	

	input	[1:0]	buttons_export;
	input		clk_clk;
	input	[15:0]	filter_x_export;
	input	[15:0]	filter_y_export;
	input	[15:0]	filter_z_export;
	output	[6:0]	hex0_export;
	output	[6:0]	hex1_export;
	output	[6:0]	hex2_export;
	output	[6:0]	hex3_export;
	output	[6:0]	hex4_export;
	output	[6:0]	hex5_export;
	output	[9:0]	leds_export;
	input		reset_reset_n;
	input	[9:0]	switches_export;
endmodule
