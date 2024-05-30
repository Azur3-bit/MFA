from fingerprint import FingerPrint 


myfingerPrint = FingerPrint()

try:
	myfingerPrint.open()
	print("hey there ! now place your finger on scanner please :)\n")
	if myfingerPrint.verify():
		print("hey authenicated user \n");
	else:
		print("there always a second chance for everything \n")
finally;
	print("closing connectin with FingerPrint scanner\n")
	myfingerPrint.close()