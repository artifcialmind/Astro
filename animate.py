root.destroy()
    root2 = tk.Tk()
    canvas2 = tk.Canvas(root2, width=600, height=700)
    temp = os.listdir(path)
    im = []
    for y in temp:
        im.append(ImageTk.PhotoImage(file=path+'/'+y))
    frames = len(im)

    count = 0
    anim = None
    gif_label = tk.Label(image='')
    gif_label.pack()
    def animation(count):
        global anim
        im2 = im[count]

        gif_label.configure(image=im2)
        count += 1
        if count == frames:
            count = 0
        anim = root2.after(40, lambda: animation(count))
    animation(count)
    root2.mainloop()