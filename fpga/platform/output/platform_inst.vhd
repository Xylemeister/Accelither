	component platform is
		port (
			clk_clk          : in std_logic                     := 'X';             -- clk
			filter_in_export : in std_logic_vector(15 downto 0) := (others => 'X'); -- export
			reset_reset_n    : in std_logic                     := 'X'              -- reset_n
		);
	end component platform;

	u0 : component platform
		port map (
			clk_clk          => CONNECTED_TO_clk_clk,          --       clk.clk
			filter_in_export => CONNECTED_TO_filter_in_export, -- filter_in.export
			reset_reset_n    => CONNECTED_TO_reset_reset_n     --     reset.reset_n
		);

