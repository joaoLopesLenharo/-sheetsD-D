import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from PIL import Image, ImageTk

class FichaDnD:
    def __init__(self, root):
        self.root = root
        self.root.title("Ficha de D&D 5.5E")
        
        # Dados de magias e talentos
        self.spells_data = []
        self.abilities_data = []

        # Sessões de interface
        self.create_basic_info_section()
        self.create_classes_section()
        self.create_attributes_section()
        self.create_proficiencies_section()
        self.create_combat_section()
        self.create_health_section()
        self.create_control_buttons()

    def create_basic_info_section(self):
        frame = ttk.LabelFrame(self.root, text="Informações Básicas")
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
        self.photo_path = None
        self.photo_image = None
        self.set_default_photo()

    def set_default_photo(self):
        """Define uma imagem padrão ou placeholder no canvas"""
        self.photo_canvas.delete("all")
        self.photo_canvas.create_rectangle(0, 0, 150, 150, fill="lightgray")
        self.photo_canvas.create_text(75, 75, text="Foto do\nPersonagem", justify="center")
        self.photo_path = None
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
                photo = ImageTk.PhotoImage(image)
                
                # Atualizar canvas
                self.photo_canvas.delete("all")
                self.photo_canvas.create_image(0, 0, anchor="nw", image=photo)
                
                # Manter referências
                self.photo_image = photo
                self.photo_path = file_path
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem: {str(e)}")
                self.set_default_photo()

    def remove_photo(self):
        """Remove a foto atual e restaura o placeholder"""
        self.set_default_photo()

    def create_classes_section(self):
        frame = ttk.LabelFrame(self.root, text="Classes")
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
        frame = ttk.LabelFrame(self.root, text="Atributos")
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.attribute_vars = {}
        self.modifier_labels = {}  # Para mostrar os modificadores
        attributes = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]

        for i, attr in enumerate(attributes):
            ttk.Label(frame, text=attr).grid(row=i, column=0, padx=5, pady=5)
            var = tk.StringVar()
            var.trace('w', lambda *args, attr=attr: self.update_modifiers(attr))
            entry = ttk.Entry(frame, textvariable=var, width=5)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.attribute_vars[attr] = var
            
            # Label para modificador
            mod_label = ttk.Label(frame, text="(+0)")
            mod_label.grid(row=i, column=2, padx=5, pady=5)
            self.modifier_labels[attr] = mod_label

    def create_proficiencies_section(self):
        frame = ttk.LabelFrame(self.root, text="Proficiências")
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
            
            cb1 = ttk.Checkbutton(check_frame, variable=prof1_var, command=lambda s=skill: self.update_skill_total(s))
            cb1.pack(side="left", padx=2)
            
            cb2 = ttk.Checkbutton(check_frame, variable=prof2_var, command=lambda s=skill: self.update_skill_total(s))
            cb2.pack(side="left", padx=2)
            
            # Label com nome da perícia
            skill_label = ttk.Label(skill_frame, text=f"{skill} ({attr})", width=20, anchor="w")
            skill_label.pack(side="left", padx=(5, 10))
            
            # Entry para bônus extra
            bonus_var = tk.StringVar(value="0")
            bonus_var.trace('w', lambda *args, s=skill: self.update_skill_total(s))
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

    def update_skill_total(self, skill):
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
        prof_bonus = self.get_proficiency_bonus()
        
        for skill, data in self.skill_vars.items():
            modifier = self.get_modifier(data["attr"])
            total = modifier
            
            # Adiciona o bônus de proficiência para cada checkbox marcado
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
            
            data["label"].config(text=f"{'+' if total >= 0 else ''}{total}")

    def create_combat_section(self):
        frame = ttk.LabelFrame(self.root, text="Combate")
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
        
        self.ac_label = ttk.Label(frame, text="CA Total: 10")
        self.ac_label.grid(row=0, column=3, padx=5)

        # CD de Magias
        ttk.Label(frame, text="CD de Magias:").grid(row=1, column=0, padx=5, pady=5)
        self.spell_attr_var = tk.StringVar(value="INT")
        ttk.Combobox(frame, textvariable=self.spell_attr_var,
                     values=["INT", "SAB", "CAR"],
                     width=5).grid(row=1, column=1, padx=5)
        
        self.cd_label = ttk.Label(frame, text="CD: 8")
        self.cd_label.grid(row=1, column=2, padx=5)

        # Percepção Passiva
        ttk.Label(frame, text="Percepção Passiva:").grid(row=2, column=0, padx=5, pady=5)
        self.passive_perception_label = ttk.Label(frame, text="10")
        self.passive_perception_label.grid(row=2, column=1, padx=5)

        # Configurar traces para atualizações automáticas
        self.base_ac_var.trace('w', self.update_ac)
        self.ac_attr_var.trace('w', self.update_ac)
        self.spell_attr_var.trace('w', self.update_spell_dc)

    def create_health_section(self):
        frame = ttk.LabelFrame(self.root, text="Recursos")
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
        frame = ttk.Frame(self.root)
        frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(frame, text="Tela de Magias", command=self.open_spells_screen).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Tela de Talentos", command=self.open_abilities_screen).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Inventário", command=self.open_inventory_screen).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame, text="Habilidades", command=self.open_features_screen).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(frame, text="Exportar para JSON", command=self.export_to_json).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frame, text="Importar de JSON", command=self.import_from_json).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(frame, text="Exportar para PDF", command=self.export_to_pdf).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(frame, text="Importar de PDF", command=self.import_from_pdf).grid(row=0, column=7, padx=5, pady=5)

    def open_spells_screen(self):
        SpellScreen(self)

    def open_abilities_screen(self):
        AbilityScreen(self)

    def open_inventory_screen(self):
        InventoryScreen(self)

    def open_features_screen(self):
        FeatureScreen(self)

    def export_to_json(self):
        data = {
            'version': '1.1',  # Adicionando controle de versão
            'basic_info': {
                k: v.get() for k, v in self.basic_info_vars.items()
            },
            'classes': {
                k: v.get() for k, v in self.class_vars.items()
            },
            'attributes': {
                k: v.get() for k, v in self.attribute_vars.items()
            },
            'skills': {
                k: {
                    'prof1': v['prof1'].get(),
                    'prof2': v['prof2'].get(),
                    'attr': v['attr'],
                    'bonus': v.get('bonus', tk.StringVar(value='0')).get()  # Compatibilidade com versões antigas
                } for k, v in self.skill_vars.items()
            },
            'combat': {
                'base_ac': self.base_ac_var.get(),
                'ac_attr': self.ac_attr_var.get(),
                'spell_attr': self.spell_attr_var.get()
            },
            'resources': {
                k: {
                    'atual': self.resources_vars[k].get(),
                    'max': self.resources_max_vars[k].get()
                } for k in self.resources_vars.keys()
            },
            'custom_resources': [
                {
                    'nome': r['name'].get(),
                    'atual': r['atual'].get(),
                    'max': r['max'].get()
                } for r in self.custom_resources
            ],
            'spells': [
                {
                    'nivel': spell.get('nivel', ''),
                    'nome': spell.get('nome', ''),
                    'escola': spell.get('escola', ''),
                    'tempo_conjuracao': spell.get('tempo_conjuracao', ''),
                    'alcance': spell.get('alcance', ''),
                    'componentes': spell.get('componentes', ''),
                    'duracao': spell.get('duracao', ''),
                    'teste_resistencia': spell.get('teste_resistencia', ''),
                    'dano_efeito': spell.get('dano_efeito', ''),
                    'descricao': spell.get('descricao', '')
                } for spell in self.spells_data
            ],
            'features': [
                {
                    'nome': feature.get('nome', ''),
                    'descricao': feature.get('descricao', '')
                } for feature in getattr(self, 'features_data', [])
            ],
            'inventory': [
                {
                    'nome': item.get('nome', ''),
                    'tipo': item.get('tipo', ''),
                    'bonus_atributos': item.get('bonus_atributos', {
                        'FOR': '0', 'DES': '0', 'CON': '0', 
                        'INT': '0', 'SAB': '0', 'CAR': '0'
                    }),
                    'bonus_ca': item.get('bonus_ca', '0'),
                    'bonus_cd': item.get('bonus_cd', '0'),
                    'dano_dado': item.get('dano_dado', ''),
                    'dano_tipo': item.get('dano_tipo', ''),
                    'descricao': item.get('descricao', '')
                } for item in getattr(self, 'inventory_data', [])
            ],
            'photo_path': self.photo_path,  # Adicionar caminho da foto
        }

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile="ficha_dnd.json"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                messagebox.showinfo("Sucesso", "Ficha salva com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar a ficha: {str(e)}")

    def import_from_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")],
            initialfile="ficha_dnd.json"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Verificar versão e aplicar migrações necessárias
                version = data.get('version', '1.0')
                data = self._migrate_json_data(data, version)

                # Limpar recursos customizados existentes
                for resource in self.custom_resources:
                    resource['frame'].destroy()
                self.custom_resources.clear()

                # Importar dados básicos
                for k, v in data.get('basic_info', {}).items():
                    if k in self.basic_info_vars:
                        self.basic_info_vars[k].set(v)

                for k, v in data.get('classes', {}).items():
                    if k in self.class_vars:
                        self.class_vars[k].set(v)

                for k, v in data.get('attributes', {}).items():
                    if k in self.attribute_vars:
                        self.attribute_vars[k].set(v)

                # Importar perícias com compatibilidade
                for skill, skill_data in data.get('skills', {}).items():
                    if skill in self.skill_vars:
                        self.skill_vars[skill]['prof1'].set(skill_data.get('prof1', False))
                        self.skill_vars[skill]['prof2'].set(skill_data.get('prof2', False))
                        if 'bonus' in skill_data:
                            self.skill_vars[skill]['bonus'].set(skill_data['bonus'])

                # Importar recursos padrão
                for k, v in data.get('resources', {}).items():
                    if k in self.resources_vars:
                        self.resources_vars[k].set(v.get('atual', '0'))
                        self.resources_max_vars[k].set(v.get('max', '0'))

                # Importar recursos customizados
                for custom_resource in data.get('custom_resources', []):
                    self.add_custom_resource()
                    last_resource = self.custom_resources[-1]
                    last_resource['name'].set(custom_resource.get('nome', ''))
                    last_resource['atual'].set(custom_resource.get('atual', '0'))
                    last_resource['max'].set(custom_resource.get('max', '0'))

                # Importar listas de dados
                self.spells_data = data.get('spells', [])
                self.abilities_data = data.get('abilities', [])
                self.features_data = data.get('features', [])
                self.inventory_data = data.get('inventory', [])

                # Atualizar interface
                self.update_modifiers()
                self.update_proficiency_bonus()
                self.update_ac()
                self.update_spell_dc()
                self.update_passive_perception()

                # Carregar foto se existir
                photo_path = data.get('photo_path')
                if photo_path and os.path.exists(photo_path):
                    self.photo_path = photo_path
                    self.select_photo()  # Isso vai recarregar a foto
                else:
                    self.set_default_photo()

                messagebox.showinfo("Sucesso", "Ficha carregada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar a ficha: {str(e)}")
                import traceback
                traceback.print_exc()

    def _migrate_json_data(self, data, version):
        """Migra dados de versões antigas para o formato atual"""
        if version == '1.0':
            # Migrar dados da versão 1.0 para 1.1
            if 'skills' in data:
                for skill in data['skills'].values():
                    if 'bonus' not in skill:
                        skill['bonus'] = '0'
            
            if 'custom_resources' not in data:
                data['custom_resources'] = []

            if 'photo_path' not in data:
                data['photo_path'] = None
            
            if 'basic_info' in data and 'Antecedente' not in data['basic_info']:
                data['basic_info']['Antecedente'] = ''

            data['version'] = '1.1'

        return data

    def update_modifiers(self, attr=None):
        for attribute, var in self.attribute_vars.items():
            try:
                value = int(var.get())
                modifier = (value - 10) // 2
                self.modifier_labels[attribute].config(text=f"({'+' if modifier >= 0 else ''}{modifier})")
            except ValueError:
                self.modifier_labels[attribute].config(text="(+0)")
        
        self.update_skills()
        self.update_ac()
        self.update_spell_dc()
        self.update_passive_perception()

    def get_modifier(self, attr):
        try:
            value = int(self.attribute_vars[attr].get())
            return (value - 10) // 2
        except (ValueError, KeyError):
            return 0

    def update_ac(self, *args):
        try:
            base_ac = int(self.base_ac_var.get())
            modifier = self.get_modifier(self.ac_attr_var.get())
            total_ac = base_ac + modifier
            self.ac_label.config(text=f"CA Total: {total_ac}")
        except ValueError:
            self.ac_label.config(text="CA Total: 10")

    def update_spell_dc(self, *args):
        try:
            modifier = self.get_modifier(self.spell_attr_var.get())
            nivel = int(self.basic_info_vars["Nível"].get())
            prof_bonus = 2 + ((nivel - 1) // 4)
            dc = 8 + modifier + prof_bonus
            self.cd_label.config(text=f"CD: {dc}")
        except ValueError:
            self.cd_label.config(text="CD: 8")

    def update_passive_perception(self):
        wisdom_mod = self.get_modifier("SAB")
        try:
            nivel = int(self.basic_info_vars["Nível"].get())
            prof_bonus = 2 + ((nivel - 1) // 4)
            has_prof = self.skill_vars["Percepção"]["prof1"].get()
            passive = 10 + wisdom_mod + (prof_bonus if has_prof else 0)
            self.passive_perception_label.config(text=str(passive))
        except ValueError:
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
        # Atualiza todas as perícias e CD de magias
        self.update_skills()
        self.update_spell_dc()
        self.update_passive_perception()

    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="ficha_dnd.pdf"
        )
        
        if not file_path:
            return

        try:
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            
            # Configurações de fonte
            c.setFont("Helvetica-Bold", 16)
            title_font = ("Helvetica-Bold", 14)
            header_font = ("Helvetica-Bold", 12)
            normal_font = ("Helvetica", 10)
            
            # Título
            c.drawString(50, height - 50, "Ficha de Personagem D&D 5.5E")
            
            # Informações Básicas
            y = height - 80
            c.setFont(*header_font)
            c.drawString(50, y, "Informações Básicas")
            c.setFont(*normal_font)
            y -= 20
            
            # Verifica se há informações básicas preenchidas
            has_basic_info = any(var.get() for var in self.basic_info_vars.values())
            if has_basic_info:
                for label, var in self.basic_info_vars.items():
                    value = var.get()
                    if value:  # Só imprime se houver valor
                        c.drawString(50, y, f"{label}: {value}")
                        y -= 20
            else:
                c.drawString(50, y, "Nenhuma informação básica preenchida")
                y -= 20
                
            # Classes
            y -= 10
            c.setFont(*header_font)
            c.drawString(50, y, "Classes")
            c.setFont(*normal_font)
            y -= 20
            
            has_classes = any(var.get() for var in self.class_vars.values())
            if has_classes:
                for label, var in self.class_vars.items():
                    value = var.get()
                    if value:
                        c.drawString(50, y, f"{label}: {value}")
                        y -= 20
            else:
                c.drawString(50, y, "Nenhuma classe selecionada")
                y -= 20
                
            # Atributos e Modificadores
            y -= 10
            c.setFont(*header_font)
            c.drawString(50, y, "Atributos")
            c.setFont(*normal_font)
            y -= 20
            
            has_attributes = any(var.get() for var in self.attribute_vars.values())
            if has_attributes:
                for attr, var in self.attribute_vars.items():
                    value = var.get()
                    if value:
                        mod = self.get_modifier(attr)
                        mod_text = f"+{mod}" if mod >= 0 else str(mod)
                        c.drawString(50, y, f"{attr}: {value} ({mod_text})")
                        y -= 20
            else:
                c.drawString(50, y, "Nenhum atributo definido")
                y -= 20
                
            # Perícias
            y -= 10
            c.setFont(*header_font)
            c.drawString(50, y, "Perícias")
            c.setFont(*normal_font)
            y -= 20
            
            has_proficiencies = any(data['prof1'].get() or data['prof2'].get() 
                                  for data in self.skill_vars.values())
            if has_proficiencies:
                for skill, data in self.skill_vars.items():
                    if data['prof1'].get() or data['prof2'].get():  # Só mostra perícias com alguma proficiência
                        prof_text = ""
                        if data['prof1'].get():
                            prof_text += "■"
                        else:
                            prof_text += "□"
                        if data['prof2'].get():
                            prof_text += "■"
                        else:
                            prof_text += "□"
                        c.drawString(50, y, f"{skill} ({data['attr']}) {prof_text}")
                        y -= 15
            else:
                c.drawString(50, y, "Nenhuma proficiência selecionada")
                y -= 20
                
            # Recursos
            y -= 10
            c.setFont(*header_font)
            c.drawString(50, y, "Recursos")
            c.setFont(*normal_font)
            y -= 20
            
            has_resources = any(self.resources_vars[r].get() or self.resources_max_vars[r].get() 
                              for r in self.resources_vars.keys())
            if has_resources:
                for resource in self.resources_vars.keys():
                    atual = self.resources_vars[resource].get()
                    maximo = self.resources_max_vars[resource].get()
                    if atual or maximo:  # Só mostra recursos com algum valor
                        c.drawString(50, y, f"{resource}: {atual or '0'}/{maximo or '0'}")
                        y -= 20
            else:
                c.drawString(50, y, "Nenhum recurso definido")
                y -= 20
                
            # Magias (nova página)
            spells_data = getattr(self, 'spells_data', [])
            if spells_data and any(isinstance(spell, dict) for spell in spells_data):
                c.showPage()
                c.setFont(*title_font)
                c.drawString(50, height - 50, "Magias")
                y = height - 80
                
                for spell in spells_data:
                    if not isinstance(spell, dict):
                        continue
                        
                    if y < 100:
                        c.showPage()
                        y = height - 50
                    
                    nome = spell.get('nome', '').strip()
                    nivel = spell.get('nivel', '0')
                    
                    if nome:
                        c.setFont(*header_font)
                        c.drawString(50, y, f"{nome} (Nível {nivel})")
                        y -= 20
                        c.setFont(*normal_font)
                        
                        # Campos opcionais da magia
                        campos = {
                            'escola': 'Escola',
                            'tempo_conjuracao': 'Tempo de Conjuração',
                            'alcance': 'Alcance',
                            'componentes': 'Componentes',
                            'duracao': 'Duração',
                            'teste_resistencia': 'Teste de Resistência',
                            'dano_efeito': 'Dano/Efeito'
                        }
                        
                        for campo, label in campos.items():
                            valor = spell.get(campo, '').strip()
                            if valor:
                                c.drawString(70, y, f"{label}: {valor}")
                                y -= 15
                        
                        descricao = spell.get('descricao', '').strip()
                        if descricao:
                            desc_lines = self._wrap_text(descricao, c, normal_font[0], normal_font[1], width - 140)
                            for line in desc_lines:
                                if y < 100:
                                    c.showPage()
                                    y = height - 50
                                c.drawString(70, y, line)
                                y -= 15
                        y -= 20

            # Habilidades (nova página)
            features_data = getattr(self, 'features_data', [])
            if features_data and any(isinstance(feature, dict) for feature in features_data):
                c.showPage()
                c.setFont(*title_font)
                c.drawString(50, height - 50, "Habilidades")
                y = height - 80
                
                for feature in features_data:
                    if not isinstance(feature, dict):
                        continue
                        
                    if y < 100:
                        c.showPage()
                        y = height - 50
                    
                    nome = feature.get('nome', '').strip()
                    descricao = feature.get('descricao', '').strip()
                    
                    if nome:
                        c.setFont(*header_font)
                        c.drawString(50, y, nome)
                        y -= 20
                        
                        if descricao:
                            c.setFont(*normal_font)
                            desc_lines = self._wrap_text(descricao, c, normal_font[0], normal_font[1], width - 120)
                            for line in desc_lines:
                                if y < 100:
                                    c.showPage()
                                    y = height - 50
                                c.drawString(70, y, line)
                                y -= 15
                        y -= 20

            # Inventário (nova página)
            inventory_data = getattr(self, 'inventory_data', [])
            if inventory_data and any(isinstance(item, dict) for item in inventory_data):
                c.showPage()
                c.setFont(*title_font)
                c.drawString(50, height - 50, "Inventário")
                y = height - 80
                
                for item in inventory_data:
                    if not isinstance(item, dict):
                        continue
                        
                    if y < 100:
                        c.showPage()
                        y = height - 50
                    
                    nome = item.get('nome', '').strip()
                    tipo = item.get('tipo', '').strip()
                    
                    if nome:
                        c.setFont(*header_font)
                        header_text = nome
                        if tipo:
                            header_text += f" ({tipo})"
                        c.drawString(50, y, header_text)
                        y -= 20
                        c.setFont(*normal_font)
                        
                        # Bônus de atributos (se existir e tiver valores válidos)
                        bonus_atributos = item.get('bonus_atributos', {})
                        if isinstance(bonus_atributos, dict):
                            bonus_validos = {k: v for k, v in bonus_atributos.items() 
                                           if v and str(v).strip() != "0"}
                            if bonus_validos:
                                bonus_str = ", ".join(f"{attr}: {val}" for attr, val in bonus_validos.items())
                                c.drawString(70, y, f"Bônus de Atributos: {bonus_str}")
                                y -= 15
                        
                        # Outros bônus e informações
                        bonus_ca = item.get('bonus_ca', '').strip()
                        if bonus_ca and bonus_ca != "0":
                            c.drawString(70, y, f"Bônus de CA: {bonus_ca}")
                            y -= 15
                        
                        dano_dado = item.get('dano_dado', '').strip()
                        if dano_dado:
                            dano_tipo = item.get('dano_tipo', '').strip()
                            dano_text = f"Dano: {dano_dado}"
                            if dano_tipo:
                                dano_text += f" ({dano_tipo})"
                            c.drawString(70, y, dano_text)
                            y -= 15
                        
                        descricao = item.get('descricao', '').strip()
                        if descricao:
                            desc_lines = self._wrap_text(descricao, c, normal_font[0], normal_font[1], width - 140)
                            for line in desc_lines:
                                if y < 100:
                                    c.showPage()
                                    y = height - 50
                                c.drawString(70, y, line)
                                y -= 15
                        y -= 20

            c.save()
            messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")

    def _wrap_text(self, text, canvas, font_name, font_size, max_width):
        """Quebra o texto em linhas para caber na largura especificada"""
        canvas.setFont(font_name, font_size)
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if canvas.stringWidth(test_line) < max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def import_from_pdf(self):
        try:
            from pdfminer.high_level import extract_text
            from pdfminer.layout import LAParams
        except ImportError:
            messagebox.showerror("Erro", "Por favor, instale a biblioteca pdfminer.six usando: pip install pdfminer.six")
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="ficha_dnd.pdf"
        )
        
        if not file_path:
            return

        try:
            text = extract_text(file_path, laparams=LAParams())
            sections = text.split('\n\n')
            
            extracted_data = {
                'basic_info': {},
                'classes': {},
                'attributes': {},
                'skills': {},
                'spells': [],
                'abilities': [],
                'features': [],
                'inventory': [],
                'resources': {
                    'Vida': {'atual': '0', 'max': '0'},
                    'Mana': {'atual': '0', 'max': '0'},
                    'Estamina': {'atual': '0', 'max': '0'}
                }
            }
            
            current_section = None
            current_item = None
            
            for section in sections:
                section = section.strip()
                
                # Identificar seções principais
                if "Recursos" in section:
                    current_section = 'resources'
                    continue
                elif "Informações Básicas" in section:
                    current_section = 'basic_info'
                    continue
                elif "Classes" in section:
                    current_section = 'classes'
                    continue
                elif "Atributos" in section:
                    current_section = 'attributes'
                    continue
                elif "Magias" in section:
                    current_section = 'spells'
                    continue
                elif "Talentos" in section:
                    current_section = 'abilities'
                    continue
                elif "Habilidades" in section:
                    current_section = 'features'
                    continue
                elif "Inventário" in section:
                    current_section = 'inventory'
                    continue
                
                # Processar recursos
                if current_section == 'resources':
                    for line in section.split('\n'):
                        line = line.strip()
                        if not line or ':' not in line:
                            continue
                        
                        # Formato esperado: "Recurso: atual/máximo"
                        for resource in ['Vida', 'Mana', 'Estamina']:
                            if line.startswith(resource):
                                values = line.split(':')[1].strip()
                                if '/' in values:
                                    atual, maximo = values.split('/')
                                    extracted_data['resources'][resource] = {
                                        'atual': atual.strip(),
                                        'max': maximo.strip()
                                    }
                
                # Processar conteúdo baseado na seção atual
                if current_section == 'basic_info':
                    for line in section.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            if key in ['Nome', 'Raça', 'Nível']:
                                extracted_data['basic_info'][key] = value
                
                elif current_section == 'attributes':
                    for line in section.split('\n'):
                        if ':' in line:
                            attr, value = line.split(':', 1)
                            attr = attr.strip()
                            if '(' in value:
                                value = value.split('(')[0].strip()
                            if attr in ['FOR', 'DES', 'CON', 'INT', 'SAB', 'CAR']:
                                extracted_data['attributes'][attr] = value
                
                elif current_section == 'spells':
                    spell = {}
                    for line in section.split('\n'):
                        if line.startswith('Nível'):
                            if spell:
                                extracted_data['spells'].append(spell.copy())
                                spell = {}
                            spell['nivel'] = line.split(':')[1].strip()
                        elif ':' in line:
                            key, value = line.split(':', 1)
                            spell[key.strip().lower()] = value.strip()
                    if spell:
                        extracted_data['spells'].append(spell)
                
                elif current_section in ['abilities', 'features']:
                    if ':' in section:
                        name, desc = section.split(':', 1)
                        item = {
                            'nome': name.strip(),
                            'descricao': desc.strip()
                        }
                        extracted_data[current_section].append(item)
                
                elif current_section == 'inventory':
                    lines = section.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Novo item começa quando encontramos um nome
                        if line and not line.startswith(('Bônus', 'Dano', 'Tipo', 'CA:', 'CD:')):
                            if current_item:
                                extracted_data['inventory'].append(current_item.copy())
                            current_item = {
                                'nome': line,
                                'tipo': '',
                                'bonus_atributos': {'FOR': '0', 'DES': '0', 'CON': '0', 
                                                  'INT': '0', 'SAB': '0', 'CAR': '0'},
                                'bonus_ca': '0',
                                'bonus_cd': '0',
                                'dano_dado': '',
                                'dano_tipo': '',
                                'descricao': ''
                            }
                        elif current_item:
                            if 'Bônus de Atributos:' in line:
                                bonus_str = line.split('Bônus de Atributos:')[1].strip()
                                for bonus in bonus_str.split(','):
                                    if ':' in bonus:
                                        attr, val = bonus.strip().split(':')
                                        current_item['bonus_atributos'][attr.strip()] = val.strip()
                            elif line.startswith('Bônus de CA:'):
                                current_item['bonus_ca'] = line.split(':')[1].strip()
                            elif line.startswith('Bônus de CD:'):
                                current_item['bonus_cd'] = line.split(':')[1].strip()
                            elif line.startswith('Dano:'):
                                dano_info = line.split(':')[1].strip()
                                if '(' in dano_info:
                                    current_item['dano_dado'] = dano_info.split('(')[0].strip()
                                    current_item['dano_tipo'] = dano_info.split('(')[1].rstrip(')').strip()
                                else:
                                    current_item['dano_dado'] = dano_info
                            elif line.startswith('Tipo:'):
                                current_item['tipo'] = line.split(':')[1].strip()
                            else:
                                if current_item['descricao']:
                                    current_item['descricao'] += '\n'
                                current_item['descricao'] += line

                    # Adicionar o último item se existir
                    if current_item:
                        extracted_data['inventory'].append(current_item)

            # Atualizar interface com dados extraídos
            self._update_interface_from_extracted_data(extracted_data)
            messagebox.showinfo("Sucesso", "Dados importados do PDF com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar PDF: {str(e)}")
            import traceback
            traceback.print_exc()  # Isso ajudará a debugar mostrando o erro completo

    def _update_interface_from_extracted_data(self, data):
        """Atualiza a interface com os dados extraídos do PDF"""
        
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

