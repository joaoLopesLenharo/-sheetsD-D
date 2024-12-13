import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from PIL import Image, ImageTk
import io
import base64

# Primeiro, definir a classe BackgroundScreen
class BackgroundScreen:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Background do Personagem")
        
        # Maximizar a janela deixando a barra de tarefas visível
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight() - 60  # Aumentado para 60 pixels
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Criar canvas principal com scrollbar
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        self.main_frame = ttk.Frame(canvas)

        # Configurar scroll
        canvas.configure(yscrollcommand=scrollbar.set)
        self.main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Usar screen_width ao invés de window_width indefinido
        canvas.create_window((0, 0), window=self.main_frame, anchor="nw", width=screen_width-20)  # -20 para compensar scrollbar

        # Empacotar widgets principais
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Criar layout principal com dois frames lado a lado (agora dentro do main_frame)
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side="left", fill="both", padx=5, pady=5)

        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.create_photo_section(left_frame)
        self.create_basic_info_section(left_frame)
        self.create_characteristics_section(right_frame)

        # Carregar dados existentes
        self.load_background()

    def create_photo_section(self, parent):
        """Cria a seção da foto do personagem"""
        photo_frame = ttk.LabelFrame(parent, text="Imagem do Personagem")
        photo_frame.pack(fill="x", padx=5, pady=5)

        # Canvas para a imagem
        self.photo_canvas = tk.Canvas(photo_frame, width=150, height=150)
        self.photo_canvas.pack(pady=5)

        # Carregar foto atual se existir
        self.photo_image = None
        if hasattr(self.parent, 'photo_data') and self.parent.photo_data:
            try:
                image_data = base64.b64decode(self.parent.photo_data)
                image = Image.open(io.BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)
                self.photo_canvas.create_image(0, 0, anchor="nw", image=photo)
                self.photo_image = photo
            except:
                self.set_default_photo()
        else:
            self.set_default_photo()

    def create_basic_info_section(self, parent):
        """Cria a seção de informações básicas"""
        info_frame = ttk.LabelFrame(parent, text="Informações de Identidade")
        info_frame.pack(fill="x", padx=5, pady=5)

        labels = [
            "Idade", "Altura", "Peso", "Olhos", "Pele", "Cabelo"
        ]
        self.identity_vars = {}

        for i, label in enumerate(labels):
            ttk.Label(info_frame, text=label).grid(row=i//2, column=(i%2)*2, padx=5, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(info_frame, textvariable=var)
            entry.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=5)
            self.identity_vars[label] = var

    def set_default_photo(self):
        """Define uma imagem padrão no canvas"""
        self.photo_canvas.delete("all")
        self.photo_canvas.create_rectangle(0, 0, 150, 150, fill="lightgray")
        self.photo_canvas.create_text(75, 75, text="Foto do\nPersonagem", justify="center")

    def create_characteristics_section(self, parent):
        # Frame para características
        char_frame = ttk.Frame(parent)
        char_frame.pack(fill="both", expand=True)

        # Notebook para organizar as diferentes seções
        notebook = ttk.Notebook(char_frame)
        notebook.pack(fill="both", expand=True)

        # Definir as seções com seus subtópicos
        sections = {
            "Desenvolvimento": [
                "Motivações",
                "Objetivos",
                "Medos",
                "Sonhos",
                "Traumas"
            ],
            "Interações": [
                "Relacionamentos",
                "Amizades",
                "Inimizades",
                "Família",
                "Organizações"
            ],
            "História": [
                "Origem",
                "Eventos Importantes",
                "Conquistas",
                "Fracassos",
                "Momentos Marcantes"
            ],
            "Caracterização": [
                "Aparência",
                "Personalidade",
                "Maneirismos",
                "Hábitos",
                "Peculiaridades"
            ]
        }

        self.text_widgets = {}

        # Criar abas para cada seção principal
        for section, subtopics in sections.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=section)
            
            # Criar subframes com scrollbar
            canvas = tk.Canvas(frame)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            canvas.configure(yscrollcommand=scrollbar.set)

            # Configurar scroll
            def on_configure(event, c=canvas, sf=scrollable_frame):
                c.configure(scrollregion=c.bbox("all"))
            
            scrollable_frame.bind("<Configure>", on_configure)
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())

            # Empacotar widgets
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Criar campos para cada subtópico
            for subtopic in subtopics:
                topic_frame = ttk.LabelFrame(scrollable_frame, text=subtopic)
                topic_frame.pack(fill="x", padx=5, pady=5)

                text = tk.Text(topic_frame, wrap=tk.WORD, height=4)
                text.pack(fill="both", expand=True, padx=5, pady=5)

                self.text_widgets[f"{section}_{subtopic}"] = text

        # Frame separado para Alinhamento
        alignment_frame = ttk.LabelFrame(char_frame, text="Alinhamento")
        alignment_frame.pack(fill="x", padx=5, pady=5)

        # Dois Comboboxes para eixos de alinhamento
        moral_frame = ttk.Frame(alignment_frame)
        moral_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(moral_frame, text="Eixo Moral:").pack(side="left", padx=5)
        self.moral_var = tk.StringVar()
        ttk.Combobox(moral_frame, textvariable=self.moral_var,
                    values=["Bom", "Neutro", "Mau"],
                    state="readonly", width=15).pack(side="left", padx=5)

        order_frame = ttk.Frame(alignment_frame)
        order_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(order_frame, text="Eixo da Ordem:").pack(side="left", padx=5)
        self.order_var = tk.StringVar()
        ttk.Combobox(order_frame, textvariable=self.order_var,
                    values=["Leal", "Neutro", "Caótico"],
                    state="readonly", width=15).pack(side="left", padx=5)

        # Botões de controle
        button_frame = ttk.Frame(char_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Salvar", 
                  command=self.save_background).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar", 
                  command=self.clear_all).pack(side="left", padx=5)

    def save_background(self):
        """Salva todas as informações do background"""
        background_data = {
            'identity': {key: var.get() for key, var in self.identity_vars.items()},
            'texts': {key: widget.get("1.0", tk.END).strip() 
                     for key, widget in self.text_widgets.items()},
            'alignment': {
                'moral': self.moral_var.get(),
                'order': self.order_var.get()
            }
        }
        
        self.parent.background_data = background_data
        messagebox.showinfo("Sucesso", "Background salvo com sucesso!")

    def clear_all(self):
        """Limpa todos os campos de texto"""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todos os campos?"):
            for widget in self.text_widgets.values():
                widget.delete("1.0", tk.END)
            self.moral_var.set("")
            self.order_var.set("")

    def load_background(self):
        """Carrega os dados do background se existirem"""
        if hasattr(self.parent, 'background_data') and self.parent.background_data:
            data = self.parent.background_data
            
            # Carregar informações de identidade
            for key, value in data.get('identity', {}).items():
                if key in self.identity_vars:
                    self.identity_vars[key].set(value)
            
            # Carregar textos
            for key, text in data.get('texts', {}).items():
                if key in self.text_widgets:
                    self.text_widgets[key].delete("1.0", tk.END)
                    self.text_widgets[key].insert("1.0", text)
            
            # Carregar alinhamento
            alignment = data.get('alignment', {})
            self.moral_var.set(alignment.get('moral', ''))
            self.order_var.set(alignment.get('order', ''))

