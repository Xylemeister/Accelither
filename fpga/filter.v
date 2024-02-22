module filter (
	input clk,
	input sdi,
	output sdo,
	output cs_n,
	output sclk,
	output [15:0] out,
	output [9:0] t1
);

parameter FILTER_SHIFT = 2; 								  // Creates 2**FILTER_SHIFT registers
parameter TARG_SCLK = 2_000_000;						     // Target frequency for SCLK
parameter CLK_NUM_FOR_SCLK = 50_000_000 / TARG_SCLK; // Base clock is 50MHz
parameter SCLK_CYCLES_BETWEEN_READS = TARG_SCLK / 3200;				  // Number of SCLK cycles before read is performed

/*
reg [16 * (2**FILTER_SHIFT) - 1:0] buffer;
reg [$clog2(CLK_NUM_FOR_SCLK)/*-1:0]  sclk_timer;
reg [(($clog2(SCLK_CYCLES_BETWEEN_READS) > 4)	 // Need at least 16 states
		? $clog2(SCLK_CYCLES_BETWEEN_READS)
		: 5)/*-1 : 0] read_wait_timer;
reg read_wait;	// 0 - read, 1 - wait
reg cs_n_reg1;
reg cs_n_reg2;
reg sclk_reg;
reg sdi_reg;

localparam READ_ADDR = 8'b11110010; // Read multibit X

assign cs_n = (cs_n_reg1 || cs_n_reg2);
assign out  = ((buffer[15:0] + buffer[31:16]) >> FILTER_SHIFT);
assign sclk = sclk_reg || cs_n;

reg p0;
reg p1;
assign t1 = {cs_n, sclk, sdi, sdo, 4'b0, p0 && sclk_reg & !cs_n, p1 && sclk_reg && !cs_n};

assign sdi = (read_wait_timer < 8) ? sdi_reg : 1'bx;

always @(posedge clk)
	if (sclk_timer < CLK_NUM_FOR_SCLK)
		sclk_timer <= sclk_timer + 1;
	else
	begin
		sclk_timer <= 0;
		sclk_reg <= !sclk_reg;
	end
	
always @(negedge sclk_reg)
begin
	if (read_wait)
		if (read_wait_timer < SCLK_CYCLES_BETWEEN_READS)
			read_wait_timer <= read_wait_timer + 1;
		else
		begin
			read_wait_timer <= 0;
			read_wait <= 0;
			cs_n_reg1 <= 0;
		end
	else
		if (read_wait_timer < 24)
		begin
			if (read_wait_timer < 8)
				sdi_reg <= READ_ADDR[7 - read_wait_timer];
			else
				buffer <= {buffer[16 * (2**FILTER_SHIFT) - 1:1], sdo};
			read_wait_timer <= read_wait_timer + 1;
		end
		else
		begin
			read_wait_timer <= 0;
			read_wait <= 1;
			cs_n_reg1 <= 1;
		end
end

always @(posedge sclk_reg)
begin
	if (!read_wait) cs_n_reg2 <= 0;
	else cs_n_reg2 <= 1;
	if (sdi)
	begin
		p1 <= 1;
		p0 <= 0;
	end
	else 
	begin
		p0 <= 1;
		p1 <= 0;
	end
end
		
initial read_wait = 1;
*/

reg status;
localparam IDLE = 0;
localparam SENDING = 1;
initial status = IDLE;

reg [$clog2(CLK_NUM_FOR_SCLK)/*-1*/:0]  sclk_timer;
reg sclk_reg;
always @(posedge clk)
	if (sclk_timer < CLK_NUM_FOR_SCLK)
		sclk_timer <= sclk_timer + 1;
	else
	begin
		sclk_timer <= 0;
		sclk_reg <= !sclk_reg;
	end	
assign sclk = sclk_reg || cs_n;

reg cs_n_reg;
assign cs_n = cs_n_reg;
initial cs_n_reg = 1;

reg [(($clog2(SCLK_CYCLES_BETWEEN_READS) > 4)	 // Need at least 16 states
		? $clog2(SCLK_CYCLES_BETWEEN_READS)
		: 5)/*-1*/ : 0] sclk_count;

reg [15:0] write_val;
reg [2:0] initial_instr;
localparam INITIAL_INSTR_COUNT = 2;
initial initial_instr = 0;
initial write_val = 16'b00_110001_00000000;
always @(*)
	case (initial_instr)
	0:	write_val <= 16'b00_110001_00000000; // Standard 4 lane SPI operation
	1: write_val <= 16'b00_101100_00001111; // 3200 Hz mode
	//2: write_val <= 16'b
	2: write_val <= 16'b11_110010_00000000; // Read
	endcase

reg [16 * (2**FILTER_SHIFT) - 1:0] buffer;

reg sdo_reg;
assign sdo = sdo_reg;

always @(negedge sclk_reg)
begin
	if (status == IDLE)
		if (sclk_count < SCLK_CYCLES_BETWEEN_READS)
			sclk_count <= sclk_count + 1;
		else
		begin
			sclk_count <= 0;
			status <= SENDING;
		end
	else
		if (sclk_count < (initial_instr < INITIAL_INSTR_COUNT ? 16 : 24))
		begin
			cs_n_reg <= 0;
			if ((initial_instr < INITIAL_INSTR_COUNT) || (sclk_count < 8)) sdo_reg <= write_val[15-sclk_count];
			else buffer <= {buffer[16 * (2**FILTER_SHIFT) - 2:0], sdi};
			sclk_count <= sclk_count + 1;
		end
		else
		begin
			sclk_count <= 0;
			cs_n_reg <= 1;
			status <= IDLE;
			if (initial_instr < INITIAL_INSTR_COUNT) initial_instr <= initial_instr + 1;
		end
end

reg [15:0] out_reg;
wire [15 + FILTER_SHIFT : 0] filter_val;
assign filter_val = ({buffer[   7:   0], buffer[   15:   8]} +
							{buffer[16+7:16+0], buffer[16+15:16+8]} +
							{buffer[32+7:32+0], buffer[32+15:32+8]} +
							{buffer[48+7:48+0], buffer[48+15:48+8]}) >> FILTER_SHIFT;


assign out = out_reg;
always @(posedge cs_n)
	out_reg <= filter_val;


reg p0;
reg p1;
assign t1 = {cs_n, sclk, sdi, sdo, sdi == 0, sdo == 0, 2'b0, p0 && sclk_reg && !cs_n, p1 && sclk_reg && !cs_n};

always @(posedge sclk_reg)
begin
	if (sdo)
	begin
		p1 <= 1;
		p0 <= 0;
	end
	else 
	begin
		p0 <= 1;
		p1 <= 0;
	end
end

endmodule
