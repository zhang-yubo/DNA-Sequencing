# Python 3 code to rename multiple
# files in a directory or folder

# importing os module
import os

# Function to rename multiple files
def main():

	folder = "."
	for count, filename in enumerate(os.listdir(folder)):
		
		src = filename # foldername/filename, if .py file is outside folder
		

		dst = f"readmapping{filename[9:]}"
		if count < 5:
			print(dst)
		
		# rename() function will
		# rename all the files
		os.rename(src, dst)

# Driver Code
if __name__ == '__main__':
	
	# Calling main() function
	main()
