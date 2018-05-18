test:
	python main.py data/g200reads.fa 8

clean:
	rm debruijn.pyc output/* data/reads_temp.fa

