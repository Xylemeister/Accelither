# Project Source Files

## /fpga/

This directory contains all the code relating to the FPGA device.

### Features and functionality:

The FPGA device is programmed with a NIOS II instance, which is connected to the DE10's LEDs, 7 segment displays, switches, buttons and accelerometer. It is then programmed to receive inputs for the LEDs and 7 segment displays (which are immediately applied) and responds with the states of the switches, buttons, and accelerometer.

All communication is performed with hex values (0-9, a-f), where every hex value represents 4 bits.
Messages to the FPGA are 13 characters long (`7 segment displays + LEDs` = `(7 * 6) + (10 * 1) = 52` -> `52 / 4 = 13`), and must be initiated by first sending a '/' character, making messages a total of 14 characters long. 
Messages from the FPGA are 15 characters long (`accelerometer axes + switches + buttons` = `(3 * 16) + (10 * 1) + (2 * 1) = 60` -> `60 / 4 = 15`).

The accelerometer hardware, which performs high-speed SPI communication, then performs rudimentary smoothing, is in `/fpga/filter.v`.

The platform designer project files are in `/fpga/platform/`. They are already compiled in the repo.

### How to use:

- Ensure the DE10 is connected and working,
- Start Quartus and open `/fpga/fpga_code.qpf`,
- (Optional) Recompile the project, but repo already contains the compiled project,
- Open the Programmer, which should open `top.cdf`,
- Start the code on the DE10.

## /fpga/software/

This directory contains all the code to be run on the NIOS II instance on the cpu.

### Features and functionality:

For details on communication, see Features and functionality in [/fpga/](#fpga). The implementation uses `alt_getchar()` and `alt_putchar()` for input and output.

The source code is all in `/fpga/software/nios_code/hello_world_small.c`

The BSP is in `/fpga/software/nios_code_bsp/`

### How to use:

- First, ensure the FPGA is programmed, as described in [/fpga/](#fpga),
- Open "Nios II Software Build Tools for Eclipse" in Quartus,
- Ensure the Eclipse workspace contains both the `/fpga/software/nios_code/` and `/fpga/software/nios_code_bsp/` directories,
- (Optional) Generate the BSP and rebuild the project. Only should be necessary if the FPGA code was recompiled. The project already contains the compiled binary in `/fpga/software/nios_code/nios_code.elf`
- Run the project on DE10.
- To have programmatic access to the DE10, ensure the terminal in Eclipse is closed and ensure the I/O stream is constantly running, as described in [/local/de10/stream/](#local-de10-stream).

## /local/de10/

This is a python module which interacts with the DE10, giving the user options to get inputs from and set outputs to the board.

### Features and functionality:

Provides 3 namespaces with functions:

- `Raw` contains functions which get and set with minimal processing. It is designed to be akin to working directly with NIOS II, with the only major difference being that the order of the 7 segment displays was changes from right-to-left to left-to-right (so 7 segment display 0 is the hardware `HEX[5]`).
- `Input` contains functions which get and set, but with an emphasis on programmer-intuitiveness. Some functions are synonymous to their `Raw` equivalents, but there are differences:
	- The 7 segment displays have `0`/`False` mean unlit and `1`/`True` mean lit (i.e. the values are inverted compared to the `Raw` equivalent). There is also a collection of preset numbers/letters/symbols, removing the need to directly work with individual segments in most use cases.
	- The buttons have `0`/`False` mean unpressed and `1`/`True` mean pressed (i.e. the values are inverted compared to the `Raw` equivalent).
	- The accelerometer readings are normalised to the range `[-1, 1]` (based on values obtained in the `Calibration` namespace, see below). These readings also have an adjustable "deadzone" and "maximum threshhold", which round the readings, to 0 and -1/1 respectively, when the obtained value is close enough, so expecting an output value of exactly -1, 0, or 1, is very reasonable and consistently achievable.
	- The accelerometer readings can be obtained in a format more akin to that of a joystick: instead of outputting x, y and z, it instead outputs an angle and magnitude in the x-y plane. One version of this function returns the observed magnitude total magnitude (which ideally should only be gravity and be constant, but will have noticeable variations as users will inevitable cause translation movement and not just rotation), and the other version outputs values which only change when the total magnitude is equal to gravity (it outputs the most recent valid reading at all times, and ignores readings with abnormal magnitudes).
- `Calibration` contains functions which get the range of expected values in all axes and stores them in a file for normalising future readings (see `Input` namespace above). Consideration was put into making the calibration easy to incorporate with a user interface, so the directions which still need to be calibrated can be obtained (to then forward to the user). However, this theoretically only needs to be performed once per DE10 board, so the final project doesn't necessarily need to use any of this functionality, as long as the boards are all calibrated in advance.

### How to use:
- Ensure the FPGA is programmed, the NIOS II code is running and the shell script in the `/stream/` subdirectory is running,
- Copy this directory to the directory with your python program wanting to interact with the de10,
- Use `import de10` to import.

## <a name="local-de10-stream"></a>/local/de10/stream/

This directory contains a shell script which has to be run to have programmatic access to the DE10.

### Features and functionality:

Uses shared memory to perform I/O with the DE10 in parallel to other programs. The `de10` Python module connects to this shared memory behind-the-scenes.

If a problem with the DE10 occurs, the shell script crashes and needs to manually be restarted.

### How to use:

- Ensure the FPGA is programmed and the NIOS II code is running, and no other instance of `nios2-terminal` is running (including the instance in Eclipse),
-  Open a terminal and run `NIOS II Command Shell.bat` (the default path is provided at the start of both Python files in the directory),
- `cd` into this directory, such that `accelerometer_stream.sh` is shown after `ls`
- Run `./accelerometer_stream.sh`. The terminal can now be minimised but shouldn't be closed.
