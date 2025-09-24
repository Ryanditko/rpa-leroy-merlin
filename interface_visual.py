#!/usr/bin/env python3
"""
🎨 INTERFACE VISUAL - AUTOMAÇÃO LEROY MERLIN
Interface gráfica moderna para execução das automações

Cores Leroy Merlin:
- Verde Principal: #00A859
- Verde Escuro: #008A47
- Laranja: #FF6B35
- Cinza Escuro: #333333
- Branco: #FFFFFF
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import sys
import os
from datetime import datetime
import subprocess
from tkinter import messagebox as mb
from tkinter import ttk

# Adicionar o diretório src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

# Importar renomeador
from renomeador_inteligente import RenomeadorInteligente

class AutomacaoLeroyMerlinGUI:
    """Interface visual para automação Leroy Merlin"""
    
    def __init__(self):
        # Cores da Leroy Merlin
        self.CORES = {
            'verde_principal': '#00A859',
            'verde_escuro': '#008A47', 
            'verde_claro': '#4CAF50',
            'laranja': '#FF6B35',
            'laranja_escuro': '#E55A2B',
            'azul_info': '#17A2B8',
            'azul_escuro': '#138496',
            'cinza_escuro': '#333333',
            'cinza_medio': '#666666',
            'cinza_claro': '#F5F5F5',
            'cinza_muito_claro': '#FAFAFA',
            'branco': '#FFFFFF',
            'amarelo': '#FFC107',
            'vermelho': '#DC3545'
        }
        
        self.janela_principal = None
        self.texto_log = None
        self.botao_executar = None
        self.botao_renomear = None
        self.progresso = None
        self.status_label = None
        self.executando = False
        self.renomeador = RenomeadorInteligente()
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria a interface principal"""
        # Janela principal
        self.janela_principal = tk.Tk()
        self.janela_principal.title("🚀 Automação Leroy Merlin - RPA Boletins v2.2")
        self.janela_principal.geometry("1000x700")  # Altura otimizada para melhor usabilidade
        self.janela_principal.configure(bg=self.CORES['cinza_muito_claro'])
        self.janela_principal.minsize(900, 700)
        
        # Ícone da janela (se disponível)
        try:
            self.janela_principal.iconbitmap(default="favicon.ico")
        except:
            pass
        
        # Estilo personalizado
        self.configurar_estilos()
        
        # Criar canvas principal com scroll
        self.criar_canvas_principal()
        
        # Header com logo e título
        self.criar_header()
        
        # Área de controles (prioridade)
        self.criar_controles()
        
        # Área de logs (compacta)
        self.criar_area_logs()
        
        # Footer com informações
        self.criar_footer()
        
        # Configurar scroll da janela
        self.configurar_scroll()
        
        # Centralizar janela
        self.centralizar_janela()
    
    def configurar_estilos(self):
        """Configura estilos personalizados com visual melhorado"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Botão principal verde com hover melhorado
        style.configure(
            'Verde.TButton',
            background=self.CORES['verde_principal'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 11, 'bold'),
            padding=(20, 15),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Verde.TButton',
                  background=[('active', self.CORES['verde_escuro']),
                             ('pressed', self.CORES['verde_escuro']),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão renomear verde claro com melhor visual
        style.configure(
            'VerdeClaro.TButton',
            background=self.CORES['verde_claro'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 12),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('VerdeClaro.TButton',
                  background=[('active', self.CORES['verde_principal']),
                             ('pressed', self.CORES['verde_escuro']),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão laranja com visual melhorado
        style.configure(
            'Laranja.TButton',
            background=self.CORES['laranja'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 9, 'bold'),
            padding=(15, 10),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Laranja.TButton',
                  background=[('active', self.CORES['laranja_escuro']),
                             ('pressed', self.CORES['laranja_escuro']),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão info azul melhorado
        style.configure(
            'Info.TButton',
            background=self.CORES['azul_info'],
            foreground=self.CORES['branco'],
            font=('Segoe UI', 9, 'bold'),
            padding=(12, 8),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Info.TButton',
                  background=[('active', self.CORES['azul_escuro']),
                             ('pressed', self.CORES['azul_escuro']),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Botão perigo vermelho melhorado
        style.configure(
            'Perigo.TButton',
            background='#DC3545',
            foreground=self.CORES['branco'],
            font=('Segoe UI', 9, 'bold'),
            padding=(10, 8),
            relief='flat',
            borderwidth=0,
            focuscolor='none'
        )
        style.map('Perigo.TButton',
                  background=[('active', '#C82333'),
                             ('pressed', '#BD2130'),
                             ('disabled', '#CCCCCC')],
                  foreground=[('disabled', '#666666')])
        
        # Barra de progresso verde personalizada
        style.configure(
            'Verde.Horizontal.TProgressbar',
            troughcolor=self.CORES['cinza_claro'],
            background=self.CORES['verde_principal'],
            lightcolor=self.CORES['verde_claro'],
            darkcolor=self.CORES['verde_escuro'],
            relief='flat',
            borderwidth=2,
            focuscolor='none'
        )
    
    def criar_canvas_principal(self):
        """Cria canvas principal com scroll para interface responsiva"""
        # Canvas principal
        self.canvas = tk.Canvas(
            self.janela_principal,
            bg=self.CORES['cinza_muito_claro'],
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.janela_principal, 
            orient="vertical", 
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame que conterá todo o conteúdo
        self.frame_conteudo = tk.Frame(self.canvas, bg=self.CORES['cinza_muito_claro'])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_conteudo, anchor="nw")
        
        # Posicionar canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind para atualizar scroll region
        self.frame_conteudo.bind("<Configure>", self.atualizar_scroll)
        self.canvas.bind("<Configure>", self.redimensionar_canvas)
        
        # Habilitar scroll com mouse wheel
        self.canvas.bind("<MouseWheel>", self.scroll_mouse)
        
        # Agora usar frame_conteudo como container principal
        self.container_principal = self.frame_conteudo
    
    def criar_header(self):
        """Cria o cabeçalho com logo e título melhorado"""
        # Frame principal do header com gradiente visual
        header_frame = tk.Frame(self.container_principal, bg=self.CORES['verde_principal'], height=70)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Frame interno para centralização
        header_content = tk.Frame(header_frame, bg=self.CORES['verde_principal'])
        header_content.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Ícone do foguete (maior e melhor posicionado)
        icon_label = tk.Label(
            header_content,
            text="🚀",
            font=('Segoe UI Emoji', 28, 'bold'),
            bg=self.CORES['verde_principal'],
            fg=self.CORES['branco']
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        # Frame para textos
        texto_frame = tk.Frame(header_content, bg=self.CORES['verde_principal'])
        texto_frame.pack(side='left', fill='y', expand=True)
        
        # Título principal
        titulo_label = tk.Label(
            texto_frame,
            text="AUTOMAÇÃO LEROY MERLIN",
            font=('Segoe UI', 18, 'bold'),
            bg=self.CORES['verde_principal'],
            fg=self.CORES['branco']
        )
        titulo_label.pack(anchor='w')
        
        # Subtítulo melhorado
        subtitulo_label = tk.Label(
            texto_frame,
            text="Processamento Automático • Renomeação Inteligente • Interface Visual v2.2",
            font=('Segoe UI', 10, 'normal'),
            bg=self.CORES['verde_principal'],
            fg=self.CORES['cinza_muito_claro']
        )
        subtitulo_label.pack(anchor='w', pady=(2, 0))
        
        # Frame para status/indicadores (lado direito)
        status_frame = tk.Frame(header_content, bg=self.CORES['verde_principal'])
        status_frame.pack(side='right', fill='y')
        
        # Indicador de sistema online
        online_label = tk.Label(
            status_frame,
            text="🟢 SISTEMA ONLINE",
            font=('Segoe UI', 9, 'bold'),
            bg=self.CORES['verde_principal'],
            fg=self.CORES['branco']
        )
        online_label.pack(anchor='e')
        
        # Data/hora
        from datetime import datetime
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        data_label = tk.Label(
            status_frame,
            text=f"📅 {agora}",
            font=('Segoe UI', 9, 'normal'),
            bg=self.CORES['verde_principal'],
            fg=self.CORES['cinza_muito_claro']
        )
        data_label.pack(anchor='e', pady=(2, 0))
        
        # Linha decorativa
        linha_decorativa = tk.Frame(header_frame, bg=self.CORES['laranja'], height=3)
        linha_decorativa.pack(fill='x', side='bottom')
    
    def criar_controles(self):
        """Cria área de controles e opções"""
        controles_frame = tk.Frame(self.container_principal, bg=self.CORES['cinza_muito_claro'])
        controles_frame.pack(fill='x', padx=15, pady=10)
        
        # Frame superior com duas colunas
        superior_frame = tk.Frame(controles_frame, bg=self.CORES['cinza_muito_claro'])
        superior_frame.pack(fill='x', pady=(0, 8))
        
        # Coluna esquerda - Opções de Execução (melhorada)
        opcoes_frame = tk.LabelFrame(
            superior_frame,
            text="📋 Opções de Execução",
            font=('Segoe UI', 12, 'bold'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_escuro'],
            relief='groove',
            bd=2,
            padx=15,
            pady=12
        )
        opcoes_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Variáveis para checkboxes
        self.var_genesys = tk.BooleanVar(value=True)
        self.var_salesforce = tk.BooleanVar(value=True)
        self.var_verbose = tk.BooleanVar(value=False)
        
        # Checkboxes melhorados com estilo moderno
        checkbox_frame = tk.Frame(opcoes_frame, bg=self.CORES['branco'])
        checkbox_frame.pack(fill='x', padx=5, pady=8)
        
        # Checkbox Genesys melhorado
        cb_genesys = tk.Checkbutton(
            checkbox_frame,
            text="📊 Processar Genesys (VOZ, TEXTO, GESTÃO)",
            variable=self.var_genesys,
            font=('Segoe UI', 11, 'normal'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_escuro'],
            activebackground=self.CORES['verde_claro'],
            activeforeground=self.CORES['branco'],
            selectcolor=self.CORES['verde_principal'],
            relief='flat',
            highlightthickness=0,
            bd=0
        )
        cb_genesys.pack(anchor='w', pady=5)
        
        # Checkbox Salesforce melhorado
        cb_salesforce = tk.Checkbutton(
            checkbox_frame,
            text="💼 Processar Salesforce (CRIADO, RESOLVIDO, COMENTÁRIOS)",
            variable=self.var_salesforce,
            font=('Segoe UI', 11, 'normal'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_escuro'],
            activebackground=self.CORES['verde_claro'],
            activeforeground=self.CORES['branco'],
            selectcolor=self.CORES['verde_principal'],
            relief='flat',
            highlightthickness=0,
            bd=0
        )
        cb_salesforce.pack(anchor='w', pady=5)
        
        # Checkbox Verbose melhorado
        cb_verbose = tk.Checkbutton(
            checkbox_frame,
            text="🔍 Modo detalhado (logs completos)",
            variable=self.var_verbose,
            font=('Segoe UI', 10, 'normal'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_medio'],
            activebackground=self.CORES['azul_info'],
            activeforeground=self.CORES['branco'],
            selectcolor=self.CORES['azul_info'],
            relief='flat',
            highlightthickness=0,
            bd=0
        )
        cb_verbose.pack(anchor='w', pady=5)
        
        # Coluna direita - Gestão de Arquivos
        gestao_frame = tk.LabelFrame(
            superior_frame,
            text="📁 Gestão de Arquivos",
            font=('Arial', 12, 'bold'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_escuro'],
            relief='solid',
            bd=1,
            padx=10,
            pady=10
        )
        gestao_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Botões de gestão de arquivos
        gestao_botoes_frame = tk.Frame(gestao_frame, bg=self.CORES['branco'])
        gestao_botoes_frame.pack(fill='x', padx=10, pady=10)
        
        # Botão renomear arquivos (NOVO)
        self.botao_renomear = ttk.Button(
            gestao_botoes_frame,
            text="� Renomear Arquivos",
            style='VerdeClaro.TButton',
            command=self.renomear_arquivos
        )
        self.botao_renomear.pack(fill='x', pady=(0, 5))
        
        # Botão verificar arquivos
        botao_verificar = ttk.Button(
            gestao_botoes_frame,
            text="📁 Verificar Arquivos",
            style='Info.TButton',
            command=self.verificar_arquivos
        )
        botao_verificar.pack(fill='x', pady=3)
        
        # Botão abrir pasta dados
        botao_pasta = ttk.Button(
            gestao_botoes_frame,
            text="📂 Abrir Pasta Dados",
            style='Info.TButton',
            command=self.abrir_pasta_dados
        )
        botao_pasta.pack(fill='x', pady=(3, 3))
        
        # Separador visual
        separador = tk.Frame(gestao_botoes_frame, height=2, bg=self.CORES['cinza_claro'])
        separador.pack(fill='x', pady=5)
        
        # Label para seção de planilhas
        label_planilhas = tk.Label(
            gestao_botoes_frame,
            text="🔗 Acesso Rápido às Planilhas",
            font=('Arial', 9, 'bold'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_escuro']
        )
        label_planilhas.pack(pady=(5, 5))
        
        # Botão planilha Genesys
        botao_planilha_genesys = ttk.Button(
            gestao_botoes_frame,
            text="📊 Planilha Genesys",
            style='VerdeClaro.TButton',
            command=lambda: self.abrir_planilha('genesys')
        )
        botao_planilha_genesys.pack(fill='x', pady=(0, 3))
        
        # Botão planilha Salesforce
        botao_planilha_salesforce = ttk.Button(
            gestao_botoes_frame,
            text="💼 Planilha Salesforce",
            style='Info.TButton',
            command=lambda: self.abrir_planilha('salesforce')
        )
        botao_planilha_salesforce.pack(fill='x', pady=(3, 0))
        
        # Frame para botões principais
        botoes_frame = tk.Frame(controles_frame, bg=self.CORES['cinza_muito_claro'])
        botoes_frame.pack(fill='x', pady=15)
        
        # Frame para botões individuais (primeira linha)
        botoes_individuais_frame = tk.Frame(botoes_frame, bg=self.CORES['cinza_muito_claro'])
        botoes_individuais_frame.pack(fill='x', pady=(0, 10))
        
        # Botão Genesys individual
        self.botao_genesys = ttk.Button(
            botoes_individuais_frame,
            text="📊 GENESYS APENAS",
            style='Verde.TButton',
            command=lambda: self.executar_individual('genesys')
        )
        self.botao_genesys.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        # Botão Salesforce individual  
        self.botao_salesforce = ttk.Button(
            botoes_individuais_frame,
            text="💼 SALESFORCE APENAS", 
            style='Verde.TButton',
            command=lambda: self.executar_individual('salesforce')
        )
        self.botao_salesforce.pack(side='right', expand=True, fill='x', padx=(5, 0))
        
        # Botão principal EXECUTAR (centralizado e maior) - segunda linha
        botoes_principais_frame = tk.Frame(botoes_frame, bg=self.CORES['cinza_muito_claro'])
        botoes_principais_frame.pack(expand=True)
        
        self.botao_executar = ttk.Button(
            botoes_principais_frame,
            text="🚀 EXECUTAR AUTOMAÇÃO COMPLETA",
            style='Verde.TButton',
            command=self.executar_automacao
        )
        self.botao_executar.pack(side='left', padx=10)
        
        # Botão limpar logs
        botao_limpar = ttk.Button(
            botoes_principais_frame,
            text="🧹 Limpar Logs",
            style='Laranja.TButton',
            command=self.limpar_logs
        )
        botao_limpar.pack(side='left', padx=10)
        
        # Status e barra de progresso melhorados
        status_frame = tk.LabelFrame(
            controles_frame,
            text="📊 Status do Sistema",
            font=('Arial', 10, 'bold'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_escuro'],
            relief='solid',
            bd=1,
            padx=10,
            pady=5
        )
        status_frame.pack(fill='x', pady=(10, 0))
        
        # Label de status melhorado
        self.status_label = tk.Label(
            status_frame,
            text="💚 Sistema pronto para execução",
            font=('Segoe UI', 11, 'bold'),
            bg=self.CORES['branco'],
            fg=self.CORES['verde_escuro']
        )
        self.status_label.pack(anchor='w', pady=(8, 8))
        
        # Barra de progresso com estilo melhorado
        self.progresso = ttk.Progressbar(
            status_frame,
            style='Verde.Horizontal.TProgressbar',
            mode='indeterminate',
            length=500
        )
        self.progresso.pack(fill='x', pady=(0, 8))
    
    def criar_area_logs(self):
        """Cria área de logs compacta"""
        logs_frame = tk.LabelFrame(
            self.container_principal,
            text="📄 Logs de Execução",
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['branco'],
            fg=self.CORES['cinza_escuro'],
            relief='groove',
            bd=1,
            padx=5,
            pady=5
        )
        logs_frame.pack(fill='x', padx=15, pady=(5, 10))
        logs_frame.pack_propagate(False)
        logs_frame.configure(height=120)  # Altura bem reduzida
        
        # Frame interno para melhor organização
        logs_content = tk.Frame(logs_frame, bg=self.CORES['branco'])
        logs_content.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Área de texto compacta
        self.texto_log = scrolledtext.ScrolledText(
            logs_content,
            font=('Consolas', 8),
            bg='#2D2D2D',
            fg='#FFFFFF',
            insertbackground='white',
            selectbackground='#0078D4',
            selectforeground='white',
            wrap='word',
            height=5,  # Altura bem reduzida
            width=100,
            relief='flat',
            bd=0,
            padx=3,
            pady=2,
            state='normal'
        )
        self.texto_log.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Inserir texto de teste imediatamente
        self.texto_log.insert('end', "🔧 Sistema iniciando...\n")
        self.texto_log.see('end')
        
        # Configurar tags para cores melhoradas e modernas
        self.texto_log.tag_configure('sucesso', foreground='#50FA7B', font=('Consolas', 8, 'bold'))
        self.texto_log.tag_configure('erro', foreground='#FF5555', font=('Consolas', 8, 'bold'))
        self.texto_log.tag_configure('info', foreground='#8BE9FD', font=('Consolas', 8))
        self.texto_log.tag_configure('aviso', foreground='#F1FA8C', font=('Consolas', 8, 'bold'))
        self.texto_log.tag_configure('destaque', foreground='#BD93F9', font=('Consolas', 8, 'bold'))
        
        # Forçar atualização antes de adicionar mensagens
        self.janela_principal.update_idletasks()
        
        # Exibir mensagens iniciais imediatamente
        self.exibir_mensagens_iniciais()
    
    def exibir_mensagens_iniciais(self):
        """Exibe mensagens iniciais no log"""
        self.log_mensagem("🎯 Interface Visual Leroy Merlin v2.2 iniciada com sucesso!", 'destaque')
        self.log_mensagem("📋 Configure as opções acima e execute a automação", 'info')
        self.log_mensagem("🔗 NOVO: Use os links rápidos para acessar as planilhas diretamente", 'aviso')
        self.log_mensagem("✨ NOVIDADES: Execução individual + Encoding robusto + Coloração completa", 'aviso')
        self.log_mensagem("🎨 Agora todas as linhas da planilha são pintadas com verde Leroy Merlin!", 'sucesso')
        self.log_mensagem("-" * 70, 'info')
    
    def criar_footer(self):
        """Cria rodapé simplificado"""
        footer_frame = tk.Frame(self.container_principal, bg=self.CORES['verde_escuro'], height=40)
        footer_frame.pack(fill='x', pady=(5, 0))
        footer_frame.pack_propagate(False)
        
        # Informações do sistema - layout mais limpo
        info_frame = tk.Frame(footer_frame, bg=self.CORES['verde_escuro'])
        info_frame.pack(expand=True, fill='both')
        
        # Data/hora
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data_label = tk.Label(
            info_frame,
            text=f"⏰ {agora}",
            font=('Arial', 9),
            bg=self.CORES['verde_escuro'],
            fg=self.CORES['branco']
        )
        data_label.pack(side='left', padx=20, pady=12)
        
        # Versão (centralizada)
        versao_label = tk.Label(
            info_frame,
            text="✨ Automação Boletins Leroy Merlin v2.2",
            font=('Segoe UI', 10, 'bold'),
            bg=self.CORES['verde_escuro'],
            fg=self.CORES['branco']
        )
        versao_label.pack(expand=True, pady=12)
        
        # Status (direita)
        status_label = tk.Label(
            info_frame,
            text="� Pronto para uso",
            font=('Arial', 9),
            bg=self.CORES['verde_escuro'],
            fg=self.CORES['branco']
        )
        status_label.pack(side='right', padx=20, pady=12)
    
    def configurar_scroll(self):
        """Configura os eventos de scroll da interface"""
        # Atualizar scroll region após criar todos os elementos
        self.janela_principal.after(100, self.atualizar_scroll)
    
    def atualizar_scroll(self, event=None):
        """Atualiza a região de scroll baseada no conteúdo"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def redimensionar_canvas(self, event):
        """Redimensiona o canvas quando a janela muda de tamanho"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def scroll_mouse(self, event):
        """Habilita scroll com mouse wheel"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.janela_principal.update_idletasks()
        largura = self.janela_principal.winfo_width()
        altura = self.janela_principal.winfo_height()
        x = (self.janela_principal.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela_principal.winfo_screenheight() // 2) - (altura // 2)
        self.janela_principal.geometry(f'{largura}x{altura}+{x}+{y}')
    
    def log_mensagem(self, mensagem, tag=None):
        """Adiciona mensagem ao log com timestamp e cores"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            mensagem_completa = f"[{timestamp}] {mensagem}\n"
            
            # Debug: imprimir no console também
            print(f"LOG: {mensagem_completa.strip()}")
            
            # Garantir que o widget existe
            if hasattr(self, 'texto_log') and self.texto_log:
                # Sempre manter habilitado para inserção
                self.texto_log.configure(state='normal')
                self.texto_log.insert('end', mensagem_completa, tag)
                self.texto_log.see('end')  # Auto-scroll para o final
                # Não desabilitar mais - deixar sempre editável
                self.janela_principal.update()  # Atualização imediata
            else:
                print("Widget texto_log não encontrado!")
        except Exception as e:
            print(f"Erro ao adicionar log: {e}")  # Fallback para console
    
    def verificar_arquivos(self):
        """Verifica arquivos CSV disponíveis"""
        self.log_mensagem("🔍 Verificando arquivos disponíveis...", 'info')
        
        data_dir = os.path.join(current_dir, 'data')
        
        if not os.path.exists(data_dir):
            self.log_mensagem("❌ Pasta 'data' não encontrada!", 'erro')
            messagebox.showerror("Erro", "Pasta 'data' não encontrada!\nCrie a pasta e adicione os arquivos CSV.")
            return
        
        arquivos_csv = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]
        
        if not arquivos_csv:
            self.log_mensagem("⚠️ Nenhum arquivo CSV encontrado na pasta data/", 'aviso')
            messagebox.showwarning("Aviso", "Nenhum arquivo CSV encontrado na pasta data/")
        else:
            self.log_mensagem(f"📁 Encontrados {len(arquivos_csv)} arquivos CSV:", 'sucesso')
            for arquivo in sorted(arquivos_csv):
                tamanho = os.path.getsize(os.path.join(data_dir, arquivo))
                tamanho_mb = tamanho / (1024 * 1024)
                self.log_mensagem(f"   📄 {arquivo} ({tamanho_mb:.2f} MB)", 'info')
    
    def abrir_pasta_dados(self):
        """Abre a pasta de dados no explorer"""
        data_dir = os.path.join(current_dir, 'data')
        
        if not os.path.exists(data_dir):
            # Criar pasta se não existir
            os.makedirs(data_dir)
            self.log_mensagem("📁 Pasta 'data' criada", 'info')
        
        try:
            # Abrir pasta no Windows Explorer
            os.startfile(data_dir)
            self.log_mensagem("📂 Pasta de dados aberta", 'sucesso')
        except Exception as e:
            self.log_mensagem(f"❌ Erro ao abrir pasta: {e}", 'erro')
    
    def abrir_url(self, url):
        """Abre URL no navegador padrão"""
        import webbrowser
        try:
            webbrowser.open(url)
            self.log_mensagem(f"🌐 Abrindo planilha no navegador...", 'info')
        except Exception as e:
            self.log_mensagem(f"❌ Erro ao abrir link: {e}", 'erro')
    
    def abrir_planilha(self, tipo):
        """Abre planilha oficial no navegador"""
        urls = {
            'genesys': 'https://docs.google.com/spreadsheets/d/14vJpMHAXOBnWOLLqYyB1yDazjU0yMbSuCWKyuIhzPLc',      # Planilha oficial Genesys
            'salesforce': 'https://docs.google.com/spreadsheets/d/1uBsjcNt2ZTvRlU7hkiIGLxLEGEFLYB-BEg8dm9jsM_0'  # Planilha oficial Salesforce
        }
        
        if tipo in urls:
            self.abrir_url(urls[tipo])
            self.log_mensagem(f"🔗 Planilha {tipo.title()} aberta no navegador", 'sucesso')
        else:
            self.log_mensagem(f"❌ Tipo de planilha desconhecido: {tipo}", 'erro')
    
    def limpar_logs(self):
        """Limpa a área de logs"""
        self.texto_log.configure(state='normal')
        self.texto_log.delete(1.0, 'end')
        self.texto_log.configure(state='disabled')
        self.log_mensagem("🧹 Logs limpos", 'info')
        self.log_mensagem("💚 Sistema pronto para nova operação", 'sucesso')
    
    def renomear_arquivos(self):
        """Executa renomeação inteligente de arquivos"""
        if self.executando:
            mb.showwarning("Aviso", "Operação já está em execução!")
            return
        
        # Primeiro mostrar preview
        self.log_mensagem("🔍 Analisando arquivos para renomeação...", 'info')
        
        try:
            preview = self.renomeador.preview_renomeacoes()
            
            if not preview['renomeacoes']:
                self.log_mensagem("✅ Todos os arquivos já estão com nomes padronizados!", 'sucesso')
                mb.showinfo("Informação", "Todos os arquivos já estão com nomes padronizados!")
                return
            
            # Mostrar preview das renomeações
            preview_texto = f"📝 PREVIEW DE RENOMEAÇÕES:\n\n"
            for item in preview['renomeacoes']:
                preview_texto += f"📄 {item['nome_original']}\n"
                preview_texto += f"   ➡️  {item['nome_novo']}\n"
                preview_texto += f"   🎯 {item['tipo_detectado']} ({item['tamanho_mb']} MB)\n\n"
            
            self.log_mensagem("📋 Preview das renomeações:", 'destaque')
            for item in preview['renomeacoes']:
                self.log_mensagem(f"   📄 {item['nome_original']}", 'info')
                self.log_mensagem(f"      ➡️  {item['nome_novo']}", 'aviso')
                self.log_mensagem(f"      🎯 {item['tipo_detectado']} ({item['tamanho_mb']} MB)", 'sucesso')
            
            # Perguntar confirmação
            resposta = mb.askyesno(
                "Confirmar Renomeação", 
                f"Encontrados {len(preview['renomeacoes'])} arquivos para renomear.\n\n"
                f"Deseja executar as renomeações?\n\n"
                f"(Os nomes originais serão salvos no histórico)"
            )
            
            if resposta:
                self.log_mensagem("🚀 Executando renomeações...", 'destaque')
                
                # Executar renomeações
                resultado = self.renomeador.executar_renomeacoes()
                
                if resultado['sucesso']:
                    self.log_mensagem(f"✅ Renomeação concluída com sucesso!", 'sucesso')
                    self.log_mensagem(f"📊 {resultado['sucessos']} arquivos renomeados", 'info')
                    
                    if resultado['falhas'] > 0:
                        self.log_mensagem(f"⚠️ {resultado['falhas']} arquivos com problemas", 'aviso')
                    
                    # Mostrar resultados detalhados
                    for item in resultado['renomeacoes']:
                        if item['status'] == 'sucesso':
                            self.log_mensagem(f"   ✅ {item['nome_novo']}", 'sucesso')
                        else:
                            self.log_mensagem(f"   ❌ {item['nome_original']} - {item.get('erro', 'Erro desconhecido')}", 'erro')
                    
                    mb.showinfo("Sucesso", f"Renomeação concluída!\n\n✅ {resultado['sucessos']} sucessos\n❌ {resultado['falhas']} falhas")
                else:
                    self.log_mensagem("❌ Falha na renomeação", 'erro')
                    mb.showerror("Erro", "Falha ao renomear arquivos!")
            else:
                self.log_mensagem("🚫 Renomeação cancelada pelo usuário", 'aviso')
                
        except Exception as e:
            self.log_mensagem(f"❌ Erro na renomeação: {str(e)}", 'erro')
            mb.showerror("Erro", f"Erro na renomeação:\n{str(e)}")
    
    def executar_individual(self, sistema):
        """Executa apenas um sistema específico (genesys ou salesforce)"""
        if self.executando:
            messagebox.showwarning("Aviso", "Automação já está em execução!")
            return
        
        # Confirmar execução
        sistema_nome = "📊 Genesys" if sistema == 'genesys' else "💼 Salesforce"
        resposta = messagebox.askyesno(
            f"Confirmar Execução - {sistema_nome}",
            f"Executar automação apenas para {sistema_nome}?\n\n"
            f"Isso processará somente os dados relacionados ao {sistema.upper()}."
        )
        
        if not resposta:
            return
        
        # Temporariamente definir checkboxes para executar apenas o sistema escolhido
        checkbox_original_genesys = self.var_genesys.get()
        checkbox_original_salesforce = self.var_salesforce.get()
        
        # Configurar para executar apenas o sistema selecionado
        if sistema == 'genesys':
            self.var_genesys.set(True)
            self.var_salesforce.set(False)
        else:  # salesforce
            self.var_genesys.set(False)
            self.var_salesforce.set(True)
        
        try:
            # Iniciar execução em thread separada
            thread = threading.Thread(
                target=self._executar_automacao_individual_thread, 
                args=(sistema, checkbox_original_genesys, checkbox_original_salesforce),
                daemon=True
            )
            thread.start()
        except Exception as e:
            # Restaurar checkboxes originais em caso de erro
            self.var_genesys.set(checkbox_original_genesys)
            self.var_salesforce.set(checkbox_original_salesforce)
            messagebox.showerror("Erro", f"Erro ao iniciar execução: {str(e)}")
    
    def _executar_automacao_individual_thread(self, sistema, original_genesys, original_salesforce):
        """Thread específica para execução individual"""
        try:
            # Usar o mesmo método de execução, mas com parâmetros específicos
            self._executar_automacao_thread()
        finally:
            # Sempre restaurar checkboxes originais no final
            self.var_genesys.set(original_genesys)
            self.var_salesforce.set(original_salesforce)
    
    def executar_automacao(self):
        """Executa a automação em thread separada"""
        if self.executando:
            messagebox.showwarning("Aviso", "Automação já está em execução!")
            return
        
        # Verificar se pelo menos uma opção está selecionada
        if not self.var_genesys.get() and not self.var_salesforce.get():
            messagebox.showerror("Erro", "Selecione pelo menos uma opção (Genesys ou Salesforce)!")
            return
        
        # Iniciar execução em thread separada
        thread = threading.Thread(target=self._executar_automacao_thread, daemon=True)
        thread.start()
    
    def _executar_automacao_thread(self):
        """Thread para execução da automação com encoding robusto"""
        try:
            self.executando = True
            
            # Atualizar interface
            self.botao_executar.configure(text="⏳ EXECUTANDO...", state='disabled')
            self.botao_genesys.configure(state='disabled')
            self.botao_salesforce.configure(state='disabled')
            self.botao_renomear.configure(state='disabled')
            self.status_label.configure(text="🔄 Executando automação...", fg=self.CORES['laranja'])
            self.progresso.start()
            
            self.log_mensagem("🚀 Iniciando automação...", 'sucesso')
            
            # Construir comando
            comando = ["python", "main.py"]
            
            # Adicionar opções baseadas nos checkboxes
            if self.var_genesys.get() and not self.var_salesforce.get():
                comando.append("--genesys")
                self.log_mensagem("🎯 Modo: Apenas Genesys", 'info')
            elif self.var_salesforce.get() and not self.var_genesys.get():
                comando.append("--salesforce")
                self.log_mensagem("🎯 Modo: Apenas Salesforce", 'info')
            else:
                self.log_mensagem("🎯 Modo: Genesys + Salesforce", 'info')
            
            if self.var_verbose.get():
                comando.append("--verbose")
                self.log_mensagem("🔍 Modo detalhado ativado", 'info')
            
            # Configurar variáveis de ambiente para encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONLEGACYWINDOWSFSENCODING'] = '0'
            
            self.log_mensagem(f"📋 Comando: {' '.join(comando)}", 'info')
            
            # Executar comando com encoding robusto
            processo = subprocess.Popen(
                comando,
                cwd=current_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,  # Capturar stderr separadamente
                text=True,
                encoding='utf-8',
                errors='replace',  # Substituir caracteres inválidos
                universal_newlines=True,
                env=env,
                bufsize=0  # Sem buffer para saída em tempo real
            )
            
            # Ler saída em tempo real (stdout e stderr)
            import select
            import time
            
            # Para Windows, ler linha por linha
            linha_count = 0
            while processo.poll() is None:
                # Ler stdout
                if processo.stdout.readable():
                    linha = processo.stdout.readline()
                    if linha:
                        linha = linha.strip()
                        if linha:
                            linha_count += 1
                            # Detectar tipo de mensagem baseado em emojis/símbolos
                            if '✅' in linha or 'sucesso' in linha.lower():
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'sucesso')
                            elif '❌' in linha or 'erro' in linha.lower() or 'falha' in linha.lower():
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'erro')
                            elif '⚠️' in linha or 'aviso' in linha.lower():
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'aviso')
                            elif '🔍' in linha or '📊' in linha or '💼' in linha:
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'info')
                            elif linha.startswith('=') or linha.startswith('-'):
                                self.log_mensagem(f"[{linha_count:03d}] {linha}", 'destaque')
                            else:
                                self.log_mensagem(f"[{linha_count:03d}] {linha}")
                
                time.sleep(0.01)  # Pequena pausa para não sobrecarregar CPU
            
            # Ler qualquer saída restante
            stdout_restante, stderr_output = processo.communicate()
            
            if stdout_restante:
                for linha in stdout_restante.split('\n'):
                    linha = linha.strip()
                    if linha:
                        linha_count += 1
                        self.log_mensagem(f"[{linha_count:03d}] {linha}")
            
            # Capturar stderr se houver
            if stderr_output:
                self.log_mensagem("🔍 Saída de erro (stderr):", 'aviso')
                for linha in stderr_output.split('\n'):
                    linha = linha.strip()
                    if linha:
                        linha_count += 1
                        self.log_mensagem(f"[ERR{linha_count:03d}] {linha}", 'erro')
            
            # Verificar código de retorno
            if processo.returncode == 0:
                self.log_mensagem("🎉 Automação concluída com sucesso!", 'sucesso')
                self.status_label.configure(text="✅ Automação concluída com sucesso!", fg=self.CORES['verde_principal'])
                messagebox.showinfo("Sucesso", "Automação concluída com sucesso! ✅")
            else:
                self.log_mensagem(f"❌ Automação falhou (código {processo.returncode})", 'erro')
                self.status_label.configure(text="❌ Automação falhou", fg=self.CORES['laranja'])
                
                # Construir mensagem de erro mais detalhada
                erro_msg = f"Automação falhou (código {processo.returncode})"
                if stderr_output:
                    erro_msg += f"\n\nDetalhes do erro:\n{stderr_output[:500]}"  # Limitar tamanho
                
                messagebox.showerror("Erro", erro_msg)
                
        except Exception as e:
            error_msg = str(e)
            self.log_mensagem(f"❌ Erro na execução: {error_msg}", 'erro')
            self.status_label.configure(text="❌ Erro na execução", fg=self.CORES['laranja'])
            
            # Tentar capturar mais detalhes do erro
            import traceback
            traceback_info = traceback.format_exc()
            self.log_mensagem(f"🔍 Traceback completo:", 'info')
            for linha in traceback_info.split('\n'):
                if linha.strip():
                    self.log_mensagem(f"    {linha}", 'erro')
            
            messagebox.showerror("Erro", f"Erro na execução:\n{error_msg}\n\nVerifique o log para mais detalhes.")
            
        finally:
            # Restaurar interface
            self.executando = False
            self.botao_executar.configure(text="🚀 EXECUTAR AUTOMAÇÃO COMPLETA", state='normal')
            self.botao_genesys.configure(state='normal')
            self.botao_salesforce.configure(state='normal')
            self.botao_renomear.configure(state='normal')
            self.progresso.stop()
            if not self.status_label.cget('text').startswith(('❌', '✅')):
                self.status_label.configure(text="💚 Pronto para nova execução", fg=self.CORES['verde_escuro'])
    
    def executar(self):
        """Inicia a interface"""
        try:
            self.janela_principal.mainloop()
        except KeyboardInterrupt:
            print("Interface encerrada pelo usuário")
        except Exception as e:
            print(f"Erro na interface: {e}")

def main():
    """Função principal"""
    try:
        app = AutomacaoLeroyMerlinGUI()
        app.executar()
    except Exception as e:
        print(f"Erro ao iniciar interface: {e}")

if __name__ == "__main__":
    main()