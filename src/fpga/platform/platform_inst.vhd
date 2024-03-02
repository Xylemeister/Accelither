	component platform is
		port (
			buttons_export  : in  std_logic_vector(1 downto 0)  := (others => 'X'); -- export
			clk_clk         : in  std_logic                     := 'X';             -- clk
			filter_x_export : in  std_logic_vector(15 downto 0) := (others => 'X'); -- export
			filter_y_export : in  std_logic_vector(15 downto 0) := (others => 'X'); -- export
			filter_z_export : in  std_logic_vector(15 downto 0) := (others => 'X'); -- export
			hex0_export     : out std_logic_vector(6 downto 0);                     -- export
			hex1_export     : out std_logic_vector(6 downto 0);                     -- export
			hex2_export     : out std_logic_vector(6 downto 0);                     -- export
			hex3_export     : out std_logic_vector(6 downto 0);                     -- export
			hex4_export     : out std_logic_vector(6 downto 0);                     -- export
			hex5_export     : out std_logic_vector(6 downto 0);                     -- export
			leds_export     : out std_logic_vector(9 downto 0);                     -- export
			reset_reset_n   : in  std_logic                     := 'X';             -- reset_n
			switches_export : in  std_logic_vector(9 downto 0)  := (others => 'X')  -- export
		);
	end component platform;

	u0 : component platform
		port map (
			buttons_export  => CONNECTED_TO_buttons_export,  --  buttons.export
			clk_clk         => CONNECTED_TO_clk_clk,         --      clk.clk
			filter_x_export => CONNECTED_TO_filter_x_export, -- filter_x.export
			filter_y_export => CONNECTED_TO_filter_y_export, -- filter_y.export
			filter_z_export => CONNECTED_TO_filter_z_export, -- filter_z.export
			hex0_export     => CONNECTED_TO_hex0_export,     --     hex0.export
			hex1_export     => CONNECTED_TO_hex1_export,     --     hex1.export
			hex2_export     => CONNECTED_TO_hex2_export,     --     hex2.export
			hex3_export     => CONNECTED_TO_hex3_export,     --     hex3.export
			hex4_export     => CONNECTED_TO_hex4_export,     --     hex4.export
			hex5_export     => CONNECTED_TO_hex5_export,     --     hex5.export
			leds_export     => CONNECTED_TO_leds_export,     --     leds.export
			reset_reset_n   => CONNECTED_TO_reset_reset_n,   --    reset.reset_n
			switches_export => CONNECTED_TO_switches_export  -- switches.export
		);

