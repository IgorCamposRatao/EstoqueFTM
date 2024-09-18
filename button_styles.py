def style_button_confirm(button):
    button.config(
        bg="#4CAF50",            
        fg="white",              
        bd=2,                    
        relief="raised",         
        font=("Arial", 10, "bold") 
    )

    # Efeito de passar o mouse sobre o botão
    def on_enter(event):
        button.config(bg="#45a049")  
    def on_leave(event):
        button.config(bg="#4CAF50")  

    # Efeito ao clicar no botão
    def on_click(event):
        button.config(relief="sunken")  

    def on_release(event):
        button.config(relief="raised")  

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress>", on_click)
    button.bind("<ButtonRelease>", on_release)

def style_button_cancel(button):
    button.config(
        bg="#f44336",           
        fg="white",              
        bd=2,                   
        relief="raised",         
        font=("Arial", 10, "bold") 
    )

    # Efeito de passar o mouse sobre o botão
    def on_enter(event):
        button.config(bg="#d32f2f")  

    def on_leave(event):
        button.config(bg="#f44336")  

    # Efeito ao clicar no botão
    def on_click(event):
        button.config(relief="sunken")  

    def on_release(event):
        button.config(relief="raised")  

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress>", on_click)
    button.bind("<ButtonRelease>", on_release)

# Estilo para os demais botões
def style_button_default(button):
    button.config(
        bg="#515151",            
        fg="white",              
        bd=2,                    
        relief="raised",         
        font=("Arial", 10, "bold") 
    )

    # Efeito de passar o mouse sobre o botão
    def on_enter(event):
        button.config(bg="#666666")  

    def on_leave(event):
        button.config(bg="#515151")  

    # Efeito ao clicar no botão
    def on_click(event):
        button.config(relief="sunken")  

    def on_release(event):
        button.config(relief="raised")  

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress>", on_click)
    button.bind("<ButtonRelease>", on_release)


def style_button_default2(button):
    button.config(
        bg="#2699e6",            
        fg="white",              
        bd=2,                    
        relief="raised",         
        font=("Arial", 10, "bold")
    )

    # Efeito de passar o mouse sobre o botão
    def on_enter(event):
        button.config(bg="#1a66cc")  

    def on_leave(event):
        button.config(bg="#2699e6")  

    # Efeito ao clicar no botão
    def on_click(event):
        button.config(relief="sunken")  

    def on_release(event):
        button.config(relief="raised")  

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress>", on_click)
    button.bind("<ButtonRelease>", on_release)
