from tkinter import *

root = Tk()

def update(data):
	listbox.delete(0, END)
	for item in data:
		listbox.insert(END, item)

def fillout(e):
	entry.delete(0, END)
	entry.insert(0, listbox.get(ANCHOR))

def check(e):
	typed = entry.get()
	length_of_typed = len(typed)

	# if there are no characters in entrybox, return the default list
	if typed == '':
		data = wordbox
	# if there is any character in the entrybox, search for data that contains the first occurance of the characters
	else:
		data = []
		for item in wordbox:
			if typed.lower() in item.lower()[0:length_of_typed]:
				data.append(item)
	update(data)

label = Label(root, text="basic search box")
label.pack(pady=20)


entry = Entry(root)
entry.pack()

listbox = Listbox(root, width=50)
listbox.pack(pady=40)


wordbox = ["Walmart", "Tesla", "TSLA", "FNG", "MLX", "JPM"]
update(wordbox)

#binding to listbox
listbox.bind("<<ListboxSelect>>", fillout)

#binding to entrybox
entry.bind("<KeyRelease>", check)


root.mainloop()
