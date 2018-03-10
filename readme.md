# Random Number Generator
A number generator that produces numbers by given probabilities.

## Installing / Getting started
Compatible with Python 2.7

If you're using Ubuntu, it comes with Python 2.7. For other operating systems, please take a look at https://www.python.org/downloads/

After installing Python 2.7. You can either clone the code,

```shell
mkdir <FOLDER>
cd <FOLDER>
git clone https://github.com/e1560762/RandomNumberGenerator.git --branch master
```

or download as a zip file and extract the content to a specific folder.
After downloading the source code, you can run the code from command line,

```shell
cd <FOLDER>/RandomNumberGenerator
python run.py -g <number_of_iterations_for_generator> -w <number_of_iterations_for_writer> -f <path_to_file_to_write_most_recently_generated_number> -m <file_mode>
```

## Features
* Generates numbers randomly by their corresponding probabilities and stores most recent 100 numbers.
* Writes most recently produced number to a file.
* Computes the percentages of frequencies of the generated numbers (up to last 100) at any state.
* Both generators and writers can run concurrently.

##Configuration
###Parameters
-g : Integer. Sets number of iterations for generator. If it is less than 1, then the program runs in an infinite loop. Default value is 0. 
-w : Integer. Sets number of iterations for writer. If it is less than 1, then the program runs in an infinite loop. Default value is 0.
-f : String. Sets the path to file to write most recently generated number. Default value is output.txt
-m : String. Sets file mode given with -f parameter. It can be either 'w' or 'a'. Default value is 'w'