class SpellScreen:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Magias")
        self.window.geometry("1000x600")
        
        # Dados de magias
        self.spells_data = getattr(parent, 'spells_data', [])
        parent.spells_data = self.spells_data
        
        # Criar search_var antes de usar
        self.search_var = tk.StringVar()
        
        # Criar interface
        self.create_interface()
        self.load_spells()

    def create_interface(self):
        # Adicionar barra de busca no topo
        search_frame = ttk.Frame(self.window)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_var.trace('w', lambda *args: self.filter_spells())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Notebook para níveis de magia
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Criar abas para cada nível de magia (0-9)
        self.spell_frames = {}
        self.spell_lists = {}
        
        for level in range(10):
            frame = ttk.Frame(self.notebook)
            self.spell_frames[level] = frame
            self.notebook.add(frame, text=f"Nível {level}")
            
            # Lista de magias
            list_frame = ttk.Frame(frame)
            list_frame.pack(side="left", fill="both", expand=True)
            
            spell_list = tk.Listbox(list_frame, width=30)
            spell_list.pack(side="left", fill="both", expand=True)
            self.spell_lists[level] = spell_list
            
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=spell_list.yview)
            scrollbar.pack(side="right", fill="y")
            spell_list.config(yscrollcommand=scrollbar.set)
            
            # Formulário de cadastro
            form_frame = ttk.LabelFrame(frame, text="Nova Magia")
            form_frame.pack(side="right", fill="both", padx=5)
            
            self.create_spell_form(form_frame, level)

    def filter_spells(self, *args):
        search_term = self.search_var.get().lower().strip()
        
        # Limpar e recarregar todas as listas
        for level, spell_list in self.spell_lists.items():
            spell_list.delete(0, tk.END)
            
            if level in self.all_spells:
                for spell in self.all_spells[level]:
                    # Busca no nome e na descrição
                    if (search_term in spell['nome'].lower() or 
                        search_term in spell.get('descricao', '').lower()):
                        spell_list.insert(tk.END, spell['nome'])
    
    def load_spells(self):
        # Organizar magias por nível
        self.all_spells = {i: [] for i in range(10)}
        for spell in self.parent.spells_data:
            level = spell.get('nivel', 0)
            if isinstance(level, (int, str)) and 0 <= int(level) <= 9:
                self.all_spells[int(level)].append(spell)
        
        # Carregar listas inicialmente
        self.filter_spells()

    def create_spell_form(self, frame, level):
        # Campos padrão do D&D 5e
        fields = [
            ("Nome", "entry"),
            ("Escola", "combo", ["Abjuração", "Adivinhação", "Conjuração", "Encantamento", 
                               "Evocação", "Ilusão", "Necromancia", "Transmutação"]),
            ("Tempo de Conjuração", "entry"),
            ("Alcance", "entry"),
            ("Componentes", "entry"),
            ("Duração", "entry"),
            ("Teste de Resistência", "combo", ["Nenhum", "Força", "Destreza", "Constituição", 
                                             "Inteligência", "Sabedoria", "Carisma"]),
            ("Dano/Efeito", "entry"),
            ("Descrição", "text")
        ]
        
        entries = {}
        row = 0
        
        for field_info in fields:
            field_name = field_info[0]
            field_type = field_info[1]
            
            ttk.Label(frame, text=field_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            
            if field_type == "entry":
                entry = ttk.Entry(frame, width=40)
                entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
                entries[field_name] = entry
            
            elif field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(frame, textvariable=var, values=field_info[2], width=37)
                combo.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
                entries[field_name] = combo
            
            elif field_type == "text":
                text = tk.Text(frame, height=6, width=40)
                text.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
                entries[field_name] = text
            
            row += 1
        
        ttk.Button(frame, text="Salvar Magia", 
                  command=lambda: self.save_spell(level, entries)).grid(row=row, column=0, 
                  columnspan=2, pady=10)
                  
        return entries

    def save_spell(self, level, entries):
        spell = {
            'nivel': level,
            'nome': entries['Nome'].get(),
            'escola': entries['Escola'].get(),
            'tempo_conjuracao': entries['Tempo de Conjuração'].get(),
            'alcance': entries['Alcance'].get(),
            'componentes': entries['Componentes'].get(),
            'duracao': entries['Duração'].get(),
            'teste_resistencia': entries['Teste de Resistência'].get(),
            'dano_efeito': entries['Dano/Efeito'].get(),
            'descricao': entries['Descrição'].get("1.0", tk.END).strip()
        }

        self.parent.spells_data.append(spell)
        self.spell_lists[level].insert(tk.END, spell['nome'])
        
        # Limpar campos
        for entry in entries.values():
            if isinstance(entry, (ttk.Entry, ttk.Combobox)):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.Text):
                entry.delete('1.0', tk.END)
        
        self.parent.update_all()

    def on_spell_select(self, level):
        spell_list = self.spell_lists[level]
        selection = spell_list.curselection()
        
        if not selection:
            return
            
        index = selection[0]
        spell_name = spell_list.get(index)
        
        # Encontrar a magia nos dados
        spell = next((s for s in self.parent.spells_data if s['nome'] == spell_name and s['nivel'] == level), None)
        
        if spell:
            entries = self.spell_frames[level].winfo_children()[1].winfo_children()
            form_entries = {}
            current_label = None
            
            for widget in entries:
                if isinstance(widget, ttk.Label):
                    current_label = widget['text']
                elif isinstance(widget, (ttk.Entry, ttk.Combobox, tk.Text)):
                    form_entries[current_label] = widget
            
            # Preencher os campos
            for field, value in spell.items():
                if field == 'nivel':
                    continue
                    
                field_map = {
                    'nome': 'Nome',
                    'escola': 'Escola',
                    'tempo_conjuracao': 'Tempo de Conjuração',
                    'alcance': 'Alcance',
                    'componentes': 'Componentes',
                    'duracao': 'Duração',
                    'teste_resistencia': 'Teste de Resistência',
                    'dano_efeito': 'Dano/Efeito',
                    'descricao': 'Descrição'
                }
                
                field_name = field_map.get(field)
                if field_name and field_name in form_entries:
                    entry = form_entries[field_name]
                    if isinstance(entry, (ttk.Entry, ttk.Combobox)):
                        entry.delete(0, tk.END)
                        entry.insert(0, value)
                    elif isinstance(entry, tk.Text):
                        entry.delete('1.0', tk.END)
                        entry.insert('1.0', value)

    def delete_spell(self, level):
        spell_list = self.spell_lists[level]
        selection = spell_list.curselection()
        
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma magia para excluir")
            return
            
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta magia?"):
            index = selection[0]
            spell_name = spell_list.get(index)
            
            # Remover da lista e dos dados
            spell_list.delete(index)
            self.parent.spells_data = [s for s in self.parent.spells_data 
                                     if not (s['nome'] == spell_name and s['nivel'] == level)]
            
            self.clear_form(level)

    def clear_form(self, level):
        entries = self.spell_frames[level].winfo_children()[1].winfo_children()
        for widget in entries:
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
        
        self.spell_lists[level].selection_clear(0, tk.END)

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
    