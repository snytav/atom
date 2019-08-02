author: Pierre Cerantola
email: cerantolap@eisti.eu


Instructions to edit/create a configuration file:

0: you can see "input_config.txt" to have an idea of the right structure to follow
1: each non-blank line must be a parameter line
2: each parameter line must follow the structure "numeric_parameter			# comment about numeric_parameter"
	2.1: spaces or tabulations doesn't affect the program
	2.2: comment about parameter can be empty, but '#' character is always required
	2.3: please note that parameter order is fixed
3: there can be one or more blank lines between each parameter line
4: please note that syntax errors, missing parameters lines or incoherent parameters are detected and displayed by the program as fatal errors or warnings


Instructions for compiling and executing "plasma_init_code.py" program:

0: be sure to have Python 3 environment and numpy, netCDF4, mpl_toolkits.mplot3d, matplotlib modules installed
1: open system console and execute command "python plasma_init_code.py input_config.txt output_plasma.nc"; where input_config.txt is the text file containing plasma parameters, and where output_plasma.nc will be the generated NetCDF file
	1.1: you can execute command "python plasma_init_code.py -h" or "python plasma_init_code.py --help" to display help
2: follow displayed instructions