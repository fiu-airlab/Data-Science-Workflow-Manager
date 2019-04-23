OUT_DEST=/home/surge/Documents/DSWM/Data/
FILES = $(shell find /home/surge/Documents/DSWM/Data/CPI/ -type f)

# The all rule allows all the srcipts to be ran when the Makefile is ran using Make
all: cpi oil db1b merged

# Each rule runs a specified script and passes the two directories as command line arguments. The first is the directory where the raw data to be processed is located and the second is the destination of csv file created by the scripts.
# Scripts can be added by creating rules and defining the necessary actions for the script. For the added scripts to run when the Makefile is ran using make they need to be added to the all rule. The merge rule does not include the directories because they are defined in the script directly.
cpi : /home/surge/Documents/DSWM/Data/CPI/ $(FILES)
	python3 cpi_processing.py /home/surge/Documents/DSWM/Data/CPI/ $(OUT_DEST)

oil :
	python3 oil_price_processing.py /home/surge/Documents/Spring2019/CIS4911/DSWM/Data/Oil/ $(OUT_DEST)

db1b :
	python3 db1b_processing.py /home/surge/Documents/Spring2019/CIS4911/DSWM/Data/DB1B/ $(OUT_DEST)

merged : 
	python3 merged_data_processing.py
