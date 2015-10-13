## tying makefile dependencies with SGE_Array job dependencies

done.txt.maked: file1.txt.maked file2.txt.maked
	echo sleep 30\; touch done.txt.maked  | SGE_Array --hold_names jmake_file_1,jmake_file_2,jmake_file_3

file1.txt.maked:
	echo sleep 30\; touch file1.txt.maked | SGE_Array -r jmake_file_1
	
file2.txt.maked:
	echo sleep 30\; touch file2.txt.maked | SGE_Array -r jmake_file_2

file3.txt.maked:
	echo sleep 30\; touch file3.txt.maked | SGE_Array -r jmake_file_3

