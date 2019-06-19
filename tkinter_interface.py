from tkinter import *
from sequence_alignment import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.matrix = []
        self.penalty = 0
        self.sequence_a = ''
        self.sequence_b = ''
        self.solution_a = ''
        self.solution_b = ''

        self.pack()

        frame = StartPage(parent=self)
        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_solution_frame(self):
        frame = SolutionPage(self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise
        

class StartPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.sequence_a_label = Label(self, text="Sequence A")
        self.sequence_a_label.pack()

        self.entry_sequence_a = Entry(self)
        self.entry_sequence_a["width"] = 200
        self.entry_sequence_a.pack()
        
        self.sequence_b_label = Label(self, text="Sequence B")
        self.sequence_b_label.pack()

        self.entry_sequence_b = Entry(self)
        self.entry_sequence_b["width"] = 200
        self.entry_sequence_b.pack()

        self.solve = Button(self, text="Solve", width=50, height=8, bg="#9db4f5", command=self.btn_solve_click)
        self.solve.pack()
        
        self.close = Button(self, text="Quit", width=50, bg="#cc0000", command=self.quit)
        self.close.pack()

    def btn_solve_click(self):
        self.parent.sequence_a = self.entry_sequence_a.get()
        self.parent.sequence_b = self.entry_sequence_b.get()

        self.parent.matrix, self.parent.penalty = build_solution(self.entry_sequence_a.get(), self.entry_sequence_b.get())

        self.parent.solution_a, self.parent.solution_b = find_solution(self.parent.matrix, self.entry_sequence_a.get(), self.entry_sequence_b.get())

        print(self.parent.penalty)
        print(self.parent.solution_a)
        print(self.parent.solution_b)

        self.parent.show_solution_frame()

class SolutionPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label_penalty = Label(self, text="Penalty")
        self.label_penalty.pack()

        self.penalty = Label(self, text=parent.penalty)
        self.penalty.pack()

        self.label_solution_a = Label(self, text="Solution A")
        self.label_solution_a.pack()

        self.solution_a = Label(self, text=parent.solution_a)
        self.solution_a.pack()

        self.label_solution_b = Label(self, text="Solution B")
        self.label_solution_b.pack()

        self.solution_b = Label(self, text=parent.solution_b)
        self.solution_b.pack()

        result = print_solution(parent.matrix, parent.sequence_a, parent.sequence_b)
        self.matrix_solution = Label(self, text=result)
        self.matrix_solution.pack(side=BOTTOM)
        
        self.close = Button(self, text="Quit", width=20, height=10, bg="#cc0000", command=self.quit)
        self.close.pack(side=RIGHT)

if __name__ == '__main__':
    app = Application()
    app.master.title("Sequence Alignment")
    app.master.geometry("1700x600")
    mainloop()