# Depois, definir a classe FichaDnD
class FichaDnD:
    def __init__(self, root):
        self.root = root
        self.root.title("Ficha de D&D 5.5E")
        
        # Criar menu
        self.create_menu()
        
        # Maximizar a janela deixando a barra de tarefas visível
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight() - 60  # Aumentado para 60 pixels
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Adicionar variável para armazenar o caminho do arquivo atual
        self.current_file_path = None
        
        # Criar canvas principal com scrollbar
        self.main_canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)

        # Configurar scroll
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame.bind("<Configure>", 
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Empacotar canvas e scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configurar scroll com mousewheel
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Dados de magias e talentos
        self.spells_data = []
        self.abilities_data = []
        self.features_data = []
        self.inventory_data = []
        self.background_data = {}

        # Configurar atalho Ctrl+S
        self.root.bind('<Control-s>', self.quick_save)

        # Sessões de interface (agora usando scrollable_frame como parent)
        self.create_basic_info_section()
        self.create_classes_section()
        self.create_attributes_section()
        self.create_proficiencies_section()
        self.create_combat_section()
        self.create_health_section()
        self.create_control_buttons()

    def create_menu(self):
        """Cria a barra de menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Submenu Exportar
        export_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Exportar", menu=export_menu)
        export_menu.add_command(label="Exportar para JSON", command=self.export_to_json)
        export_menu.add_command(label="Exportar para PDF", command=self.export_to_pdf)
        
        # Submenu Importar
        import_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Importar", menu=import_menu)
        import_menu.add_command(label="Importar de JSON", command=self.import_from_json)
        import_menu.add_command(label="Importar de PDF", command=self.import_from_pdf)
        
        # Adicionar separador e opção de Sair
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

    def _on_mousewheel(self, event):
        """Função para permitir scroll com o mousewheel"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_basic_info_section(self):
        frame = ttk.LabelFrame(self.scrollable_frame, text="Informações Básicas")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame esquerdo para informações textuais
        info_frame = ttk.Frame(frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        labels = ["Nome", "Raça", "Antecedente", "Nível"]
        self.basic_info_vars = {}

        for i, label in enumerate(labels):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            var = tk.StringVar()
            if label == "Nível":
                var.trace('w', self.update_proficiency_bonus)
            entry = ttk.Entry(info_frame, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.basic_info_vars[label] = var

        # Botão Background
        ttk.Button(info_frame, text="Background", 
                   command=self.open_background_screen).grid(row=len(labels), 
                   column=0, columnspan=2, pady=10)

        # Frame direito para a foto
        photo_frame = ttk.Frame(frame)
        photo_frame.pack(side="right", padx=5, pady=5)

        # Canvas para a imagem
        self.photo_canvas = tk.Canvas(photo_frame, width=150, height=150)
        self.photo_canvas.pack(pady=(0, 5))

        # Frame para os botões da foto
        button_frame = ttk.Frame(photo_frame)
        button_frame.pack(fill="x")

        # Botões lado a lado
        ttk.Button(button_frame, text="Selecionar Foto", 
                   command=self.select_photo).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Remover Foto", 
                   command=self.remove_photo).pack(side="left", padx=2)

        # Imagem padrão ou placeholder
        self.photo_data = None
        self.photo_image = None
        self.set_default_photo()

    def set_default_photo(self):
        """Define uma imagem padrão ou placeholder no canvas"""
        self.photo_canvas.delete("all")
        self.photo_canvas.create_rectangle(0, 0, 150, 150, fill="lightgray")
        self.photo_canvas.create_text(75, 75, text="Foto do\nPersonagem", justify="center")
        self.photo_data = None
        self.photo_image = None

    def select_photo(self):
        """Permite ao usuário selecionar uma foto"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Carregar e redimensionar a imagem
                image = Image.open(file_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                
                # Converter imagem para base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                self.photo_data = base64.b64encode(buffered.getvalue()).decode()
                
                # Atualizar canvas
                photo = ImageTk.PhotoImage(image)
                self.photo_canvas.delete("all")
                self.photo_canvas.create_image(0, 0, anchor="nw", image=photo)
                self.photo_image = photo
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem: {str(e)}")
                self.set_default_photo()

    def remove_photo(self):
        """Remove a foto atual e restaura o placeholder"""
        self.set_default_photo()

    def create_classes_section(self):
        frame = ttk.LabelFrame(self.scrollable_frame, text="Classes")
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        classes = ["Classe Primária", "Classe Secundária", "Classe Terciária"]
        self.class_vars = {}

        for i, label in enumerate(classes):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.class_vars[label] = var

    def create_attributes_section(self):
        frame = ttk.LabelFrame(self.scrollable_frame, text="Atributos")
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Frame esquerdo para atributos e saves
        left_frame = ttk.Frame(frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.attribute_vars = {}
        self.modifier_labels = {}
        self.save_vars = {}
        self.save_labels = {}
        attributes = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]

        # Frame para atributos
        attr_frame = ttk.LabelFrame(left_frame, text="Valores Base")
        attr_frame.pack(fill="x", padx=5, pady=5)

        for i, attr in enumerate(attributes):
            ttk.Label(attr_frame, text=attr).grid(row=i, column=0, padx=5, pady=5)
            var = tk.StringVar()
            var.trace('w', lambda *args, attr=attr: self.update_modifiers(attr))
            entry = ttk.Entry(attr_frame, textvariable=var, width=5)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.attribute_vars[attr] = var
            
            # Label para modificador
            mod_label = ttk.Label(attr_frame, text="(+0)")
            mod_label.grid(row=i, column=2, padx=5, pady=5)
            self.modifier_labels[attr] = mod_label

        # Frame para salva-guardas
        save_frame = ttk.LabelFrame(left_frame, text="Salva-Guardas")
        save_frame.pack(fill="x", padx=5, pady=5)

        # Cabeçalho dos saves
        ttk.Label(save_frame, text="Prof.").grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(save_frame, text="Total").grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(save_frame, text="Tipo").grid(row=0, column=2, padx=5, pady=2)

        for i, attr in enumerate(attributes):
            # Checkbox para proficiência em save
            save_var = tk.BooleanVar()
            save_var.trace('w', lambda *args, attr=attr: self.update_saves(attr))
            save_check = ttk.Checkbutton(save_frame, variable=save_var)
            save_check.grid(row=i+1, column=0, padx=5, pady=2)
            self.save_vars[attr] = save_var

            # Label para o total do save
            save_label = ttk.Label(save_frame, text="+0")
            save_label.grid(row=i+1, column=1, padx=5, pady=2)
            self.save_labels[attr] = save_label

            # Label para o nome do save
            ttk.Label(save_frame, text=f"Save de {attr}").grid(row=i+1, column=2, padx=5, pady=2, sticky="w")

        # Novo frame para anotações
        notes_frame = ttk.LabelFrame(frame, text="Anotações")
        notes_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Área de texto para anotações
        self.attr_notes = tk.Text(notes_frame, width=30, height=20)
        self.attr_notes.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbar para as anotações
        notes_scroll = ttk.Scrollbar(notes_frame, orient="vertical", command=self.attr_notes.yview)
        notes_scroll.pack(side="right", fill="y")
        self.attr_notes.configure(yscrollcommand=notes_scroll.set)

    def create_proficiencies_section(self):
        frame = ttk.LabelFrame(self.scrollable_frame, text="Proficiências")
        frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Bônus de Proficiência
        ttk.Label(frame, text="Bônus de Proficiência:").grid(row=0, column=0, padx=5, pady=5)
        self.prof_bonus_label = ttk.Label(frame, text="+2")
        self.prof_bonus_label.grid(row=0, column=1, padx=5, pady=5)

        # Perícias
        self.skill_vars = {}
        skills = {
            "Acrobacia": "DES", "Arcanismo": "INT", "Atletismo": "FOR",
            "Atuação": "CAR", "Enganação": "CAR", "Furtividade": "DES",
            "História": "INT", "Intimidação": "CAR", "Intuição": "SAB",
            "Investigação": "INT", "Lidar com Animais": "SAB", "Medicina": "SAB",
            "Natureza": "INT", "Percepção": "SAB", "Persuasão": "CAR",
            "Prestidigitação": "DES", "Religião": "INT", "Sobrevivência": "SAB"
        }

        for i, (skill, attr) in enumerate(skills.items(), start=1):
            # Frame para cada perícia
            skill_frame = ttk.Frame(frame)
            skill_frame.grid(row=i, column=0, columnspan=3, sticky="w", padx=5)
            
            # Frame para os checkboxes e label
            check_frame = ttk.Frame(skill_frame)
            check_frame.pack(side="left")
            
            # Checkboxes
            prof1_var = tk.BooleanVar()
            prof2_var = tk.BooleanVar()
            
            cb1 = ttk.Checkbutton(check_frame, variable=prof1_var, command=lambda s=skill: self.update_skills_total(s))
            cb1.pack(side="left", padx=2)
            
            cb2 = ttk.Checkbutton(check_frame, variable=prof2_var, command=lambda s=skill: self.update_skills_total(s))
            cb2.pack(side="left", padx=2)
            
            # Label com nome da perícia
            skill_label = ttk.Label(skill_frame, text=f"{skill} ({attr})", width=20, anchor="w")
            skill_label.pack(side="left", padx=(5, 10))
            
            # Entry para bônus extra
            bonus_var = tk.StringVar(value="0")
            bonus_var.trace('w', lambda *args, s=skill: self.update_skills_total(s))
            bonus_entry = ttk.Entry(skill_frame, textvariable=bonus_var, width=3)
            bonus_entry.pack(side="left", padx=5)
            
            # Label para total
            total_label = ttk.Label(skill_frame, text="+0")
            total_label.pack(side="left", padx=5)
            
            # Armazenar todas as variáveis
            self.skill_vars[skill] = {
                "prof1": prof1_var,
                "prof2": prof2_var,
                "attr": attr,
                "bonus": bonus_var,
                "label": total_label
            }

    def update_skills_total(self, skill):
        data = self.skill_vars[skill]
        modifier = self.get_modifier(data["attr"])
        prof_bonus = self.get_proficiency_bonus()
        
        # Calcula bônus de proficiência
        total = modifier
        if data["prof1"].get():
            total += prof_bonus
        if data["prof2"].get():
            total += prof_bonus
            
        # Adiciona bônus extra
        try:
            bonus = int(data["bonus"].get() or 0)
            total += bonus
        except ValueError:
            pass  # Ignora valores inválidos no bônus
        
        # Atualiza label
        data["label"].config(text=f"{'+' if total >= 0 else ''}{total}")

    def update_skills(self):
        """Atualiza todas as perícias"""
        prof_bonus = self.get_proficiency_bonus()
        
        for skill, data in self.skill_vars.items():
            modifier = self.get_modifier(data["attr"])
            total = modifier
            
            if data["prof1"].get():
                total += prof_bonus
            if data["prof2"].get():
                total += prof_bonus
                
            try:
                bonus = int(data["bonus"].get() or 0)
                total += bonus
            except ValueError:
                pass
            
            data["label"].config(text=f"{'+' if total >= 0 else ''}{total}")

    def create_combat_section(self):
        frame = ttk.LabelFrame(self.scrollable_frame, text="Combate")
        frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # CA
        ttk.Label(frame, text="Classe de Armadura:").grid(row=0, column=0, padx=5, pady=5)
        self.base_ac_var = tk.StringVar(value="10")
        ttk.Entry(frame, textvariable=self.base_ac_var, width=5).grid(row=0, column=1, padx=5, pady=5)
        
        # Atributo para CA
        self.ac_attr_var = tk.StringVar(value="DES")
        ttk.Combobox(frame, textvariable=self.ac_attr_var, 
                     values=["FOR", "DES", "CON", "INT", "SAB", "CAR"],
                     width=5).grid(row=0, column=2, padx=5)
        
        # Bônus adicional de CA
        ttk.Label(frame, text="Bônus:").grid(row=0, column=3, padx=5, pady=5)
        self.ac_bonus_var = tk.StringVar(value="0")
        ttk.Entry(frame, textvariable=self.ac_bonus_var, width=5).grid(row=0, column=4, padx=5)
        
        self.ac_label = ttk.Label(frame, text="CA Total: 10")
        self.ac_label.grid(row=0, column=5, padx=5)

        # Lista de bônus de CA
        self.ac_bonus_list = []
        self.ac_bonus_frame = ttk.Frame(frame)
        self.ac_bonus_frame.grid(row=1, column=0, columnspan=6, sticky="ew")
        
        ttk.Button(frame, text="Adicionar Bônus CA",
                   command=self.add_ac_bonus).grid(row=2, column=0, columnspan=6, pady=5)

        # CD de Magias
        cd_frame = ttk.LabelFrame(frame, text="CD de Magias")
        cd_frame.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

        # Atributo base
        ttk.Label(cd_frame, text="Atributo:").grid(row=0, column=0, padx=5, pady=5)
        self.spell_attr_var = tk.StringVar(value="INT")
        ttk.Combobox(cd_frame, textvariable=self.spell_attr_var,
                     values=["INT", "SAB", "CAR"],
                     width=5).grid(row=0, column=1, padx=5)
        
        # Bônus adicional
        ttk.Label(cd_frame, text="Bônus:").grid(row=0, column=2, padx=5, pady=5)
        self.cd_bonus_var = tk.StringVar(value="0")
        ttk.Entry(cd_frame, textvariable=self.cd_bonus_var, width=5).grid(row=0, column=3, padx=5)
        
        # Lista de bônus extras
        self.cd_bonus_list = []
        bonus_list_frame = ttk.Frame(cd_frame)
        bonus_list_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
        # Botão para adicionar novo bônus
        ttk.Button(cd_frame, text="Adicionar Bônus CD",
                   command=self.add_cd_bonus).grid(row=2, column=0, columnspan=4, pady=5)
        
        # Label para CD total
        self.cd_label = ttk.Label(cd_frame, text="CD: 8")
        self.cd_label.grid(row=3, column=0, columnspan=4, pady=5)

        # Frame para lista de bônus
        self.cd_bonus_frame = ttk.Frame(cd_frame)
        self.cd_bonus_frame.grid(row=4, column=0, columnspan=4, sticky="ew")

        # Configurar traces para atualização automática
        self.base_ac_var.trace('w', self.update_ac)
        self.ac_attr_var.trace('w', self.update_ac)
        self.ac_bonus_var.trace('w', self.update_ac)
        self.spell_attr_var.trace('w', self.update_spell_dc)
        self.cd_bonus_var.trace('w', self.update_spell_dc)

        # Adicionar label para Percepção Passiva
        ttk.Label(frame, text="Percepção Passiva:").grid(row=4, column=0, padx=5, pady=5)
        self.passive_perception_label = ttk.Label(frame, text="10")
        self.passive_perception_label.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

    def add_cd_bonus(self):
        """Adiciona um novo bônus à CD"""
        bonus_frame = ttk.Frame(self.cd_bonus_frame)
        bonus_frame.pack(fill="x", pady=2)
        
        # Descrição do bônus
        ttk.Label(bonus_frame, text="Fonte:").pack(side="left", padx=2)
        desc_var = tk.StringVar()
        ttk.Entry(bonus_frame, textvariable=desc_var, width=15).pack(side="left", padx=2)
        
        # Valor do bônus
        ttk.Label(bonus_frame, text="Valor:").pack(side="left", padx=2)
        value_var = tk.StringVar(value="0")
        entry = ttk.Entry(bonus_frame, textvariable=value_var, width=5)
        entry.pack(side="left", padx=2)
        
        # Configurar trace para atualização automática
        value_var.trace('w', self.update_spell_dc)
        
        # Botão remover
        remove_btn = ttk.Button(bonus_frame, text="X", width=2,
                               command=lambda: self.remove_cd_bonus(bonus_frame))
        remove_btn.pack(side="left", padx=2)
        
        # Adicionar à lista de bônus
        bonus_data = {
            'frame': bonus_frame,
            'desc': desc_var,
            'value': value_var
        }
        self.cd_bonus_list.append(bonus_data)
        
        # Atualizar CD total
        self.update_spell_dc()

    def remove_cd_bonus(self, frame):
        """Remove um bônus da CD"""
        self.cd_bonus_list = [b for b in self.cd_bonus_list if b['frame'] != frame]
        frame.destroy()
        self.update_spell_dc()

    def update_spell_dc(self, *args):
        """Atualiza o valor total da CD"""
        try:
            # Base 8 + proficiência + modificador
            base = 8
            prof_bonus = self.get_proficiency_bonus()
            attr_mod = self.get_modifier(self.spell_attr_var.get())
            
            # Bônus adicional padrão
            try:
                bonus = int(self.cd_bonus_var.get() or 0)
            except ValueError:
                bonus = 0
                
            # Somar bônus extras
            for bonus_data in self.cd_bonus_list:
                try:
                    bonus += int(bonus_data['value'].get() or 0)
                except ValueError:
                    continue
            
            total = base + prof_bonus + attr_mod + bonus
            self.cd_label.config(text=f"CD: {total}")
        except:
            self.cd_label.config(text="CD: 8")

    def add_ac_bonus(self):
        """Adiciona um novo bônus à CA"""
        bonus_frame = ttk.Frame(self.ac_bonus_frame)
        bonus_frame.pack(fill="x", pady=2)
        
        ttk.Label(bonus_frame, text="Fonte:").pack(side="left", padx=2)
        desc_var = tk.StringVar()
        ttk.Entry(bonus_frame, textvariable=desc_var, width=15).pack(side="left", padx=2)
        
        ttk.Label(bonus_frame, text="Valor:").pack(side="left", padx=2)
        value_var = tk.StringVar(value="0")
        entry = ttk.Entry(bonus_frame, textvariable=value_var, width=5)
        entry.pack(side="left", padx=2)
        
        # Configurar trace para atualizaç��o automática
        value_var.trace('w', self.update_ac)
        
        remove_btn = ttk.Button(bonus_frame, text="X", width=2,
                               command=lambda: self.remove_ac_bonus(bonus_frame))
        remove_btn.pack(side="left", padx=2)
        
        bonus_data = {
            'frame': bonus_frame,
            'desc': desc_var,
            'value': value_var
        }
        self.ac_bonus_list.append(bonus_data)
        
        # Atualizar CA total
        self.update_ac()

    def remove_ac_bonus(self, frame):
        """Remove um bônus da CA"""
        self.ac_bonus_list = [b for b in self.ac_bonus_list if b['frame'] != frame]
        frame.destroy()
        self.update_ac()

    def update_ac(self, *args):
        """Atualiza o valor total da CA"""
        try:
            base = int(self.base_ac_var.get() or 10)
            attr_mod = self.get_modifier(self.ac_attr_var.get())
            
            # Bônus adicional padrão
            try:
                bonus = int(self.ac_bonus_var.get() or 0)
            except ValueError:
                bonus = 0
                
            # Somar bônus extras
            for bonus_data in self.ac_bonus_list:
                try:
                    bonus += int(bonus_data['value'].get() or 0)
                except ValueError:
                    continue
            
            total = base + attr_mod + bonus
            self.ac_label.config(text=f"CA Total: {total}")
        except:
            self.ac_label.config(text="CA Total: 10")

    def create_health_section(self):
        frame = ttk.LabelFrame(self.scrollable_frame, text="Recursos")
        frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Frame para recursos padrão
        default_frame = ttk.Frame(frame)
        default_frame.pack(fill="x", padx=5, pady=5)

        resources = ["Vida", "Mana", "Estamina"]
        self.resources_vars = {}
        self.resources_max_vars = {}

        for i, resource in enumerate(resources):
            ttk.Label(default_frame, text=resource).grid(row=i, column=0, padx=5, pady=5)
            
            # Valor atual
            var_atual = tk.StringVar()
            entry_atual = ttk.Entry(default_frame, textvariable=var_atual, width=5)
            entry_atual.grid(row=i, column=1, padx=5, pady=5)
            self.resources_vars[resource] = var_atual
            
            ttk.Label(default_frame, text="/").grid(row=i, column=2)
            
            # Valor máximo
            var_max = tk.StringVar()
            entry_max = ttk.Entry(default_frame, textvariable=var_max, width=5)
            entry_max.grid(row=i, column=3, padx=5, pady=5)
            self.resources_max_vars[resource] = var_max

        # Separador
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=5, pady=10)

        # Frame para recursos customizados
        custom_frame = ttk.Frame(frame)
        custom_frame.pack(fill="x", padx=5, pady=5)

        # Lista para armazenar recursos customizados
        self.custom_resources = []

        # Botão para adicionar novo recurso
        ttk.Button(custom_frame, text="Adicionar Recurso", 
                   command=self.add_custom_resource).pack(pady=5)

        # Frame para listar recursos customizados
        self.custom_resources_frame = ttk.Frame(frame)
        self.custom_resources_frame.pack(fill="x", padx=5, pady=5)

    def add_custom_resource(self):
        # Criar novo frame para o recurso
        resource_frame = ttk.Frame(self.custom_resources_frame)
        resource_frame.pack(fill="x", pady=2)

        # Entry para nome do recurso
        name_var = tk.StringVar()
        name_entry = ttk.Entry(resource_frame, textvariable=name_var, width=15)
        name_entry.pack(side="left", padx=2)

        # Valor atual
        atual_var = tk.StringVar()
        atual_entry = ttk.Entry(resource_frame, textvariable=atual_var, width=5)
        atual_entry.pack(side="left", padx=2)

        # Separador
        ttk.Label(resource_frame, text="/").pack(side="left", padx=2)

        # Valor máximo
        max_var = tk.StringVar()
        max_entry = ttk.Entry(resource_frame, textvariable=max_var, width=5)
        max_entry.pack(side="left", padx=2)

        # Botão remover
        remove_btn = ttk.Button(resource_frame, text="X", width=2,
                               command=lambda: self.remove_custom_resource(resource_frame))
        remove_btn.pack(side="left", padx=2)

        # Adicionar à lista de recursos
        self.custom_resources.append({
            'frame': resource_frame,
            'name': name_var,
            'atual': atual_var,
            'max': max_var
        })

    def remove_custom_resource(self, frame):
        # Remover da lista
        self.custom_resources = [r for r in self.custom_resources if r['frame'] != frame]
        # Destruir frame
        frame.destroy()

    def create_control_buttons(self):
        frame = ttk.Frame(self.scrollable_frame)
        frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(frame, text="Tela de Magias", command=self.open_spells_screen).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Tela de Talentos", command=self.open_abilities_screen).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Inventário", command=self.open_inventory_screen).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame, text="Habilidades", command=self.open_features_screen).grid(row=0, column=3, padx=5, pady=5)

    def open_spells_screen(self):
        SpellScreen(self)

    def open_abilities_screen(self):
        AbilityScreen(self)

    def open_inventory_screen(self):
        InventoryScreen(self)

    def open_features_screen(self):
        FeatureScreen(self)

    def quick_save(self, event=None):
        """Salva rapidamente no arquivo atual ou abre diálogo se não houver arquivo"""
        if self.current_file_path:
            self.export_to_json(self.current_file_path)
        else:
            self.export_to_json()

    def export_to_json(self, file_path=None):
        """Exporta os dados para um arquivo JSON"""
        if not file_path:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")],
                initialfile="ficha_dnd.json"
            )
        
        if file_path:
            try:
                # Preparar dados para salvar
                data = {
                    'version': '1.2',
                    'filename': os.path.basename(file_path),
                    'photo_data': self.photo_data,  # Armazenar a imagem como base64
                    'basic_info': {key: var.get() for key, var in self.basic_info_vars.items()},
                    'classes': {key: var.get() for key, var in self.class_vars.items()},
                    'attributes': {
                        attr: {
                            'value': var.get(),
                            'modifier': self.modifier_labels[attr].cget('text'),
                            'save_proficiency': self.save_vars[attr].get(),
                            'save_total': self.save_labels[attr].cget('text')
                        } for attr, var in self.attribute_vars.items()
                    },
                    'attribute_notes': self.attr_notes.get('1.0', tk.END).strip(),
                    'skills': {
                        skill: {
                            'prof1': data['prof1'].get(),
                            'prof2': data['prof2'].get(),
                            'bonus': data['bonus'].get(),
                            'total': data['label'].cget('text')
                        } for skill, data in self.skill_vars.items()
                    },
                    'resources': {
                        resource: {
                            'atual': self.resources_vars[resource].get(),
                            'max': self.resources_max_vars[resource].get()
                        } for resource in self.resources_vars.keys()
                    },
                    'custom_resources': [
                        {
                            'name': resource['name'].get(),
                            'atual': resource['atual'].get(),
                            'max': resource['max'].get()
                        } for resource in self.custom_resources
                    ],
                    'spells': self.spells_data,
                    'abilities': self.abilities_data,
                    'features': self.features_data,
                    'inventory': self.inventory_data,
                    'background': self.background_data,
                    
                    # Adicionar dados da CA
                    'armor_class': {
                        'base': self.base_ac_var.get(),
                        'attr': self.ac_attr_var.get(),
                        'bonus': self.ac_bonus_var.get(),
                        'bonus_list': [
                            {
                                'desc': bonus['desc'].get(),
                                'value': bonus['value'].get()
                            }
                            for bonus in self.ac_bonus_list
                        ]
                    },
                }

                # Salvar JSON
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                
                # Atualizar caminho do arquivo atual
                self.current_file_path = file_path
                # Atualizar título da janela
                self.root.title(f"Ficha de D&D 5.5E - {os.path.basename(file_path)}")
                
                messagebox.showinfo("Sucesso", "Ficha salva com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar a ficha: {str(e)}")

    def import_from_json(self, file_path=None):
        """Importa dados de um arquivo JSON"""
        if not file_path:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON Files", "*.json")],
                initialfile="ficha_dnd.json"
            )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Carregar imagem se existir
                self.photo_data = data.get('photo_data', None)
                self.load_existing_photo()

                # Carregar informações básicas
                for key, value in data.get('basic_info', {}).items():
                    if key in self.basic_info_vars:
                        self.basic_info_vars[key].set(value)

                # Carregar classes
                for key, value in data.get('classes', {}).items():
                    if key in self.class_vars:
                        self.class_vars[key].set(value)

                # Carregar atributos
                for attr, value in data.get('attributes', {}).items():
                    if attr in self.attribute_vars:
                        if isinstance(value, dict):
                            self.attribute_vars[attr].set(value.get('value', '10'))
                            if attr in self.save_vars:
                                self.save_vars[attr].set(value.get('save_proficiency', False))
                        else:
                            # Para compatibilidade com versões antigas
                            self.attribute_vars[attr].set(value)

                # Carregar anotações de atributos
                if 'attribute_notes' in data:
                    self.attr_notes.delete('1.0', tk.END)
                    self.attr_notes.insert('1.0', data['attribute_notes'])

                # Carregar perícias
                for skill, skill_data in data.get('skills', {}).items():
                    if skill in self.skill_vars:
                        if isinstance(skill_data, dict):
                            self.skill_vars[skill]['prof1'].set(skill_data.get('prof1', False))
                            self.skill_vars[skill]['prof2'].set(skill_data.get('prof2', False))
                            self.skill_vars[skill]['bonus'].set(skill_data.get('bonus', '0'))

                # Carregar recursos
                for resource, value in data.get('resources', {}).items():
                    if resource in self.resources_vars:
                        self.resources_vars[resource].set(value.get('atual', '0'))
                        self.resources_max_vars[resource].set(value.get('max', '0'))

                # Carregar recursos customizados
                self.clear_custom_resources()
                for custom_resource in data.get('custom_resources', []):
                    self.add_custom_resource()
                    last_resource = self.custom_resources[-1]
                    last_resource['name'].set(custom_resource.get('name', ''))
                    last_resource['atual'].set(custom_resource.get('atual', '0'))
                    last_resource['max'].set(custom_resource.get('max', '0'))

                # Carregar dados adicionais
                self.spells_data = data.get('spells', [])
                self.abilities_data = data.get('abilities', [])
                self.features_data = data.get('features', [])
                self.inventory_data = data.get('inventory', [])
                self.background_data = data.get('background', {})

                # Atualizar caminho do arquivo atual
                self.current_file_path = file_path
                # Atualizar título da janela
                self.root.title(f"Ficha de D&D 5.5E - {os.path.basename(file_path)}")

                # Carregar dados da CA
                ac_data = data.get('armor_class', {})
                self.base_ac_var.set(ac_data.get('base', '10'))
                self.ac_attr_var.set(ac_data.get('attr', 'DES'))
                self.ac_bonus_var.set(ac_data.get('bonus', '0'))
                
                # Limpar e recarregar bônus extras da CA
                for bonus in self.ac_bonus_list:
                    bonus['frame'].destroy()
                self.ac_bonus_list.clear()
                
                for bonus in ac_data.get('bonus_list', []):
                    self.add_ac_bonus()
                    last_bonus = self.ac_bonus_list[-1]
                    last_bonus['desc'].set(bonus.get('desc', ''))
                    last_bonus['value'].set(bonus.get('value', '0'))
                
                # Atualizar CA total
                self.update_ac()

                # Atualizar todos os cálculos
                self.update_all()

                messagebox.showinfo("Sucesso", "Ficha carregada com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar a ficha: {str(e)}")
                import traceback
                traceback.print_exc()

    def load_existing_photo(self):
        """Carrega uma foto existente a partir dos dados em base64"""
        try:
            if self.photo_data:
                image_data = base64.b64decode(self.photo_data)
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.photo_canvas.delete("all")
                self.photo_canvas.create_image(0, 0, anchor="nw", image=photo)
                self.photo_image = photo  # Manter referência para evitar garbage collection
            else:
                self.set_default_photo()
        except Exception as e:
            print(f"Erro ao carregar foto: {str(e)}")
            self.set_default_photo()

    def save_last_file_path(self, file_path):
        """Salva o caminho do último arquivo usado"""
        try:
            config_dir = os.path.join(os.path.expanduser('~'), '.ficha_dnd')
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                
            config_file = os.path.join(config_dir, 'last_file.txt')
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(file_path)
        except Exception as e:
            print(f"Erro ao salvar caminho do arquivo: {str(e)}")
            # Não exibir mensagem de erro para o usuário, pois isso é apenas uma funcionalidade auxiliar

    def get_last_file_path(self):
        """Recupera o caminho do último arquivo usado"""
        try:
            config_file = os.path.join(os.path.expanduser('~'), '.ficha_dnd', 'last_file.txt')
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except Exception:
            pass
        return None

    def clear_custom_resources(self):
        """Limpa todos os recursos customizados"""
        for resource in self.custom_resources:
            for widget in resource['frame'].winfo_children():
                widget.destroy()
            resource['frame'].destroy()
        self.custom_resources.clear()

    def update_all(self):
        """Atualiza todos os valores calculados"""
        # Atualizar modificadores de atributos
        for attr in ["FOR", "DES", "CON", "INT", "SAB", "CAR"]:
            self.update_modifiers(attr)  
        
        # Atualizar bônus de proficiência
        self.update_proficiency_bonus()
        
        # Atualizar CA
        if hasattr(self, 'ac_attr_var'):
            self.update_ac()
        
        # Atualizar CD de magias
        if hasattr(self, 'spell_attr_var'):
            self.update_spell_dc()
        
        # Atualizar perícias
        self.update_skills()  # Removido o argumento skill_data
        
        # Atualizar percepção passiva
        self.update_passive_perception()

    def update_modifiers(self, attr):
        try:
            value = int(self.attribute_vars[attr].get())
            modifier = (value - 10) // 2
            sign = "+" if modifier >= 0 else ""
            self.modifier_labels[attr].config(text=f"({sign}{modifier})")
            
            self.update_saves(attr)
            
            # Atualizar perícias relacionadas
            self.update_skills()  # Removido o argumento data
            
            if hasattr(self, 'ac_attr_var') and self.ac_attr_var.get() == attr:
                self.update_ac()
            
            if hasattr(self, 'spell_attr_var') and self.spell_attr_var.get() == attr:
                self.update_spell_dc()
            
            if attr == "SAB":
                self.update_passive_perception()
            
        except ValueError:
            self.modifier_labels[attr].config(text="(+0)")

    def update_saves(self, attr=None):
        try:
            nivel = int(self.basic_info_vars["Nível"].get())
            prof_bonus = 2 + ((nivel - 1) // 4)
        except ValueError:
            prof_bonus = 2

        for attribute, var in self.attribute_vars.items():
            try:
                value = int(var.get())
                modifier = (value - 10) // 2
                
                # Adiciona bônus de proficiência se tiver proficiência no save
                if self.save_vars[attribute].get():
                    total = modifier + prof_bonus
                else:
                    total = modifier
                
                self.save_labels[attribute].config(text=f"{'+' if total >= 0 else ''}{total}")
            except ValueError:
                self.save_labels[attribute].config(text="+0")

    def get_modifier(self, attr):
        try:
            value = int(self.attribute_vars[attr].get())
            return (value - 10) // 2
        except (ValueError, KeyError):
            return 0

    def update_passive_perception(self):
        """Atualiza o valor da percepção passiva"""
        try:
            # Base 10 + modificador de Sabedoria + bônus de proficiência se aplicável
            wis_mod = self.get_modifier("SAB")
            base = 10
            bonus = 0
            
            # Verificar proficiência em Percepção
            if "Percepção" in self.skill_vars:
                skill_data = self.skill_vars["Percepção"]
                prof_bonus = self.get_proficiency_bonus()
                
                if skill_data['prof1'].get():
                    bonus += prof_bonus
                if skill_data['prof2'].get():
                    bonus += prof_bonus
                    
                # Adicionar bônus extra da perícia
                try:
                    bonus += int(skill_data['bonus'].get() or 0)
                except ValueError:
                    pass
            
            passive = base + wis_mod + bonus
            self.passive_perception_label.config(text=str(passive))
        except Exception as e:
            print(f"Erro ao atualizar percepção passiva: {str(e)}")
            self.passive_perception_label.config(text="10")

    def get_proficiency_bonus(self):
        try:
            nivel = int(self.basic_info_vars["Nível"].get())
            # Cálculo do bônus de proficiência padrão do D&D 5e
            if nivel >= 17:
                return 6
            elif nivel >= 13:
                return 5
            elif nivel >= 9:
                return 4
            elif nivel >= 5:
                return 3
            else:
                return 2
        except ValueError:
            return 2

    def update_proficiency_bonus(self, *args):
        bonus = self.get_proficiency_bonus()
        self.prof_bonus_label.config(text=f"+{bonus}")
        # Atualiza todas as perícias, saves e CD de magias
        self.update_skills()
        self.update_saves()
        self.update_spell_dc()
        self.update_passive_perception()

    def export_to_pdf(self):
        """Exporta a ficha para PDF"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="ficha_dnd.pdf"
        )
        
        if not file_path:
            return

        try:
            # Criar PDF
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4

            # Definir fonte e tamanho padrão
            c.setFont("Helvetica-Bold", 14)
            
            # Informações Básicas
            c.drawString(50, height - 50, "FICHA DE PERSONAGEM D&D 5.5E")
            c.setFont("Helvetica", 12)
            
            y = height - 80
            for key, var in self.basic_info_vars.items():
                c.drawString(50, y, f"{key}: {var.get()}")
                y -= 20

            # Classes
            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "CLASSES")
            c.setFont("Helvetica", 12)
            y -= 20
            for key, var in self.class_vars.items():
                c.drawString(50, y, f"{key}: {var.get()}")
                y -= 20

            # Atributos e Saves
            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "ATRIBUTOS E SAVES")
            c.setFont("Helvetica", 12)
            y -= 20
            
            for attr, var in self.attribute_vars.items():
                mod = self.modifier_labels[attr].cget('text')
                save = self.save_labels[attr].cget('text')
                prof = "✓" if self.save_vars[attr].get() else "□"
                c.drawString(50, y, f"{attr}: {var.get()} {mod} | Save: {save} {prof}")
                y -= 20

            # Anotações dos Atributos
            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "ANOTAÇÕES DOS ATRIBUTOS")
            c.setFont("Helvetica", 10)
            y -= 20
            
            notes = self.attr_notes.get("1.0", tk.END).strip().split('\n')
            for note in notes:
                if y < 50:  # Nova página se necessário
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = height - 50
                c.drawString(50, y, note)
                y -= 15

            # Perícias
            c.showPage()
            y = height - 50
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "PERÍCIAS")
            c.setFont("Helvetica", 12)
            y -= 20

            for skill, data in self.skill_vars.items():
                prof1 = "✓" if data['prof1'].get() else "□"
                prof2 = "✓" if data['prof2'].get() else "□"
                total = data['label'].cget('text')
                c.drawString(50, y, f"{skill} [{prof1}{prof2}] {total}")
                y -= 20

            # Recursos
            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "RECURSOS")
            c.setFont("Helvetica", 12)
            y -= 20

            for resource, var in self.resources_vars.items():
                atual = var.get()
                maximo = self.resources_max_vars[resource].get()
                c.drawString(50, y, f"{resource}: {atual}/{maximo}")
                y -= 20

            # Recursos Customizados
            if self.custom_resources:
                y -= 20
                c.drawString(50, y, "Recursos Customizados:")
                y -= 20
                for resource in self.custom_resources:
                    nome = resource['name'].get()
                    atual = resource['atual'].get()
                    maximo = resource['max'].get()
                    c.drawString(50, y, f"{nome}: {atual}/{maximo}")
                    y -= 20

            # Magias
            c.showPage()
            y = height - 50
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "MAGIAS")
            c.setFont("Helvetica", 10)
            y -= 20

            for spell in self.spells_data:
                if y < 100:  # Nova página se necessário
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = height - 50

                c.drawString(50, y, f"Nível {spell['nivel']}: {spell['nome']}")
                y -= 15
                c.drawString(70, y, f"Escola: {spell['escola']}")
                y -= 15
                c.drawString(70, y, f"Tempo: {spell['tempo_conjuracao']}")
                y -= 15
                c.drawString(70, y, f"Alcance: {spell['alcance']}")
                y -= 15
                c.drawString(70, y, f"Componentes: {spell['componentes']}")
                y -= 15
                c.drawString(70, y, f"Duração: {spell['duracao']}")
                y -= 15
                
                # Quebrar descrição em linhas
                desc_lines = spell['descricao'].split('\n')
                for line in desc_lines:
                    if y < 50:
                        c.showPage()
                        c.setFont("Helvetica", 10)
                        y = height - 50
                    c.drawString(70, y, line)
                    y -= 15
                y -= 10

            # Talentos
            c.showPage()
            y = height - 50
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "TALENTOS")
            c.setFont("Helvetica", 10)
            y -= 20

            for ability in self.abilities_data:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = height - 50

                c.drawString(50, y, ability['nome'])
                y -= 15
                desc_lines = ability['descricao'].split('\n')
                for line in desc_lines:
                    if y < 50:
                        c.showPage()
                        c.setFont("Helvetica", 10)
                        y = height - 50
                    c.drawString(70, y, line)
                    y -= 15
                y -= 10

            # Inventário
            c.showPage()
            y = height - 50
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "INVENTÁRIO")
            c.setFont("Helvetica", 10)
            y -= 20

            for item in self.inventory_data:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = height - 50

                c.drawString(50, y, f"{item['nome']} ({item['tipo']}")
                y -= 15
                
                # Bônus de atributos
                bonus_str = ", ".join([f"{attr}: {val}" for attr, val in item['bonus_atributos'].items() if val != '0'])
                if bonus_str:
                    c.drawString(70, y, f"Bônus de Atributos: {bonus_str}")
                    y -= 15

                if item['bonus_ca'] != '0':
                    c.drawString(70, y, f"Bônus de CA: {item['bonus_ca']}")
                    y -= 15

                if item['bonus_cd'] != '0':
                    c.drawString(70, y, f"Bônus de CD: {item['bonus_cd']}")
                    y -= 15

                if item['dano_dado']:
                    dano_str = f"Dano: {item['dano_dado']}"
                    if item['dano_tipo']:
                        dano_str += f" ({item['dano_tipo']})"
                    c.drawString(70, y, dano_str)
                    y -= 15

                desc_lines = item['descricao'].split('\n')
                for line in desc_lines:
                    if y < 50:
                        c.showPage()
                        c.setFont("Helvetica", 10)
                        y = height - 50
                    c.drawString(70, y, line)
                    y -= 15
                y -= 10

            c.save()
            messagebox.showinfo("Sucesso", "PDF exportado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar PDF: {str(e)}")

    def import_from_pdf(self):
        """Importa dados de um PDF"""
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="ficha_dnd.pdf"
        )
        
        if not file_path:
            return

        try:
            import PyPDF2
            
            extracted_data = {
                'basic_info': {},
                'classes': {},
                'attributes': {},
                'attribute_notes': '',
                'skills': {},
                'resources': {},
                'custom_resources': [],
                'spells': [],
                'abilities': [],
                'features': [],
                'inventory': []
            }

            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                full_text = ""
                for page in reader.pages:
                    full_text += page.extract_text() + "\n"

            # Dividir o texto em seções
            sections = full_text.split("\n")
            current_section = None
            current_item = None
            buffer = []

            for line in sections:
                line = line.strip()
                
                # Identificar seções principais
                if line.startswith("FICHA DE PERSONAGEM"):
                    current_section = "basic_info"
                    continue
                elif line == "CLASSES":
                    current_section = "classes"
                    continue
                elif line == "ATRIBUTOS E SAVES":
                    current_section = "attributes"
                    continue
                elif line == "ANOTAÇÕES DOS ATRIBUTOS":
                    current_section = "attribute_notes"
                    continue
                elif line == "PERÍCIAS":
                    current_section = "skills"
                    continue
                elif line == "RECURSOS":
                    current_section = "resources"
                    continue
                elif line == "MAGIAS":
                    current_section = "spells"
                    continue
                elif line == "TALENTOS":
                    current_section = "abilities"
                    continue
                elif line == "INVENTÁRIO":
                    current_section = "inventory"
                    continue

                # Processar linha baseado na seção atual
                if current_section == "basic_info":
                    if ":" in line:
                        key, value = line.split(":", 1)
                        extracted_data['basic_info'][key.strip()] = value.strip()
                
                elif current_section == "classes":
                    if ":" in line:
                        key, value = line.split(":", 1)
                        extracted_data['classes'][key.strip()] = value.strip()
                
                elif current_section == "attributes":
                    if ":" in line and "|" in line:
                        attr_part, save_part = line.split("|")
                        attr_name = attr_part.split(":")[0].strip()
                        attr_value = attr_part.split(":")[1].split()[0].strip()
                        modifier = attr_part.split(":")[1].split()[1].strip()
                        save_value = save_part.split(":")[1].split()[0].strip()
                        save_prof = "✓" in save_part
                        
                        extracted_data['attributes'][attr_name] = {
                            'value': attr_value,
                            'modifier': modifier,
                            'save_total': save_value,
                            'save_proficiency': save_prof
                        }
                
                elif current_section == "attribute_notes":
                    if line:
                        buffer.append(line)
                    extracted_data['attribute_notes'] = "\n".join(buffer)
                
                elif current_section == "skills":
                    if "[" in line and "]" in line:
                        skill_name = line[:line.find("[")].strip()
                        profs = line[line.find("[")+1:line.find("]")].strip()
                        total = line[line.find("]")+1:].strip()
                        
                        extracted_data['skills'][skill_name] = {
                            'prof1': "✓" in profs[0],
                            'prof2': "✓" in profs[1],
                            'total': total,
                            'bonus': '0'  # Valor padrão
                        }
                
                # ... continuar com o processamento das outras seções ...

            # Atualizar interface com dados extraídos
            self._update_interface_from_extracted_data(extracted_data)
            messagebox.showinfo("Sucesso", "Dados importados do PDF com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar PDF: {str(e)}")
            import traceback
            traceback.print_exc()

    def _update_interface_from_extracted_data(self, data):
        """Atualiza a interface com os dados extraídos"""
        
        # Atualizar informações básicas
        for key, value in data['basic_info'].items():
            if key in self.basic_info_vars:
                self.basic_info_vars[key].set(value)
        
        # Atualizar atributos
        for attr, value in data['attributes'].items():
            if attr in self.attribute_vars:
                self.attribute_vars[attr].set(value)
        
        # Atualizar magias
        self.spells_data = data['spells']
        
        # Atualizar talentos
        self.abilities_data = data['abilities']
        
        # Atualizar habilidades
        self.features_data = data['features']
        
        # Atualizar inventário
        self.inventory_data = data['inventory']
        
        # Atualizar recursos
        for resource, values in data['resources'].items():
            if resource in self.resources_vars:
                self.resources_vars[resource].set(values['atual'])
                self.resources_max_vars[resource].set(values['max'])
        
        # Atualizar recursos customizados
        if 'custom_resources' in data:
            for custom_resource in data['custom_resources']:
                self.add_custom_resource()
                last_resource = self.custom_resources[-1]
                last_resource['name'].set(custom_resource['nome'])
                last_resource['atual'].set(custom_resource['atual'])
                last_resource['max'].set(custom_resource['max'])
        
        # Atualizar modificadores e outros cálculos
        self.update_modifiers()
        self.update_proficiency_bonus()
        self.update_ac()
        self.update_spell_dc()
        self.update_passive_perception()
        
        # Carregar dados da CA
        if 'armor_class' in data:
            ac_data = data['armor_class']
            
            # Carregar valores base
            self.base_ac_var.set(ac_data.get('base', '10'))
            self.ac_attr_var.set(ac_data.get('attr', 'DES'))
            self.ac_bonus_var.set(ac_data.get('bonus', '0'))
            
            # Limpar bônus existentes
            for bonus in self.ac_bonus_list:
                bonus['frame'].destroy()
            self.ac_bonus_list.clear()
            
            # Recriar lista de bônus
            for bonus_data in ac_data.get('bonus_list', []):
                # Criar novo frame de bônus
                bonus_frame = ttk.Frame(self.ac_bonus_frame)
                bonus_frame.pack(fill="x", pady=2)
                
                # Descrição do bônus
                ttk.Label(bonus_frame, text="Fonte:").pack(side="left", padx=2)
                desc_var = tk.StringVar(value=bonus_data.get('desc', ''))
                ttk.Entry(bonus_frame, textvariable=desc_var, width=15).pack(side="left", padx=2)
                
                # Valor do bônus
                ttk.Label(bonus_frame, text="Valor:").pack(side="left", padx=2)
                value_var = tk.StringVar(value=bonus_data.get('value', '0'))
                entry = ttk.Entry(bonus_frame, textvariable=value_var, width=5)
                entry.pack(side="left", padx=2)
                
                # Botão remover
                remove_btn = ttk.Button(bonus_frame, text="X", width=2,
                                  command=lambda f=bonus_frame: self.remove_ac_bonus(f))
                remove_btn.pack(side="left", padx=2)
                
                # Adicionar à lista de bônus
                self.ac_bonus_list.append({
                    'frame': bonus_frame,
                    'desc': desc_var,
                    'value': value_var
                })
                
                # Configurar trace para atualização automática
                value_var.trace('w', self.update_ac)
        
        # Atualizar CA total
        self.update_ac()

    def open_background_screen(self):
        """Abre a tela de background do personagem"""
        BackgroundScreen(self)

