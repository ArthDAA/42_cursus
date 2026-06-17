import sys
import typing


try:
	accfold: str = sys.argv[1]
	print(
		"=== Cyber Archives Recovery & Preservation ===\n"
		f"Accessing file '{accfold}'"
	)
	try:
		f: typing.IO = open(accfold, "r")
		contenu: str = f.read()
		f.close()
		print(
			"---\n"
			f"{contenu}"
			"---\n"
			f"File '{accfold}' closed."
		)
		lignes: list = contenu.splitlines()
		nouvelles: list = []
		for ligne in lignes:
			nouvelles.append(ligne + "#")
		transforme: str = "\n".join(nouvelles)
		print(
			"Transform data:\n"
			"---\n"
			f"{transforme}\n"
			"---"
		)
		nom: str = input("Enter new file name (or empty): ")
		if (nom):
			g: typing.IO = open(nom, "w")
			g.write(transforme + "\n")
			g.close()
			print(
				f"Saving data to '{nom}'\n"
				f"Data saved in file '{nom}'."
			)
		else:
			print("Not saving data.")
	except Exception as e:
		print(f"Error opening file '{accfold}': {e}")
except IndexError:
	print("Usage: ft_archive_creation.py <file>")