def center_window(window, width, height):
    """Centraliza uma janela na tela, considerando a barra de tarefas"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight() - 60  # Compensar barra de tarefas
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

class SpellScreen:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Magias")
        self.window.geometry("1000x600")
        
        # Inicializar dicionários e variáveis antes de criar a interface
        self.spell_lists = {}
        self.spell_frames = {}
        self.prepared_spells = set()
        self.spells_data = getattr(parent, 'spells_data', [])
        parent.spells_data = self.spells_data
        
        # Adicionar variáveis de filtro
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_spells)
        self.filter_prepared = tk.StringVar(value="todas")
        self.filter_prepared.trace('w', self.filter_spells)
        
        # Criar interface
        self.create_interface()
        
        # Organizar magias por nível
        self.all_spells = {i: [] for i in range(10)}
        self.load_spells()

    def create_interface(self):
        # Frame para filtros no topo
        filter_frame = ttk.Frame(self.window)
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        # Frame para busca
        search_frame = ttk.Frame(filter_frame)
        search_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Frame para filtro de preparadas
        prepared_frame = ttk.Frame(filter_frame)
        prepared_frame.pack(side="right", padx=5)
        
        ttk.Label(prepared_frame, text="Mostrar:").pack(side="left", padx=5)
        prepared_filter = ttk.Combobox(prepared_frame, 
                                     textvariable=self.filter_prepared,
                                     values=["todas", "preparadas", "não preparadas"],
                                     state="readonly",
                                     width=15)
        prepared_filter.pack(side="left", padx=5)
        
        # Frame principal dividido em lista e formulário
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Notebook para níveis de magia (lado esquerdo)
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side="left", fill="both", expand=True)
        
        self.notebook = ttk.Notebook(list_frame)
        self.notebook.pack(expand=True, fill="both")
        
        # Adicionar aba "Todas as Magias"
        all_frame = ttk.Frame(self.notebook)
        self.spell_frames['all'] = all_frame
        self.notebook.add(all_frame, text="Todas")
        
        # Lista de todas as magias
        list_container = ttk.Frame(all_frame)
        list_container.pack(fill="both", expand=True)
        
        spell_list = tk.Listbox(list_container, width=30)
        spell_list.pack(side="left", fill="both", expand=True)
        self.spell_lists['all'] = spell_list
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=spell_list.yview)
        scrollbar.pack(side="right", fill="y")
        spell_list.config(yscrollcommand=scrollbar.set)
        
        # Criar abas para cada nível de magia (0-9)
        for level in range(10):
            frame = ttk.Frame(self.notebook)
            self.spell_frames[level] = frame
            self.notebook.add(frame, text=f"Nível {level}")
            
            # Lista de magias
            list_container = ttk.Frame(frame)
            list_container.pack(fill="both", expand=True)
            
            spell_list = tk.Listbox(list_container, width=30)
            spell_list.pack(side="left", fill="both", expand=True)
            self.spell_lists[level] = spell_list
            
            scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=spell_list.yview)
            scrollbar.pack(side="right", fill="y")
            spell_list.config(yscrollcommand=scrollbar.set)
        
        # Formulário de cadastro (lado direito)
        form_frame = ttk.LabelFrame(main_frame, text="Magia")
        form_frame.pack(side="right", fill="both", padx=5)
        
        self.spell_form = self.create_spell_form(form_frame)

        # Adicionar bind para seleção em cada lista
        for spell_list in self.spell_lists.values():
            spell_list.bind('<<ListboxSelect>>', self.on_spell_select)

    def create_spell_form(self, frame):
        entries = {}
        
        # Campos do formulário
        fields = [
            ("Nome", "entry"),
            ("Nível", "combo", [str(i) for i in range(10)]),
            ("Escola", "combo", ["Abjuração", "Adivinhação", "Conjuração", "Encantamento", 
                               "Evocação", "Ilusão", "Necromancia", "Transmutação"]),
            ("Preparada", "check"),
            ("Tempo de Conjuração", "entry"),
            ("Alcance", "entry"),
            ("Componentes", "entry"),
            ("Duração", "entry"),
            ("Teste de Resistência", "combo", ["Nenhum", "Força", "Destreza", "Constituição", 
                                             "Inteligência", "Sabedoria", "Carisma"]),
            ("Dano/Efeito", "entry"),
            ("Descrição", "text"),
            ("Em Níveis Superiores", "text")  # Novo campo
        ]
        
        row = 0
        for field_info in fields:
            field_name = field_info[0]
            field_type = field_info[1]
            
            ttk.Label(frame, text=field_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            
            if field_type == "entry":
                var = tk.StringVar()
                entry = ttk.Entry(frame, textvariable=var, width=40)
                entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
                entries[field_name] = var
            
            elif field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(frame, textvariable=var, values=field_info[2], width=37)
                combo.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
                entries[field_name] = var
            
            elif field_type == "check":
                var = tk.BooleanVar()
                check = ttk.Checkbutton(frame, variable=var)
                check.grid(row=row, column=1, padx=5, pady=2, sticky="w")
                entries[field_name] = var
            
            elif field_type == "text":
                text = tk.Text(frame, height=4 if field_name == "Em Níveis Superiores" else 6, width=40)
                text.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
                entries[field_name] = text
            
            row += 1
        
        # Frame para os botões
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Nova Magia", 
                  command=self.clear_form).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Salvar Magia", 
                  command=lambda: self.save_spell(entries)).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Excluir Magia", 
                  command=self.delete_spell).pack(side="left", padx=5)
        
        return entries

    def save_spell(self, entries):
        spell = {
            'nome': entries['Nome'].get(),
            'nivel': int(entries['Nível'].get() or 0),
            'escola': entries['Escola'].get(),
            'preparada': entries['Preparada'].get(),
            'tempo_conjuracao': entries['Tempo de Conjuração'].get(),
            'alcance': entries['Alcance'].get(),
            'componentes': entries['Componentes'].get(),
            'duracao': entries['Duração'].get(),
            'teste_resistencia': entries['Teste de Resistência'].get(),
            'dano_efeito': entries['Dano/Efeito'].get(),
            'descricao': entries['Descrição'].get("1.0", tk.END).strip(),
            'niveis_superiores': entries['Em Níveis Superiores'].get("1.0", tk.END).strip()  # Novo campo
        }

        # Atualizar magia existente ou adicionar nova
        selected = self.get_selected_spell()
        if selected:
            # Encontrar e atualizar magia existente
            for i, existing_spell in enumerate(self.spells_data):
                if existing_spell['nome'] == selected['nome']:
                    self.spells_data[i] = spell
                    break
        else:
            # Adicionar nova magia
            self.spells_data.append(spell)

        # Atualizar listas
        self.load_spells()
        self.clear_form()
        messagebox.showinfo("Sucesso", "Magia salva com sucesso!")

    def get_selected_spell(self):
        """Retorna a magia selecionada em qualquer uma das listas"""
        current_tab = self.notebook.select()
        tab_id = self.notebook.index(current_tab)
        
        selection = None
        spell_name = None
        
        if tab_id == 0:  # Aba "Todas"
            selection = self.spell_lists['all'].curselection()
            if selection:
                spell_text = self.spell_lists['all'].get(selection[0])
                spell_name = spell_text.split('] ')[-1].strip()  # Remove o nível e status
        else:
            selection = self.spell_lists[tab_id-1].curselection()
            if selection:
                spell_text = self.spell_lists[tab_id-1].get(selection[0])
                spell_name = spell_text.split(' ', 1)[-1].strip()  # Remove o status
        
        if spell_name:
            return next((s for s in self.spells_data if s['nome'] == spell_name), None)
        return None

    def clear_form(self):
        """Limpa todos os campos do formulário"""
        for key, entry in self.spell_form.items():
            if isinstance(entry, tk.BooleanVar):
                entry.set(False)  # Para checkboxes
            elif isinstance(entry, tk.StringVar):
                entry.set("")     # Para campos de texto e combos
            elif isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)  # Para áreas de texto

    def delete_spell(self):
        selected = self.get_selected_spell()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma magia para excluir")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta magia?"):
            self.spells_data.remove(selected)
            self.load_spells()
            self.clear_form()

    def load_spells(self):
        # Limpar todas as listas
        for spell_list in self.spell_lists.values():
            spell_list.delete(0, tk.END)

        # Organizar magias por nível
        self.all_spells = {i: [] for i in range(10)}
        for spell in self.spells_data:
            level = spell.get('nivel', 0)
            self.all_spells[level].append(spell)

        # Atualizar lista "Todas"
        for spell in self.spells_data:
            prepared = '✓' if spell.get('preparada', False) else ' '
            display_text = f"[{spell['nivel']}] {prepared} {spell['nome']}"
            self.spell_lists['all'].insert(tk.END, display_text)

        # Atualizar listas por nível
        for level, spells in self.all_spells.items():
            for spell in spells:
                prepared = '✓' if spell.get('preparada', False) else ' '
                display_text = f"{prepared} {spell['nome']}"
                self.spell_lists[level].insert(tk.END, display_text)

    def filter_spells(self, *args):
        """Filtra as magias com base na busca e no status de preparada"""
        search_term = self.search_var.get().lower().strip()
        prepared_filter = self.filter_prepared.get()
        
        # Limpar todas as listas
        for spell_list in self.spell_lists.values():
            spell_list.delete(0, tk.END)
        
        # Filtrar e exibir magias
        for spell in self.spells_data:
            # Verificar filtro de preparada
            is_prepared = spell.get('preparada', False)
            if prepared_filter == "preparadas" and not is_prepared:
                continue
            if prepared_filter == "não preparadas" and is_prepared:
                continue
            
            # Verificar termo de busca
            spell_name = spell['nome'].lower()
            spell_desc = spell.get('descricao', '').lower()
            
            if search_term and not (search_term in spell_name or search_term in spell_desc):
                continue
            
            # Adicionar à lista 'todas'
            prepared_mark = '✓' if is_prepared else ' '
            display_text = f"[{spell['nivel']}] {prepared_mark} {spell['nome']}"
            self.spell_lists['all'].insert(tk.END, display_text)
            
            # Adicionar à lista do nível específico
            level = spell.get('nivel', 0)
            display_text = f"{prepared_mark} {spell['nome']}"
            self.spell_lists[level].insert(tk.END, display_text)

    def load_spells(self):
        """Carrega todas as magias nas listas"""
        # Organizar magias por nível
        self.all_spells = {i: [] for i in range(10)}
        for spell in self.spells_data:
            level = spell.get('nivel', 0)
            self.all_spells[level].append(spell)
        
        # Aplicar filtros
        self.filter_spells()

    def on_spell_select(self, event):
        """Manipula o evento de seleção de uma magia na lista"""
        selected_spell = self.get_selected_spell()
        if not selected_spell:
            return
            
        # Limpar o formulário antes de carregar os novos dados
        self.clear_form()
        
        # Preencher os campos com os dados da magia
        form = self.spell_form
        form['Nome'].set(selected_spell.get('nome', ''))
        form['Nível'].set(str(selected_spell.get('nivel', '0')))
        form['Escola'].set(selected_spell.get('escola', ''))
        form['Preparada'].set(selected_spell.get('preparada', False))
        form['Tempo de Conjuração'].set(selected_spell.get('tempo_conjuracao', ''))
        form['Alcance'].set(selected_spell.get('alcance', ''))
        form['Componentes'].set(selected_spell.get('componentes', ''))
        form['Duração'].set(selected_spell.get('duracao', ''))
        form['Teste de Resistência'].set(selected_spell.get('teste_resistencia', 'Nenhum'))
        form['Dano/Efeito'].set(selected_spell.get('dano_efeito', ''))
        
        # Para campos de texto (Text widget)
        form['Descrição'].delete('1.0', tk.END)
        form['Descrição'].insert('1.0', selected_spell.get('descricao', ''))
        
        form['Em Níveis Superiores'].delete('1.0', tk.END)
        form['Em Níveis Superiores'].insert('1.0', selected_spell.get('niveis_superiores', ''))

class AbilityScreen:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Talentos")
        self.window.geometry("800x600")
        
        # Adicionar barra de busca no topo
        search_frame = ttk.Frame(self.window)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_abilities)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Frame principal dividido em duas partes
        self.create_split_layout()
        
        # Armazenar todos os talentos
        self.all_abilities = []
        self.load_abilities()
        
        # Bind para seleção de talento
        self.ability_list.bind('<<ListboxSelect>>', self.on_ability_select)

    def create_split_layout(self):
        # Frame esquerdo para lista de talentos
        left_frame = ttk.Frame(self.window)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Lista de talentos
        ttk.Label(left_frame, text="Talentos").pack(anchor="w")
        
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill="both", expand=True)
        
        self.ability_list = tk.Listbox(list_container, width=30)
        self.ability_list.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.ability_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.ability_list.config(yscrollcommand=scrollbar.set)
        
        # Frame direito para formulário
        right_frame = ttk.Frame(self.window)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Formulário
        form_frame = ttk.LabelFrame(right_frame, text="Detalhes do Talento")
        form_frame.pack(fill="both", expand=True)
        
        # Campo Nome
        ttk.Label(form_frame, text="Nome:").pack(anchor="w", padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=40).pack(fill="x", padx=5, pady=2)
        
        # Campo Descrição
        ttk.Label(form_frame, text="Descrição:").pack(anchor="w", padx=5, pady=2)
        
        text_frame = ttk.Frame(form_frame)
        text_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.description_text = tk.Text(text_frame, wrap=tk.WORD, height=20)
        self.description_text.pack(side="left", fill="both", expand=True)
        
        desc_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.description_text.yview)
        desc_scrollbar.pack(side="right", fill="y")
        self.description_text.config(yscrollcommand=desc_scrollbar.set)
        
        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Salvar", command=self.save_ability).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Novo", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_ability).pack(side="left", padx=5)

    def filter_abilities(self, *args):
        search_term = self.search_var.get().lower().strip()
        
        self.ability_list.delete(0, tk.END)
        for ability in self.all_abilities:
            # Busca no nome e na descrição
            if (search_term in ability['nome'].lower() or 
                search_term in ability.get('descricao', '').lower()):
                self.ability_list.insert(tk.END, ability['nome'])
    
    def load_abilities(self):
        self.all_abilities = getattr(self.parent, 'abilities_data', []).copy()
        self.filter_abilities()

    def on_ability_select(self, event):
        selection = self.ability_list.curselection()
        
        if not selection:
            return
            
        index = selection[0]
        ability_name = self.ability_list.get(index)
        
        # Encontrar o talento nos dados
        ability = next((a for a in self.parent.abilities_data if a['nome'] == ability_name), None)
        
        if ability:
            self.name_var.set(ability['nome'])
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert("1.0", ability['descricao'])

    def delete_ability(self):
        selected = self.ability_list.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um talento para excluir")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este talento?"):
            index = selected[0]
            self.ability_list.delete(index)
            self.parent.abilities_data.pop(index)
            self.clear_form()
            self.all_abilities = self.parent.abilities_data.copy()

    def clear_form(self):
        self.name_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.ability_list.selection_clear(0, tk.END)

    def save_ability(self):
        ability = {
            'nome': self.name_var.get(),
            'descricao': self.description_text.get("1.0", tk.END).strip()
        }

        selected = self.ability_list.curselection()
        if selected:
            # Atualizar talento existente
            index = selected[0]
            self.parent.abilities_data[index] = ability
            self.ability_list.delete(index)
            self.ability_list.insert(index, ability['nome'])
        else:
            # Novo talento
            self.parent.abilities_data.append(ability)
            self.ability_list.insert(tk.END, ability['nome'])

        messagebox.showinfo("Sucesso", "Talento salvo com sucesso!")
        self.clear_form()
        self.all_abilities = self.parent.abilities_data.copy()

class InventoryScreen:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Inventário")
        self.window.geometry("1000x600")
        
        # Dados do inventário
        self.inventory_data = getattr(parent, 'inventory_data', [])
        parent.inventory_data = self.inventory_data
        
        # Criar interface
        self.create_interface()
        self.load_inventory()

    def create_interface(self):
        # Frame principal dividido em duas partes
        list_frame = ttk.Frame(self.window)
        list_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        form_frame = ttk.Frame(self.window)
        form_frame.pack(side="right", fill="both", padx=5, pady=5)

        # Lista de itens
        ttk.Label(list_frame, text="Itens do Inventário").pack(anchor="w")
        
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill="both", expand=True)
        
        self.item_list = tk.Listbox(list_container, width=40, height=20)
        self.item_list.pack(side="left", fill="both", expand=True)
        self.item_list.bind('<<ListboxSelect>>', self.on_select_item)
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.item_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.item_list.config(yscrollcommand=scrollbar.set)

        # Formulário
        form = ttk.LabelFrame(form_frame, text="Detalhes do Item")
        form.pack(fill="both", expand=True)

        # Campos básicos
        basic_frame = ttk.Frame(form)
        basic_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(basic_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(basic_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=2)
        self.type_var = tk.StringVar()
        ttk.Combobox(basic_frame, textvariable=self.type_var, 
                     values=["Arma", "Armadura", "Item Mágico", "Consumível", "Outro"],
                     width=27).grid(row=1, column=1, padx=5, pady=2)

        # Frame para bônus
        bonus_frame = ttk.LabelFrame(form, text="Bônus")
        bonus_frame.pack(fill="x", padx=5, pady=5)

        # Bônus de atributos
        attrs_frame = ttk.Frame(bonus_frame)
        attrs_frame.pack(fill="x", padx=5, pady=5)
        
        self.attr_vars = {}
        attrs = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
        for i, attr in enumerate(attrs):
            ttk.Label(attrs_frame, text=attr).grid(row=i//3, column=(i%3)*2, padx=5, pady=2)
            var = tk.StringVar(value="0")
            ttk.Entry(attrs_frame, textvariable=var, width=5).grid(row=i//3, column=(i%3)*2+1, padx=5, pady=2)
            self.attr_vars[attr] = var

        # Outros bônus
        other_bonus_frame = ttk.Frame(bonus_frame)
        other_bonus_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(other_bonus_frame, text="CA:").grid(row=0, column=0, padx=5, pady=2)
        self.ac_bonus_var = tk.StringVar(value="0")
        ttk.Entry(other_bonus_frame, textvariable=self.ac_bonus_var, width=5).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(other_bonus_frame, text="CD:").grid(row=0, column=2, padx=5, pady=2)
        self.cd_bonus_var = tk.StringVar(value="0")
        ttk.Entry(other_bonus_frame, textvariable=self.cd_bonus_var, width=5).grid(row=0, column=3, padx=5, pady=2)

        # Frame para dano (se for arma)
        damage_frame = ttk.LabelFrame(form, text="Dano")
        damage_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(damage_frame, text="Dados de Dano:").grid(row=0, column=0, padx=5, pady=2)
        self.damage_dice_var = tk.StringVar()
        ttk.Entry(damage_frame, textvariable=self.damage_dice_var, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(damage_frame, text="Tipo de Dano:").grid(row=0, column=2, padx=5, pady=2)
        self.damage_type_var = tk.StringVar()
        ttk.Combobox(damage_frame, textvariable=self.damage_type_var,
                     values=["Cortante", "Perfurante", "Contundente", "Fogo", "Gelo", "Elétrico", "Ácido", "Veneno", "Psíquico", "Necrótico", "Radiante"],
                     width=15).grid(row=0, column=3, padx=5, pady=2)

        # Descrição
        desc_frame = ttk.LabelFrame(form, text="Descrição")
        desc_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.description_text = tk.Text(desc_frame, height=6, width=40)
        self.description_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Botões de controle
        button_frame = ttk.Frame(form)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Salvar Item", command=self.save_item).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Novo Item", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Excluir Item", command=self.delete_item).pack(side="left", padx=5)

    def save_item(self):
        item = {
            'nome': self.name_var.get(),
            'tipo': self.type_var.get(),
            'bonus_atributos': {attr: var.get() for attr, var in self.attr_vars.items()},
            'bonus_ca': self.ac_bonus_var.get(),
            'bonus_cd': self.cd_bonus_var.get(),
            'dano_dado': self.damage_dice_var.get(),
            'dano_tipo': self.damage_type_var.get(),
            'descricao': self.description_text.get("1.0", tk.END).strip()
        }

        selected = self.item_list.curselection()
        if selected:
            # Atualizar item existente
            index = selected[0]
            self.inventory_data[index] = item
            self.item_list.delete(index)
            self.item_list.insert(index, item['nome'])
        else:
            # Novo item
            self.inventory_data.append(item)
            self.item_list.insert(tk.END, item['nome'])

        messagebox.showinfo("Sucesso", "Item salvo com sucesso!")
        self.clear_form()

    def load_inventory(self):
        for item in self.inventory_data:
            self.item_list.insert(tk.END, item['nome'])

    def on_select_item(self, event):
        selected = self.item_list.curselection()
        if not selected:
            return

        item = self.inventory_data[selected[0]]
        self.name_var.set(item['nome'])
        self.type_var.set(item['tipo'])
        
        for attr, bonus in item['bonus_atributos'].items():
            self.attr_vars[attr].set(bonus)
            
        self.ac_bonus_var.set(item['bonus_ca'])
        self.cd_bonus_var.set(item['bonus_cd'])
        self.damage_dice_var.set(item['dano_dado'])
        self.damage_type_var.set(item['dano_tipo'])
        
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", item['descricao'])

    def clear_form(self):
        self.name_var.set("")
        self.type_var.set("")
        for var in self.attr_vars.values():
            var.set("0")
        self.ac_bonus_var.set("0")
        self.cd_bonus_var.set("0")
        self.damage_dice_var.set("")
        self.damage_type_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.item_list.selection_clear(0, tk.END)

    def delete_item(self):
        selected = self.item_list.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um item para excluir")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este item?"):
            index = selected[0]
            self.item_list.delete(index)
            self.inventory_data.pop(index)
            self.clear_form()

class FeatureScreen:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Habilidades")
        self.window.geometry("800x600")
        
        # Adicionar barra de busca no topo
        search_frame = ttk.Frame(self.window)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_features)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Frame principal dividido em duas partes
        self.create_split_layout()
        
        # Armazenar todas as habilidades
        self.all_features = []
        self.load_features()
        
        # Bind para seleção de habilidade
        self.feature_list.bind('<<ListboxSelect>>', self.on_feature_select)

    def create_split_layout(self):
        # Frame esquerdo para lista de habilidades
        left_frame = ttk.Frame(self.window)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Lista de habilidades
        ttk.Label(left_frame, text="Habilidades").pack(anchor="w")
        
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill="both", expand=True)
        
        self.feature_list = tk.Listbox(list_container, width=30)
        self.feature_list.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.feature_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.feature_list.config(yscrollcommand=scrollbar.set)
        
        # Frame direito para formulário
        right_frame = ttk.Frame(self.window)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Formulário
        form_frame = ttk.LabelFrame(right_frame, text="Detalhes da Habilidade")
        form_frame.pack(fill="both", expand=True)
        
        # Campo Nome
        ttk.Label(form_frame, text="Nome:").pack(anchor="w", padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=40).pack(fill="x", padx=5, pady=2)
        
        # Campo Descrição
        ttk.Label(form_frame, text="Descrição:").pack(anchor="w", padx=5, pady=2)
        
        text_frame = ttk.Frame(form_frame)
        text_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.description_text = tk.Text(text_frame, wrap=tk.WORD, height=20)
        self.description_text.pack(side="left", fill="both", expand=True)
        
        desc_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.description_text.yview)
        desc_scrollbar.pack(side="right", fill="y")
        self.description_text.config(yscrollcommand=desc_scrollbar.set)
        
        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Salvar", command=self.save_feature).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Novo", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_feature).pack(side="left", padx=5)

    def filter_features(self, *args):
        search_term = self.search_var.get().lower().strip()
        
        self.feature_list.delete(0, tk.END)
        for feature in self.all_features:
            # Busca no nome e na descrição
            if (search_term in feature['nome'].lower() or 
                search_term in feature.get('descricao', '').lower()):
                self.feature_list.insert(tk.END, feature['nome'])
    
    def load_features(self):
        self.all_features = self.parent.features_data.copy()
        self.filter_features()

    def on_feature_select(self, event):
        selected = self.feature_list.curselection()
        
        if not selected:
            return
            
        index = selected[0]
        feature = self.parent.features_data[index]
        
        self.name_var.set(feature['nome'])
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", feature['descricao'])

    def clear_form(self):
        self.name_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.feature_list.selection_clear(0, tk.END)

    def delete_feature(self):
        selected = self.feature_list.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma habilidade para excluir")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta habilidade?"):
            index = selected[0]
            self.feature_list.delete(index)
            self.parent.features_data.pop(index)
            self.clear_form()
            self.parent.update_all()

    def save_feature(self):
        feature = {
            'nome': self.name_var.get() or "Sem nome",
            'descricao': self.description_text.get("1.0", tk.END).strip() or "Sem descrição"
        }

        selected = self.feature_list.curselection()
        if selected:
            # Atualizar habilidade existente
            index = selected[0]
            self.parent.features_data[index] = feature
            self.feature_list.delete(index)
            self.feature_list.insert(index, feature['nome'])
        else:
            # Nova habilidade
            self.parent.features_data.append(feature)
            self.feature_list.insert(tk.END, feature['nome'])

        messagebox.showinfo("Sucesso", "Habilidade salva com sucesso!")
        self.clear_form()
        self.all_features = self.parent.features_data.copy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FichaDnD(root)
    root.mainloop()
    